import logging
import re
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from typing import Any

import httpx
import pdfplumber
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.db.models import IngestionLog, IngestionStatus

logger = logging.getLogger(__name__)

TCBS_URL = "https://static.tcbs.com.vn/oneclick/{symbol}.pdf"

METRIC_MAP: dict[str, str | None] = {
    "SL Cổ phiếu (tr)": "issued_shares",
    "Doanh thu thuần": "revenue",
    "Lợi nhuận sau thuế": "net_income",
    "Tổng tài sản": "total_assets",
    "Tổng nợ": "total_liabilities",
    "Vốn CSH": "total_equity",
    "Tiền & ĐT NH": "cash",
    "Tổng vay": "debt",
    "Free CashFlow": "free_cash_flow",
    "EBITDA": None,
    "Giá vốn bán hàng": "cost_of_goods_sold",
    "Lợi nhuận gộp": "gross_profit",
    "Chi phí hoạt động": "operating_expense",
    "LN hoạt động": "operating_profit",
}

MULTIPLIERS: dict[str, int] = {
    "issued_shares": 1_000_000,
}

RE_NUMBER = re.compile(r'^-?[\d,]+(?:\.[\d,]+)?%?$')


def _parse_num(text: str) -> Decimal | None:
    text = text.strip().replace(",", "")
    if not text or text == "-" or text == "N/A":
        return None
    is_pct = text.endswith("%")
    if is_pct:
        text = text[:-1]
    try:
        return Decimal(text)
    except Exception:
        return None


async def download_pdf(symbol: str, dest: Path | None = None) -> bytes:
    url = TCBS_URL.format(symbol=symbol)
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        return resp.content


def extract_financial_data_from_pdf(pdf_bytes: bytes) -> list[dict[str, Any]]:
    """Parse TCBS one-click PDF report.

    Returns a list of dicts, one per year with actual data (not projections).
    """
    import io
    pdf_file = io.BytesIO(pdf_bytes)

    pages_data: list[list[dict]] = []  # list of pages, each page is list of {x, y, text}

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            words = page.extract_words(keep_blank_chars=True)
            page_words = [
                {"x": int(w["x0"]), "y": int(w["top"]), "text": w["text"]}
                for w in words
            ]
            pages_data.append(page_words)

    # Find "Năm - VNDbn" header on page 2 to locate the table
    header_page = None
    header_y = None
    columns: list[dict] = []  # [{x, year_label}]

    for pi, page_words in enumerate(pages_data):
        for w in page_words:
            if "VNDbn" in w["text"] or "VND" in w["text"]:
                header_page = page_words
                header_y = w["y"]
                break
        if header_page is not None:
            break

    if header_page is None:
        logger.warning("Could not find 'VNDbn' header in PDF")
        return []

    # Extract year columns from header row: find words on same y as header
    # that look like years
    header_words = [w for w in header_page if abs(w["y"] - header_y) <= 8]
    header_words.sort(key=lambda w: w["x"])

    for w in header_words:
        text = w["text"].strip()
        if text.isdigit() and len(text) == 4 and 2020 <= int(text) <= 2035:
            columns.append({"x": w["x"], "year": int(text)})

    if not columns:
        logger.warning("No year columns found in header")
        return []

    logger.info("Found columns: %s", [(c["year"], c["x"]) for c in columns])

    # Build metric label rows from the page
    metrics: list[dict] = []
    for w in header_page:
        x = w["x"]
        text = w["text"].strip()
        if text in METRIC_MAP and x < 60:
            metrics.append({"label": text, "y": w["y"], "field": METRIC_MAP[text]})

    metrics.sort(key=lambda m: m["y"])
    logger.info("Found %d metrics: %s", len(metrics), [m["label"] for m in metrics])

    if not metrics:
        logger.warning("No recognized metrics found on header page")
        return []

    # Extract data: for each metric row, find values at each column x-position
    column_tolerance = 20

    records_by_year: dict[int, dict] = {}
    for col in columns:
        records_by_year[col["year"]] = {"year": col["year"], "period": "FY"}

    for metric in metrics:
        metric_y = metric["y"]
        field = metric["field"]
        if field is None:
            continue

        for col in columns:
            col_x = col["x"]
            year = col["year"]

            found_words = [
                w for w in header_page
                if abs(w["y"] - metric_y) <= 6
                and abs(w["x"] - col_x) <= column_tolerance
                and RE_NUMBER.match(w["text"].strip())
            ]
            if found_words:
                word = min(found_words, key=lambda w: abs(w["x"] - col_x))
                val = _parse_num(word["text"])
                multiplier = MULTIPLIERS.get(field, 1)
                if val is not None and multiplier != 1:
                    val = val * multiplier
                records_by_year[year][field] = val

    actual_years = [y for y in records_by_year if y <= date.today().year]
    actual_years.sort()

    result = [records_by_year[y] for y in actual_years]
    return result


