"""Add execution, monitoring, risk management tables

Revision ID: 003
Revises: 002
Create Date: 2026-05-21

"""
from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "order_log",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(50), nullable=False),
        sa.Column("symbol", sa.String(10), nullable=False),
        sa.Column("side", sa.String(10), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(15, 2), nullable=True),
        sa.Column("order_type", sa.String(10), server_default="LO"),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("remote_order_id", sa.String(50), nullable=True),
        sa.Column("filled_quantity", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_order_log_run_id", "order_log", ["run_id"])

    op.create_table(
        "approval_requests",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(50), nullable=False),
        sa.Column("proposed_trades", sa.Text(), nullable=False),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("approval_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("decided_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("run_id"),
    )
    op.create_index("ix_approval_requests_run_id", "approval_requests", ["run_id"])

    op.create_table(
        "risk_events",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("triggered_at", sa.DateTime(), nullable=False),
        sa.Column("acknowledged", sa.Boolean(), server_default="false"),
        sa.Column("acknowledged_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_risk_events_event_type", "risk_events", ["event_type"])

    op.create_table(
        "telegram_log",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("message_type", sa.String(50), nullable=False),
        sa.Column("content_preview", sa.String(255), nullable=True),
        sa.Column("sent_at", sa.DateTime(), nullable=False),
        sa.Column("success", sa.Boolean(), server_default="false"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "paper_trades",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(50), nullable=False),
        sa.Column("symbol", sa.String(10), nullable=False),
        sa.Column("side", sa.String(10), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(15, 2), nullable=False),
        sa.Column("order_type", sa.String(10), server_default="LO"),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("filled_quantity", sa.Integer(), nullable=True),
        sa.Column("fill_price", sa.Numeric(15, 2), nullable=True),
        sa.Column("slippage_pct", sa.Numeric(10, 4), nullable=True),
        sa.Column("simulated_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_paper_trades_run_id", "paper_trades", ["run_id"])


def downgrade():
    op.drop_table("paper_trades")
    op.drop_table("telegram_log")
    op.drop_table("risk_events")
    op.drop_table("approval_requests")
    op.drop_table("order_log")
