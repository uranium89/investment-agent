import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from pipeline.config import settings
from pipeline.ai.news_sentiment import get_news_sentiment, get_market_summary
from pipeline.clients.fireant import FireAntClient

logger = logging.getLogger(__name__)


async def generate_ai_report(
    session: AsyncSession,
    fireant: FireAntClient | None = None,
) -> str:
    today = datetime.utcnow().date()

    score_result = await session.execute(
        text("""
            SELECT symbol, total_score, quality_score, value_score,
                   technical_score, signal, passed_screening
            FROM score_snapshots
            WHERE time::date = :today
            ORDER BY total_score DESC NULLS LAST
        """),
        {"today": today},
    )
    scores = score_result.fetchall()

    portfolio_result = await session.execute(
        text("""
            SELECT symbol, weight_pct, current_value, pnl_pct, sector
            FROM portfolio_state
            WHERE status = 'active'
            ORDER BY weight_pct DESC
        """),
    )
    positions = portfolio_result.fetchall()

    dd_result = await session.execute(
        text("""
            WITH pv AS (
                SELECT time::date as d, SUM(coalesce(current_value, 0)) as v
                FROM portfolio_state WHERE status = 'active'
                GROUP BY d ORDER BY d DESC LIMIT 60
            )
            SELECT MIN(v) as min_v, MAX(v) as max_v FROM pv
        """),
    )
    dd_row = dd_result.fetchone()

    lines = []
    lines.append("=" * 60)
    lines.append(f"  VN30 INVESTMENT REPORT — {today}")
    lines.append("=" * 60)
    lines.append("")

    if scores:
        enter = [s for s in scores if s[5] == "ENTER"]
        hold = [s for s in scores if s[5] == "HOLD"]
        lines.append(f"📊 SIGNALS: {len(enter)} ENTER, {len(hold)} HOLD, {len(scores) - len(enter) - len(hold)} NONE (out of {len(scores)})")
        lines.append("")

        if enter:
            lines.append("✅  ENTER (highest conviction):")
            for s in enter[:5]:
                lines.append(f"    {s[0]:6s}  total={float(s[1]):.2f}  Q={float(s[2]):.2f}  V={float(s[3]):.2f}  T={float(s[4]):.2f}")
            lines.append("")

        if hold:
            lines.append("🟡  HOLD (monitor):")
            for s in hold[:8]:
                lines.append(f"    {s[0]:6s}  total={float(s[1]):.2f}")
            lines.append("")
    else:
        lines.append("📊 No scores available for today.")
        lines.append("")

    lines.append("-" * 60)
    lines.append("")
    if positions:
        total_value = sum(float(p[2] or 0) for p in positions)
        lines.append(f"💼 PORTFOLIO ({len(positions)} positions, {total_value:>12,.0f} VND):")
        lines.append(f"    {'Symbol':6s}  {'Weight':8s}  {'Value':14s}  {'P&L':10s}  {'Sector':15s}")
        lines.append(f"    {'─'*6}  {'─'*8}  {'─'*14}  {'─'*10}  {'─'*15}")
        for p in positions:
            sym, weight, value, pnl, sector = p
            pnl_str = f"{float(pnl):+.2f}%" if pnl else "N/A"
            lines.append(f"    {sym:6s}  {float(weight):6.1f}%  {float(value or 0):>12,.0f}  {pnl_str:>8s}  {sector or 'N/A':15s}")
    else:
        lines.append("💼 PORTFOLIO: 100% cash")
    lines.append("")

    if dd_row and dd_row[1] and float(dd_row[1]) > 0:
        dd_pct = (float(dd_row[1]) - float(dd_row[0])) / float(dd_row[1]) * 100
        lines.append(f"📉 MAX DRAWDOWN (60d): {dd_pct:.1f}%")
        lines.append("")

    if fireant:
        try:
            summary = await get_market_summary(fireant)
            if summary["headlines"]:
                lines.append("📰 MARKET NEWS:")
                for h in summary["headlines"][:5]:
                    lines.append(f"    • {h}")
                lines.append("")
        except Exception:
            pass

    lines.append("=" * 60)
    lines.append("  DISCLAIMER: AI-generated report. Not financial advice.")
    lines.append("=" * 60)

    return "\n".join(lines)
