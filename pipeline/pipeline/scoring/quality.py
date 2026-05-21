import logging
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def compute_quality_score(
    session: AsyncSession,
    symbol: str,
) -> dict[str, Any]:
    result = await session.execute(
        text("""
            SELECT net_income, total_equity, debt, free_cash_flow, issued_shares
            FROM financial_reports
            WHERE symbol = :symbol
            ORDER BY year DESC, period DESC
            LIMIT 1
        """),
        {"symbol": symbol},
    )
    row = result.fetchone()

    roe_score_val = Decimal("0")
    de_score_val = Decimal("0")
    fcf_score_val = Decimal("0")
    roe_val = None
    de_val = None
    fcf_yield_val = None

    if row:
        net_income, total_equity, debt, fcf, shares = row

        if total_equity and net_income and Decimal(str(total_equity)) != 0:
            roe = Decimal(str(net_income)) / Decimal(str(total_equity))
            roe_val = roe
            if roe > Decimal("0.15"):
                roe_score_val = Decimal("10")
            elif roe > Decimal("0.12"):
                roe_score_val = Decimal("7")
            elif roe > Decimal("0.10"):
                roe_score_val = Decimal("5")

        if total_equity and debt and Decimal(str(total_equity)) != 0:
            de_ratio = Decimal(str(debt)) / Decimal(str(total_equity))
            de_val = de_ratio
            if de_ratio < Decimal("0.5"):
                de_score_val = Decimal("10")
            elif de_ratio < Decimal("1.0"):
                de_score_val = Decimal("7")
            elif de_ratio < Decimal("1.5"):
                de_score_val = Decimal("5")

        if fcf and shares:
            price_result = await session.execute(
                text("""
                    SELECT close FROM ohlc_prices
                    WHERE symbol = :symbol
                    ORDER BY time DESC LIMIT 1
                """),
                {"symbol": symbol},
            )
            price_row = price_result.fetchone()
            if price_row and price_row[0]:
                current_price = Decimal(str(price_row[0]))
                shares_dec = Decimal(str(shares))
                market_cap = current_price * shares_dec
                if market_cap > 0:
                    fcf_dec = Decimal(str(fcf))
                    fcf_yield = fcf_dec / market_cap
                    fcf_yield_val = fcf_yield
                    if fcf_yield > Decimal("0.04"):
                        fcf_score_val = Decimal("10")
                    elif fcf_yield > Decimal("0.02"):
                        fcf_score_val = Decimal("7")
                    elif fcf_yield > Decimal("0"):
                        fcf_score_val = Decimal("5")

    if roe_val is None:
        ind_result = await session.execute(
            text("""
                SELECT roe FROM financial_indicators
                WHERE symbol = :symbol AND roe IS NOT NULL
                ORDER BY date DESC LIMIT 1
            """),
            {"symbol": symbol},
        )
        ind_row = ind_result.fetchone()
        if ind_row and ind_row[0]:
            roe_dec = Decimal(str(ind_row[0])) / Decimal("100")
            roe_val = roe_dec
            if roe_dec > Decimal("0.15"):
                roe_score_val = Decimal("10")
            elif roe_dec > Decimal("0.12"):
                roe_score_val = Decimal("7")
            elif roe_dec > Decimal("0.10"):
                roe_score_val = Decimal("5")

    if de_val is None:
        ind_result = await session.execute(
            text("""
                SELECT de_ratio FROM financial_indicators
                WHERE symbol = :symbol AND de_ratio IS NOT NULL
                ORDER BY date DESC LIMIT 1
            """),
            {"symbol": symbol},
        )
        ind_row = ind_result.fetchone()
        if ind_row and ind_row[0]:
            de_dec = Decimal(str(ind_row[0]))
            de_val = de_dec
            if de_dec < Decimal("0.5"):
                de_score_val = Decimal("10")
            elif de_dec < Decimal("1.0"):
                de_score_val = Decimal("7")
            elif de_dec < Decimal("1.5"):
                de_score_val = Decimal("5")

    total_score = (
        roe_score_val * Decimal("0.40")
        + de_score_val * Decimal("0.30")
        + fcf_score_val * Decimal("0.30")
    )

    return {
        "score": total_score,
        "roe": roe_val,
        "de": de_val,
        "fcf_yield": fcf_yield_val,
    }
