import asyncio
import logging

from pipeline.db.connection import async_session_factory
from pipeline.ingestors.tcbs_financial_reports import ingest_tcbs_financial_reports, download_pdf
from pipeline.tasks.celery_app import celery_app
from pipeline.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def daily_tcbs_pipeline(self):
    """Chạy sau daily-close: tải TCBS PDF balance sheet cho tất cả VN30 symbols."""
    logger.info("=== Daily TCBS Pipeline started ===")
    asyncio.run(_run_tcbs_pipeline())
    logger.info("=== Daily TCBS Pipeline completed ===")


async def _run_tcbs_pipeline():
    async with async_session_factory() as session:
        for symbol in settings.vn30_symbols:
            try:
                pdf_bytes = await download_pdf(symbol)
                await ingest_tcbs_financial_reports(session, symbol, pdf_bytes=pdf_bytes)
                await session.commit()
            except Exception as e:
                logger.error("Error ingesting TCBS reports for %s: %s", symbol, e)
                await session.rollback()
                continue


def run():
    logging.basicConfig(level=getattr(logging, settings.log_level))
    daily_tcbs_pipeline.delay()


if __name__ == "__main__":
    run()
