import logging
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.config import settings

logger = logging.getLogger(__name__)

SECTOR_LIMITS = {
    "financial": Decimal(str(settings.max_sector_finance_pct)),
    "real_estate": Decimal(str(settings.max_sector_realestate_pct)),
}


async def check_sector_exposure(session: AsyncSession) -> dict:
    result = await session.execute(
        text("""
            SELECT
                COALESCE(sector, 'other') as sector,
                SUM(weight_pct) as total_weight
            FROM portfolio_state
            WHERE status = 'active'
            GROUP BY sector
        """),
    )
    rows = result.fetchall()
    exposures = {}
    for r in rows:
        exposures[r[0]] = Decimal(str(r[1])) if r[1] else Decimal("0")

    breaches = []
    for sector, limit in SECTOR_LIMITS.items():
        current = exposures.get(sector, Decimal("0"))
        if current > limit:
            breaches.append({
                "sector": sector,
                "current_pct": float(current),
                "limit_pct": float(limit),
                "excess_pct": float(current - limit),
            })

    return {
        "exposures": {k: float(v) for k, v in exposures.items()},
        "breaches": breaches,
        "breach_count": len(breaches),
        "all_clear": len(breaches) == 0,
    }


async def get_sector_breakdown(session: AsyncSession) -> list[dict]:
    result = await session.execute(
        text("""
            SELECT
                COALESCE(sector, 'other') as sector,
                COUNT(*) as position_count,
                SUM(weight_pct) as total_weight,
                SUM(current_value) as total_value
            FROM portfolio_state
            WHERE status = 'active'
            GROUP BY sector
            ORDER BY total_weight DESC
        """),
    )
    rows = result.fetchall()
    return [
        {
            "sector": r[0],
            "position_count": int(r[1]),
            "total_weight_pct": float(r[2]) if r[2] else 0,
            "total_value": float(r[3]) if r[3] else 0,
        }
        for r in rows
    ]