import logging
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.config import settings

logger = logging.getLogger(__name__)


async def check_black_swan(session: AsyncSession) -> dict:
    threshold = Decimal(str(settings.black_swan_threshold_pct))

    result = await session.execute(
        text("""
            WITH latest_close AS (
                SELECT close, time
                FROM ohlc_prices
                WHERE symbol = 'VCB'
                ORDER BY time DESC
                LIMIT 1
            ),
            prev_close AS (
                SELECT close
                FROM ohlc_prices
                WHERE symbol = 'VCB'
                ORDER BY time DESC
                OFFSET 1 LIMIT 1
            )
            SELECT
                l.close as current_close,
                p.close as prev_close
            FROM latest_close l, prev_close p
        """),
    )
    row = result.fetchone()
    if not row or not row[1] or Decimal(str(row[1])) == 0:
        return {"triggered": False, "message": "Not enough price data"}

    current = Decimal(str(row[0]))
    prev = Decimal(str(row[1]))
    change_pct = (current - prev) / prev * Decimal("100")

    triggered = change_pct <= threshold

    status = {
        "triggered": triggered,
        "vnindex_change_pct": float(change_pct),
        "threshold_pct": float(threshold),
        "current_close": float(current),
        "prev_close": float(prev),
    }

    if triggered:
        status["message"] = (
            f"⚠️  BLACK SWAN: VN-Index dropped {float(change_pct):.1f}% "
            f"(threshold: {float(threshold):.1f}%). All trading suspended."
        )
        status["action"] = "FREEZE_ALL"
        logger.warning(status["message"])
    else:
        status["message"] = f"VN-Index change: {float(change_pct):.1f}% (threshold: {float(threshold):.1f}%)"
        status["action"] = "NORMAL"

    return status


async def check_recent_crash(session: AsyncSession, lookback_days: int = 5) -> dict:
    result = await session.execute(
        text("""
            WITH daily_change AS (
                SELECT
                    time::date as trade_date,
                    (close - LAG(close) OVER (ORDER BY time)) / LAG(close) OVER (ORDER BY time) * 100 as change_pct
                FROM ohlc_prices
                WHERE symbol = 'VCB'
                ORDER BY time DESC
                LIMIT :lookback
            )
            SELECT MIN(change_pct) as worst_day
            FROM daily_change
        """),
        {"lookback": lookback_days},
    )
    row = result.fetchone()
    worst = Decimal(str(row[0])) if row and row[0] else Decimal("0")
    triggered = worst <= Decimal(str(settings.black_swan_threshold_pct))
    return {
        "triggered": triggered,
        "worst_day_pct": float(worst),
        "lookback_days": lookback_days,
    }