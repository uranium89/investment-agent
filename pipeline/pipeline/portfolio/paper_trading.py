import logging
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

import numpy as np
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.config import settings

logger = logging.getLogger(__name__)

SLIPPAGE_BUY = Decimal("0.001")
SLIPPAGE_SELL = Decimal("0.001")
REBALANCE_FREQ_DAYS = 5

SECTOR_MAP: dict[str, str] = {
    "ACB": "financial", "BID": "financial", "CTG": "financial",
    "VCB": "financial", "TCB": "financial", "MBB": "financial",
    "VPB": "financial", "HDB": "financial", "TPB": "financial",
    "SHB": "financial", "STB": "financial", "SSB": "financial",
    "SSI": "financial",
    "VHM": "real_estate", "VIC": "real_estate", "VRE": "real_estate",
    "NVL": "real_estate", "PDR": "real_estate",
}

BANK_SYMBOLS = {"BID", "CTG", "VCB", "TCB", "MBB", "ACB", "VPB",
                 "HDB", "TPB", "SHB", "STB", "SSB"}


async def run_backtest(
    session: AsyncSession,
    start_date: str,
    end_date: str,
    initial_capital: Decimal = Decimal("100_000_000"),
    enter_threshold: Decimal = Decimal("5.0"),
    exit_threshold: Decimal = Decimal("3.5"),
    max_positions: int = 10,
    max_single_pct: Decimal = Decimal("10"),
    cash_pct: Decimal = Decimal("25"),
    rebalance_days: int = REBALANCE_FREQ_DAYS,
) -> dict[str, Any]:
    trading_days = await _get_trading_days(session, start_date, end_date)

    capital = initial_capital
    positions: dict[str, dict] = {}
    trade_log = []
    equity_curve = []
    all_signals: dict[str, list] = {}

    rebalance_dates = [
        trading_days[i] for i in range(0, len(trading_days), rebalance_days)
    ]

    for day in rebalance_dates:
        await _process_day(
            session, day, trading_days, positions, capital,
            enter_threshold, exit_threshold, max_positions,
            max_single_pct, cash_pct, trade_log, all_signals,
        )

        portfolio_value = await _compute_portfolio_value(
            session, day, positions, capital,
        )
        capital = portfolio_value - sum(
            p["shares"] * pos_value
            for p, pos_value in positions.values()
        ) if isinstance(positions, dict) else portfolio_value
        equity_curve.append({"date": str(day), "value": float(portfolio_value)})

    total_pnl = portfolio_value - initial_capital
    total_return = (portfolio_value / initial_capital - Decimal("1")) * Decimal("100")

    metrics = _compute_performance_metrics(
        equity_curve, trade_log, initial_capital, portfolio_value,
    )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "initial_capital": float(initial_capital),
        "final_value": float(portfolio_value),
        "total_return_pct": float(total_return),
        "total_pnl": float(total_pnl),
        **metrics,
        "final_positions": len(positions),
        "trade_log": trade_log[:100],
        "equity_curve": equity_curve,
        "signal_summary": {k: v[-5:] if v else [] for k, v in all_signals.items()},
    }


async def _get_trading_days(session: AsyncSession, start: str, end: str) -> list:
    result = await session.execute(
        text("""
            SELECT DISTINCT time::date as d
            FROM ohlc_prices
            WHERE time::date BETWEEN :start AND :end
            ORDER BY d
        """),
        {"start": start, "end": end},
    )
    return [r[0] for r in result.fetchall()]


async def _process_day(
    session, day, trading_days, positions, capital,
    enter_threshold, exit_threshold, max_positions,
    max_single_pct, cash_pct, trade_log, all_signals,
):
    enter, hold, score_map = await _compute_signals(
        session, day, enter_threshold, exit_threshold,
    )
    all_signals[str(day)] = [
        {"symbol": s, "signal": signal, "score": float(score_map.get(s, Decimal("0")))}
        for s, signal in [*[(s, "ENTER") for s in enter], *[(s, "HOLD") for s in hold]]
    ]

    await _process_exits(
        session, day, enter, hold, positions, capital, trade_log,
    )

    await _process_entries(
        session, day, enter, positions, capital,
        max_positions, max_single_pct, cash_pct, trade_log, score_map,
    )


