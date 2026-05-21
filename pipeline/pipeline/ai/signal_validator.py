import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.config import settings

logger = logging.getLogger(__name__)


async def validate_signals(
    session: AsyncSession,
    scored_symbols: list,
) -> dict[str, Any]:
    validations = []
    disagreement_count = 0

    for ss in scored_symbols:
        if ss.signal == "NONE":
            continue
        val = _validate_single(session, ss)
        validations.append(val)
        if val.get("disagreement"):
            disagreement_count += 1

    return {
        "total_scored": len(scored_symbols),
        "signals_validated": len(validations),
        "disagreements": disagreement_count,
        "validations": validations,
        "verdict": "caution" if disagreement_count > 0 else "normal",
    }


def _validate_single(session, ss) -> dict:
    checks = []
    warnings = []

    q = ss.quality.get("score", Decimal("0"))
    v = ss.value.get("score", Decimal("0"))
    t_score = ss.technical.get("total", Decimal("0"))

    if ss.signal == "ENTER":
        if q < Decimal("5"):
            checks.append("quality_below_mid")
        if t_score < Decimal("2"):
            checks.append("weak_technical")

    if ss.signal == "HOLD":
        if q < Decimal("3"):
            checks.append("quality_low_for_hold")

    if q > Decimal("7") and v > Decimal("7") and ss.signal != "ENTER":
        warnings.append("high_quality_value_but_not_enter")
        checks.append("missed_opportunity")

    if t_score > Decimal("5") and q < Decimal("3"):
        warnings.append("technical_overbought_weak_fundamental")
        checks.append("divergence")

    disagreement = len([c for c in checks if c in (
        "weak_technical", "quality_below_mid", "divergence",
    )]) >= 2

    return {
        "symbol": ss.symbol,
        "signal": ss.signal,
        "total_score": float(ss.total_score),
        "q_score": float(q),
        "v_score": float(v),
        "t_score": float(t_score),
        "checks": checks,
        "warnings": warnings,
        "disagreement": disagreement,
    }
