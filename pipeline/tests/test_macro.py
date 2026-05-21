from decimal import Decimal
from unittest.mock import MagicMock
import pytest

from pipeline.scoring.macro import compute_macro_overlay


@pytest.mark.asyncio
async def test_macro_vnindex_uptrend(mock_session):
    closes_250 = [Decimal("100") + Decimal(str(i)) for i in range(250)]
    mock_session.execute.side_effect = [
        MagicMock(fetchall=MagicMock(
            return_value=[[None, c] for c in reversed(closes_250)]
        )),
        MagicMock(fetchall=MagicMock(return_value=[])),
    ]
    result = await compute_macro_overlay(mock_session)
    assert result["adjustment"] > 0
    assert "vnindex_uptrend" in result["signals"]


@pytest.mark.asyncio
async def test_macro_vnindex_downtrend(mock_session):
    closes_250 = [Decimal("100") - Decimal(str(i * 0.5)) for i in range(250)]
    mock_session.execute.side_effect = [
        MagicMock(fetchall=MagicMock(
            return_value=[[None, c] for c in reversed(closes_250)]
        )),
        MagicMock(fetchall=MagicMock(return_value=[])),
    ]
    result = await compute_macro_overlay(mock_session)
    assert result["adjustment"] < 0
    assert "vnindex_downtrend" in result["signals"]


@pytest.mark.asyncio
async def test_macro_no_data(mock_session):
    mock_session.execute.return_value.fetchall.return_value = []
    result = await compute_macro_overlay(mock_session)
    assert result["adjustment"] == Decimal("0")
    assert result["signals"] == []
