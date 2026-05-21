from decimal import Decimal
import pytest

from pipeline.scoring.gates import (
    check_screening_gate,
    _check_de,
    _check_roe_consistent,
    _check_market_cap,
    _check_adtv,
    _check_fcf,
)
from tests.conftest import make_mock_result


@pytest.mark.asyncio
async def test_de_check_pass(mock_session):
    mock_session.execute.return_value = make_mock_result(
        single_row=(Decimal("5000"), Decimal("10000"))
    )
    ok, val = await _check_de(mock_session, "FPT", is_bank=False)
    assert ok is True
    assert val == Decimal("0.5")


@pytest.mark.asyncio
async def test_de_check_fail(mock_session):
    mock_session.execute.return_value = make_mock_result(
        single_row=(Decimal("20000"), Decimal("10000"))
    )
    ok, val = await _check_de(mock_session, "FPT", is_bank=False)
    assert ok is False
    assert val == Decimal("2.0")


@pytest.mark.asyncio
async def test_de_check_bank_pass(mock_session):
    mock_session.execute.return_value = make_mock_result(
        single_row=(Decimal("50000"), Decimal("10000"))
    )
    ok, val = await _check_de(mock_session, "BID", is_bank=True)
    assert ok is True


@pytest.mark.asyncio
async def test_de_check_missing(mock_session):
    mock_session.execute.return_value = make_mock_result(single_row=None)
    ok, val = await _check_de(mock_session, "FPT", is_bank=False)
    assert ok is None
    assert val is None


@pytest.mark.asyncio
async def test_roe_consistent_pass(mock_session):
    mock_session.execute.return_value = make_mock_result(rows=[
        (2025, Decimal("3000"), Decimal("10000")),
        (2024, Decimal("2500"), Decimal("9000")),
        (2023, Decimal("2000"), Decimal("8000")),
    ])
    ok, val = await _check_roe_consistent(mock_session, "FPT")
    assert ok is True


@pytest.mark.asyncio
async def test_roe_consistent_fail(mock_session):
    mock_session.execute.return_value = make_mock_result(rows=[
        (2025, Decimal("500"), Decimal("10000")),
        (2024, Decimal("300"), Decimal("9000")),
        (2023, Decimal("100"), Decimal("8000")),
    ])
    ok, val = await _check_roe_consistent(mock_session, "FPT")
    assert ok is False


@pytest.mark.asyncio
async def test_roe_consistent_not_enough_data(mock_session):
    mock_session.execute.return_value = make_mock_result(rows=[
        (2025, Decimal("3000"), Decimal("10000")),
    ])
    ok, val = await _check_roe_consistent(mock_session, "FPT")
    assert ok is None


@pytest.mark.asyncio
async def test_market_cap_pass(mock_session):
    mock_session.execute.return_value = make_mock_result(
        single_row=(Decimal("10e12"),)
    )
    ok, val = await _check_market_cap(mock_session, "FPT")
    assert ok is True
    assert val == Decimal("10000")


@pytest.mark.asyncio
async def test_market_cap_fail(mock_session):
    mock_session.execute.return_value = make_mock_result(
        single_row=(Decimal("1e12"),)
    )
    ok, val = await _check_market_cap(mock_session, "FPT")
    assert ok is False


@pytest.mark.asyncio
async def test_adtv_pass(mock_session):
    mock_session.execute.return_value = make_mock_result(
        rows=tuple((Decimal("5e6"),) for _ in range(20))
    )
    ok, val = await _check_adtv(mock_session, "FPT")
    assert ok is True


@pytest.mark.asyncio
async def test_adtv_not_enough_data(mock_session):
    mock_session.execute.return_value = make_mock_result(
        rows=tuple((Decimal("5e6"),) for _ in range(5))
    )
    ok, val = await _check_adtv(mock_session, "FPT")
    assert ok is None


@pytest.mark.asyncio
async def test_fcf_pass(mock_session):
    mock_session.execute.return_value = make_mock_result(rows=[
        (2025, Decimal("1000")),
        (2024, Decimal("800")),
        (2023, Decimal("-200")),
    ])
    ok, val = await _check_fcf(mock_session, "FPT")
    assert ok is True


@pytest.mark.asyncio
async def test_fcf_fail(mock_session):
    mock_session.execute.return_value = make_mock_result(rows=[
        (2025, Decimal("-1000")),
        (2024, Decimal("-800")),
        (2023, Decimal("200")),
    ])
    ok, val = await _check_fcf(mock_session, "FPT")
    assert ok is False


@pytest.mark.asyncio
async def test_full_gate_pass(mock_session):
    mock_session.execute.side_effect = [
        make_mock_result(single_row=(Decimal("5000"), Decimal("10000"))),
        make_mock_result(rows=[
            (2025, Decimal("3000"), Decimal("10000")),
            (2024, Decimal("2500"), Decimal("9000")),
            (2023, Decimal("2000"), Decimal("8000")),
        ]),
        make_mock_result(single_row=(Decimal("10e12"),)),
        make_mock_result(rows=tuple((Decimal("5e6"),) for _ in range(20))),
        make_mock_result(rows=[(2025, Decimal("1000")), (2024, Decimal("800")), (2023, Decimal("200"))]),
    ]
    result = await check_screening_gate(mock_session, "FPT")
    assert result["passed"] is True
