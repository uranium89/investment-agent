# Hướng dẫn vận hành Pipeline

## Yêu cầu

- Python 3.12+
- Node.js v22+
- PostgreSQL (local Docker)
- Redis (local Docker)

## Quick Start

### 1. Setup môi trường

```bash
cd investment-agent

# Tạo Python venv
python3.12 -m venv pipeline/.venv
source pipeline/.venv/bin/activate

# Cài dependencies
pip install -e pipeline/

# Copy env
cp pipeline/.env.example pipeline/.env
# Sửa .env với connection strings
```

### 2. Build MCP servers

```bash
(cd mcp-server && npm install && npm run build)
(cd mcp-server-dnse && npm install && npm run build)
```

### 3. Setup database

```bash
cd pipeline
docker compose --profile local-db up -d
```

### 4. Run migrations

```bash
cd pipeline
source .venv/bin/activate
python3 -c "
import asyncio
from pipeline.db.connection import engine
async def run():
    async with engine.begin() as conn:
        await conn.run_sync(__import__('pipeline.db.models', fromlist=['Base']).Base.metadata.create_all)
    await engine.dispose()
    print('Schema created')
asyncio.run(run())
"
```

### 5. Seed VN30 symbols

```bash
python3 -c "
import asyncio
from pipeline.db.connection import async_session_factory
from pipeline.db.models import VN30Symbol

async def run():
    async with async_session_factory() as session:
        # Chạy seed script hoặc INSERT manually
        print('DB ready')
asyncio.run(run())
"
```

### 6. Setup Grafana

```bash
docker compose --profile grafana up -d
# Grafana at http://localhost:3000 (admin/admin)
# Dashboard tự động provision từ grafana/dashboards/
```

### 7. Chạy manual pipeline

```bash
cd pipeline
source .venv/bin/activate
python -m pipeline.tasks.daily_close
```

## Cấu trúc .env

```env
# Database
PIPELINE_DB_URL=postgresql+asyncpg://vn30:vn30_dev_only@localhost:5432/vn30_pipeline
PIPELINE_DB_URL_SYNC=postgresql://vn30:vn30_dev_only@localhost:5432/vn30_pipeline

# Redis (cho Celery)
PIPELINE_REDIS_URL=redis://localhost:6379/0

# MCP servers
PIPELINE_FIREANT_MCP_DIR=../mcp-server
PIPELINE_DNSE_MCP_DIR=../mcp-server-dnse

# Telegram (optional—chưa config)
PIPELINE_TELEGRAM_BOT_TOKEN=
PIPELINE_TELEGRAM_CHAT_ID=

# DNSE (optional—cần để thực thi)
PIPELINE_DNSE_EMAIL=
PIPELINE_DNSE_ACCOUNT_NO=

# Scoring thresholds
PIPELINE_ENTER_THRESHOLD=5.0
PIPELINE_EXIT_THRESHOLD=3.5
PIPELINE_MAX_DRAWDOWN_PCT=15
PIPELINE_BLACK_SWAN_THRESHOLD_PCT=5
PIPELINE_APPROVAL_REQUIRED=true
PIPELINE_APPROVAL_TIMEOUT_MINUTES=30

# Logging
PIPELINE_LOG_LEVEL=INFO
```

## CLI Commands

```bash
# Chạy daily-close pipeline (OHLC + financials + technicals)
vn30-pipeline

# Backtest + parameter sensitivity
vn30-backtest --start 2025-06-01 --end 2026-05-21 --capital 1000000000 --sensitivity

# Generate AI daily report
vn30-report
```

## Kiểm tra FireAnt connection

```python
import asyncio
from pipeline.clients.fireant import FireAntClient

async def test():
    async with FireAntClient() as client:
        info = await client.symbol_info("FPT")
        print(info["name"])  # CTCP FPT

        quotes = await client.historical_quotes(
            "FPT", "2026-05-01", "2026-05-20"
        )
        print(f"Quotes: {len(quotes)} days")

        fund = await client.fundamental("FPT")
        print(f"P/E: {fund['pe']}")

asyncio.run(test())
```

## Các lệnh hữu ích

```bash
# Chạy Celery worker
celery -A pipeline.tasks.celery_app worker --loglevel=info

# Chạy Celery Beat
celery -A pipeline.tasks.celery_app beat --loglevel=info

# Manual ingestion cho 1 symbol
python3 -c "
import asyncio
from pipeline.clients.fireant import FireAntClient
from pipeline.db.connection import async_session_factory
from pipeline.ingestors.prices import ingest_ohlc

async def run():
    async with FireAntClient() as fireant:
        async with async_session_factory() as session:
            await ingest_ohlc(session, fireant, 'ACB', lookback_days=90)
            await session.commit()

asyncio.run(run())
"

# Export parquet cho backtesting
python3 -c "
import asyncio
from pipeline.db.connection import async_session_factory
from pipeline.storage.warehouse import export_ohlc_parquet

async def run():
    async with async_session_factory() as session:
        path = await export_ohlc_parquet(session, 'ACB')
        print(f'Exported: {path}')

asyncio.run(run())
"
```

## Grafana

- Dashboard: **VN30 Pipeline** — portfolio overview, 9 panels
  - Portfolio Value (time series)
  - Drawdown %
  - Score Distribution (table)
  - VN30 Universe Overview (table)
  - VN30 Sector Distribution (pie)
  - VN30 Market Cap by Sector (bar gauge)
  - Sector Exposure (pie)
  - Order Logs
  - Risk Events
  - Data Ingestion Status
- Provisioning: auto từ `grafana/dashboards/dashboard.json`
- Stock Detail dashboard đã xoá (theo yêu cầu)

## Celery Beat Schedule

```
08:30  daily-open        — Company info update
15:30  daily-close       — OHLC + financials + technicals
15:32  daily-tcbs        — TCBS PDF download + balance sheet
15:35  daily-scoring     — Screener → Score → Signal
15:40  daily-execution    — Risk → Approval → OTP → Orders
16:00  daily-monitoring   — Report → Telegram → Risk review
```

## Debug

### Kiểm tra MCP server

```bash
# Kiểm tra FireAnt MCP server
echo '{"jsonrpc":"2.0","id":1,"method":"initialize",
  "params":{"protocolVersion":"2024-11-05","capabilities":{},
  "clientInfo":{"name":"test","version":"1.0"}}}' \
| node mcp-server/build/index.js

# Kiểm tra DNSE MCP server (cần env vars)
DNSE_API_KEY=xxx DNSE_API_SECRET=xxx \
  node mcp-server-dnse/build/index.js
```

### Logs

Pipeline logs ra stdout với format:
```
INFO:pipeline.clients.fireant:FireAnt MCP client initialized
INFO:pipeline.ingestors.prices:Ingested 5 OHLC rows for ACB
INFO:pipeline.features.technical:Inserted 3 technical indicator rows for FPT
```

### Troubleshooting

| Vấn đề | Nguyên nhân | Giải pháp |
|---|---|---|
| `fetch failed` | FireAnt API không reachable | Kiểm tra network, proxy |
| `connect ECONNREFUSED` | PostgreSQL không chạy | Start Docker |
| `MCP process not running` | Node.js MCP server lỗi | Rebuild: `npm run build` |
| `No access_token` | FireAnt API thay đổi | Check auth.ts, update endpoint |
| `OTP required` | Cần trading token | Gọi `send_email_otp` trước |
| `relation "xxx" does not exist` | DB chưa migrate | Chạy migration script |
| `cannot find grafana/dashboards/` | Directory rỗng | Đảm bảo có ít nhất 1 dashboard JSON |
