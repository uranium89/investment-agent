import json
import logging
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, Date, Numeric, BigInteger, Integer, Text, Boolean
from sqlalchemy.orm import DeclarativeBase
import enum


logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class IngestionStatus(str, enum.Enum):
    running = "running"
    completed = "completed"
    failed = "failed"
    skipped = "skipped"


class VN30Symbol(Base):
    __tablename__ = "vn30_symbols"

    symbol = Column(String(10), primary_key=True)
    company_name = Column(String(255), nullable=False)
    icb_code = Column(String(20), nullable=True)
    icb_name = Column(String(255), nullable=True)
    market_cap = Column(Numeric(20, 2), nullable=True)
    listed_date = Column(Date, nullable=True)
    status = Column(String(20), default="active")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OHLCPrice(Base):
    __tablename__ = "ohlc_prices"

    time = Column(DateTime, primary_key=True)
    symbol = Column(String(10), primary_key=True)
    open = Column(Numeric(15, 2), nullable=False)
    high = Column(Numeric(15, 2), nullable=False)
    low = Column(Numeric(15, 2), nullable=False)
    close = Column(Numeric(15, 2), nullable=False)
    volume = Column(BigInteger, nullable=False)
    adj_close = Column(Numeric(15, 2), nullable=True)


class FinancialReport(Base):
    __tablename__ = "financial_reports"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False, index=True)
    period = Column(String(10), nullable=False)
    year = Column(Integer, nullable=False)
    revenue = Column(Numeric(20, 2), nullable=True)
    cost_of_goods_sold = Column(Numeric(20, 2), nullable=True)
    gross_profit = Column(Numeric(20, 2), nullable=True)
    operating_expense = Column(Numeric(20, 2), nullable=True)
    operating_profit = Column(Numeric(20, 2), nullable=True)
    net_income = Column(Numeric(20, 2), nullable=True)
    total_assets = Column(Numeric(20, 2), nullable=True)
    total_liabilities = Column(Numeric(20, 2), nullable=True)
    total_equity = Column(Numeric(20, 2), nullable=True)
    cash = Column(Numeric(20, 2), nullable=True)
    debt = Column(Numeric(20, 2), nullable=True)
    free_cash_flow = Column(Numeric(20, 2), nullable=True)
    issued_shares = Column(Numeric(20, 2), nullable=True)
    dividend_per_share = Column(Numeric(15, 2), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FinancialIndicator(Base):
    __tablename__ = "financial_indicators"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False, index=True)
    date = Column(Date, nullable=False)
    pe = Column(Numeric(15, 2), nullable=True)
    pb = Column(Numeric(15, 2), nullable=True)
    ps = Column(Numeric(15, 2), nullable=True)
    ev_ebitda = Column(Numeric(15, 2), nullable=True)
    roe = Column(Numeric(10, 4), nullable=True)
    roa = Column(Numeric(10, 4), nullable=True)
    de_ratio = Column(Numeric(10, 4), nullable=True)
    current_ratio = Column(Numeric(10, 4), nullable=True)
    dividend_yield = Column(Numeric(10, 4), nullable=True)
    market_cap = Column(Numeric(20, 2), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        {"info": {"comment": "symbol + date snapshot"}},
    )


class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

    time = Column(DateTime, primary_key=True)
    symbol = Column(String(10), primary_key=True)
    ma_20 = Column(Numeric(15, 2), nullable=True)
    ma_50 = Column(Numeric(15, 2), nullable=True)
    ma_200 = Column(Numeric(15, 2), nullable=True)
    rsi_14 = Column(Numeric(10, 4), nullable=True)
    macd = Column(Numeric(15, 4), nullable=True)
    macd_signal = Column(Numeric(15, 4), nullable=True)
    macd_histogram = Column(Numeric(15, 4), nullable=True)
    bollinger_upper = Column(Numeric(15, 2), nullable=True)
    bollinger_middle = Column(Numeric(15, 2), nullable=True)
    bollinger_lower = Column(Numeric(15, 2), nullable=True)
    atr_14 = Column(Numeric(15, 4), nullable=True)
    volume_sma_20 = Column(BigInteger, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class IngestionLog(Base):
    __tablename__ = "ingestion_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_name = Column(String(100), nullable=False)
    symbol = Column(String(10), nullable=True)
    status = Column(String(20), nullable=False)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    rows_inserted = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)


