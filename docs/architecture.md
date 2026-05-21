# Kiến trúc hệ thống

## Tổng quan

```
┌────────────────────────────────────────────────────────────────────┐
│                        CRON SCHEDULER                              │
│              Celery Beat (daily: 08:30, 15:30)                    │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────┐  ┌──────────────┐   ┌──────────────┐           │
│  │ DATA INGEST    │─▶│ FEATURE ENG  │──▶│ SCORING ENG  │           │
│  │ (FireAnt+TCBS) │  │ (Python)     │   │ (VMQ30 Rule) │  PHASE 2  │
│  └────────────────┘  └──────────────┘   └──────┬───────┘           │
│                                                 │                  │
│  ┌──────────────────────────────────────────────────────┐         │
│  │               AI LAYER                                 │         │
│  │  News Sentiment → Signal Validator → Report Generator │  PHASE 3 │
│  └────────────────────────┬─────────────────────────────┘         │
│                            │                                       │
│  ┌──────────────┐   ┌─────┴────────┐   ┌──────────────┐           │
│  │ MACRO OVERLAY│──▶│ PORTFOLIO    │◀──│ PAPER TRADING│           │
│  │ (Dalio Rule) │   │ CONSTRUCTOR  │   │ (Backtest)   │  PHASE 3  │
│  └──────────────┘   └──────┬───────┘   └──────────────┘           │
│                             │                                      │
│  ┌──────────────┐          │           ┌──────────────┐           │
│  │ RISK MANAGER │◀─────────┼──────────▶│ HUMAN REVIEW │           │
│  │ (Hard Rules) │          │           │ (Approval)   │           │
│  └──────────────┘          │           └──────┬───────┘           │
│                             │                  │                   │
│                             ▼                  ▼                   │
│  ┌──────────────────────────────────────────────────────┐         │
│  │                 DNSE EXECUTION                        │         │
│  │     (OTP → Place Order → Confirm → Log)               │         │
│  └──────────────────────────────────────────────────────┘         │
│                                                                     │
│  ┌──────────────────────────────────────────────────────┐         │
│  │              MONITORING & LOGGING                     │         │
│  │    Grafana (dashboard) + Telegram (alerts) + Audit DB │         │
│  └──────────────────────────────────────────────────────┘         │
└────────────────────────────────────────────────────────────────────┘
```

## Chi tiết các lớp

### 1. Data Layer (MVP đã hoàn thành)

**Nguồn dữ liệu:**
- **FireAnt MCP** (45 tools): OHLC giá, fundamental, chỉ số định giá, thông tin công ty, tin tức
- **TCBS PDF** (static.tcbs.com.vn/oneclick/): Balance sheet cho 32 VN30 (revenue, net_income, total_assets, total_equity, debt, cash, FCF) — banks không có FCF
- **DNSE MCP** (20 tools, read-only trong MVP): OHLC real-time, security definition

**Lưu trữ:**
- **PostgreSQL** (local Docker) — không TimescaleDB
- Bảng `ohlc_prices`: hypertable (time-series optimized)
- Bảng `financial_reports`: báo cáo tài chính quý
- Bảng `financial_indicators`: P/E, P/B, ROE, v.v.
- Bảng `technical_indicators`: MA, RSI, MACD, Bollinger, ATR
- Bảng `vn30_symbols`: 32 mã với icb_name, icb_code, market_cap, listed_date, company_name

### 2. Analysis Layer (Phase 2 đã hoàn thành)

- **Technical indicators**: MA20/50/200, RSI14, MACD, Bollinger Bands (2σ), ATR14
- **Fundamental metrics**: ROE, P/E, P/B, D/E, FCF yield
- **Scoring engine** (VMQ30 hybrid): Quality (ROE 40%, D/E 30%, FCF Yield 30%) + Value + Technical + Moat + Management
- **Screening gates**: D/E < 1.5 (bank < 10), ROE > 10% (3 năm), ADTV > 30 tỷ, Market Cap > 5k tỷ, FCF dương 2/3 năm
- **Portfolio construction**: Top ENTER signals, weight theo score, sector caps (finance 40%, real estate 20%)

### 3. AI Layer (Phase 3)

- **`ai/news_sentiment.py`**: Keyword-based sentiment từ FireAnt posts + market news summary
- **`ai/signal_validator.py`**: Cross-check Q/V/T scores vs signal, divergence detection
- **`ai/report_generator.py`**: Daily AI report — signals, portfolio, drawdown, market news

### 4. Paper Trading (Phase 3)

- **`portfolio/paper_trading.py`**: Backtesting engine: historical scoring simulation, monthly rebalance, 0.1% slippage, position sizing
- **Parameter sensitivity**: 45 combos (5 entry × 5 exit thresholds × 3 cash levels × 3 max positions)
- **Performance metrics**: Sharpe, Sortino, max drawdown, Calmar, win rate, profit factor

### 5. Execution Layer (Phase 3)

- **DNSE MCP** gửi lệnh (cần OTP — human-in-the-loop)
- **Position sizing**: Kelly Criterion điều chỉnh (half-Kelly)
- **Risk management**: drawdown control, black swan detection, sector limits, volatility targeting

### 6. Monitoring (Phase 3)

- **Grafana dashboard** (port 3000, admin/admin): portfolio value, drawdown, score distribution, sector exposure, order logs, risk events, VN30 overview, data ingestion status
- **Telegram Bot**: real-time alerts for trades, risks, orders, daily reports (chưa cấu hình)

## Tech Stack

| Layer | Công nghệ | Ghi chú |
|---|---|---|
| Language | Python 3.12+ | Quant analysis, pipeline |
| MCP Clients | Python asyncio + subprocess stdio | Gọi MCP servers từ Python |
| PDF Parsing | pdfplumber | TCBS one-click report balance sheet (daily auto via Celery) |
| Database | PostgreSQL (local Docker) | TimescaleDB optional |
| Queue | Redis (local) | Celery broker |
| Task Queue | Celery | Schedule + worker |
| Scheduling | Celery Beat / cron | Daily 08:30, 15:30, 15:32, 15:35, 15:40, 16:00 |
| Dashboard | Grafana | Portfolio overview (1 dashboard, 9 panels) |
| Alerting | Telegram Bot | Chưa active (cần bot token) |

## Data Flow

```
FireAnt API
    ↓ (HTTP)
FireAnt MCP Server (Node.js)
    ↓ (stdio JSON-RPC)
pipeline/clients/fireant.py (Python async)
    ↓
pipeline/ingestors/ (data transformation)
    ↓
PostgreSQL
    ↓
pipeline/features/ (technical + fundamental)
    ↓
PostgreSQL (technical_indicators table)
    ↓
pipeline/scoring/ → portfolio/ → execution/ → monitoring/
    ↓
Grafana ← DB query ← PostgreSQL
Telegram ← async HTTP ← monitoring/telegram.py
```

## MCP Communication Protocol

```
Python Client                    MCP Server (Node.js)
    │                                   │
    │──── initialize ──────────────────▶│
    │◀── protocolVersion + capabilities │
    │                                   │
    │──── tools/call ──────────────────▶│
    │    {name, arguments}              │
    │◀── {content: [{type: "text"}]}    │
    │                                   │
```

Mỗi MCP server là một subprocess Node.js, giao tiếp qua stdin/stdout với JSON-RPC 2.0.
