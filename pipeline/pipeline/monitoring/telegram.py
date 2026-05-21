import logging
from typing import Any

import httpx

from pipeline.config import settings

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


async def send_telegram(message: str, parse_mode: str = "HTML") -> bool:
    token = settings.telegram_bot_token
    chat_id = settings.telegram_chat_id
    if not token or not chat_id:
        logger.warning("Telegram not configured (bot_token=%s, chat_id=%s)", bool(token), bool(chat_id))
        return False

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                TELEGRAM_API.format(token=token),
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": parse_mode,
                    "disable_web_page_preview": True,
                },
            )
            resp.raise_for_status()
            logger.info("Telegram message sent")
            return True
    except Exception as e:
        logger.error("Telegram send failed: %s", e)
        return False


async def alert_trade(portfolio_result: dict[str, Any]) -> bool:
    positions = portfolio_result.get("positions", [])
    if not positions:
        msg = (
            "<b>🏦 Portfolio Update</b>\n"
            "No positions today. 100% cash."
        )
    else:
        lines = [f"<b>🏦 Portfolio — {len(positions)} positions</b>"]
        for p in positions:
            emoji = "🟢" if p.get("signal") == "ENTER" else "🟡"
            lines.append(f"{emoji} {p['symbol']}: score={p['score']:.2f} weight={p['weight_pct']:.1f}%")
        lines.append(f"\n💵 Cash: {portfolio_result.get('cash_pct', 0):.1f}%")
        msg = "\n".join(lines)
    return await send_telegram(msg)


async def alert_risk(risk_type: str, details: dict) -> bool:
    emoji_map = {
        "drawdown": "📉",
        "black_swan": "🚨",
        "sector_breach": "⚠️",
    }
    emoji = emoji_map.get(risk_type, "🔔")
    msg = f"<b>{emoji} Risk Alert: {risk_type.upper()}</b>\n"
    for k, v in details.items():
        msg += f"  {k}: {v}\n"
    return await send_telegram(msg)


async def alert_order_execution(order_results: list[dict]) -> bool:
    success = [o for o in order_results if o.get("status") == "submitted"]
    failed = [o for o in order_results if o.get("status") == "failed"]
    lines = ["<b>📊 Order Execution Results</b>"]
    if success:
        lines.append(f"\n✅ <b>Success ({len(success)}):</b>")
        for s in success:
            lines.append(f"  {s['side']} {s['symbol']} x{s['quantity']}")
    if failed:
        lines.append(f"\n❌ <b>Failed ({len(failed)}):</b>")
        for f in failed:
            lines.append(f"  {f['symbol']}: {f.get('error', 'unknown')}")
    return await send_telegram("\n".join(lines))


async def alert_daily_report(report: str) -> bool:
    msg = f"<b>📋 Daily Report</b>\n<pre>{report[:3800]}</pre>"
    return await send_telegram(msg)