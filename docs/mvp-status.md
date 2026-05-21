# MVP Status — Những gì đã xây dựng

## ✅ Đã hoàn thành (Phase 1 — Infrastructure)

### 1. Python Package Infrastructure

| File | Trạng thái | Mô tả |
|---|---|---|
| `pipeline/pyproject.toml` | ✅ | Python project config, dependencies |
| `pipeline/docker-compose.yml` | ✅ | Optional local dev environment |
| `pipeline/Dockerfile` | ✅ | Container build |
| `pipeline/.env.example` | ✅ | Environment variables mẫu |
| `pipeline/pipeline/config.py` | ✅ | Settings + VN32 symbols |

### 2. Database Schema

| Table | Type | Mô tả |
|---|---|---|
| `vn30_symbols` | Regular | Danh sách 32 mã VN30 (có icb_name, icb_code, market_cap, listed_date) |
| `ohlc_prices` | TimescaleDB hypertable | OHLC giá lịch sử |
| `financial_reports` | Regular | Báo cáo tài chính quý |
| `financial_indicators` | Regular | Chỉ số định giá hàng ngày |
| `technical_indicators` | TimescaleDB hypertable | MA, RSI, MACD, Bollinger, ATR |
| `ingestion_log` | Regular | Audit trail cho data pipeline |
| `order_log` | Regular | Order execution history |
| `approval_requests` | Regular | Human approval audit trail |
| `risk_events` | Regular | Drawdown/black swan/sector breach events |
| `telegram_log` | Regular | Telegram message delivery log |
| `paper_trades` | Regular | Paper trading simulation records |

### 3. FireAnt MCP Client (`clients/fireant.py` — 236 dòng)

- Async stdio transport với FireAnt MCP server
- Auto initialize + error handling
- Wrappers cho 13 tools quan trọng:
  - `symbol_info`, `historical_quotes`, `financial_reports`
  - `financial_indicators`, `company_profile`
  - `fundamental`, `holders`, `officers`
  - `symbol_posts`, `screener`, `dividends`
  - `transactions`, `instruments`, `rrg`
- **Đã test live với 5 symbols: ACB, FPT, VNM, HPG, VCB**

### 4. DNSE MCP Client (`clients/dnse.py` — extended, 12 trading methods)

- Async stdio transport với DNSE MCP server
- Read-only + trading methods: OTP, order CRUD, positions, balances, PPSE

### 5. Data Ingestors

| Ingestor | Nguồn | Bảng đích |
|---|---|---|
| `ingestors/prices.py` | `historical_quotes` | `ohlc_prices` |
| `ingestors/financials.py` | `fundamental` + `financial_indicators` | `financial_reports` + `financial_indicators` |
| `ingestors/company.py` | `symbol_info` | `vn30_symbols` |
| `ingestors/tcbs_financial_reports.py` | TCBS PDF | `financial_reports` (balance sheet) |

### 6. Feature Engineering

| Module | Indicators |
|---|---|
| `features/technical.py` | MA20/50/200, RSI14, MACD (line+signal+histogram), Bollinger Bands (2σ), ATR14 |
| `features/fundamental.py` | ROE, P/E, P/B, D/E, Market Cap |

### 7. Celery Tasks

- `tasks/celery_app.py` — Celery app config + Beat schedule
- `tasks/daily_close.py` — 15:30: OHLC ingestion → fundamental → technical indicators
- `tasks/daily_open.py` — 08:30: company info update
- `tasks/daily_tcbs.py` — 15:32: TCBS PDF download → balance sheet ingest
- `tasks/daily_scoring.py` — 15:35: scoring pipeline
- `tasks/daily_execution.py` — 15:40: risk checks → approval → OTP → orders → reconcile
- `tasks/daily_monitoring.py` — 16:00: report → Telegram → risk review

### 8. Storage

- `storage/warehouse.py` — Parquet export cho backtesting

### 9. Bootstrap

- `scripts/bootstrap.sh` — Auto setup: build MCP → venv → database → seed

## ✅ Đã hoàn thành (Phase 2 — Scoring Engine)

### 10. VMQ30 Scoring Engine

