import asyncio
import logging

from pipeline.clients.fireant import FireAntClient
from pipeline.db.connection import async_session_factory
from pipeline.ai.report_generator import generate_ai_report
from pipeline.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("report")


async def main():
    async with FireAntClient() as fireant:
        async with async_session_factory() as session:
            report = await generate_ai_report(session, fireant)
            print("\n" + report + "\n")


if __name__ == "__main__":
    asyncio.run(main())
