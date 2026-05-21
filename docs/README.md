# VN30 Investment Agent — Tài liệu hệ thống

Hệ thống đầu tư tự động cho VN30 sử dụng **FireAnt MCP** (dữ liệu thị trường) và **DNSE MCP** (thực thi lệnh), được thiết kế bởi Hội đồng Đầu tư với Warren Buffett làm Chủ tịch.

## Mục lục tài liệu

| Tài liệu | Mô tả |
|---|---|
| [Kiến trúc hệ thống](architecture.md) | Thiết kế end-to-end pipeline, tech stack, data flow |
| [MVP Status](mvp-status.md) | Những gì đã xây dựng, module nào đã hoàn thành |
| [Lộ trình phát triển](roadmap.md) | Roadmap 30 ngày, 90 ngày, KPI, failure modes |
| [Chiến lược VMQ30](strategy.md) | Chiến lược đầu tư: scoring model, signal generation |
| [Quản trị rủi ro](risk-management.md) | Risk framework, position sizing, drawdown control |
| [Hướng dẫn vận hành](pipeline-guide.md) | Cách chạy pipeline, setup database, debug |

## Tổng quan nhanh

```
pipeline/               ← Python data pipeline (MVP đã hoàn thành)
├── clients/            ← FireAnt + DNSE MCP clients
├── ingestors/          ← Data ingestion (OHLC, financials, company)
├── features/           ← Technical + fundamental indicators
├── tasks/              ← Celery tasks (daily_close, daily_open)
├── db/                 ← Database models + connection
└── storage/            ← Parquet export

mcp-server/             ← FireAnt MCP server (45 tools) [có sẵn]
mcp-server-dnse/        ← DNSE MCP server (20 tools) [có sẵn]
```

## Công nghệ

- **Python 3.12+** — quantitative analysis, pipeline orchestration
- **PostgreSQL + TimescaleDB** — data storage (Supabase hoặc local Docker)
- **Redis** — Celery broker (Upstash hoặc local Docker)
- **Celery** — task scheduling
- **FireAnt API** — dữ liệu thị trường Việt Nam
- **DNSE API** — thực thi lệnh

## Hội đồng Đầu tư

| Thành viên | Vai trò |
|---|---|
| Warren Buffett | Chủ tịch — tư duy đầu tư giá trị, moat, kỷ luật vốn |
| Charlie Munger | Tư duy đa ngành, mental models, tránh ngu ngốc |
| Benjamin Graham | Biên an toàn, định giá, nguyên tắc phòng thủ |
| Ray Dalio | Chu kỳ vĩ mô, quản trị rủi ro, diversification |
| Peter Lynch | Tăng trưởng thực tế, hiểu doanh nghiệp đơn giản |
| George Soros | Phản xạ thị trường, tâm lý và dòng tiền |
| Philip Fisher | Chất lượng quản trị, tầm nhìn dài hạn |
