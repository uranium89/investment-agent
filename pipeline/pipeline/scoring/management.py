import logging
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.clients.fireant import FireAntClient

logger = logging.getLogger(__name__)


async def compute_management_score(
    session: AsyncSession,
    fireant: FireAntClient,
    symbol: str,
) -> dict:
    score = Decimal("5")
    details = []

    try:
        transactions = await fireant.transactions(symbol)
        if isinstance(transactions, list):
            suspicious = 0
            insider_buying = 0
            for tx in transactions:
                if not isinstance(tx, dict):
                    continue
                tx_type = str(tx.get("type", "")).lower()
                tx_vol = tx.get("volume") or tx.get("dealVolume") or 0
                if "buy" in tx_type or "mua" in tx_type:
                    insider_buying += int(tx_vol) if tx_vol else 0
                elif "sell" in tx_type or "ban" in tx_type:
                    suspicious += int(tx_vol) if tx_vol else 0

            if insider_buying > suspicious * 2:
                score += Decimal("3")
                details.append("insider_buying")
            elif suspicious > insider_buying * 2:
                score -= Decimal("3")
                details.append("insider_selling")
    except Exception as e:
        logger.warning("Management score transactions failed for %s: %s", symbol, e)

    try:
        officers = await fireant.officers(symbol)
        if isinstance(officers, list):
            has_ceo = any(
                isinstance(o, dict)
                and ("ceo" in str(o.get("position", "")).lower()
                     or "general director" in str(o.get("position", "")).lower())
                for o in officers
            )
            if has_ceo:
                score += Decimal("1")
                details.append("ceo_identified")
    except Exception as e:
        logger.warning("Management score officers failed for %s: %s", symbol, e)

    return {"score": min(max(score, Decimal("0")), Decimal("10")), "details": details}
