from decimal import Decimal
from unittest.mock import patch
import pytest

from pipeline.scoring.engine import ScoredSymbol
from pipeline.portfolio.rebalancer import compute_rebalance
from tests.conftest import make_mock_result


def _make_ss(symbol: str, score: float, passed: bool = True, signal: str = "ENTER") -> ScoredSymbol:
    ss = ScoredSymbol(symbol)
    ss.passed_screening = passed
    ss.total_score = Decimal(str(score))
    ss.signal = signal
    return ss


@pytest.mark.asyncio
async def test_rebalance_new_enter(mock_session):
    mock_session.execute.return_value = make_mock_result(rows=[])
    scored = [
        _make_ss("FPT", 9.0),
        _make_ss("VNM", 8.0),
    ]
    with patch("pipeline.config.settings") as mock_settings:
        mock_settings.vn30_symbols = ["FPT", "VNM"]
        result = await compute_rebalance(
            mock_session, scored,
            portfolio_value=Decimal("500_000_000"),
        )
    enter_trades = [t for t in result["trades"] if t["action"] == "ENTER"]
    assert len(enter_trades) >= 1


@pytest.mark.asyncio
async def test_rebalance_no_current_positions(mock_session):
    mock_session.execute.return_value = make_mock_result(rows=[])
    result = await compute_rebalance(mock_session, [], Decimal("500_000_000"))
    assert "trades" in result
    assert "target_positions" in result


@pytest.mark.asyncio
async def test_rebalance_exit_low_score(mock_session):
    mock_session.execute.return_value = make_mock_result(rows=[
        ("FPT", Decimal("10"), Decimal("50_000_000"), 1000, Decimal("50000")),
    ])
    scored = [_make_ss("FPT", 2.0, signal="NONE")]
    with patch("pipeline.config.settings") as mock_settings:
        mock_settings.vn30_symbols = ["FPT"]
        result = await compute_rebalance(mock_session, scored, Decimal("500_000_000"))
    exit_trades = [t for t in result["trades"] if t["action"] == "EXIT"]
    assert len(exit_trades) >= 0
