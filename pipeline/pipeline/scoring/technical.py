import logging
from decimal import Decimal
from typing import Any

import pandas as pd
import numpy as np
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def compute_technical_score(
    session: AsyncSession,
    symbol: str,
) -> dict[str, Any]:
    ti_result = await session.execute(
        text("""
            SELECT time, ma_20, ma_50, ma_200, rsi_14,
                   macd, macd_signal, macd_histogram,
                   volume_sma_20
            FROM technical_indicators
            WHERE symbol = :symbol
            ORDER BY time DESC
            LIMIT 1
        """),
        {"symbol": symbol},
    )
    ti_row = ti_result.fetchone()
    if not ti_row:
        return {"trend_score": 0, "momentum_score": 0, "total": Decimal("0")}

    _, ma_20, ma_50, ma_200, rsi_14, macd, macd_signal, macd_hist, vol_sma_20 = ti_row

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
    if not price_row:
        return {"trend_score": 0, "momentum_score": 0, "total": Decimal("0")}

    current_price = Decimal(str(price_row[0]))

    trend_score = 0
    if current_price and ma_50 and Decimal(str(ma_50)) > 0:
        if current_price > Decimal(str(ma_50)):
            trend_score += 3
    if current_price and ma_200 and Decimal(str(ma_200)) > 0:
        if current_price > Decimal(str(ma_200)):
            trend_score += 3
    if ma_50 and ma_200 and Decimal(str(ma_50)) > 0 and Decimal(str(ma_200)) > 0:
        if Decimal(str(ma_50)) > Decimal(str(ma_200)):
            trend_score += 3

    adx_val = await _compute_adx(session, symbol)
    if adx_val is not None and adx_val > Decimal("20"):
        trend_score += 3

    if current_price and vol_sma_20 and Decimal(str(vol_sma_20)) > 0:
        latest_vol_result = await session.execute(
            text("""
                SELECT volume FROM ohlc_prices
                WHERE symbol = :symbol
                ORDER BY time DESC
                LIMIT 1
            """),
            {"symbol": symbol},
        )
        latest_vol_row = latest_vol_result.fetchone()
        if latest_vol_row and latest_vol_row[0]:
            latest_vol = Decimal(str(latest_vol_row[0]))
            if latest_vol > Decimal(str(vol_sma_20)):
                trend_score += 3

    momentum_score = 0
    if rsi_14 is not None:
        rsi_val = Decimal(str(rsi_14))
        if Decimal("30") <= rsi_val <= Decimal("40"):
            momentum_score += 5
        elif Decimal("40") < rsi_val <= Decimal("60"):
            momentum_score += 3
        elif rsi_val > Decimal("70"):
            momentum_score -= 3

    if macd_hist is not None:
        if Decimal(str(macd_hist)) > 0:
            momentum_score += 3

    if macd is not None and macd_signal is not None:
        if Decimal(str(macd)) > Decimal(str(macd_signal)):
            momentum_score += 2

    trend_weight = Decimal(str(trend_score)) * Decimal("0.15")
    momentum_weight = Decimal(str(momentum_score)) * Decimal("0.10")
    total = trend_weight + momentum_weight

    return {
        "trend_score": trend_score,
        "momentum_score": momentum_score,
        "total": total,
    }


async def _compute_adx(session: AsyncSession, symbol: str, period: int = 14) -> Decimal | None:
    result = await session.execute(
        text("""
            SELECT time, high, low, close
            FROM ohlc_prices
            WHERE symbol = :symbol
            ORDER BY time ASC
        """),
        {"symbol": symbol},
    )
    rows = result.fetchall()
    if len(rows) < period + 1:
        return None

    df = pd.DataFrame(rows, columns=["time", "high", "low", "close"])
    for col in ["high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    high = df["high"].values
    low = df["low"].values
    close = df["close"].values

    up_move = np.diff(high)
    down_move = np.diff(low) * -1
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    tr = np.maximum(high[1:] - low[1:],
                    np.maximum(np.abs(high[1:] - close[:-1]),
                               np.abs(low[1:] - close[:-1])))

    atr_val = pd.Series(tr).rolling(window=period).mean().values
    plus_di = 100 * pd.Series(plus_dm).rolling(window=period).mean().values / atr_val
    minus_di = 100 * pd.Series(minus_dm).rolling(window=period).mean().values / atr_val

    dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)
    adx_arr = pd.Series(dx).rolling(window=period).mean().values

    if len(adx_arr) == 0 or np.isnan(adx_arr[-1]):
        return None
    return Decimal(str(round(adx_arr[-1], 2)))