class ScoreSnapshot(Base):
    __tablename__ = "score_snapshots"

    time = Column(DateTime, primary_key=True)
    symbol = Column(String(10), primary_key=True)
    quality_score = Column(Numeric(5, 2), nullable=True)
    value_score = Column(Numeric(5, 2), nullable=True)
    technical_score = Column(Numeric(5, 2), nullable=True)
    moat_score = Column(Numeric(5, 2), nullable=True)
    management_score = Column(Numeric(5, 2), nullable=True)
    macro_overlay = Column(Numeric(5, 2), nullable=True)
    total_score = Column(Numeric(5, 2), nullable=True)
    passed_screening = Column(Boolean, default=False)
    screening_detail = Column(Text, nullable=True)
    signal = Column(String(10), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PortfolioState(Base):
    __tablename__ = "portfolio_state"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False, index=True)
    entry_date = Column(DateTime, nullable=False)
    entry_price = Column(Numeric(15, 2), nullable=False)
    current_price = Column(Numeric(15, 2), nullable=True)
    shares = Column(BigInteger, nullable=False)
    cost_basis = Column(Numeric(20, 2), nullable=False)
    current_value = Column(Numeric(20, 2), nullable=True)
    weight_pct = Column(Numeric(5, 2), nullable=True)
    sector = Column(String(50), nullable=True)
    pnl_pct = Column(Numeric(10, 4), nullable=True)
    signal = Column(String(10), nullable=True)
    status = Column(String(20), default="active")
    closed_date = Column(DateTime, nullable=True)
    closed_reason = Column(String(100), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False, index=True)
    date = Column(Date, nullable=False)
    passed = Column(Boolean, default=False)
    de_check = Column(Boolean, nullable=True)
    roe_check = Column(Boolean, nullable=True)
    market_cap_check = Column(Boolean, nullable=True)
    adtv_check = Column(Boolean, nullable=True)
    fcf_check = Column(Boolean, nullable=True)
    details = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OrderLog(Base):
    __tablename__ = "order_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False, index=True)
    symbol = Column(String(10), nullable=False)
    side = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(15, 2), nullable=True)
    order_type = Column(String(10), default="LO")
    status = Column(String(20), nullable=False)
    remote_order_id = Column(String(50), nullable=True)
    filled_quantity = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False, unique=True, index=True)
    proposed_trades = Column(Text, nullable=False)
    status = Column(String(20), default="pending")
    approval_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RiskEvent(Base):
    __tablename__ = "risk_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_type = Column(String(50), nullable=False, index=True)
    severity = Column(String(20), nullable=False)
    details = Column(Text, nullable=True)
    triggered_at = Column(DateTime, nullable=False)
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TelegramLog(Base):
    __tablename__ = "telegram_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message_type = Column(String(50), nullable=False)
    content_preview = Column(String(255), nullable=True)
    sent_at = Column(DateTime, nullable=False)
    success = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)


class PaperTrade(Base):
    __tablename__ = "paper_trades"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(String(50), nullable=False, index=True)
    symbol = Column(String(10), nullable=False)
    side = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(15, 2), nullable=False)
    order_type = Column(String(10), default="LO")
    status = Column(String(20), default="pending")
    filled_quantity = Column(Integer, nullable=True)
    fill_price = Column(Numeric(15, 2), nullable=True)
    slippage_pct = Column(Numeric(10, 4), nullable=True)
    simulated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
