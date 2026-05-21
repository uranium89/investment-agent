import asyncio
import logging

from pipeline.db.connection import async_session_factory
from pipeline.monitoring.report import generate_daily_report
from pipeline.monitoring.telegram import alert_daily_report
from pipeline.risk.drawdown import check_max_drawdown
from pipeline.risk.black_swan import check_black_swan
from pipeline.risk.sector import check_sector_exposure
from pipeline.tasks.celery_app import celery_app
from pipeline.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def daily_monitoring_pipeline(self):
    logger.info("=== Daily Monitoring Pipeline started ===")
    asyncio.run(_run_monitoring())
    logger.info("=== Daily Monitoring Pipeline completed ===")


async def _run_monitoring():
    async with async_session_factory() as session:
        report = await generate_daily_report(session)
        logger.info("Daily report:\n%s", report)
        await alert_daily_report(report)

        dd = await check_max_drawdown(session)
        logger.info("Drawdown check: %s", dd["message"])

        bs = await check_black_swan(session)
        logger.info("Black swan check: %s", bs["message"])

        se = await check_sector_exposure(session)
        logger.info("Sector exposure check: %s breaches", se["breach_count"])


def run():
    logging.basicConfig(level=getattr(logging, settings.log_level))
    daily_monitoring_pipeline.delay()


if __name__ == "__main__":
    run()