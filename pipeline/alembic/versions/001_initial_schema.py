"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-21
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, None] = None
depends_on: Union[str, None] = None


def upgrade():
    op.create_table(
        "vn30_symbols",
        sa.Column("symbol", sa.String(10), primary_key=True),
        sa.Column("company_name", sa.String(255), nullable=False),
        sa.Column("icb_code", sa.String(20), nullable=True),
        sa.Column("icb_name", sa.String(255), nullable=True),
        sa.Column("market_cap", sa.Numeric(20, 2), nullable=True),
        sa.Column("listed_date", sa.Date(), nullable=True),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "ohlc_prices",
        sa.Column("time", sa.DateTime(), primary_key=True),
        sa.Column("symbol", sa.String(10), primary_key=True),
        sa.Column("open", sa.Numeric(15, 2), nullable=False),
        sa.Column("high", sa.Numeric(15, 2), nullable=False),
        sa.Column("low", sa.Numeric(15, 2), nullable=False),
        sa.Column("close", sa.Numeric(15, 2), nullable=False),
        sa.Column("volume", sa.BigInteger(), nullable=False),
        sa.Column("adj_close", sa.Numeric(15, 2), nullable=True),
    )
    op.create_index("idx_ohlc_prices_time", "ohlc_prices", ["time"])
    op.create_index("idx_ohlc_prices_symbol_time", "ohlc_prices", ["symbol", "time"])

    op.create_table(
        "financial_reports",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("symbol", sa.String(10), nullable=False, index=True),
        sa.Column("period", sa.String(10), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("revenue", sa.Numeric(20, 2), nullable=True),
        sa.Column("cost_of_goods_sold", sa.Numeric(20, 2), nullable=True),
        sa.Column("gross_profit", sa.Numeric(20, 2), nullable=True),
        sa.Column("operating_expense", sa.Numeric(20, 2), nullable=True),
        sa.Column("operating_profit", sa.Numeric(20, 2), nullable=True),
        sa.Column("net_income", sa.Numeric(20, 2), nullable=True),
        sa.Column("total_assets", sa.Numeric(20, 2), nullable=True),
        sa.Column("total_liabilities", sa.Numeric(20, 2), nullable=True),
        sa.Column("total_equity", sa.Numeric(20, 2), nullable=True),
        sa.Column("cash", sa.Numeric(20, 2), nullable=True),
        sa.Column("debt", sa.Numeric(20, 2), nullable=True),
        sa.Column("free_cash_flow", sa.Numeric(20, 2), nullable=True),
        sa.Column("issued_shares", sa.Numeric(20, 2), nullable=True),
        sa.Column("dividend_per_share", sa.Numeric(15, 2), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "financial_indicators",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("symbol", sa.String(10), nullable=False, index=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("pe", sa.Numeric(15, 2), nullable=True),
        sa.Column("pb", sa.Numeric(15, 2), nullable=True),
        sa.Column("ps", sa.Numeric(15, 2), nullable=True),
        sa.Column("ev_ebitda", sa.Numeric(15, 2), nullable=True),
        sa.Column("roe", sa.Numeric(10, 4), nullable=True),
        sa.Column("roa", sa.Numeric(10, 4), nullable=True),
        sa.Column("de_ratio", sa.Numeric(10, 4), nullable=True),
        sa.Column("current_ratio", sa.Numeric(10, 4), nullable=True),
        sa.Column("dividend_yield", sa.Numeric(10, 4), nullable=True),
        sa.Column("market_cap", sa.Numeric(20, 2), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "technical_indicators",
        sa.Column("time", sa.DateTime(), primary_key=True),
        sa.Column("symbol", sa.String(10), primary_key=True),
        sa.Column("ma_20", sa.Numeric(15, 2), nullable=True),
        sa.Column("ma_50", sa.Numeric(15, 2), nullable=True),
        sa.Column("ma_200", sa.Numeric(15, 2), nullable=True),
        sa.Column("rsi_14", sa.Numeric(10, 4), nullable=True),
        sa.Column("macd", sa.Numeric(15, 4), nullable=True),
        sa.Column("macd_signal", sa.Numeric(15, 4), nullable=True),
        sa.Column("macd_histogram", sa.Numeric(15, 4), nullable=True),
        sa.Column("bollinger_upper", sa.Numeric(15, 2), nullable=True),
        sa.Column("bollinger_middle", sa.Numeric(15, 2), nullable=True),
        sa.Column("bollinger_lower", sa.Numeric(15, 2), nullable=True),
        sa.Column("atr_14", sa.Numeric(15, 4), nullable=True),
        sa.Column("volume_sma_20", sa.BigInteger(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_technical_indicators_time", "technical_indicators", ["time"])
    op.create_index("idx_technical_indicators_symbol_time", "technical_indicators", ["symbol", "time"])

    op.create_table(
        "ingestion_log",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("task_name", sa.String(100), nullable=False),
        sa.Column("symbol", sa.String(10), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("rows_inserted", sa.Integer(), default=0),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_table("ingestion_log")
    op.drop_table("technical_indicators")
    op.drop_table("financial_indicators")
    op.drop_table("financial_reports")
    op.drop_table("ohlc_prices")
    op.drop_table("vn30_symbols")
