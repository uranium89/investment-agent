from decimal import Decimal
import pytest

from pipeline.portfolio.sizing import calculate_position_size
from tests.conftest import make_mock_result


@pytest.mark.asyncio
async def test_sizing_with_atr(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=(Decimal("1000"),)),
        make_mock_result(single_row=(Decimal("50000"),)),
    ]
    result = await calculate_position_size(
        mock_session, "FPT",
        portfolio_value=Decimal("500_000_000"),
        weight_pct=Decimal("10"),
    )
    assert result["final_shares"] > 0
    assert result["symbol"] == "FPT"


@pytest.mark.asyncio
async def test_sizing_no_atr(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=None),
        make_mock_result(single_row=(Decimal("50000"),)),
    ]
    result = await calculate_position_size(
        mock_session, "FPT",
        portfolio_value=Decimal("500_000_000"),
        weight_pct=Decimal("10"),
    )
    assert result["final_shares"] >= 0


@pytest.mark.asyncio
async def test_sizing_minimum_shares(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=(Decimal("1000"),)),
        make_mock_result(single_row=(Decimal("100000"),)),
    ]
    result = await calculate_position_size(
        mock_session, "FPT",
        portfolio_value=Decimal("10_000_000"),
        weight_pct=Decimal("5"),
    )
    assert result["final_shares"] >= 0
