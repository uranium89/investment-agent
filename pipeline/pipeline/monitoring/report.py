import logging
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def generate_daily_report(session: AsyncSession) -> str:
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
            SELECT symbol, weight_pct, current_value, pnl_pct, sector, status
            FROM portfolio_state
            WHERE status = 'active'
            ORDER BY weight_pct DESC
        """),
    )
    positions = portfolio_result.fetchall()

    lines = []
    lines.append(f"Report Date: {today}")
    lines.append("")

    if scores:
        enter = [s for s in scores if s[5] == "ENTER"]
        hold = [s for s in scores if s[5] == "HOLD"]
        lines.append(f"Scores: {len(enter)} ENTER, {len(hold)} HOLD, {len(scores) - len(enter) - len(hold)} NONE")
        lines.append("")
        if enter:
            lines.append("ENTER:")
            for s in enter:
                lines.append(f"  {s[0]:6s}  total={float(s[1]):.2f}  Q={float(s[2]):.2f}  V={float(s[3]):.2f}  T={float(s[4]):.2f}")
        if hold:
            lines.append("HOLD:")
            for s in hold[:5]:
                lines.append(f"  {s[0]:6s}  total={float(s[1]):.2f}")
    else:
        lines.append("No scores for today.")

    lines.append("")
    if positions:
        lines.append(f"Portfolio ({len(positions)} positions):")
        total_value = Decimal("0")
        for p in positions:
            symbol, weight, value, pnl, sector, status = p
            val = Decimal(str(value)) if value else Decimal("0")
            total_value += val
            pnl_str = f"{float(pnl):+.2f}%" if pnl else "N/A"
            lines.append(f"  {symbol:6s}  weight={float(weight):.1f}%  value={float(val):,.0f}  P&L={pnl_str}")
        cash_pct_result = await session.execute(
            text("SELECT MIN(cash_pct) FROM portfolio_state WHERE status = 'cash'"),
        )
        lines.append(f"  {'CASH':6s}  weight={100 - sum(float(p[1] or 0) for p in positions):.1f}%")
    else:
        lines.append("Portfolio: 100% cash")

    return "\n".join(lines)