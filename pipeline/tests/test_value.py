from decimal import Decimal
import pytest

from pipeline.scoring.value import compute_value_score
from tests.conftest import make_mock_result


@pytest.mark.asyncio
async def test_value_low_pe_high_score(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=(Decimal("8"), Decimal("1.5"))),
        make_mock_result(rows=[
            ("ACB", 12), ("FPT", 15), ("HPG", 10),
            ("VNM", 8), ("VCB", 18), ("MWG", 14),
            ("TCB", 9), ("MBB", 11), ("CTG", 16),
            ("BID", 20), ("VPB", 13), ("HDB", 17),
            ("SSI", 7), ("STB", 6),
        ]),
    ]
    result = await compute_value_score(mock_session, "VNM")
    assert result["score"] > Decimal("7")
    assert result["pe"] == Decimal("8")


@pytest.mark.asyncio
async def test_value_high_pe_low_score(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=(Decimal("25"), Decimal("3.5"))),
        make_mock_result(rows=[
            ("ACB", 12), ("FPT", 15), ("HPG", 10),
            ("VNM", 8), ("VCB", 18), ("MWG", 14),
        ]),
    ]
    result = await compute_value_score(mock_session, "XYZ")
    assert result["score"] < Decimal("3")
    assert result["pb"] == Decimal("3.5")


@pytest.mark.asyncio
async def test_value_pb_bonus(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=(Decimal("10"), Decimal("1.2"))),
        make_mock_result(rows=[
            ("ACB", 12), ("FPT", 15), ("HPG", 10),
            ("VNM", 8), ("VCB", 18), ("MWG", 14),
            ("TCB", 9), ("MBB", 11), ("CTG", 16),
            ("BID", 20), ("VPB", 13), ("HDB", 17),
            ("SSI", 7), ("STB", 6),
        ]),
    ]
    result = await compute_value_score(mock_session, "ACB")
    assert result["pe"] == Decimal("10")


@pytest.mark.asyncio
async def test_value_no_pe_data(mock_session):
    mock_session.execute.return_value = make_mock_result(single_row=None)
    result = await compute_value_score(mock_session, "XYZ")
    assert result["score"] == Decimal("0")
