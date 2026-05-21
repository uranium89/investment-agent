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
│  ┌──────────────┐   ┌──────────────┐           │                  │
│  │ MACRO OVERLAY│──▶│ PORTFOLIO    │◀──────────┘                  │
│  │ (Dalio Rule) │   │ CONSTRUCTOR  │                              │
│  └──────────────┘   └──────┬───────┘                              │
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
│  │                 MONITORING & LOGGING                   │         │
│  │   (Grafana + Prometheus + Audit DB + Telegram)       │         │
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
- **PostgreSQL + TimescaleDB** — Supabase hoặc local Docker
- Bảng `ohlc_prices`: TimescaleDB hypertable (time-series optimized)
- Bảng `financial_reports`: báo cáo tài chính quý
- Bảng `financial_indicators`: P/E, P/B, ROE, v.v.
- Bảng `technical_indicators`: MA, RSI, MACD, Bollinger, ATR

### 2. Analysis Layer (Phase 2 đã hoàn thành)

- **Technical indicators**: MA20/50/200, RSI14, MACD, Bollinger Bands (2σ), ATR14
- **Fundamental metrics**: ROE, P/E, P/B, D/E, FCF yield
- **Scoring engine** (VMQ30 hybrid): Quality (ROE 40%, D/E 30%, FCF Yield 30%) + Value + Technical + Moat + Management
- **Screening gates**: D/E < 1.5 (bank < 10), ROE > 10% (3 năm), ADTV > 30 tỷ, Market Cap > 5k tỷ, FCF dương 2/3 năm
- **Portfolio construction**: Top ENTER signals, weight theo score, sector caps

### 3. Execution Layer (PHASE 3)

- **DNSE MCP** gửi lệnh (cần OTP — human-in-the-loop)
- **Position sizing**: Kelly Criterion điều chỉnh (half-Kelly)
- **Risk management**: drawdown control, sector limits, volatility targeting

## Tech Stack

| Layer | Công nghệ | Ghi chú |
|---|---|---|---|
| Language | Python 3.12+ | Quant analysis, pipeline |
| MCP Clients | Python asyncio + subprocess stdio | Gọi MCP servers từ Python |
| PDF Parsing | pdfplumber | TCBS one-click report balance sheet (daily auto via Celery) |
| Database | PostgreSQL (local Docker) | TimescaleDB optional |
| Queue | Redis (local) | Celery broker |
| Task Queue | Celery | Schedule + worker |
| Scheduling | Celery Beat / cron | Daily 08:30 và 15:30 |
| Monitoring | Prometheus + Grafana | PHASE 3 |
| Alerting | Telegram Bot | PHASE 3 |

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
PostgreSQL / TimescaleDB
    ↓
pipeline/features/ (technical + fundamental)
    ↓
TimescaleDB (technical_indicators table)
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
