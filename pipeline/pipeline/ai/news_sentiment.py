import logging
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.clients.fireant import FireAntClient

logger = logging.getLogger(__name__)

POSITIVE_KEYWORDS = [
    "lợi nhuận", "tăng trưởng", "cổ tức", "mở rộng", "đầu tư",
    "hợp tác", "ký kết", "xuất khẩu", "doanh thu", "profit",
    "growth", "dividend", "expansion", "partnership", "contract",
]
NEGATIVE_KEYWORDS = [
    "thua lỗ", "giảm", "cắt lỗ", "rủi ro", "kiện tụng",
    "phá sản", "thoái vốn", "bán tháo", "điều chỉnh", "loss",
    "decline", "risk", "lawsuit", "bankruptcy", "selloff",
]


async def get_news_sentiment(fireant: FireAntClient, symbol: str) -> dict[str, Any]:
    try:
        posts = await fireant.symbol_posts(symbol)
    except Exception as e:
        logger.warning("Failed to get posts for %s: %s", symbol, e)
        posts = []

    news_items = []
    if isinstance(posts, dict):
        posts = posts.get("data", posts.get("items", [posts]))
    if isinstance(posts, list):
        for post in posts[:30]:
            if isinstance(post, dict):
                content = post.get("content") or post.get("text") or post.get("description", "")
            else:
                content = str(post)

            if not isinstance(content, str) or len(content) < 20:
                continue

            sent = _classify_sentiment(content)
            news_items.append({
                "content_preview": content[:200],
                "sentiment": sent,
                "score": 1 if sent == "positive" else (-1 if sent == "negative" else 0),
            })

    if not news_items:
        return {"symbol": symbol, "news_count": 0, "sentiment_score": 0, "label": "neutral"}

    avg_score = sum(n["score"] for n in news_items) / len(news_items)

    return {
        "symbol": symbol,
        "news_count": len(news_items),
        "positive_count": sum(1 for n in news_items if n["sentiment"] == "positive"),
        "negative_count": sum(1 for n in news_items if n["sentiment"] == "negative"),
        "sentiment_score": avg_score,
        "label": "positive" if avg_score > 0.2 else ("negative" if avg_score < -0.2 else "neutral"),
        "recent_headlines": [n["content_preview"] for n in news_items[:5]],
    }


def _classify_sentiment(text: str) -> str:
    text_lower = text.lower()
    pos_count = sum(1 for kw in POSITIVE_KEYWORDS if kw.lower() in text_lower)
    neg_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw.lower() in text_lower)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


async def get_market_summary(fireant: FireAntClient) -> dict[str, Any]:
    try:
        news = await fireant.news_feed()
    except Exception:
        news = []

    headlines = []
    if isinstance(news, dict):
        items = news.get("data", news.get("items", []))
    elif isinstance(news, list):
        items = news
    else:
        items = []

    for item in items[:10]:
        if isinstance(item, dict):
            title = item.get("title") or item.get("content", "")[:100]
            headlines.append(str(title)[:200])
    return {"headlines": headlines, "count": len(headlines)}
