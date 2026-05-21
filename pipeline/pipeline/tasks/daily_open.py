import asyncio
import logging

from pipeline.clients.fireant import FireAntClient
from pipeline.db.connection import async_session_factory
from pipeline.ingestors.company import ingest_company_info
from pipeline.tasks.celery_app import celery_app
from pipeline.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def daily_open_pipeline(self):
    """Chạy trước giờ mở cửa: cập nhật thông tin công ty, tin tức."""
    logger.info("=== Daily Open Pipeline started ===")
    asyncio.run(_run_open_pipeline())
    logger.info("=== Daily Open Pipeline completed ===")


async def _run_open_pipeline():
    async with FireAntClient() as fireant:
        async with async_session_factory() as session:
            for symbol in settings.vn30_symbols:
                try:
                    await ingest_company_info(session, fireant, symbol)
                    await session.commit()
                except Exception as e:
                    logger.error("Error updating company info for %s: %s", symbol, e)
                    await session.rollback()
                    continue
