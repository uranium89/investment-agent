import logging
from datetime import datetime
from decimal import Decimal
from typing import Any

import pandas as pd
import numpy as np
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.db.models import TechnicalIndicator

logger = logging.getLogger(__name__)


async def calculate_technical_indicators(
    session: AsyncSession,
    symbol: str,
) -> int:
    rows = await session.execute(
        text("""
            SELECT time, close, high, low, volume
            FROM ohlc_prices
            WHERE symbol = :symbol
            ORDER BY time ASC
        """),
        {"symbol": symbol},
    )
    records = rows.fetchall()
    if len(records) < 200:
        logger.warning("Not enough data for %s (%d rows)", symbol, len(records))
        return 0

    df = pd.DataFrame(records, columns=["time", "close", "high", "low", "volume"])
    df = df.sort_values("time").reset_index(drop=True)

    for col in ["close", "high", "low", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["ma_20"] = df["close"].rolling(window=20).mean()
    df["ma_50"] = df["close"].rolling(window=50).mean()
    df["ma_200"] = df["close"].rolling(window=200).mean()
    df["volume_sma_20"] = df["volume"].rolling(window=20).mean()

    df["rsi_14"] = _rsi(df["close"], 14)

    macd_data = _macd(df["close"])
    df["macd"] = macd_data["macd"]
    df["macd_signal"] = macd_data["signal"]
    df["macd_histogram"] = macd_data["histogram"]

    bollinger = _bollinger_bands(df["close"], 20, 2)
    df["bollinger_upper"] = bollinger["upper"]
    df["bollinger_middle"] = bollinger["middle"]
    df["bollinger_lower"] = bollinger["lower"]

    df["atr_14"] = _atr(df["high"], df["low"], df["close"], 14)

    df = df.iloc[200:].reset_index(drop=True)

    inserted = 0
    for _, row in df.iterrows():
        ts = row["time"]
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                ts = datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")

        existing = await session.execute(
            text("""
                SELECT 1 FROM technical_indicators
                WHERE time = :time AND symbol = :symbol
            """),
            {"time": ts, "symbol": symbol},
        )
        if existing.fetchone():
            continue

        record = TechnicalIndicator(
            time=ts,
            symbol=symbol,
            ma_20=_d(row.get("ma_20")),
            ma_50=_d(row.get("ma_50")),
            ma_200=_d(row.get("ma_200")),
            rsi_14=_d(row.get("rsi_14")),
            macd=_d(row.get("macd")),
            macd_signal=_d(row.get("macd_signal")),
            macd_histogram=_d(row.get("macd_histogram")),
            bollinger_upper=_d(row.get("bollinger_upper")),
            bollinger_middle=_d(row.get("bollinger_middle")),
            bollinger_lower=_d(row.get("bollinger_lower")),
            atr_14=_d(row.get("atr_14")),
            volume_sma_20=_d(row.get("volume_sma_20")),
        )
        session.add(record)
        inserted += 1

    await session.flush()
    logger.info("Inserted %d technical indicator rows for %s", inserted, symbol)
    return inserted


def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = (-delta.clip(upper=0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def _macd(series: pd.Series) -> dict[str, pd.Series]:
    ema_12 = series.ewm(span=12, adjust=False).mean()
    ema_26 = series.ewm(span=26, adjust=False).mean()
    macd_line = ema_12 - ema_26
    signal = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal
    return {"macd": macd_line, "signal": signal, "histogram": histogram}


def _bollinger_bands(series: pd.Series, period: int = 20, num_std: int = 2) -> dict[str, pd.Series]:
    middle = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    upper = middle + num_std * std
    lower = middle - num_std * std
    return {"upper": upper, "middle": middle, "lower": lower}


def _atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def _d(val: Any) -> Decimal | None:
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None
    try:
        return Decimal(str(val))
    except (ValueError, TypeError):
        return None
