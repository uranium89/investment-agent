import logging
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Any

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.clients.fireant import FireAntClient
from pipeline.db.models import OHLCPrice, IngestionLog, IngestionStatus

logger = logging.getLogger(__name__)


async def ingest_ohlc(
    session: AsyncSession,
    client: FireAntClient,
    symbol: str,
    end_date: date | None = None,
    lookback_days: int = 365,
) -> int:
    end = end_date or date.today()
    start = end - timedelta(days=lookback_days)

    log_entry = IngestionLog(
        task_name="ohlc_ingestion",
        symbol=symbol,
        status=IngestionStatus.running,
        started_at=datetime.utcnow(),
    )
    session.add(log_entry)
    await session.flush()

    try:
        total = 0
        chunk_end = end

        while chunk_end > start:
            chunk_start = max(chunk_end - timedelta(days=30), start)
            raw_data = await client.historical_quotes(
                symbol=symbol,
                start_date=chunk_start.isoformat(),
                end_date=chunk_end.isoformat(),
                limit=500,
            )
            if not raw_data:
                chunk_end = chunk_start
                continue

            for item in raw_data:
                if not isinstance(item, dict):
                    continue

                ts = item.get("date") or item.get("tradingDate")
                if not ts:
                    continue
                if isinstance(ts, str):
                    try:
                        price_date = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    except ValueError:
                        price_date = datetime.strptime(ts[:10], "%Y-%m-%d")
                else:
                    price_date = datetime.utcnow()

                exists = await session.execute(
                    select(OHLCPrice).where(
                        OHLCPrice.time == price_date,
                        OHLCPrice.symbol == symbol,
                    )
                )
                if exists.scalar_one_or_none():
                    continue

                record = OHLCPrice(
                    time=price_date,
                    symbol=symbol,
                    open=_d(item.get("priceOpen") or item.get("open")),
                    high=_d(item.get("priceHigh") or item.get("high")),
                    low=_d(item.get("priceLow") or item.get("low")),
                    close=_d(item.get("priceClose") or item.get("close")),
                    volume=int(item.get("totalVolume") or item.get("dealVolume") or item.get("volume") or 0),
                    adj_close=_d(item.get("adjClose")),
                )
                session.add(record)
                total += 1

            chunk_end = chunk_start

        await session.flush()
        log_entry.status = IngestionStatus.completed
        log_entry.rows_inserted = total
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.info("Ingested %d OHLC rows for %s", total, symbol)
        return total

    except Exception as e:
        log_entry.status = IngestionStatus.failed
        log_entry.error_message = str(e)
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.error("OHLC ingestion failed for %s: %s", symbol, e)
        raise


async def ingest_realtime_close(
    session: AsyncSession,
    dnse_client,
    fireant_client: FireAntClient,
    symbol: str,
) -> int:
    try:
        dnse_close = await dnse_client.close_price(symbol=symbol)
        close_price = dnse_close.get("close") or dnse_close.get("price")
        if not close_price:
            return 0

        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        exists = await session.execute(
            select(OHLCPrice).where(
                OHLCPrice.time == today,
                OHLCPrice.symbol == symbol,
            )
        )
        existing = exists.scalar_one_or_none()
        if existing:
            existing.close = _d(close_price)
            existing.updated_at = datetime.utcnow()
            await session.flush()
            return 1
        return 0
    except Exception as e:
        logger.warning("Realtime close failed for %s: %s", symbol, e)
        return 0


def _d(val: Any) -> Decimal | None:
    if val is None:
        return None
    try:
        return Decimal(str(val))
    except (ValueError, TypeError):
        return None