async def _compute_signals(
    session: AsyncSession, day, enter_threshold: Decimal, exit_threshold: Decimal,
):
    scores = {}
    for symbol in settings.vn30_symbols:
        score = await _compute_historical_score(session, symbol, day)
        if score is not None:
            scores[symbol] = score

    enter = [s for s, sc in scores.items()
             if sc >= enter_threshold and await _check_screening(session, s, day)]
    hold = [s for s, sc in scores.items()
            if enter_threshold > sc >= exit_threshold and await _check_screening(session, s, day)]
    return enter, hold, scores


async def _compute_historical_score(
    session: AsyncSession, symbol: str, day,
) -> Decimal | None:
    tech = await _compute_historical_technical(session, symbol, day)
    value = await _compute_historical_value(session, symbol, day)
    quality = await _compute_historical_quality(session, symbol, day)

    if any(x is None for x in (tech, value, quality)):
        return None

    total = (tech["total"] + value["score"] + quality["score"] + Decimal("5")) / Decimal("5")
    return max(total, Decimal("0"))


async def _compute_historical_technical(
    session: AsyncSession, symbol: str, day,
) -> dict | None:
    result = await session.execute(
        text("""
            SELECT ma_20, ma_50, ma_200, rsi_14, macd, macd_signal, macd_histogram, volume_sma_20
            FROM technical_indicators
            WHERE symbol = :symbol AND time::date <= :day
            ORDER BY time DESC LIMIT 1
        """),
        {"symbol": symbol, "day": day},
    )
    row = result.fetchone()
    if not row or row[0] is None:
        return None

    ma_20, ma_50, ma_200, rsi_14, macd, macd_signal, macd_hist, vol_sma_20 = row

    price_result = await session.execute(
        text("SELECT close FROM ohlc_prices WHERE symbol = :s AND time::date <= :d ORDER BY time DESC LIMIT 1"),
        {"s": symbol, "d": day},
    )
    price_row = price_result.fetchone()
    if not price_row:
        return None
    current_price = Decimal(str(price_row[0]))

    trend = 0
    if current_price and ma_50 and Decimal(str(ma_50)) > 0 and current_price > Decimal(str(ma_50)):
        trend += 3
    if current_price and ma_200 and Decimal(str(ma_200)) > 0 and current_price > Decimal(str(ma_200)):
        trend += 3
    if ma_50 and ma_200 and Decimal(str(ma_50)) > 0 and Decimal(str(ma_200)) > 0 and Decimal(str(ma_50)) > Decimal(str(ma_200)):
        trend += 3

    mom = 0
    if rsi_14 is not None:
        rsi_val = Decimal(str(rsi_14))
        if Decimal("30") <= rsi_val <= Decimal("40"):
            mom += 5
        elif Decimal("40") < rsi_val <= Decimal("60"):
            mom += 3

    if macd_hist is not None and Decimal(str(macd_hist)) > 0:
        mom += 3
    if macd is not None and macd_signal is not None and Decimal(str(macd)) > Decimal(str(macd_signal)):
        mom += 2

    total = Decimal(str(trend)) * Decimal("0.15") + Decimal(str(mom)) * Decimal("0.10")
    return {"total": total, "trend_score": trend, "momentum_score": mom}


async def _compute_historical_value(
    session: AsyncSession, symbol: str, day,
) -> dict | None:
    result = await session.execute(
        text("""
            SELECT fi.pe, fi.pb
            FROM financial_indicators fi
            WHERE fi.symbol = :s AND fi.date <= :d AND fi.pe IS NOT NULL
            ORDER BY fi.date DESC LIMIT 1
        """),
        {"s": symbol, "d": day},
    )
    row = result.fetchone()
    if not row or not row[0]:
        return {"score": Decimal("0"), "pe": None, "pb": None}

    current_pe = Decimal(str(row[0]))
    current_pb = Decimal(str(row[1])) if row[1] else None

    all_pe = await session.execute(
        text("""
            WITH ranked AS (
                SELECT fi.symbol, fi.pe,
                       ROW_NUMBER() OVER (PARTITION BY fi.symbol ORDER BY fi.date DESC) as rn
                FROM financial_indicators fi
                WHERE fi.symbol = ANY(:symbols) AND fi.date <= :d AND fi.pe IS NOT NULL
            )
            SELECT symbol, pe FROM ranked WHERE rn = 1
        """),
        {"symbols": settings.vn30_symbols, "d": day},
    )
    all_pe_rows = all_pe.fetchall()
    pe_values = sorted(set(
        Decimal(str(r[1])) for r in all_pe_rows if r[1] and Decimal(str(r[1])) > 0
    ))
    if not pe_values or len(pe_values) < 2:
        return {"score": Decimal("5"), "pe": current_pe, "pb": current_pb}

    rank = sum(1 for p in pe_values if p < current_pe)
    percentile = Decimal(str(rank)) / Decimal(str(len(pe_values) - 1))
    pe_score = (Decimal("1") - percentile) * Decimal("10")
    bonus = Decimal("2") if current_pb and current_pb < Decimal("2") else Decimal("0")
    score = min(pe_score + bonus, Decimal("10"))

    return {"score": score, "pe": current_pe, "pb": current_pb, "pe_percentile": percentile}


