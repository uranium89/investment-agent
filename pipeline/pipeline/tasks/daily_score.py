import asyncio
import logging
from datetime import datetime

from pipeline.clients.fireant import FireAntClient
from pipeline.db.connection import async_session_factory
from pipeline.scoring.engine import run_scoring
from pipeline.portfolio.constructor import construct_portfolio
from pipeline.tasks.celery_app import celery_app
from pipeline.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def daily_scoring_pipeline(self):
    logger.info("=== Daily Scoring Pipeline started ===")
    asyncio.run(_run_scoring())
    logger.info("=== Daily Scoring Pipeline completed ===")


async def _run_scoring():
    async with FireAntClient() as fireant:
        async with async_session_factory() as session:
            scored = await run_scoring(session, fireant)
            await session.commit()

            passed = [ss for ss in scored if ss.passed_screening]
            logger.info("Symbols passed screening: %d/%d", len(passed), len(scored))

            portfolio = await construct_portfolio(session, scored)
            await session.commit()

            if portfolio["positions"]:
                logger.info("Target portfolio: %d positions, cash %.1f%%",
                            portfolio["total_positions"], portfolio["cash_pct"])
                for p in portfolio["positions"]:
                    logger.info("  %s: score=%.2f weight=%.1f%% sector=%s",
                                p["symbol"], p["score"], p["weight_pct"], p["sector"])
            else:
                logger.info("No target positions for today")


def run():
    logging.basicConfig(level=getattr(logging, settings.log_level))
    daily_scoring_pipeline.delay()


if __name__ == "__main__":
    run()
