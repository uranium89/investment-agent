import logging
from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.config import settings

logger = logging.getLogger(__name__)

BANK_SYMBOLS = {"BID", "CTG", "VCB", "TCB", "MBB", "ACB", "VPB", "HDB", "TPB", "SHB", "STB", "SSB", "LPB", "OCB", "MSB", "EIB", "NAB", "VIB", "OCE"}
BANK_SPECIAL_DE = 10.0
MIN_MARKET_CAP = Decimal("5000")  # tỷ
MIN_ADTV = Decimal("30")  # tỷ/ngày


async def check_screening_gate(
    session: AsyncSession,
    symbol: str,
) -> dict[str, Any]:
    is_bank = symbol in BANK_SYMBOLS

    de_ok, de_val = await _check_de(session, symbol, is_bank)
    roe_ok, roe_val = await _check_roe_consistent(session, symbol)
    mcap_ok, mcap_val = await _check_market_cap(session, symbol)
    adtv_ok, adtv_val = await _check_adtv(session, symbol)
    fcf_ok, fcf_val = await _check_fcf(session, symbol)

    checks = {
        "de_check": de_ok,
        "de_value": de_val,
        "roe_check": roe_ok,
        "roe_value": roe_val,
        "market_cap_check": mcap_ok,
        "market_cap_value": mcap_val,
        "adtv_check": adtv_ok,
        "adtv_value": adtv_val,
        "fcf_check": fcf_ok,
        "fcf_value": fcf_val,
    }

    passed = all([
        de_ok is not False,
        roe_ok is not False,
        mcap_ok is not False,
        adtv_ok is not False,
        fcf_ok is not False,
    ])

    return {"passed": passed, **checks}


async def _check_de(session: AsyncSession, symbol: str, is_bank: bool) -> tuple[bool | None, Decimal | None]:
    max_de = BANK_SPECIAL_DE if is_bank else Decimal("1.5")
    result = await session.execute(
        text("""
            SELECT debt, total_equity FROM financial_reports
            WHERE symbol = :symbol AND debt IS NOT NULL AND total_equity IS NOT NULL
            ORDER BY year DESC, period DESC
            LIMIT 1
        """),
        {"symbol": symbol},
    )
    row = result.fetchone()
    if not row:
        return None, None
    debt, equity = row
    if not debt or not equity or Decimal(str(equity)) == 0:
        return None, None
    de = Decimal(str(debt)) / Decimal(str(equity))
    return de < max_de, de


async def _check_roe_consistent(session: AsyncSession, symbol: str) -> tuple[bool | None, Decimal | None]:
    result = await session.execute(
        text("""
            SELECT year, net_income, total_equity FROM financial_reports
            WHERE symbol = :symbol AND net_income IS NOT NULL AND total_equity IS NOT NULL
            ORDER BY year DESC
            LIMIT 3
        """),
        {"symbol": symbol},
    )
    rows = result.fetchall()
    if len(rows) < 3:
        return None, None
    roe_values = []
    for r in rows:
        _, net_income, total_equity = r
        if total_equity and Decimal(str(total_equity)) != 0:
            roe = Decimal(str(net_income)) / Decimal(str(total_equity))
            roe_values.append(roe)
    if len(roe_values) < 2:
        return None, None
    latest_roe = roe_values[0]
    all_above_10 = all(r > Decimal("0.10") for r in roe_values)
    return all_above_10, latest_roe


async def _check_market_cap(session: AsyncSession, symbol: str) -> tuple[bool | None, Decimal | None]:
    result = await session.execute(
        text("""
            SELECT market_cap FROM financial_indicators
            WHERE symbol = :symbol AND market_cap IS NOT NULL
            ORDER BY date DESC
            LIMIT 1
        """),
        {"symbol": symbol},
    )
    row = result.fetchone()
    if not row:
        return None, None
    mcap = Decimal(str(row[0])) / Decimal("1e9")
    return mcap >= MIN_MARKET_CAP, mcap


async def _check_adtv(session: AsyncSession, symbol: str) -> tuple[bool | None, Decimal | None]:
    result = await session.execute(
        text("""
            SELECT volume FROM ohlc_prices
            WHERE symbol = :symbol AND volume IS NOT NULL
            ORDER BY time DESC
            LIMIT 20
        """),
        {"symbol": symbol},
    )
    rows = result.fetchall()
    if len(rows) < 20:
        return None, None
    volumes = [Decimal(str(r[0])) for r in rows if r[0]]
    if not volumes:
        return None, None
    avg_volume = sum(volumes) / len(volumes)
    avg_value_vnd = avg_volume * Decimal("1e4")
    avg_value_billion = avg_value_vnd / Decimal("1e9")
    return avg_value_billion >= MIN_ADTV, avg_value_billion


async def _check_fcf(session: AsyncSession, symbol: str) -> tuple[bool | None, Decimal | None]:
    result = await session.execute(
        text("""
            SELECT year, free_cash_flow FROM financial_reports
            WHERE symbol = :symbol AND free_cash_flow IS NOT NULL
            ORDER BY year DESC
            LIMIT 3
        """),
        {"symbol": symbol},
    )
    rows = result.fetchall()
    if not rows:
        return None, None
    positive_count = sum(1 for r in rows if r[1] and Decimal(str(r[1])) > 0)
    latest_fcf = Decimal(str(rows[0][1])) if rows[0][1] else None
    return positive_count >= 2, latest_fcf
