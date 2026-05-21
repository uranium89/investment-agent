import asyncio
import logging
from datetime import datetime

from pipeline.clients.dnse import DNSEClient
from pipeline.db.connection import async_session_factory
from pipeline.execution.otp import send_otp, create_trading_token
from pipeline.execution.approval import create_approval_request, wait_for_approval
from pipeline.execution.orders import place_orders, reconcile_orders, get_portfolio_value
from pipeline.monitoring.telegram import alert_trade, alert_order_execution, alert_risk
from pipeline.risk.drawdown import check_max_drawdown
from pipeline.risk.black_swan import check_black_swan
from pipeline.risk.sector import check_sector_exposure
from pipeline.tasks.celery_app import celery_app
from pipeline.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def daily_execution_pipeline(self):
    logger.info("=== Daily Execution Pipeline started ===")
    asyncio.run(_run_execution())
    logger.info("=== Daily Execution Pipeline completed ===")


async def _run_execution():
    async with DNSEClient() as dnse:
        async with async_session_factory() as session:
            dd = await check_max_drawdown(session)
            if dd.get("breached"):
                logger.warning("Drawdown limit breached. Skipping trading.")
                await alert_risk("drawdown", dd)
                return

            bs = await check_black_swan(session)
            if bs.get("triggered"):
                logger.warning("Black swan detected. Skipping trading.")
                await alert_risk("black_swan", bs)
                return

            se = await check_sector_exposure(session)
            if se.get("breach_count", 0) > 0:
                logger.warning("Sector limits breached: %s", se["breaches"])
                await alert_risk("sector_breach", se)

            account_no = settings.dnse_account_no
            if not account_no:
                logger.warning("DNSE account not configured, skipping execution")
                return

            # Rebuild target portfolio from latest scores
            from pipeline.scoring.engine import run_scoring
            from pipeline.portfolio.constructor import construct_portfolio
            from pipeline.clients.fireant import FireAntClient

            async with FireAntClient() as fireant:
                scored = await run_scoring(session, fireant)
                await session.commit()

                portfolio = await construct_portfolio(session, scored)
                await session.commit()

            if not portfolio["positions"]:
                await alert_trade(portfolio)
                logger.info("No ENTER signals. 100% cash. Skipping execution.")
                return

            await alert_trade(portfolio)
            logger.info("Target portfolio: %d positions", len(portfolio["total_positions"]))

            # Build proposed trades
            proposed = []
            for p in portfolio["positions"]:
                proposed.append({
                    "symbol": p["symbol"],
                    "side": "BUY",
                    "quantity": 0,
                    "weight_pct": p["weight_pct"],
                    "score": p["score"],
                    "notes": f"ENTER signal",
                })

            run_id = create_approval_request(proposed)
            approval = wait_for_approval(run_id)

            if not approval["approved"]:
                logger.warning("Trading rejected: %s", approval.get("reason", "No reason"))
                return

            logger.info("Trading approved. Proceeding with OTP flow...")

            otp_result = await send_otp(dnse)
            logger.info("OTP sent to %s", settings.dnse_email)

            passcode = input("Enter OTP code from email: ").strip()
            token_result = await create_trading_token(dnse, passcode)
            trading_token = None
            if isinstance(token_result, dict):
                data = token_result.get("data", token_result)
                trading_token = data.get("tradingToken") or data.get("token") or data.get("accessToken")

            if not trading_token:
                logger.error("Failed to get trading token")
                return

            portfolio_value = await get_portfolio_value(dnse, account_no)
            logger.info("Portfolio value: %.2f", portfolio_value)

            orders = []
            for p in proposed:
                price_result = await session.execute(
                    "SELECT close FROM ohlc_prices WHERE symbol = :s ORDER BY time DESC LIMIT 1",
                    {"s": p["symbol"]},
                )
                price_row = price_result.fetchone()
                price = float(price_row[0]) if price_row else 0

                target_val = float(portfolio_value) * p["weight_pct"] / 100.0
                quantity = int(target_val / price / 100) * 100 if price > 0 else 0
                if quantity >= 100:
                    orders.append({
                        "symbol": p["symbol"],
                        "side": "BUY",
                        "quantity": quantity,
                        "price": round(price * 1.01, 2),
                        "order_type": "LO",
                    })

            order_results = await place_orders(dnse, trading_token, orders)
            await alert_order_execution(order_results)

            reconciliation = await reconcile_orders(session, dnse, account_no, order_results)
            logger.info("Reconciliation: %d orders matched", sum(1 for r in reconciliation if r.get("matched")))


def run():
    logging.basicConfig(level=getattr(logging, settings.log_level))
    daily_execution_pipeline.delay()


if __name__ == "__main__":
    run()