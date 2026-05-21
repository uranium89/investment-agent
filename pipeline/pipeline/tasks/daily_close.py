import asyncio
import logging
from datetime import datetime

from pipeline.clients.fireant import FireAntClient
from pipeline.db.connection import async_session_factory
from pipeline.ingestors.prices import ingest_ohlc
from pipeline.ingestors.financials import ingest_fundamental, ingest_financial_indicators
from pipeline.features.technical import calculate_technical_indicators
from pipeline.features.fundamental import calculate_fundamental_metrics
from pipeline.tasks.celery_app import celery_app
from pipeline.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def daily_close_pipeline(self):
    """Chạy sau giờ đóng cửa: thu thập dữ liệu OHLC + tính indicators."""
    logger.info("=== Daily Close Pipeline started ===")
    asyncio.run(_run_close_pipeline())
    logger.info("=== Daily Close Pipeline completed ===")


async def _run_close_pipeline():
    async with FireAntClient() as fireant:
        async with async_session_factory() as session:
            for symbol in settings.vn30_symbols:
                try:
                    await ingest_ohlc(session, fireant, symbol, lookback_days=365)
                    await session.commit()
                except Exception as e:
                    logger.error("Error ingesting OHLC for %s: %s", symbol, e)
                    await session.rollback()
                    continue

            for symbol in settings.vn30_symbols:
                try:
                    await ingest_fundamental(session, fireant, symbol)
                    await session.commit()
                except Exception as e:
                    logger.error("Error ingesting fundamental for %s: %s", symbol, e)
                    await session.rollback()
                    continue

            for symbol in settings.vn30_symbols:
                try:
                    await ingest_financial_indicators(session, fireant, symbol)
                    await session.commit()
                except Exception as e:
                    logger.error("Error ingesting indicators for %s: %s", symbol, e)
                    await session.rollback()
                    continue

            for symbol in settings.vn30_symbols:
                try:
                    await calculate_technical_indicators(session, symbol)
                    await session.commit()
                except Exception as e:
                    logger.error("Error calculating technicals for %s: %s", symbol, e)
                    await session.rollback()
                    continue

            for symbol in settings.vn30_symbols:
                try:
                    await calculate_fundamental_metrics(session, symbol)
                    await session.commit()
                except Exception as e:
                    logger.error("Error calculating fundamentals for %s: %s", symbol, e)
                    await session.rollback()
                    continue


def run():
    """Entry point CLI for manual run."""
    logging.basicConfig(level=getattr(logging, settings.log_level))
    daily_close_pipeline.delay()


if __name__ == "__main__":
    run()