async def ingest_tcbs_financial_reports(
    session: AsyncSession,
    symbol: str,
    pdf_bytes: bytes | None = None,
) -> int:
    log_entry = IngestionLog(
        task_name="tcbs_financial_reports",
        symbol=symbol,
        status=IngestionStatus.running,
        started_at=datetime.utcnow(),
    )
    session.add(log_entry)
    await session.flush()

    try:
        if pdf_bytes is None:
            pdf_bytes = await download_pdf(symbol)

        records = extract_financial_data_from_pdf(pdf_bytes)
        if not records:
            log_entry.status = IngestionStatus.skipped
            log_entry.completed_at = datetime.utcnow()
            await session.flush()
            return 0

        rows = 0
        for record in records:
            year = record["year"]
            if year > date.today().year:
                continue

            existing = await session.execute(
                text("SELECT id FROM financial_reports WHERE symbol = :symbol AND year = :year FOR UPDATE"),
                {"symbol": symbol, "year": year},
            )
            row = existing.fetchone()

            field_map = {
                "revenue": record.get("revenue"),
                "net_income": record.get("net_income"),
                "total_assets": record.get("total_assets"),
                "total_liabilities": record.get("total_liabilities"),
                "total_equity": record.get("total_equity"),
                "cash": record.get("cash"),
                "debt": record.get("debt"),
                "free_cash_flow": record.get("free_cash_flow"),
                "cost_of_goods_sold": record.get("cost_of_goods_sold"),
                "gross_profit": record.get("gross_profit"),
                "operating_expense": record.get("operating_expense"),
                "operating_profit": record.get("operating_profit"),
            }
            # Only update non-None fields
            set_parts = []
            params: dict = {}
            for fname, fval in field_map.items():
                if fval is not None:
                    set_parts.append(f"{fname} = :{fname}")
                    params[fname] = fval

            shares = record.get("issued_shares")
            if shares is not None:
                set_parts.append("issued_shares = :issued_shares")
                params["issued_shares"] = shares

            if not set_parts:
                continue

            params["symbol"] = symbol
            params["year"] = year

            if row:
                set_sql = ", ".join(set_parts)
                await session.execute(
                    text(f"UPDATE financial_reports SET {set_sql} WHERE id = :id"),
                    {**params, "id": row[0]},
                )
            else:
                col_names = ", ".join(list(field_map.keys()) + ["issued_shares", "symbol", "year", "period"])
                val_placeholders = ", ".join([f":{c}" for c in list(field_map.keys()) + ["issued_shares", "symbol", "year", "period"]])
                await session.execute(
                    text(f"INSERT INTO financial_reports ({col_names}) VALUES ({val_placeholders})"),
                    {
                        **field_map,
                        "issued_shares": shares,
                        "symbol": symbol,
                        "year": year,
                        "period": "FY",
                    },
                )
            rows += 1

        await session.flush()
        log_entry.status = IngestionStatus.completed
        log_entry.rows_inserted = rows
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.info("TCBS financial reports ingested for %s (%d years)", symbol, rows)
        return rows

    except Exception as e:
        log_entry.status = IngestionStatus.failed
        log_entry.error_message = str(e)
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.error("TCBS reports ingestion failed for %s: %s", symbol, e)
        raise
