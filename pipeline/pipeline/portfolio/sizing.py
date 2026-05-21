import logging
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def calculate_position_size(
    session: AsyncSession,
    symbol: str,
    portfolio_value: Decimal,
    weight_pct: Decimal,
) -> dict[str, Any]:
    target_value = portfolio_value * (weight_pct / Decimal("100"))

    atr_result = await session.execute(
        text("""
            SELECT atr_14 FROM technical_indicators
            WHERE symbol = :symbol AND atr_14 IS NOT NULL
            ORDER BY time DESC
            LIMIT 1
        """),
        {"symbol": symbol},
    )
    atr_row = atr_result.fetchone()
    atr = Decimal(str(atr_row[0])) if atr_row else None

    price_result = await session.execute(
        text("""
            SELECT close FROM ohlc_prices
            WHERE symbol = :symbol
            ORDER BY time DESC
            LIMIT 1
        """),
        {"symbol": symbol},
    )
    price_row = price_result.fetchone()
    current_price = Decimal(str(price_row[0])) if price_row else Decimal("1")

    risk_capital = portfolio_value * Decimal("0.01")
    multiplier = Decimal("1.5")
    if atr and atr > 0:
        atr_based = risk_capital / (atr * multiplier)
        atr_shares = int(atr_based / current_price) if current_price > 0 else 0
        atr_value = atr_shares * current_price
    else:
        atr_value = risk_capital
        atr_shares = 0

    weight_shares = int(target_value / current_price) if current_price > 0 else 0
    weight_value = weight_shares * current_price

    if atr_shares > 0 and weight_shares > 0:
        final_shares = min(atr_shares, weight_shares)
    elif atr_shares > 0:
        final_shares = atr_shares
    else:
        final_shares = weight_shares

    if final_shares < 100:
        final_shares = 0

    final_value = final_shares * current_price
    actual_weight = (final_value / portfolio_value * Decimal("100")) if portfolio_value > 0 else Decimal("0")

    return {
        "symbol": symbol,
        "current_price": float(current_price),
        "atr": float(atr) if atr else None,
        "weight_target_value": float(target_value),
        "atr_limited_value": float(atr_value),
        "final_shares": final_shares,
        "final_value": float(final_value),
        "actual_weight_pct": float(actual_weight),
    }
