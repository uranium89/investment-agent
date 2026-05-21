---
name: investment-agent
description: >
  VN30 Investment Agent — automated quantitative investment pipeline for the
  Vietnamese stock market. Use this skill when working with the pipeline codebase:
  scoring (VMQ30), portfolio construction, backtesting, risk management, DNSE
  trade execution, FireAnt market data, Telegram monitoring, or Celery tasks.
---

# VN30 Investment Agent Skill

Automated investment system for VN30 using **FireAnt MCP** (market data) and **DNSE MCP** (trade execution), orchestrated by Celery scheduled tasks.

## Architecture

```
Celery Beat (daily: 08:30, 15:30, 15:32, 15:35, 15:40, 16:00)
  │
  ├─ Data Ingest (FireAnt MCP + TCBS PDF)  ──► PostgreSQL
  ├─ Feature Engineering (technical + fundamental)
  ├─ VMQ30 Scoring Engine ──► Screening ──► Quality/Value/Tech/Moat/Mgmt ──► Macro Overlay
  ├─ Portfolio Constructor ──► sector caps, 25% cash, score-weight allocation
  ├─ Risk Manager (drawdown, black swan, sector exposure)
  ├─ DNSE Execution (approval → OTP → place → reconcile)
  └─ Monitoring (Grafana + Telegram)
```

## Directory Layout

```
pipeline/                        # Python 3.12+ data pipeline
├── pipeline/
│   ├── clients/                 # FireAnt + DNSE MCP clients
│   ├── ingestors/               # OHLC, financials, company, TCBS PDF parser
│   ├── features/                # Technical + fundamental indicators
│   ├── scoring/                 # VMQ30 engine: gates, quality, value, technical, moat, management, macro
│   ├── portfolio/               # Constructor, rebalancer, sizing, paper_trading (backtest)
│   ├── execution/               # OTP, approval workflow, order management
│   ├── risk/                    # Drawdown, black swan, sector exposure
│   ├── monitoring/              # Telegram alerts, daily report
│   ├── ai/                      # News sentiment, signal validation, report generator
│   ├── tasks/                   # Celery tasks (daily_close, open, tcbs, scoring, execution, monitoring)
│   ├── scripts/                 # CLI: vn30-pipeline, vn30-backtest, vn30-report
│   ├── db/                      # Database models + connection
│   └── storage/                 # Parquet export
mcp-server/                      # FireAnt MCP server (TypeScript)
mcp-server-dnse/                 # DNSE MCP server (TypeScript)
grafana/                         # Grafana dashboard provisioning
docs/                            # System documentation
```

## VMQ30 Scoring Engine

### 1. Screening Gates (FAIL = excluded)
| Gate | Condition | Bank exception |
|------|-----------|---------------|
| D/E | < 1.5 | < 10.0 |
| ROE (3yr) | > 10% at least 2/3 years | — |
| Market Cap | > 5,000 tỷ | — |
| ADTV | > 30 tỷ/day | — |
| FCF | Positive 2/3 years | — |

### 2. Component Scores (each 0–10, averaged)
| Component | Weight in avg | Key inputs |
|-----------|--------------|------------|
| Quality | 1/5 | ROE 40% + D/E 30% + FCF Yield 30% |
| Value | 1/5 | P/E percentile in VN30, P/B < 2 bonus |
| Technical | 1/5 | Trend (EMA50/200, ADX, volume) + momentum (RSI, MACD) |
| Moat | 1/5 | Hardcoded: VNM/VCB=10, MWG/FPT/VIC/VHM/GAS/HPG=7, PNJ/SAB/PLX/MSN=5 |
| Management | 1/5 | Insider net buy +3, net sell -3, CEO identified +1 |

### 3. Macro Overlay (±20% total)
- VN-Index > MA200: +10%
- Policy rate cut: +10%
- (negative equivalents for opposite conditions)

### 4. Signal
| Score | Signal |
|-------|--------|
| >= 5.0 | ENTER |
| >= 3.5 | HOLD |
| < 3.5 | NONE |

## Portfolio Construction

1. Take top 10 ENTER signals sorted by total_score
2. Reserve 25% cash minimum
3. Allocate 75% proportionally by score weight
4. Sector caps: finance ≤40%, real estate ≤20%
5. Single position ≤10%