| Module | Mô tả |
|---|---|
| `scoring/gates.py` | Screening gate: D/E (<1.5, bank <10), ROE (>10% 3 năm), Market Cap (>5k tỷ), ADTV (>30 tỷ), FCF (dương 2/3 năm) |
| `scoring/quality.py` | Quality score: ROE 40%, D/E 30%, FCF Yield 30% — fallback `financial_indicators` khi thiếu balance sheet |
| `scoring/value.py` | Value score: P/E percentile trong VN30 |
| `scoring/technical.py` | Technical score: trend (EMA50/200, golden cross, ADX) + momentum (RSI, MACD) |
| `scoring/moat.py` | Moat score: định kỳ 6 tháng |
| `scoring/management.py` | Management score: insider transactions, ESOP dilution |
| `scoring/macro.py` | Macro overlay: lãi suất, VN-Index trend (±20%) |
| `scoring/engine.py` | Orchestrator: chạy screening → 5 component scores → normalize → signal (ENTER≥5.0, HOLD≥3.5, NONE) |

### 11. Portfolio Construction

- `portfolio/constructor.py` — Top ENTER signals, weight theo score, sector caps (finance 40%, real estate 20%), single cap 10%, cash 25%+
- Kết quả real data (21/05/2026): **ENTER: VNM (5.51)**, HOLD: 11 stocks (ACB 3.99, MBB 3.80, FPT 4.93...)

### 12. TCBS PDF Parser (Nguồn balance sheet)

| File | Mô tả |
|---|---|
| `ingestors/tcbs_financial_reports.py` | Download PDF từ `static.tcbs.com.vn/oneclick/{symbol}.pdf`, parse bằng pdfplumber, extract revenue/net_income/total_assets/total_equity/debt/cash/FCF |
| Coverage | 32/32 VN30 symbols, 5 năm (2021–2025) mỗi mã. Banks: không có FCF (báo cáo TCBS khác cấu trúc) |

## ✅ Đã hoàn thành (Phase 3 — Execution & Monitoring)

### Execution (Week 1)
| Module | Mô tả |
|---|---|
| `execution/otp.py` | Email OTP → trading token flow |
| `execution/approval.py` | Human-in-the-loop approval: file-based JSON request, polling, timeout |
| `execution/orders.py` | Order placement, build payload, reconcile, get portfolio value |
| `clients/dnse.py` | Extended: trading token, order CRUD, positions, balances, PPSE |

### Risk Management (Week 3)
| Module | Mô tả |
|---|---|
| `risk/drawdown.py` | Portfolio drawdown tracking (6-month rolling), breach alert, peak-to-current |
| `risk/black_swan.py` | VN-Index daily drop check (-5% threshold), freeze-all action |
| `risk/sector.py` | Per-sector exposure check, breach detection, breakdown report |

### Monitoring (Week 2)
| Module | Mô tả |
|---|---|
| `monitoring/telegram.py` | Async Telegram bot alerts: trade, risk, order execution, daily report (chưa active — cần bot token) |
| `monitoring/report.py` | Daily performance report: scores, portfolio, P&L, cash |
| `tasks/daily_monitoring.py` | Celery task 16:00 — report + risk check + Telegram |

### Grafana
- 1 dashboard: **VN30 Pipeline** (portfolio overview, 9 panels)
  - Portfolio Value, Drawdown, Score Distribution, VN30 Universe Overview, VN30 Sector Distribution, VN30 Market Cap by Sector, Sector Exposure, Order Logs, Risk Events, Data Ingestion Status
- Stock Detail dashboard **đã xoá** (theo yêu cầu, do dropdown bug)
- Provisioning: auto từ `grafana/dashboards/dashboard.json` (có uid để tránh duplicate)

## ✅ Đã hoàn thành (Phase 3 — Paper Trading & AI)

### Paper Trading Simulation (Week 4)
| Module | Mô tả |
|---|---|
| `portfolio/paper_trading.py` | Full backtesting engine: historical scoring, monthly rebalance, slippage, position sizing |
| `portfolio/paper_trading.py:run_parameter_sensitivity` | Parameter sweep (5 entry/exit thresholds × 3 cash levels × 3 max positions = 45 combos) |
| `scripts/run_paper_trading.py` | CLI: `vn30-backtest --start 2025-06-01 --end 2026-05-21 --sensitivity` |
| Capacity | Backtest 1 năm với 32 VN30 stocks, rebalance 5 ngày/lần |

### AI Layer
| Module | Mô tả |
|---|---|
| `ai/news_sentiment.py` | Keyword-based sentiment analysis từ FireAnt posts/news, market summary |
| `ai/signal_validator.py` | Cross-check Q/V/T scores against signal, detect disagreements, divergence warnings |
| `ai/report_generator.py` | AI report: signals, portfolio, drawdown, market news (tested OK 21/05/2026) |
| `scripts/run_report.py` | CLI: `vn30-report` |

