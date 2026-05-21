import logging
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.config import settings

logger = logging.getLogger(__name__)


async def compute_value_score(
    session: AsyncSession,
    symbol: str,
) -> dict[str, Any]:
    pe_result = await session.execute(
        text("""
            SELECT pe, pb FROM financial_indicators
            WHERE symbol = :symbol AND pe IS NOT NULL
            ORDER BY date DESC
            LIMIT 1
        """),
        {"symbol": symbol},
    )
    pe_row = pe_result.fetchone()
    if not pe_row or not pe_row[0]:
        return {"score": Decimal("0"), "pe": None, "pb": None, "pe_percentile": None}

    current_pe = Decimal(str(pe_row[0]))
    current_pb = Decimal(str(pe_row[1])) if pe_row[1] else None

    all_pe_result = await session.execute(
        text("""
            WITH ranked AS (
                SELECT fi.symbol, fi.pe,
                       ROW_NUMBER() OVER (PARTITION BY fi.symbol ORDER BY fi.date DESC) AS rn
                FROM financial_indicators fi
                WHERE fi.symbol = ANY(:symbols) AND fi.pe IS NOT NULL
            )
            SELECT symbol, pe FROM ranked WHERE rn = 1
        """),
        {"symbols": settings.vn30_symbols},
    )
    all_pe_rows = all_pe_result.fetchall()
    pe_values = sorted(set(
        Decimal(str(r[1])) for r in all_pe_rows if r[1] and Decimal(str(r[1])) > 0
    ))
    if not pe_values or len(pe_values) < 2:
        return {"score": Decimal("5"), "pe": current_pe, "pb": current_pb, "pe_percentile": None}

    rank = sum(1 for p in pe_values if p < current_pe)
    percentile = Decimal(str(rank)) / Decimal(str(len(pe_values) - 1))
    pe_score = (Decimal("1") - percentile) * Decimal("10")

    bonus = Decimal("0")
    if current_pb and current_pb < Decimal("2"):
        bonus = Decimal("2")

    score = min(pe_score + bonus, Decimal("10"))

    return {
        "score": score,
        "pe": current_pe,
        "pb": current_pb,
        "pe_percentile": percentile,
    }
