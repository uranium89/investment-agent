import logging
from datetime import datetime, date
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.clients.fireant import FireAntClient
from pipeline.config import settings
from pipeline.db.models import ScoreSnapshot
from pipeline.scoring.gates import check_screening_gate
from pipeline.scoring.quality import compute_quality_score
from pipeline.scoring.value import compute_value_score
from pipeline.scoring.technical import compute_technical_score
from pipeline.scoring.moat import compute_moat_score
from pipeline.scoring.management import compute_management_score
from pipeline.scoring.macro import compute_macro_overlay

logger = logging.getLogger(__name__)

ENTER_THRESHOLD = Decimal("5.0")
EXIT_THRESHOLD = Decimal("3.5")


class ScoredSymbol:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.passed_screening = False
        self.screening_detail: dict = {}
        self.quality: dict = {"score": Decimal("0")}
        self.value: dict = {"score": Decimal("0")}
        self.technical: dict = {"total": Decimal("0")}
        self.moat = Decimal("0")
        self.management: dict = {"score": Decimal("5")}
        self.total_score = Decimal("0")
        self.signal = "NONE"
        self.sector = "other"

    @property
    def component_total(self) -> Decimal:
        return (
            self.quality["score"]
            + self.value["score"]
            + self.technical["total"]
            + self.moat
            + self.management["score"]
        )


async def run_scoring(
    session: AsyncSession,
    fireant: FireAntClient | None = None,
) -> list[ScoredSymbol]:
    macro = await compute_macro_overlay(session)
    adjustment = macro["adjustment"]
    logger.info("Macro overlay adjustment: %s (signals: %s)", adjustment, macro["signals"])

    results: list[ScoredSymbol] = []
    for symbol in settings.vn30_symbols:
        try:
            ss = await _score_symbol(session, fireant, symbol, adjustment)
            results.append(ss)
        except Exception as e:
            logger.error("Scoring failed for %s: %s", symbol, e)
            continue

    await _persist_scores(session, results)
    logger.info("Scored %d/%d symbols", len(results), len(settings.vn30_symbols))
    return results


async def _score_symbol(
    session: AsyncSession,
    fireant: FireAntClient | None,
    symbol: str,
    macro_adjustment: Decimal,
) -> ScoredSymbol:
    ss = ScoredSymbol(symbol)

    gate = await check_screening_gate(session, symbol)
    ss.screening_detail = gate
    ss.passed_screening = gate["passed"]

    if not gate["passed"]:
        ss.signal = "NONE"
        return ss

    ss.quality = await compute_quality_score(session, symbol)
    ss.value = await compute_value_score(session, symbol)
    ss.technical = await compute_technical_score(session, symbol)
    ss.moat = compute_moat_score(symbol)

    if fireant:
        ss.management = await compute_management_score(session, fireant, symbol)

    raw_total = ss.component_total / Decimal("5")
    ss.total_score = raw_total * (Decimal("1") + macro_adjustment)
    ss.total_score = max(ss.total_score, Decimal("0"))

    ss.signal = _determine_signal(session, symbol, ss.total_score)

    return ss


def _determine_signal(
    session: AsyncSession,
    symbol: str,
    total_score: Decimal,
) -> str:
    if total_score >= ENTER_THRESHOLD:
        return "ENTER"
    elif total_score >= EXIT_THRESHOLD:
        return "HOLD"
    else:
        return "NONE"


async def _persist_scores(
    session: AsyncSession,
    scored_symbols: list[ScoredSymbol],
) -> None:
    now = datetime.utcnow()
    today_key = now.replace(hour=0, minute=0, second=0, microsecond=0)
    for ss in scored_symbols:
        existing = await session.execute(
            text("""
                SELECT 1 FROM score_snapshots
                WHERE time = :time AND symbol = :symbol
            """),
            {"time": today_key, "symbol": ss.symbol},
        )
        if existing.fetchone():
            continue

        record = ScoreSnapshot(
            time=today_key,
            symbol=ss.symbol,
            quality_score=_d(ss.quality.get("score")),
            value_score=_d(ss.value.get("score")),
            technical_score=_d(ss.technical.get("total")),
            moat_score=_d(ss.moat),
            management_score=_d(ss.management.get("score")),
            macro_overlay=None,
            total_score=_d(ss.total_score),
            passed_screening=ss.passed_screening,
            screening_detail=str(ss.screening_detail) if ss.screening_detail else None,
            signal=ss.signal,
        )
        session.add(record)
    await session.flush()
    logger.info("Persisted %d score snapshots", len(scored_symbols))


def _d(val: Any) -> Decimal | None:
    if val is None:
        return None
    try:
        return Decimal(str(val))
    except (ValueError, TypeError):
        return None
