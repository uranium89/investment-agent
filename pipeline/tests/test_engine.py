from decimal import Decimal
from unittest.mock import patch, AsyncMock
import pytest

from pipeline.scoring.engine import (
    ScoredSymbol,
    _determine_signal,
)


def test_scored_symbol_initial():
    ss = ScoredSymbol("FPT")
    assert ss.symbol == "FPT"
    assert ss.passed_screening is False
    assert ss.total_score == Decimal("0")
    assert ss.signal == "NONE"


def test_scored_symbol_component_total():
    ss = ScoredSymbol("FPT")
    ss.quality["score"] = Decimal("8")
    ss.value["score"] = Decimal("6")
    ss.technical["total"] = Decimal("4")
    ss.moat = Decimal("7")
    ss.management["score"] = Decimal("5")
    assert ss.component_total == Decimal("30")


def test_determine_signal_enter():
    assert _determine_signal(None, "FPT", Decimal("6.0")) == "ENTER"


def test_determine_signal_hold():
    assert _determine_signal(None, "FPT", Decimal("4.0")) == "HOLD"


def test_determine_signal_none():
    assert _determine_signal(None, "FPT", Decimal("2.0")) == "NONE"


@pytest.mark.asyncio
async def test_run_scoring(mock_session):
    with (
        patch("pipeline.scoring.engine.compute_macro_overlay") as mock_macro,
        patch("pipeline.scoring.engine._score_symbol") as mock_score,
        patch("pipeline.scoring.engine.settings") as mock_settings,
        patch("pipeline.scoring.engine._persist_scores") as mock_persist,
    ):
        mock_macro.return_value = {"adjustment": Decimal("0"), "signals": []}
        mock_score.return_value = ScoredSymbol("FPT")
        mock_settings.vn30_symbols = ["FPT", "ACB", "HPG"]

        from pipeline.scoring.engine import run_scoring
        result = await run_scoring(mock_session, None)

    assert len(result) == 3
    mock_macro.assert_called_once()


@pytest.mark.asyncio
async def test_run_scoring_partial_failure(mock_session):
    call_count = [0]

    async def score_side_effect(session, fireant, symbol, adjustment):
        call_count[0] += 1
        if symbol == "ACB":
            raise ValueError("Simulated failure")
        ss = ScoredSymbol(symbol)
        ss.total_score = Decimal("6")
        ss.signal = "ENTER"
        return ss

    with (
        patch("pipeline.scoring.engine.compute_macro_overlay") as mock_macro,
        patch("pipeline.scoring.engine._score_symbol", side_effect=score_side_effect),
        patch("pipeline.scoring.engine.settings") as mock_settings,
        patch("pipeline.scoring.engine._persist_scores") as mock_persist,
    ):
        mock_macro.return_value = {"adjustment": Decimal("0"), "signals": []}
        mock_settings.vn30_symbols = ["FPT", "ACB", "HPG"]

        from pipeline.scoring.engine import run_scoring
        result = await run_scoring(mock_session, None)

    assert len(result) == 2
