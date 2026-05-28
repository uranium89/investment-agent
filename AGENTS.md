# AGENTS.md — Repo Quickstart

## What this is

**Hội Đồng Cố Vấn Đầu Tư** — 4 MCP servers + knowledge base cho nhiều nhà đầu tư huyền thoại. `CLAUDE.md` là system prompt chính; file này mô tả cấu trúc vận hành.

Khi phân tích cổ phiếu, AI **mô phỏng một phiên họp hội đồng** với Buffett làm chủ tọa và Munger làm cố vấn tư duy. Mỗi thành viên tranh luận độc lập trước khi Buffett ra phán quyết cuối cùng.

## Build các MCP servers

```bash
# Cài đặt và build toàn bộ dự án từ root
npm install
npm run build
```

Có 4 MCP servers (tất cả dùng `tsc`, output là `build/index.js`, ESM `"type": "module"`):

| Server | Mục đích | Knowledge Dir |
|--------|----------|---------------|
| `mcp-server` | Fireant API (dữ liệu thị trường) | n/a |
| `mcp-server-dnse` | DNSE OpenAPI (OHLCV, orders) | n/a |
| `mcp-server-buffett` | Knowledge Warren Buffett | `knowledge/buffett/` |
| `mcp-server-munger` | Knowledge Charlie Munger | `knowledge/munger/` |

## Environment (DNSE only)

DNSE server requires env vars. Without them, OHLC/trades/orders tools will fail with a configuration error instead of crashing the server on startup:

| Var                | Required                                       |
| ------------------ | ---------------------------------------------- |
| `DNSE_API_KEY`     | yes                                            |
| `DNSE_API_SECRET`  | yes                                            |
| `DNSE_BASE_URL`    | no (defaults to `https://openapi.dnse.com.vn`) |
| `DNSE_API_VERSION` | no (defaults to `2026-05-07`)                  |

The Fireant server needs no auth — it uses anonymous access.

## Data quality notes

**Dividends:** Do NOT use `fireant_fireant_fundamental` for dividend data — its `dividend`/`dividendYield` fields are unreliable (often 0). Always use `fireant_fireant_dividends` instead, which returns full yearly history (`cashDividend`, `stockDividend`).

**TCBS one-click reports:** TCBS provides PDF company reports at `https://static.tcbs.com.vn/oneclick/{symbol}.pdf` (e.g. `https://static.tcbs.com.vn/oneclick/ACB.pdf`). Includes financial statements, ratios, ownership, valuation. Use `webfetch` to read.

## Lint, Typecheck, and Formatting Scripts

The project has integrated code quality tooling at the root level:

- Run `npm run typecheck` to verify TypeScript types.
- Run `npm run lint` to execute ESLint on all code files.
- Run `npm run format` to auto-format all code with Prettier.

The only aux script is `npm run test-fetch` in `mcp-server/`. If you add code, always run the quality check commands from the root workspace before publishing.

## Mandatory analysis rules (bắt buộc)

Khi phân tích bất kỳ cổ phiếu nào, output **BẮT BUỘC** là format **Phiên Họp Hội Đồng Cố Vấn** (đọc `buffett_read('08_decision_framework/council_debate_format.md')`).

### Cấu trúc phiên họp bắt buộc:

1. 🎩 **Buffett (Chủ Tọa)** — Nhận xét về moat, lãnh đạo, doanh nghiệp
2. 🧠 **Munger (Cố Vấn)** — Inversion + Incentive check + Bias detection
3. 🗳️ **Biểu quyết sơ bộ** — Từng thành viên MUA/THEO DÕI/TRÁNH
4. 📊 **Phân tích kỹ thuật** — Scorecard 56 điểm + Tài chính 5 năm + Định giá
5. ⚠️ **Red Flags** — Buffett + Munger cùng phát hiện
6. 🔨 **Phán quyết Buffett** — Kết luận cuối cùng của Chủ Tọa

### 8 tiêu chí nội dung (không được bỏ sót):