async def _compute_historical_quality(
    session: AsyncSession, symbol: str, day,
) -> dict | None:
    result = await session.execute(
        text("""
            SELECT net_income, total_equity, debt, free_cash_flow, issued_shares
            FROM financial_reports
            WHERE symbol = :s AND net_income IS NOT NULL
            ORDER BY year DESC, period DESC LIMIT 1
        """),
        {"s": symbol},
    )
    row = result.fetchone()
    if not row:
        ind_result = await session.execute(
            text("SELECT roe FROM financial_indicators WHERE symbol = :s AND date <= :d AND roe IS NOT NULL ORDER BY date DESC LIMIT 1"),
            {"s": symbol, "d": day},
        )
        ind_row = ind_result.fetchone()
        if ind_row and ind_row[0]:
            roe = Decimal(str(ind_row[0])) / Decimal("100")
            score = Decimal("7") if roe > Decimal("0.15") else (Decimal("5") if roe > Decimal("0.10") else Decimal("0"))
            return {"score": score, "roe": roe, "de": None, "fcf_yield": None}
        return {"score": Decimal("0"), "roe": None, "de": None, "fcf_yield": None}

    ni, te, debt, fcf, shares = row
    roe_score = de_score = fcf_score = Decimal("0")

    if te and ni and Decimal(str(te)) != 0:
        roe = Decimal(str(ni)) / Decimal(str(te))
        if roe > Decimal("0.15"): roe_score = Decimal("10")
        elif roe > Decimal("0.12"): roe_score = Decimal("7")
        elif roe > Decimal("0.10"): roe_score = Decimal("5")

    if te and debt and Decimal(str(te)) != 0:
        de = Decimal(str(debt)) / Decimal(str(te))
        if de < Decimal("0.5"): de_score = Decimal("10")
        elif de < Decimal("1.0"): de_score = Decimal("7")
        elif de < Decimal("1.5"): de_score = Decimal("5")

    if fcf and shares:
        price_row = (await session.execute(
            text("SELECT close FROM ohlc_prices WHERE symbol = :s AND time::date <= :d ORDER BY time DESC LIMIT 1"),
            {"s": symbol, "d": day},
        )).fetchone()
        if price_row and price_row[0]:
            mcap = Decimal(str(price_row[0])) * Decimal(str(shares))
            if mcap > 0:
                fcf_yield = Decimal(str(fcf)) / mcap
                if fcf_yield > Decimal("0.04"): fcf_score = Decimal("10")
                elif fcf_yield > Decimal("0.02"): fcf_score = Decimal("7")
                elif fcf_yield > Decimal("0"): fcf_score = Decimal("5")

    total = roe_score * Decimal("0.40") + de_score * Decimal("0.30") + fcf_score * Decimal("0.30")
    return {"score": total}


async def _check_screening(session: AsyncSession, symbol: str, day) -> bool:
    if symbol in BANK_SYMBOLS:
        de_ok = await _check_historical_de(session, symbol, day, is_bank=True)
    else:
        de_ok = await _check_historical_de(session, symbol, day)
    roe_ok = await _check_historical_roe(session, symbol, day)
    return bool(de_ok and roe_ok)


async def _check_historical_de(session, symbol, day, is_bank=False):
    max_de = Decimal("10") if is_bank else Decimal("1.5")
    result = await session.execute(
        text("SELECT debt, total_equity FROM financial_reports WHERE symbol = :s AND debt IS NOT NULL AND total_equity IS NOT NULL ORDER BY year DESC LIMIT 1"),
        {"s": symbol},
    )
    row = result.fetchone()
    if not row or not row[1] or Decimal(str(row[1])) == 0:
        return True
    de = Decimal(str(row[0])) / Decimal(str(row[1]))
    return de < max_de