## Key Settings (pipeline/pipeline/config.py, prefix PIPELINE_)

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_URL` | postgresql+asyncpg://vn30:vn30_dev_only@localhost:5432/vn30_pipeline | Async DB |
| `REDIS_URL` | redis://localhost:6379/0 | Celery broker |
| `MAX_DRAWDOWN_PCT` | 15.0 | Max portfolio drawdown |
| `BLACK_SWAN_THRESHOLD_PCT` | -5.0 | VN-Index daily drop freeze |
| `MAX_SECTOR_FINANCE_PCT` | 40.0 | Finance sector limit |
| `MAX_SECTOR_REALESTATE_PCT` | 20.0 | Real estate sector limit |
| `MAX_SINGLE_POSITION_PCT` | 10.0 | Per-stock limit |
| `MIN_CASH_PCT` | 25.0 | Minimum cash reserve |
| `APPROVAL_REQUIRED` | true | Human-in-loop approval |
| `ENTER_THRESHOLD` | 5.0 | ENTER signal cutoff |
| `EXIT_THRESHOLD` | 3.5 | EXIT signal cutoff |

## Database (PostgreSQL + TimescaleDB, 13 tables)

Key tables: `vn30_symbols`, `ohlc_prices` (hypertable), `financial_reports`, `financial_indicators`, `technical_indicators` (hypertable), `score_snapshots`, `screening_results`, `portfolio_state`, `order_log`, `approval_requests`, `risk_events`, `ingestion_log`, `telegram_log`, `paper_trades`.

32 VN30 symbols: ACB, BCM, BID, BVH, CTG, FPT, GAS, GVR, HDB, HPG, MBB, MSN, MWG, NVL, PDR, PLX, PNJ, POW, SAB, SHB, SSB, SSI, STB, TCB, TPB, VCB, VHM, VIC, VJC, VNM, VPB, VRE

## CLI Commands

```bash
# Run full daily-close pipeline
vn30-pipeline

# Backtest (paper trading simulation)
vn30-backtest --start 2025-06-01 --end 2026-05-21 --capital 1000000000 --sensitivity

# Generate AI daily report
vn30-report
```

## Celery Daily Schedule

| Time | Task | Description |
|------|------|-------------|
| 08:30 | daily-open | Company info update |
| 15:30 | daily-close | OHLC + financials + technicals |
| 15:32 | daily-tcbs | TCBS PDF download + balance sheet |
| 15:35 | daily-scoring | Screener → Score → Signal → Portfolio |
| 15:40 | daily-execution | Risk → Approval → OTP → Orders |
| 16:00 | daily-monitoring | Report → Telegram → Risk review |

## Risk Rules

| Drawdown | Action |
|----------|--------|
| > 10% | Reduce positions to 75%, review all |
| > 15% | Reduce to 50%, defensive only |
| > 20% | Close all, keep only VNM/VCB |

**Black swan:** VN-Index drops ≥5% in 1 day → FREEZE_ALL.  
**Stop loss:** No per-stock stop loss. Only portfolio-level drawdown control.  
**Margin:** Never use margin.  
**Cash:** Always 20-30%.

## MCP Communication

Both MCP servers (FireAnt, DNSE) are Node.js processes communicating via stdio JSON-RPC 2.0. Python clients spawn them as subprocesses.

- `pipeline/clients/fireant.py` wraps FireAnt MCP (13 tools)
- `pipeline/clients/dnse.py` wraps DNSE MCP (12 trading methods)

## Development

```bash
# Setup
python3.12 -m venv pipeline/.venv
source pipeline/.venv/bin/activate
pip install -e pipeline/
(cd mcp-server && npm install && npm run build)
(cd mcp-server-dnse && npm install && npm run build)

# DB (local Docker)
cd pipeline && docker compose --profile local-db up -d

# Run Celery worker
celery -A pipeline.tasks.celery_app worker --loglevel=info

# Run Celery Beat
celery -A pipeline.tasks.celery_app beat --loglevel=info
```

## Golden Rules (Never Violate)

1. NO margin trading
2. NO AI-only trade decisions (human approval required)
3. NO day trading or scalping
4. NO deviation from risk management rules
5. NO deploy without backtest
6. NO trading outside VN30
7. NO ignoring system errors