1. **Hiểu doanh nghiệp** — mô hình kinh doanh, khách hàng, đối thủ
2. **Lợi thế cạnh tranh (Moat)** — brand, switching cost, network effect, cost advantage
3. **Ban lãnh đạo** — insider ownership, năng lực, tính trung thực, related-party
4. **Tài chính 5 năm** — ROE, ROIC, biên lợi nhuận, FCF, nợ
5. **Định giá** — P/E, P/B, P/FCF, PEG, so sánh ngành
6. **Rủi ro & Red flags** — `buffett_read('08_decision_framework/red_flags.md')` + Munger inversion
7. **Biên an toàn (Margin of Safety)** — giá hiện tại so với giá trị nội tại
8. **Kết luận & Khuyến nghị** — điểm tổng /56, MUA/THEO DÕI/TRÁNH

**Quy tắc cứng (hard rule):**

- Nếu thiếu dữ liệu → **phải hỏi user hoặc tự đi tìm (web search, webfetch, gọi tool)**
- **Không được tự đoán**, không suy luận từ dữ liệu không có
- Phải check web để tìm rủi ro định tính (sân sau, BĐS tập trung, scandal, related-party)
- Munger **phải chạy inversion** — đây là bước không thể bỏ qua
- Kết luận cuối cùng phải do **Buffett (Chủ Tọa)** đưa ra

## Knowledge base

`knowledge/` chứa knowledge của từng nhà đầu tư:

- `knowledge/buffett/` — ~21 files across 8 subdirectories (Buffett framework)
- `knowledge/munger/` — ~16 files across 5 subdirectories (Munger mental models)
- `knowledge/reports/` — **Second Brain** — báo cáo phân tích đã lưu (tự động tạo khi dùng tools)

```
knowledge/reports/
├── index.json        ← Index tự động (metadata tất cả báo cáo)
├── MBB/
│   ├── 2026-05-28.md  ← Báo cáo với YAML frontmatter
│   └── 2026-03-15.md
└── VCB/
    └── 2026-05-20.md
```

**Cấu trúc mỗi báo cáo** (YAML frontmatter tự động thêm bởi `buffett_save_report`):
```yaml
---
symbol: MBB
company: Ngân hàng Quân Đội
date: 2026-05-28
price: 22400
verdict: THEO_DOI
score: 38
sector: banking
tags: [banking, state-owned, CASA]
---
```

**4 MCP tools Second Brain** (trong `mcp-server-buffett`):

| Tool | Mục đích |
|------|----------|
| `buffett_save_report` | Lưu báo cáo sau khi phân tích |
| `buffett_list_reports` | Liệt kê + filter theo symbol/verdict/sector |
| `buffett_read_report` | Đọc lại báo cáo (mới nhất hoặc theo ngày) |
| `buffett_search_reports` | Tìm kiếm keyword trong toàn bộ Second Brain |

MCP servers đọc files này tại runtime. Thêm/sửa file `.md` có hiệu lực ngay lập tức, không cần rebuild.

**Báo cáo Second Brain** (`knowledge/reports/`) được tự động tạo/cập nhật bởi `buffett_save_report`. Chúng có thể commit vào git để lưu trữ lịch sử phân tích.

**Thêm nhà đầu tư mới** (ví dụ: Peter Lynch):
1. Tạo `knowledge/lynch/` với các file `.md`
2. Copy `mcp-server-munger/` → `mcp-server-lynch/`, đổi `MUNGER` → `LYNCH` trong env var và server name
3. Thêm vào `workspaces` trong root `package.json`
4. Chạy `npm install && npm run build`

## Important: CLAUDE.md is the system prompt

`CLAUDE.md` is auto-loaded by Claude and defines:
- Vai trò AI (Hội Đồng Cố Vấn với Buffett làm Chủ Tọa)
- Mapping: Câu hỏi → Tool/File knowledge tương ứng
- Quy trình phiên họp hội đồng bắt buộc
- Bảng tiêu chuẩn đánh giá nhanh (Buffett Scorecard)

If you are asked to modify behavior → edit `CLAUDE.md`.
If you are asked to modify the council format → edit `knowledge/buffett/08_decision_framework/council_debate_format.md`.
AGENTS.md is for operational notes only.
