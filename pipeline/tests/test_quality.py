from decimal import Decimal
import pytest

from pipeline.scoring.quality import compute_quality_score
from tests.conftest import make_mock_result


@pytest.mark.asyncio
async def test_quality_high_roe_low_de(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=(
            Decimal("3000"), Decimal("10000"), Decimal("3000"),
            Decimal("1000"), Decimal("1000000"),
        )),
        make_mock_result(single_row=(Decimal("50000"),)),
    ]
    result = await compute_quality_score(mock_session, "FPT")
    assert result["score"] >= Decimal("7")
    assert result["roe"] == Decimal("0.3")


@pytest.mark.asyncio
async def test_quality_mid_roe(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=(
            Decimal("1300"), Decimal("10000"), Decimal("2000"),
            None, None,
        )),
    ]
    result = await compute_quality_score(mock_session, "FPT")
    assert result["de"] == Decimal("0.2")


@pytest.mark.asyncio
async def test_quality_no_data(mock_session):
    mock_session.execute.return_value = make_mock_result(single_row=None)
    result = await compute_quality_score(mock_session, "XYZ")
    assert result["score"] == Decimal("0")
    assert result["roe"] is None