async def _check_historical_roe(session, symbol, day):
    result = await session.execute(
        text("SELECT net_income, total_equity FROM financial_reports WHERE symbol = :s AND net_income IS NOT NULL AND total_equity IS NOT NULL ORDER BY year DESC LIMIT 3"),
        {"s": symbol},
    )
    rows = result.fetchall()
    if len(rows) < 2:
        return True
    roes = []
    for r in rows:
        if r[1] and Decimal(str(r[1])) != 0:
            roes.append(Decimal(str(r[0])) / Decimal(str(r[1])))
    return all(r > Decimal("0.10") for r in roes) if len(roes) >= 2 else True


async def _process_exits(session, day, enter, hold, positions, capital, trade_log):
    active_set = set(enter) | set(hold)
    to_exit = [sym for sym in list(positions.keys()) if sym not in active_set]

    for sym in to_exit:
        pos = positions.pop(sym)
        price_result = await session.execute(
            text("SELECT close FROM ohlc_prices WHERE symbol = :s AND time::date <= :d ORDER BY time DESC LIMIT 1"),
            {"s": sym, "d": day},
        )
        price_row = price_result.fetchone()
        exit_price = Decimal(str(price_row[0])) if price_row else pos["entry_price"]
        exit_price_adj = exit_price * (Decimal("1") - SLIPPAGE_SELL)
        exit_value = pos["shares"] * exit_price_adj
        pnl = exit_value - pos["cost_basis"]
        capital += exit_value
        hold_days = (day - pos["entry_date"]).days if hasattr(day, 'strftime') else 0
        trade_log.append({
            "date": str(day), "symbol": sym, "action": "SELL",
            "shares": pos["shares"], "price": float(exit_price_adj),
            "pnl": float(pnl), "return_pct": float(pnl / pos["cost_basis"] * 100),
            "hold_days": hold_days, "reason": "signal_lost",
        })


async def _process_entries(session, day, enter, positions, capital,
                            max_positions, max_single_pct, cash_pct, trade_log, score_map):
    available = max_positions - len(positions)
    if available <= 0 or not enter:
        return

    sorted_enter = sorted(enter, key=lambda s: score_map.get(s, Decimal("0")), reverse=True)[:available]

    for sym in sorted_enter:
        price_result = await session.execute(
            text("SELECT close FROM ohlc_prices WHERE symbol = :s AND time::date <= :d ORDER BY time DESC LIMIT 1"),
            {"s": sym, "d": day},
        )
        price_row = price_result.fetchone()
        price = Decimal(str(price_row[0])) if price_row else None
        if not price or price <= 0:
            continue

        score = score_map.get(sym, Decimal("5"))
        weight = min(score, Decimal("10")) / Decimal("50") * (Decimal("100") - cash_pct) / Decimal("100")
        weight = min(weight, max_single_pct / Decimal("100"))

        target_value = capital * weight
        quantity = int(target_value / (price * (Decimal("1") + SLIPPAGE_BUY)) / 100) * 100
        if quantity < 100:
            continue
        cost = quantity * price * (Decimal("1") + SLIPPAGE_BUY)
        if cost > capital:
            quantity = int(capital / (price * (Decimal("1") + SLIPPAGE_BUY)) / 100) * 100
            if quantity < 100: continue
            cost = quantity * price * (Decimal("1") + SLIPPAGE_BUY)

        capital -= cost
        entry_date = day if not hasattr(day, 'strftime') else day
        positions[sym] = {
            "entry_price": price, "cost_basis": cost,
            "shares": quantity, "entry_date": entry_date,
        }
        trade_log.append({
            "date": str(day), "symbol": sym, "action": "BUY",
            "shares": quantity, "price": float(price),
        })


async def _compute_portfolio_value(session, day, positions, capital):
    total = capital
    for sym, pos in positions.items():
        price_result = await session.execute(
            text("SELECT close FROM ohlc_prices WHERE symbol = :s AND time::date <= :d ORDER BY time DESC LIMIT 1"),
            {"s": sym, "d": day},
        )
        price_row = price_result.fetchone()
        if price_row and price_row[0]:
            total += pos["shares"] * Decimal(str(price_row[0]))
    return total


