import logging
from datetime import datetime, date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.clients.fireant import FireAntClient
from pipeline.db.models import VN30Symbol, IngestionLog, IngestionStatus

logger = logging.getLogger(__name__)


async def ingest_company_info(
    session: AsyncSession,
    client: FireAntClient,
    symbol: str,
) -> int:
    log_entry = IngestionLog(
        task_name="company_info",
        symbol=symbol,
        status=IngestionStatus.running,
        started_at=datetime.utcnow(),
    )
    session.add(log_entry)
    await session.flush()

    try:
        info = await client.symbol_info(symbol=symbol)
        if not info or not isinstance(info, dict):
            log_entry.status = IngestionStatus.skipped
            log_entry.completed_at = datetime.utcnow()
            await session.flush()
            return 0

        company_name = (
            info.get("companyName")
            or info.get("name")
            or info.get("shortName")
            or ""
        )

        existing = await session.execute(
            select(VN30Symbol).where(VN30Symbol.symbol == symbol)
        )
        row = existing.scalar_one_or_none()
        if row:
            row.company_name = company_name
            row.icb_code = str(info.get("icbCode") or info.get("industryCode") or "")
            row.icb_name = info.get("icbName") or info.get("industryName") or ""
            row.market_cap = None
            row.updated_at = datetime.utcnow()
        else:
            row = VN30Symbol(
                symbol=symbol,
                company_name=company_name,
                icb_code=str(info.get("icbCode") or info.get("industryCode") or ""),
                icb_name=info.get("icbName") or info.get("industryName") or "",
                status="active",
            )
            session.add(row)

        await session.flush()
        log_entry.status = IngestionStatus.completed
        log_entry.rows_inserted = 1
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.info("Updated company info for %s: %s", symbol, company_name)
        return 1

    except Exception as e:
        log_entry.status = IngestionStatus.failed
        log_entry.error_message = str(e)
        log_entry.completed_at = datetime.utcnow()
        await session.flush()
        logger.error("Company info failed for %s: %s", symbol, e)
        raise
