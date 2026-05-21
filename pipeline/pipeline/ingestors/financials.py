import logging
from datetime import datetime, date
from decimal import Decimal
from typing import Any

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.clients.fireant import FireAntClient
from pipeline.db.models import (
    FinancialReport, FinancialIndicator,
    IngestionLog, IngestionStatus,
)

logger = logging.getLogger(__name__)


async def ingest_fundamental(
    session: AsyncSession,
    client: FireAntClient,
    symbol: str,
) -> int:
    """Ingest fundamental data (market cap, PE, shares, etc.) from FireAnt fundamental endpoint."""
    log_entry = IngestionLog(
        task_name="fundamental_ingestion",
        symbol=symbol,
        status=IngestionStatus.running,
        started_at=datetime.utcnow(),
    )
    session.add(log_entry)
    await session.flush()

    try:
        data = await client.fundamental(symbol=symbol)
        if not data or not isinstance(data, dict):
            log_entry.status = IngestionStatus.skipped
            log_entry.completed_at = datetime.utcnow()
            await session.flush()
            return 0

        shares_outstanding = _d(data.get("sharesOutstanding"))
        market_cap = _d(data.get("marketCap"))
        pe = _d(data.get("pe"))
        eps = _d(data.get("eps"))
        beta = _d(data.get("beta"))
        dividend_yield = _d(data.get("dividendYield"))

        today = date.today()

        existing = await session.execute(
            text("SELECT id FROM financial_indicators WHERE symbol = :symbol AND date = :today FOR UPDATE"),
            {"symbol": symbol, "today": today},
        )
        row = existing.fetchone()
        if row:
            await session.execute(
                text("""
                    UPDATE financial_indicators
                    SET pe = :pe, market_cap = :market_cap, dividend_yield = :dividend_yield
                    WHERE id = :id
                """),
                {"id": row[0], "pe": pe, "market_cap": market_cap, "dividend_yield": dividend_yield},
            )
        else:
            record = FinancialIndicator(
                symbol=symbol, date=today,
                pe=pe, market_cap=market_cap, dividend_yield=dividend_yield,
            )
            session.add(record)

        existing_report = await session.execute(
            text("SELECT id FROM financial_reports WHERE symbol = :symbol AND year = :year FOR UPDATE"),
            {"symbol": symbol, "year": today.year},
        )
        report_row = existing_report.fetchone()
        net_income_val = Decimal(str(eps * shares_outstanding)) if eps and shares_outstanding else None
        if report_row:
            await session.execute(
                text("""
                    UPDATE financial_reports
                    SET issued_shares = :issued_shares, net_income = :net_income
                    WHERE id = :id
                """),
                {"id": report_row[0], "issued_shares": shares_outstanding, "net_income": net_income_val},
            )
        else:
            if shares_outstanding:
                report = FinancialReport(
                    symbol=symbol,
                    period="FY",
                    year=today.year,
                    issued_shares=shares_outstanding,
                    net_income=net_income_val,
                )
                session.add(report)

        await session.flush()
        log_entry.status = IngestionStatus.completed
        log_entry.rows_inserted = 1
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.info("Ingested fundamental data for %s", symbol)
        return 1

    except Exception as e:
        log_entry.status = IngestionStatus.failed
        log_entry.error_message = str(e)
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.error("Fundamental ingestion failed for %s: %s", symbol, e)
        raise


SHORTNAME_TO_FIELD: dict[str, str] = {
    "P/E": "pe",
    "P/S": "ps",
    "P/B": "pb",
    "ROE": "roe",
    "ROA": "roa",
    "Nợ/VCSH": "de_ratio",
    "TT Hiện hành": "current_ratio",
}


async def ingest_financial_indicators(
    session: AsyncSession,
    client: FireAntClient,
    symbol: str,
) -> int:
    log_entry = IngestionLog(
        task_name="financial_indicators",
        symbol=symbol,
        status=IngestionStatus.running,
        started_at=datetime.utcnow(),
    )
    session.add(log_entry)
    await session.flush()

    try:
        items = await client.financial_indicators(symbol=symbol)
        if not items or not isinstance(items, list):
            log_entry.status = IngestionStatus.skipped
            log_entry.completed_at = datetime.utcnow()
            await session.flush()
            return 0

        values: dict[str, Decimal | None] = {}
        for item in items:
            sn = item.get("shortName")
            if sn in SHORTNAME_TO_FIELD:
                values[SHORTNAME_TO_FIELD[sn]] = _d(item.get("value"))

        today = date.today()

        existing = await session.execute(
            text("SELECT id FROM financial_indicators WHERE symbol = :symbol AND date = :today FOR UPDATE"),
            {"symbol": symbol, "today": today},
        )
        row = existing.fetchone()

        if row:
            await session.execute(
                text("""
                    UPDATE financial_indicators
                    SET pe = :pe, ps = :ps, pb = :pb, roe = :roe, roa = :roa,
                        de_ratio = :de_ratio, current_ratio = :current_ratio
                    WHERE id = :id
                """),
                {
                    "id": row[0],
                    "pe": values.get("pe"),
                    "ps": values.get("ps"),
                    "pb": values.get("pb"),
                    "roe": values.get("roe"),
                    "roa": values.get("roa"),
                    "de_ratio": values.get("de_ratio"),
                    "current_ratio": values.get("current_ratio"),
                },
            )
        else:
            record = FinancialIndicator(
                symbol=symbol, date=today,
                pe=values.get("pe"), ps=values.get("ps"), pb=values.get("pb"),
                roe=values.get("roe"), roa=values.get("roa"),
                de_ratio=values.get("de_ratio"), current_ratio=values.get("current_ratio"),
            )
            session.add(record)

        log_entry.status = IngestionStatus.completed
        log_entry.rows_inserted = 1
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.info("Ingested indicators for %s", symbol)
        return 1

    except Exception as e:
        log_entry.status = IngestionStatus.failed
        log_entry.error_message = str(e)
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.error("Indicators ingestion failed for %s: %s", symbol, e)
        raise


def _d(val: Any) -> Decimal | None:
    if val is None:
        return None
    try:
        return Decimal(str(val))
    except (ValueError, TypeError):
        return None