def _compute_performance_metrics(equity_curve, trade_log, initial_capital, final_value):
    if not equity_curve:
        return {}

    values = np.array([e["value"] for e in equity_curve])
    returns = np.diff(values) / values[:-1]

    total_return = float(final_value / initial_capital - 1)
    n_days = len(equity_curve)

    sharpe = float(np.mean(returns) / np.std(returns) * np.sqrt(252)) if len(returns) > 1 and np.std(returns) > 0 else 0
    downside = returns[returns < 0]
    sortino = float(np.mean(returns) / np.std(downside) * np.sqrt(252)) if len(downside) > 1 and np.std(downside) > 0 else 0

    peak = np.maximum.accumulate(values)
    drawdowns = (peak - values) / peak
    max_dd = float(np.max(drawdowns))
    calmar = total_return / max_dd if max_dd > 0 else 0

    sells = [t for t in trade_log if t.get("action") == "SELL" and t.get("pnl") is not None]
    wins = [t for t in sells if t["pnl"] > 0]
    win_rate = len(wins) / len(sells) * 100 if sells else 0
    avg_win = sum(t["pnl"] for t in wins) / len(wins) if wins else 0
    avg_loss = sum(t["pnl"] for t in sells if t["pnl"] <= 0) / max(len([t for t in sells if t["pnl"] <= 0]), 1)
    profit_factor = abs(sum(t["pnl"] for t in wins) / sum(t["pnl"] for t in sells if t["pnl"] <= 0)) if sum(t["pnl"] for t in sells if t["pnl"] <= 0) != 0 else float("inf")

    hold_days = [t.get("hold_days", 0) for t in sells if t.get("hold_days")]

    return {
        "total_return_pct": round(total_return * 100, 2),
        "annualized_return_pct": round((1 + total_return) ** (252 / max(n_days, 1)) - 1, 4) * 100 if n_days > 0 else 0,
        "sharpe_ratio": round(sharpe, 3),
        "sortino_ratio": round(sortino, 3),
        "max_drawdown_pct": round(max_dd * 100, 2),
        "calmar_ratio": round(calmar, 3),
        "total_trades": len(sells),
        "win_rate_pct": round(win_rate, 1),
        "avg_win": round(avg_win, 0),
        "avg_loss": round(avg_loss, 0),
        "profit_factor": round(profit_factor, 2),
        "avg_hold_days": round(np.mean(hold_days), 1) if hold_days else 0,
        "trading_days": n_days,
    }


async def run_parameter_sensitivity(
    session: AsyncSession,
    start_date: str,
    end_date: str,
    initial_capital: Decimal = Decimal("100_000_000"),
) -> list[dict]:
    param_sets = [
        {"enter": Decimal("4.5"), "exit": Decimal("3.0"), "label": "enter_4.5_exit_3.0"},
        {"enter": Decimal("5.0"), "exit": Decimal("3.5"), "label": "enter_5.0_exit_3.5"},
        {"enter": Decimal("5.5"), "exit": Decimal("4.0"), "label": "enter_5.5_exit_4.0"},
        {"enter": Decimal("4.0"), "exit": Decimal("2.5"), "label": "enter_4.0_exit_2.5"},
        {"enter": Decimal("6.0"), "exit": Decimal("4.5"), "label": "enter_6.0_exit_4.5"},
    ]
    cash_settings = [Decimal("15"), Decimal("25"), Decimal("35")]
    max_pos_settings = [5, 10, 15]

    results = []
    for ps in param_sets:
        for cash in cash_settings:
            for mp in max_pos_settings:
                result = await run_backtest(
                    session, start_date, end_date, initial_capital,
                    enter_threshold=ps["enter"], exit_threshold=ps["exit"],
                    max_positions=mp, cash_pct=cash,
                )
                results.append({
                    "params": f"{ps['label']}_cash{cash}_max{mp}",
                    "enter_threshold": float(ps["enter"]),
                    "exit_threshold": float(ps["exit"]),
                    "cash_pct": float(cash),
                    "max_positions": mp,
                    "return_pct": result["total_return_pct"],
                    "sharpe": result.get("sharpe_ratio", 0),
                    "max_dd": result.get("max_drawdown_pct", 0),
                    "win_rate": result.get("win_rate_pct", 0),
                    "trades": result.get("total_trades", 0),
                })

    results.sort(key=lambda r: r["sharpe"], reverse=True)
    return results