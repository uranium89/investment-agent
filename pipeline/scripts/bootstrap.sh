#!/usr/bin/env bash
set -euo pipefail

echo "╔══════════════════════════════════════════════════╗"
echo "║       VN30 Pipeline — Bootstrap                  ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ── Parse arguments ──────────────────────────────────
DB_MODE="${1:-auto}"   # auto, local, supabase, skip-db
REDIS_MODE="${2:-auto}" # auto, local, upstash, skip-redis

# ── Prerequisites ─────────────────────────────────────
echo "[1/4] Kiểm tra prerequisites..."
command -v node  >/dev/null 2>&1 || { echo "  ❌ Node.js required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "  ❌ Python 3.12+ required"; exit 1; }

NODE_VER=$(node -v | cut -d. -f1 | tr -d 'v')
PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "  Node.js $NODE_VER  |  Python $PYTHON_VER"

AVAILABLE_PYTHON=$(python3 -c '
import sys
if sys.version_info >= (3, 12):
    print("ok")
else:
    print("need 3.12+")
' 2>/dev/null || echo "need 3.12+")
if [ "$AVAILABLE_PYTHON" != "ok" ]; then
    # try homebrew python3.12
    if command -v /opt/homebrew/bin/python3.12 >/dev/null 2>&1; then
        alias python3=/opt/homebrew/bin/python3.12
        echo "  Using homebrew Python 3.12"
    else
        echo "  ⚠️  Python 3.12+ recommended (found $PYTHON_VER)"
    fi
fi

# ── Build MCP servers ────────────────────────────────
echo "[2/4] Build MCP servers..."
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SCRIPT_DIR"

for dir in mcp-server mcp-server-dnse; do
    if [ -f "$dir/package.json" ]; then
        echo "  Building $dir..."
        (cd "$dir" && npm install --silent && npm run build) 2>/dev/null
    fi
done
echo "  ✅ MCP servers ready"

# ── Python setup ─────────────────────────────────────
echo "[3/4] Cài đặt Python package..."
cd "$SCRIPT_DIR"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --quiet -e .
echo "  ✅ Python package installed"

# ── Database setup ───────────────────────────────────
echo "[4/4] Database setup..."

if [ "$DB_MODE" = "skip-db" ]; then
    echo "  ⏭️  Skipping database setup"
elif [ "$DB_MODE" = "supabase" ] || ([ "$DB_MODE" = "auto" ] && command -v supabase >/dev/null 2>&1); then
    echo "  Using Supabase..."
    if [ -f .env ]; then
        source .env
    fi
    if [ -n "${PIPELINE_DB_URL:-}" ]; then
        echo "  DB_URL from .env"
        echo "  ${PIPELINE_DB_URL:0:50}..."
        python3 -c "
import asyncio
from pipeline.db.connection import engine
async def run():
    async with engine.begin() as conn:
        await conn.run_sync(__import__('pipeline.db.models', fromlist=['Base']).Base.metadata.create_all)
    await engine.dispose()
    print('  ✅ Schema created')
asyncio.run(run())
"
    else:
        echo "  ⚠️  PIPELINE_DB_URL not set. Set it in .env and re-run."
        echo "     VD: PIPELINE_DB_URL=postgresql+asyncpg://postgres:pass@db.xxx.supabase.co:5432/postgres"
    fi
elif [ "$DB_MODE" = "local" ] || ([ "$DB_MODE" = "auto" ] && command -v docker >/dev/null 2>&1); then
    echo "  Starting local Docker PostgreSQL + TimescaleDB..."
    if docker info >/dev/null 2>&1; then
        docker compose up -d postgres
        sleep 5
        echo "  Running migrations..."
        source .venv/bin/activate
        python3 -c "
import asyncio
from pipeline.db.connection import engine
async def run():
    async with engine.begin() as conn:
        await conn.run_sync(__import__('pipeline.db.models', fromlist=['Base']).Base.metadata.create_all)
    await engine.dispose()
    print('  ✅ Schema created')
asyncio.run(run())
"
    else
        echo "  ⚠️  Docker not running. Set .env and use Supabase instead."
        echo "     PIPELINE_DB_URL=postgresql+asyncpg://..."
    fi
else
    echo "  ⚠️  No database configured. Set PIPELINE_DB_URL in .env"
fi

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║       Bootstrap hoàn tất                          ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Các lệnh hữu ích:"
echo ""
echo "  Chạy pipeline (cron manual):"
echo "    cd pipeline && source .venv/bin/activate"
echo "    python -m pipeline.tasks.daily_close"
echo ""
echo "  Cấu hình cloud (recommended):"
echo "    cp .env.example .env"
echo "    # Điền Supabase URL + Upstash Redis URL vào .env"
echo ""
echo "  Cấu hình local Docker (alternate):"
echo "    docker compose --profile local-db up -d"
echo "    ./scripts/bootstrap.sh local auto"
echo ""
