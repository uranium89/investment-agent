import logging
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

MAX_ADJUSTMENT = Decimal("0.20")


async def compute_macro_overlay(
    session: AsyncSession,
) -> dict:
    adjustment = Decimal("0")
    signals = []

    try:
        vnindex_result = await session.execute(
            text("""
                SELECT time, close FROM ohlc_prices
                WHERE symbol = 'VNINDEX'
                ORDER BY time DESC
            """),
        )
        vnindex_rows = vnindex_result.fetchall()
        if len(vnindex_rows) > 200:
            closes = [Decimal(str(r[1])) for r in vnindex_rows if r[1]]
            if len(closes) >= 200:
                current_price = closes[0]
                ma_200 = sum(closes[:200]) / Decimal("200")
                if current_price > ma_200:
                    adjustment += Decimal("0.10")
                    signals.append("vnindex_uptrend")
                else:
                    adjustment -= Decimal("0.10")
                    signals.append("vnindex_downtrend")
    except Exception as e:
        logger.warning("VNINDEX macro check skipped: %s", e)

    try:
        interest_result = await session.execute(
            text("""
                SELECT value FROM macro_indicators
                WHERE indicator = 'policy_rate'
                ORDER BY date DESC
                LIMIT 2
            """),
        )
        interest_rows = interest_result.fetchall()
        if len(interest_rows) == 2:
            old_rate = Decimal(str(interest_rows[1][0]))
            new_rate = Decimal(str(interest_rows[0][0]))
            if new_rate < old_rate:
                adjustment += Decimal("0.10")
                signals.append("rate_cut")
            elif new_rate > old_rate:
                adjustment -= Decimal("0.10")
                signals.append("rate_hike")
    except Exception as e:
        logger.warning("Interest rate macro check skipped: %s", e)

    if adjustment > MAX_ADJUSTMENT:
        adjustment = MAX_ADJUSTMENT
    elif adjustment < -MAX_ADJUSTMENT:
        adjustment = -MAX_ADJUSTMENT

    return {"adjustment": adjustment, "signals": signals}
