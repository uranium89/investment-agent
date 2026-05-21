from decimal import Decimal
import pytest

from pipeline.scoring.engine import ScoredSymbol
from pipeline.portfolio.constructor import construct_portfolio


def _make_ss(symbol: str, score: float, passed: bool = True, signal: str = "ENTER") -> ScoredSymbol:
    ss = ScoredSymbol(symbol)
    ss.passed_screening = passed
    ss.total_score = Decimal(str(score))
    ss.signal = signal
    return ss


@pytest.mark.asyncio
async def test_construct_portfolio_selects_top(mock_session):
    symbols = [
        _make_ss("FPT", 9.0),
        _make_ss("VNM", 8.5),
        _make_ss("HPG", 8.0),
        _make_ss("VCB", 7.5),
        _make_ss("ACB", 2.0, signal="HOLD"),
    ]
    result = await construct_portfolio(mock_session, symbols)
    assert result["total_positions"] >= 3
    symbols_in_port = {p["symbol"] for p in result["positions"]}
    assert "FPT" in symbols_in_port
    assert "VNM" in symbols_in_port
    assert "ACB" not in symbols_in_port


@pytest.mark.asyncio
async def test_construct_portfolio_no_qualified(mock_session):
    result = await construct_portfolio(mock_session, [])
    assert result["cash_pct"] == 100
    assert result["positions"] == []


@pytest.mark.asyncio
async def test_construct_portfolio_sector_limit(mock_session):
    symbols = [
        _make_ss("ACB", 9.0),
        _make_ss("VCB", 8.5),
        _make_ss("BID", 8.0),
        _make_ss("CTG", 7.5),
        _make_ss("TCB", 7.0),
        _make_ss("MBB", 6.5),
        _make_ss("FPT", 8.0),
    ]
    result = await construct_portfolio(mock_session, symbols)
    fin_weight = sum(p["weight_pct"] for p in result["positions"] if p["sector"] == "financial")
    assert fin_weight <= 40, f"Financial sector weight {fin_weight} exceeds 40% limit"


@pytest.mark.asyncio
async def test_construct_portfolio_max_single_limit(mock_session):
    symbols = [
        _make_ss("FPT", 10.0),
        _make_ss("VNM", 2.0),
    ]
    result = await construct_portfolio(mock_session, symbols)
    for p in result["positions"]:
        assert p["weight_pct"] <= 10
