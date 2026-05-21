from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # PostgreSQL: local Docker timescale/timescaledb:2-pg16
    #     hoặc Supabase: postgresql+asyncpg://postgres.nqgmfsqnueuzxxsjwrvx:pass@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
    db_url: str = "postgresql+asyncpg://vn30:vn30_dev_only@localhost:5432/vn30_pipeline"
    db_url_sync: str = "postgresql://vn30:vn30_dev_only@localhost:5432/vn30_pipeline"

    # Redis: local hoặc Upstash Redis TCP (not HTTP API)
    #     local:   redis://localhost:6379/0
    #     Upstash: rediss://default:pass@us1-able-lion-12345.upstash.io:6379/0
    redis_url: str = "redis://localhost:6379/0"

    fireant_mcp_dir: str = str(Path(__file__).resolve().parent.parent.parent / "mcp-server")
    dnse_mcp_dir: str = str(Path(__file__).resolve().parent.parent.parent / "mcp-server-dnse")

    vn30_symbols: list[str] = [
        "ACB", "BCM", "BID", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG",
        "MBB", "MSN", "MWG", "NVL", "PDR", "PLX", "PNJ", "POW", "SAB", "SHB",
        "SSB", "SSI", "STB", "TCB", "TPB", "VCB", "VHM", "VIC", "VJC", "VNM",
        "VPB", "VRE",
    ]

    daily_close_hour: int = 15
    daily_close_minute: int = 30
    daily_open_hour: int = 8
    daily_open_minute: int = 30

    # ── DNSE Trading ──────────────────────────────────────────
    dnse_email: str = ""
    dnse_account_no: str = ""

    # ── Telegram ──────────────────────────────────────────────
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # ── Risk Management ───────────────────────────────────────
    max_drawdown_pct: float = 15.0
    black_swan_threshold_pct: float = -5.0
    max_sector_finance_pct: float = 40.0
    max_sector_realestate_pct: float = 20.0
    max_single_position_pct: float = 10.0
    min_cash_pct: float = 25.0

    # ── Human-in-loop ─────────────────────────────────────────
    approval_required: bool = True
    approval_timeout_minutes: int = 60

    telemetry_enabled: bool = False
    log_level: str = "INFO"

    model_config = {"env_prefix": "PIPELINE_", "env_file": ".env", "extra": "ignore"}


settings = Settings()
