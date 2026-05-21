import logging
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.clients.dnse import DNSEClient
from pipeline.config import settings

logger = logging.getLogger(__name__)

ORDER_STATUS_MAP = {
    "pending": "PENDING",
    "filled": "FILLED",
    "partial_filled": "PARTIAL_FILLED",
    "cancelled": "CANCELLED",
    "rejected": "REJECTED",
}


def build_order_payload(
    symbol: str,
    side: str,
    quantity: int,
    price: float | None = None,
    order_type: str = "LO",
) -> dict:
    payload = {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "orderType": order_type,
        "marketType": "STOCK",
    }
    if order_type in ("LO", "MP"):
        pass
    elif price and order_type == "LO":
        payload["price"] = price
    return payload


async def place_orders(
    dnse: DNSEClient,
    trading_token: str,
    trades: list[dict],
) -> list[dict]:
    results = []
    for trade in trades:
        try:
            payload = build_order_payload(
                symbol=trade["symbol"],
                side=trade["side"],
                quantity=trade["quantity"],
                price=trade.get("price"),
                order_type=trade.get("order_type", "LO"),
            )
            result = await dnse.post_order("STOCK", trading_token, payload)
            results.append({
                "symbol": trade["symbol"],
                "side": trade["side"],
                "quantity": trade["quantity"],
                "status": "submitted",
                "response": result,
            })
            logger.info("Order submitted: %s %s %d shares", trade["side"], trade["symbol"], trade["quantity"])
        except Exception as e:
            logger.error("Order failed for %s: %s", trade["symbol"], e)
            results.append({
                "symbol": trade["symbol"],
                "side": trade["side"],
                "quantity": trade["quantity"],
                "status": "failed",
                "error": str(e),
            })
    return results


async def reconcile_orders(
    session: AsyncSession,
    dnse: DNSEClient,
    account_no: str,
    submitted_orders: list[dict],
) -> list[dict]:
    current_orders = await dnse.get_orders(account_no)
    current_map = {}
    for co in current_orders:
        sym = co.get("symbol", "")
        current_map[sym] = co

    reconciliation = []
    for so in submitted_orders:
        symbol = so["symbol"]
        remote = current_map.get(symbol, {})
        reconciliation.append({
            "symbol": symbol,
            "side": so["side"],
            "submitted_quantity": so["quantity"],
            "submitted_status": so["status"],
            "remote_status": remote.get("orderStatus", "unknown"),
            "filled_quantity": remote.get("filledQuantity", 0),
            "matched": so["status"] == "submitted" and remote.get("orderStatus") in ("FILLED", "PARTIAL_FILLED"),
        })
    return reconciliation


async def get_portfolio_value(dnse: DNSEClient, account_no: str) -> Decimal:
    balances = await dnse.get_balances(account_no)
    data = balances.get("data", balances)
    total = Decimal("0")
    for b in data if isinstance(data, list) else [data]:
        val = b.get("totalValue", 0) or b.get("totalAmount", 0) or 0
        total += Decimal(str(val))
    return total