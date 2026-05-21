import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.config import settings

logger = logging.getLogger(__name__)


async def run_paper_trading(
    session: AsyncSession,
    start_date: str,
    end_date: str,
    initial_capital: Decimal = Decimal("100_000_000"),
) -> dict[str, Any]:
    result = await session.execute(
        text("""
            SELECT DISTINCT time::date as trade_date
            FROM score_snapshots
            WHERE time::date BETWEEN :start AND :end
            ORDER BY trade_date
        """),
        {"start": start_date, "end": end_date},
    )
    trading_days = [r[0] for r in result.fetchall()]

    capital = initial_capital
    positions: dict[str, dict] = {}
    trade_log = []
    equity_curve = []

    for day in trading_days:
        scores_result = await session.execute(
            text("""
                SELECT symbol, total_score, quality_score, value_score, technical_score, signal
                FROM score_snapshots
                WHERE time::date = :day AND passed_screening = true
                ORDER BY total_score DESC
            """),
            {"day": day},
        )
        daily_scores = scores_result.fetchall()

        price_result = await session.execute(
            text("""
                SELECT DISTINCT ON (symbol) symbol, close
                FROM ohlc_prices
                WHERE time::date <= :day
                ORDER BY symbol, time DESC
            """),
            {"day": day},
        )
        prices = {r[0]: Decimal(str(r[1])) for r in price_result.fetchall()}

        enter_signals = [s for s in daily_scores if s[5] == "ENTER"]
        hold_signals = [s for s in daily_scores if s[5] == "HOLD"]

        # Exit positions no longer in HOLD/ENTER
        to_exit = []
        for sym in list(positions.keys()):
            if sym not in {s[0] for s in enter_signals + hold_signals}:
                to_exit.append(sym)

        for sym in to_exit:
            pos = positions.pop(sym)
            exit_price = prices.get(sym, pos["entry_price"])
            exit_value = pos["shares"] * exit_price
            pnl = exit_value - pos["cost_basis"]
            capital += exit_value
            slippage = (exit_price - prices.get(sym, exit_price)) / exit_price * 100
            trade_log.append({
                "date": str(day),
                "symbol": sym,
                "action": "SELL",
                "shares": pos["shares"],
                "price": float(exit_price),
                "pnl": float(pnl),
                "slippage_pct": float(slippage),
            })

        for s in enter_signals:
            sym = s[0]
            price = prices.get(sym)
            if not price or price <= 0:
                continue
            score_weight = min(Decimal(str(s[1])) if s[1] else Decimal("5"), Decimal("10"))
            weight = score_weight / Decimal("50")
            target_value = capital * weight
            quantity = int(target_value / price / 100) * 100
            if quantity < 100:
                continue
            cost = quantity * price
            if cost > capital:
                quantity = int(capital / price / 100) * 100
                if quantity < 100:
                    continue
                cost = quantity * price
            capital -= cost
            buy_slippage = Decimal("0.001")
            positions[sym] = {
                "entry_price": price,
                "cost_basis": cost,
                "shares": quantity,
                "entry_date": day,
            }
            trade_log.append({
                "date": str(day),
                "symbol": sym,
                "action": "BUY",
                "shares": quantity,
                "price": float(price),
                "slippage_pct": float(buy_slippage * 100),
            })

        portfolio_value = capital + sum(
            pos["shares"] * prices.get(sym, pos["entry_price"])
            for sym, pos in positions.items()
        )
        equity_curve.append({"date": str(day), "value": float(portfolio_value)})

    total_pnl = portfolio_value - initial_capital
    total_return = (portfolio_value / initial_capital - Decimal("1")) * Decimal("100")
    win_trades = [t for t in trade_log if t.get("pnl", 0) > 0]
    total_trades = len([t for t in trade_log if t["action"] == "SELL"])
    win_rate = len(win_trades) / total_trades * 100 if total_trades > 0 else 0

    return {
        "start_date": start_date,
        "end_date": end_date,
        "initial_capital": float(initial_capital),
        "final_value": float(portfolio_value),
        "total_return_pct": float(total_return),
        "total_pnl": float(total_pnl),
        "total_trades": total_trades,
        "win_rate": float(win_rate),
        "final_positions": len(positions),
        "trade_log": trade_log,
        "equity_curve": equity_curve,
    }