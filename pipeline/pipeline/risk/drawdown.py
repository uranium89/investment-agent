import logging
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.config import settings

logger = logging.getLogger(__name__)


async def check_max_drawdown(session: AsyncSession) -> dict:
    max_dd_pct = Decimal(str(settings.max_drawdown_pct))

    result = await session.execute(
        text("""
            WITH portfolio_value AS (
                SELECT
                    time,
                    SUM(total_value) as pv
                FROM (
                    SELECT
                        sp.time,
                        sp.symbol,
                        sp.total_score,
                        sp.signal,
                        1.0 as qty
                    FROM score_snapshots sp
                    WHERE sp.time >= CURRENT_DATE - INTERVAL '180 days'
                ) sub
                GROUP BY time
                ORDER BY time
            )
            SELECT
                MIN(pv) as min_value,
                MAX(pv) as max_value
            FROM portfolio_value
        """),
    )
    row = result.fetchone()
    if not row or not row.max_value or row.max_value == 0:
        return {"in_drawdown": False, "current_drawdown_pct": 0, "message": "Not enough data"}

    min_val = Decimal(str(row.min_value)) if row.min_value else Decimal("0")
    max_val = Decimal(str(row.max_value))
    current_dd = (max_val - min_val) / max_val * Decimal("100")

    breached = current_dd > max_dd_pct
    status = {
        "in_drawdown": breached,
        "current_drawdown_pct": float(current_dd),
        "max_allowed_pct": float(max_dd_pct),
        "breached": breached,
    }

    if breached:
        status["message"] = f"DRAWDOWN ALERT: {float(current_dd):.1f}% exceeds limit {float(max_dd_pct):.1f}%"
        logger.warning(status["message"])
    else:
        status["message"] = f"Drawdown {float(current_dd):.1f}% within limit {float(max_dd_pct):.1f}%"

    return status


async def get_peak_to_current(session: AsyncSession) -> dict:
    result = await session.execute(
        text("""
            WITH portfolio_daily AS (
                SELECT
                    time::date as trade_date,
                    AVG(total_score) as avg_score
                FROM score_snapshots
                WHERE passed_screening = true
                GROUP BY time::date
            ),
            peak AS (
                SELECT MAX(avg_score) as peak_value
                FROM portfolio_daily
            )
            SELECT
                (SELECT peak_value FROM peak),
                (SELECT avg_score FROM portfolio_daily ORDER BY trade_date DESC LIMIT 1) as current_value
        """),
    )
    row = result.fetchone()
    if not row or not row[0]:
        return {"drawdown_pct": 0, "message": "Not enough data"}
    peak = Decimal(str(row[0]))
    current = Decimal(str(row[1])) if row[1] else peak
    dd = (peak - current) / peak * Decimal("100")
    return {
        "drawdown_pct": float(dd),
        "peak_value": float(peak),
        "current_value": float(current),
    }