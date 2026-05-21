# Hướng dẫn vận hành Pipeline

## Yêu cầu

- Python 3.12+
- Node.js v22+
- PostgreSQL + TimescaleDB (Supabase hoặc local Docker)
- Redis (Upstash hoặc local Docker)

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
# Sửa .env với connection strings của bạn
```

### 2. Build MCP servers

```bash
(cd mcp-server && npm install && npm run build)
(cd mcp-server-dnse && npm install && npm run build)
```

### 3. Setup database

**Option A: Supabase (recommended)**
```bash
# Tạo project trên supabase.com
# Enable TimescaleDB: CREATE EXTENSION IF NOT EXISTS timescaledb;
# Lấy connection string từ Settings → Database
# Điền vào .env: PIPELINE_DB_URL
```

**Option B: Local Docker**
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

### 5. Chạy manual pipeline

```bash
cd pipeline
source .venv/bin/activate
python -m pipeline.tasks.daily_close
```

## Cấu trúc .env

```env
# Database
PIPELINE_DB_URL=postgresql+asyncpg://user:pass@host:5432/db
PIPELINE_DB_URL_SYNC=postgresql://user:pass@host:5432/db

# Redis (cho Celery)
PIPELINE_REDIS_URL=rediss://default:pass@host.upstash.io:6379/0

# MCP servers (đường dẫn tuyệt đối hoặc relative)
PIPELINE_FIREANT_MCP_DIR=../mcp-server
PIPELINE_DNSE_MCP_DIR=../mcp-server-dnse

# Logging
PIPELINE_LOG_LEVEL=INFO
```

## Cách test FireAnt connection

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
# Chạy Celery worker (nếu dùng Redis)
celery -A pipeline.tasks.celery_app worker --loglevel=info

# Chạy manual ingestion cho 1 symbol
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
| `connect ECONNREFUSED` | PostgreSQL không chạy | Start Docker hoặc check Supabase |
| `MCP process not running` | Node.js MCP server lỗi | Rebuild: `npm run build` |
| `No access_token` | FireAnt API thay đổi | Check auth.ts, update endpoint |
| `OTP required` | Cần trading token | Gọi `send_email_otp` trước |
