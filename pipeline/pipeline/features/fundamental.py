import logging
from datetime import date
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.db.models import FinancialIndicator

logger = logging.getLogger(__name__)


async def calculate_fundamental_metrics(
    session: AsyncSession,
    symbol: str,
) -> int:
    result = await session.execute(
        text("""
            SELECT
                revenue,
                net_income,
                total_assets,
                total_liabilities,
                total_equity,
                debt,
                free_cash_flow,
                issued_shares
            FROM financial_reports
            WHERE symbol = :symbol
            ORDER BY year DESC, period DESC
            LIMIT 1
        """),
        {"symbol": symbol},
    )
    row = result.fetchone()
    if not row:
        return 0

    revenue, net_income, total_assets, total_liabilities, total_equity, debt, fcf, shares = row

    for v in [revenue, net_income, total_assets, total_liabilities, total_equity]:
        if v is not None and not isinstance(v, Decimal):
            return 0

    price_result = await session.execute(
        text("""
            SELECT close FROM ohlc_prices
            WHERE symbol = :symbol
            ORDER BY time DESC
            LIMIT 1
        """),
        {"symbol": symbol},
    )
    price_row = price_result.fetchone()
    current_price = Decimal(str(price_row[0])) if price_row else None
    if not current_price or not shares or shares == 0:
        return 0

    shares_dec = Decimal(str(shares))
    market_cap = current_price * shares_dec

    roe = (Decimal(str(net_income)) / Decimal(str(total_equity))) if total_equity and Decimal(str(total_equity)) != 0 else None
    roa = (Decimal(str(net_income)) / Decimal(str(total_assets))) if total_assets and Decimal(str(total_assets)) != 0 else None
    de_ratio = (Decimal(str(debt)) / Decimal(str(total_equity))) if debt and total_equity and Decimal(str(total_equity)) != 0 else None
    pe = market_cap / Decimal(str(net_income)) if net_income and Decimal(str(net_income)) != 0 else None
    pb = market_cap / Decimal(str(total_equity)) if total_equity and Decimal(str(total_equity)) != 0 else None

    existing = await session.execute(
        text("""
            SELECT 1 FROM financial_indicators
            WHERE symbol = :symbol AND date = :today
        """),
        {"symbol": symbol, "today": date.today()},
    )
    if existing.fetchone():
        await session.execute(
            text("""
                UPDATE financial_indicators
                SET pe = :pe, pb = :pb, roe = :roe, roa = :roa,
                    de_ratio = :de, market_cap = :mcap
                WHERE symbol = :symbol AND date = :today
            """),
            {
                "symbol": symbol, "today": date.today(),
                "pe": pe, "pb": pb, "roe": roe, "roa": roa,
                "de": de_ratio, "mcap": market_cap,
            },
        )
    else:
        record = FinancialIndicator(
            symbol=symbol,
            date=date.today(),
            pe=pe,
            pb=pb,
            roe=roe,
            roa=roa,
            de_ratio=de_ratio,
            market_cap=market_cap,
        )
        session.add(record)

    await session.flush()
    logger.info("Calculated fundamental metrics for %s", symbol)
    return 1
