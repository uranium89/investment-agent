import logging
from datetime import date
from pathlib import Path

import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

WAREHOUSE_DIR = Path(__file__).resolve().parent.parent.parent / "warehouse"


def ensure_warehouse_dir():
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)


async def export_ohlc_parquet(
    session: AsyncSession,
    symbol: str,
    start_date: date | None = None,
    end_date: date | None = None,
) -> Path:
    ensure_warehouse_dir()

    query = "SELECT * FROM ohlc_prices WHERE symbol = :symbol"
    params: dict = {"symbol": symbol}
    if start_date:
        query += " AND time >= :start"
        params["start"] = start_date.isoformat()
    if end_date:
        query += " AND time <= :end"
        params["end"] = end_date.isoformat()
    query += " ORDER BY time ASC"

    result = await session.execute(text(query), params)
    rows = result.fetchall()
    if not rows:
        raise ValueError(f"No data for {symbol}")

    df = pd.DataFrame(rows, columns=result.keys())
    for col in ["open", "high", "low", "close", "adj_close"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    fpath = WAREHOUSE_DIR / f"{symbol}_ohlc.parquet"
    df.to_parquet(fpath, index=False)
    logger.info("Exported %s to %s (%d rows)", symbol, fpath, len(df))
    return fpath


async def export_technical_parquet(
    session: AsyncSession,
    symbol: str,
) -> Path:
    ensure_warehouse_dir()

    result = await session.execute(
        text("""
            SELECT * FROM technical_indicators
            WHERE symbol = :symbol
            ORDER BY time ASC
        """),
        {"symbol": symbol},
    )
    rows = result.fetchall()
    if not rows:
        raise ValueError(f"No technical data for {symbol}")

    df = pd.DataFrame(rows, columns=result.keys())
    fpath = WAREHOUSE_DIR / f"{symbol}_technical.parquet"
    df.to_parquet(fpath, index=False)
    logger.info("Exported technicals for %s to %s", symbol, fpath)
    return fpath


async def export_portfolio_snapshot(
    session: AsyncSession,
    metrics: dict,
) -> Path:
    ensure_warehouse_dir()
    df = pd.DataFrame([metrics])
    fpath = WAREHOUSE_DIR / f"portfolio_snapshot_{date.today().isoformat()}.parquet"
    df.to_parquet(fpath, index=False)
    return fpath
