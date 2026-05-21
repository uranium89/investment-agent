import logging
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.db.models import PortfolioState
from pipeline.portfolio.constructor import construct_portfolio
from pipeline.scoring.engine import ScoredSymbol, EXIT_THRESHOLD

logger = logging.getLogger(__name__)

MIN_WEIGHT_CHANGE = Decimal("2.0")


async def compute_rebalance(
    session: AsyncSession,
    scored_symbols: list[ScoredSymbol],
    portfolio_value: Decimal,
) -> dict[str, Any]:
    target = await construct_portfolio(session, scored_symbols)
    target_map = {p["symbol"]: p for p in target["positions"]}

    current_result = await session.execute(
        text("""
            SELECT symbol, weight_pct, current_value, shares, entry_price
            FROM portfolio_state
            WHERE status = 'active'
        """),
    )
    current_rows = current_result.fetchall()
    current_positions = {}
    for r in current_rows:
        current_positions[r[0]] = {
            "weight_pct": Decimal(str(r[1])) if r[1] else Decimal("0"),
            "current_value": Decimal(str(r[2])) if r[2] else Decimal("0"),
            "shares": int(r[3]) if r[3] else 0,
            "entry_price": Decimal(str(r[4])) if r[4] else Decimal("0"),
        }

    trades = []
    score_map = {ss.symbol: ss for ss in scored_symbols}

    for symbol, curr in current_positions.items():
        if symbol in target_map:
            target_w = Decimal(str(target_map[symbol]["weight_pct"]))
            curr_w = curr["weight_pct"]
            diff = target_w - curr_w
            if abs(diff) >= MIN_WEIGHT_CHANGE:
                if diff > 0:
                    trades.append({"symbol": symbol, "action": "ADD", "weight_change": float(diff)})
                else:
                    trades.append({"symbol": symbol, "action": "REDUCE", "weight_change": float(abs(diff))})
        else:
            score = score_map.get(symbol)
            if score and score.total_score < EXIT_THRESHOLD:
                trades.append({"symbol": symbol, "action": "EXIT", "reason": "score_below_threshold"})
            else:
                trades.append({"symbol": symbol, "action": "HOLD", "reason": "not_in_target"})

    for tp in target["positions"]:
        if tp["symbol"] not in current_positions:
            trades.append({"symbol": tp["symbol"], "action": "ENTER", "weight_pct": tp["weight_pct"]})

    return {
        "trades": trades,
        "trade_count": len(trades),
        "target_positions": target["positions"],
        "current_cash_pct": float(current_positions.get("cash", {}).get("weight_pct", Decimal("25"))),
        "target_cash_pct": target["cash_pct"],
    }