### CLI Tools
| Command | Usage |
|---|---|
| `vn30-pipeline` | Chạy daily-close pipeline (entry point) |
| `vn30-backtest` | Paper trading: `--start --end --capital --enter --exit --sensitivity --output` |
| `vn30-report` | Generate AI daily report to stdout |

## Database Status

- **32 VN30 symbols** populated với icb_name, icb_code, market_cap (từ financial_indicators), listed_date (hardcoded), company_name, status='active'
- **portfolio_state**: rỗng (chưa có position nào)
- **Financial indicators**: đầy đủ cho 32 symbols (P/E, P/B, ROE, D/E, Market Cap)

## Fixes & Lessons

| Vấn đề | Fix |
|---|---|
| `ingest_financial_indicators` skip list format | Rewrite parser cho `{shortName, value}` mapping |
| `ingest_fundamental` không overwrite | UPSERT pattern (FOR UPDATE + UPDATE/INSERT) |
| `compute_quality_score` FCF/ROE/D/E = NULL | Fallback `financial_indicators` + TCBS PDF parser |
| Total score capped ở 10 | Bỏ cap, normalize bằng `/5` |
| TCBS feed subdomain died | URL mới: `static.tcbs.com.vn/oneclick/` |
| `portfolio_state` query trong report_generator | Dùng `updated_at` thay vì `time` |
| `grafana/dashboards/` directory rỗng | Phải có ít nhất 1 file JSON để provisioning hoạt động |
| Dashboard duplicate khi provision | Thêm `uid` vào JSON dashboard (tránh stale duplicates) |
| Grafana `disableDeletion: false` không auto-delete | Phải cleanup SQLite thủ công khi xoá file dashboard |
| Stock Detail dashboard bị blank dropdown | Template variable + 25 panels gây lỗi Grafana 13; quyết định xoá dashboard |

## Blockers

- **Telegram chưa active**: `PIPELINE_TELEGRAM_BOT_TOKEN` + `PIPELINE_TELEGRAM_CHAT_ID` đang để trống trong `.env`
- **DNSE chưa sẵn sàng**: `PIPELINE_DNSE_EMAIL` + `PIPELINE_DNSE_ACCOUNT_NO` chưa được cấu hình
- **Backtest chưa chạy**: cần run `vn30-backtest --sensitivity` để calibrate thresholds

## Pipeline Real Data Results (21/05/2026)

### Screening
- 15/32 pass screening
- ADTV fails: BCM (4.5), BVH (8.2), GAS (25.9), PNJ (14.5), SAB (10.4), SSB (24.9)
- ROE fails (3-year consistency): HPG, MSN, MWG, NVL, PDR, PLX, SSI, STB, VIC, VPB, VRE
- FCF fails (negative): HPG, NVL, VRE
- D/E fails: VIC (2.21), SSI (1.88)

### Scoring
| Stock | Total | Signal | Quality | Value | Tech |
|---|---|---|---|---|---|
| VNM | 5.51 | ENTER | 6.10 | 5.48 | 0.95 |
| FPT | 4.93 | HOLD | 6.10 | 4.84 | 1.70 |
| VCB | 4.85 | HOLD | 4.00 | 3.23 | 2.00 |
| VHM | 4.85 | HOLD | 4.00 | 6.45 | 1.80 |
| CTG | 4.04 | HOLD | 4.00 | 10.00 | 1.20 |
| ACB | 3.99 | HOLD | 4.00 | 10.00 | 0.95 |

### Portfolio
- 1 position: VNM (10%), 90% cash
- 11 HOLD, 20 NONE

## Beat Schedule

```
daily-close (15:30) → daily-tcbs (15:32) → daily-scoring (15:35)
→ daily-execution (15:40) → daily-monitoring (16:00)
→ daily-open (08:30 next day)
```

## Next Steps

1. Cấu hình Telegram bot token + chat ID
2. Chạy `vn30-backtest --start 2025-06-01 --end 2026-05-21 --sensitivity` để calibrate thresholds
3. Dựa vào backtest results, calibrate ENTER/EXIT thresholds
4. Construct portfolio từ ENTER signals → populate `portfolio_state` → verify Grafana dashboard
