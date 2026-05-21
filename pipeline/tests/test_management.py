import pytest
from decimal import Decimal

from pipeline.scoring.management import compute_management_score


@pytest.mark.asyncio
async def test_management_insider_buying(mock_session, mock_fireant):
    mock_fireant.transactions.return_value = [
        {"type": "buy", "volume": 100000},
        {"type": "buy", "volume": 50000},
        {"type": "sell", "volume": 10000},
    ]
    mock_fireant.officers.return_value = [
        {"position": "CEO - Tổng Giám Đốc"},
    ]
    result = await compute_management_score(mock_session, mock_fireant, "FPT")
    assert result["score"] > Decimal("5")


@pytest.mark.asyncio
async def test_management_insider_selling(mock_session, mock_fireant):
    mock_fireant.transactions.return_value = [
        {"type": "sell", "volume": 100000},
        {"type": "sell", "volume": 50000},
        {"type": "buy", "volume": 10000},
    ]
    mock_fireant.officers.return_value = [
        {"position": "CEO - Tổng Giám Đốc"},
    ]
    result = await compute_management_score(mock_session, mock_fireant, "FPT")
    assert result["score"] < Decimal("5")


@pytest.mark.asyncio
async def test_management_api_error(mock_session, mock_fireant):
    mock_fireant.transactions.side_effect = Exception("API error")
    mock_fireant.officers.side_effect = Exception("API error")
    result = await compute_management_score(mock_session, mock_fireant, "FPT")
    assert result["score"] == Decimal("5")
