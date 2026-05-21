import logging
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.scoring.engine import ScoredSymbol
from pipeline.config import settings

logger = logging.getLogger(__name__)

MAX_POSITIONS = 10
MAX_SECTOR_PCT = {
    "financial": Decimal("40"),
    "real_estate": Decimal("20"),
}
MAX_SINGLE_PCT = Decimal("10")
CASH_PCT = Decimal("25")

SECTOR_MAP: dict[str, str] = {
    "ACB": "financial", "BID": "financial", "CTG": "financial",
    "VCB": "financial", "TCB": "financial", "MBB": "financial",
    "VPB": "financial", "HDB": "financial", "TPB": "financial",
    "SHB": "financial", "STB": "financial", "SSB": "financial",
    "SSI": "financial",
    "VHM": "real_estate", "VIC": "real_estate", "VRE": "real_estate",
    "NVL": "real_estate", "PDR": "real_estate",
}


async def construct_portfolio(
    session: AsyncSession,
    scored_symbols: list[ScoredSymbol],
) -> dict[str, Any]:
    qualified = [
        ss for ss in scored_symbols if ss.passed_screening and ss.signal == "ENTER"
    ]
    qualified.sort(key=lambda x: x.total_score, reverse=True)
    top_n = qualified[:MAX_POSITIONS]

    if not top_n:
        return {"positions": [], "cash_pct": 100, "message": "No qualified symbols"}

    total_score = sum(ss.total_score for ss in top_n)
    if total_score == 0:
        return {"positions": [], "cash_pct": 100, "message": "All scores are zero"}

    remaining_pct = Decimal("100") - CASH_PCT
    raw_allocations = []

    for ss in top_n:
        raw_pct = (ss.total_score / total_score) * remaining_pct
        raw_allocations.append((ss, raw_pct))

    raw_allocations.sort(key=lambda x: x[1], reverse=True)

    for ss, pct in raw_allocations:
        sector = SECTOR_MAP.get(ss.symbol, "other")
        ss.sector = sector

    sector_usage: dict[str, Decimal] = {}
    final_positions = []

    for ss, pct in raw_allocations:
        sector = SECTOR_MAP.get(ss.symbol, "other")
        sector_limit = MAX_SECTOR_PCT.get(sector, Decimal("100"))
        current_sector = sector_usage.get(sector, Decimal("0"))
        max_for_sector = sector_limit - current_sector
        adjusted_pct = min(pct, MAX_SINGLE_PCT, max_for_sector)

        if adjusted_pct <= Decimal("0"):
            continue

        sector_usage[sector] = current_sector + adjusted_pct
        final_positions.append({
            "symbol": ss.symbol,
            "score": float(ss.total_score),
            "weight_pct": float(adjusted_pct),
            "sector": sector,
            "signal": "ENTER",
        })

    total_allocated = sum(Decimal(str(p["weight_pct"])) for p in final_positions)
    cash_pct = Decimal("100") - total_allocated

    return {
        "positions": final_positions,
        "cash_pct": float(cash_pct),
        "total_positions": len(final_positions),
    }
