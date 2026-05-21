"""add scoring + portfolio tables

Revision ID: 002
Revises: 001
Create Date: 2026-05-21
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, None] = None
depends_on: Union[str, None] = None


def upgrade():
    op.create_table(
        "score_snapshots",
        sa.Column("time", sa.DateTime(), primary_key=True),
        sa.Column("symbol", sa.String(10), primary_key=True),
        sa.Column("quality_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("value_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("technical_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("moat_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("management_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("macro_overlay", sa.Numeric(5, 2), nullable=True),
        sa.Column("total_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("passed_screening", sa.Boolean(), default=False),
        sa.Column("screening_detail", sa.Text(), nullable=True),
        sa.Column("signal", sa.String(10), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "portfolio_state",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("symbol", sa.String(10), nullable=False, index=True),
        sa.Column("entry_date", sa.DateTime(), nullable=False),
        sa.Column("entry_price", sa.Numeric(15, 2), nullable=False),
        sa.Column("current_price", sa.Numeric(15, 2), nullable=True),
        sa.Column("shares", sa.BigInteger(), nullable=False),
        sa.Column("cost_basis", sa.Numeric(20, 2), nullable=False),
        sa.Column("current_value", sa.Numeric(20, 2), nullable=True),
        sa.Column("weight_pct", sa.Numeric(5, 2), nullable=True),
        sa.Column("sector", sa.String(50), nullable=True),
        sa.Column("pnl_pct", sa.Numeric(10, 4), nullable=True),
        sa.Column("signal", sa.String(10), nullable=True),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("closed_date", sa.DateTime(), nullable=True),
        sa.Column("closed_reason", sa.String(100), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "screening_results",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("symbol", sa.String(10), nullable=False, index=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("passed", sa.Boolean(), default=False),
        sa.Column("de_check", sa.Boolean(), nullable=True),
        sa.Column("roe_check", sa.Boolean(), nullable=True),
        sa.Column("market_cap_check", sa.Boolean(), nullable=True),
        sa.Column("adtv_check", sa.Boolean(), nullable=True),
        sa.Column("fcf_check", sa.Boolean(), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("screening_results")
    op.drop_table("portfolio_state")
    op.drop_table("score_snapshots")
