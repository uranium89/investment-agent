from decimal import Decimal
import pytest

from pipeline.scoring.technical import compute_technical_score
from tests.conftest import make_mock_result


@pytest.mark.asyncio
async def test_technical_full_trend(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=(
            None, Decimal("50"), Decimal("100"), Decimal("80"),
            Decimal("40"), Decimal("1"), Decimal("0.5"), Decimal("0.5"),
            Decimal("100000"),
        )),
        make_mock_result(single_row=(Decimal("150"),)),
        make_mock_result(rows=tuple(
            (i, Decimal("120"), Decimal("115"), Decimal("110")) for i in range(30)
        )),
        make_mock_result(single_row=(Decimal("200000"),)),
    ]
    result = await compute_technical_score(mock_session, "FPT")
    assert result["trend_score"] >= 6


@pytest.mark.asyncio
async def test_technical_no_data(mock_session):
    mock_session.execute.return_value = make_mock_result(single_row=None)
    result = await compute_technical_score(mock_session, "XYZ")
    assert result["trend_score"] == 0
    assert result["total"] == Decimal("0")
