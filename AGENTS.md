# AGENTS.md — Repo Quickstart

## What this is

Two MCP servers + a Buffett knowledge base. The `CLAUDE.md` is the primary system prompt; this file covers operational and structural facts.

## Build both MCP servers

```bash
cd mcp-server     && npm install && npm run build
cd mcp-server-dnse && npm install && npm run build
```

Both use `tsc` only (no other build tool). Output: `build/index.js`. Both are ESM (`"type": "module"`).

## Environment (DNSE only)

DNSE server requires env vars. Without them, OHLC/trades/orders tools will fail:

| Var | Required |
|---|---|
| `DNSE_API_KEY` | yes |
| `DNSE_API_SECRET` | yes |
| `DNSE_BASE_URL` | no (defaults to `https://openapi.dnse.com.vn`) |
| `DNSE_API_VERSION` | no (defaults to `2026-05-07`) |

The Fireant server needs no auth — it uses anonymous access.

## Data quality notes

**Dividends:** Do NOT use `fireant_fireant_fundamental` for dividend data — its `dividend`/`dividendYield` fields are unreliable (often 0). Always use `fireant_fireant_dividends` instead, which returns full yearly history (`cashDividend`, `stockDividend`).

**TCBS one-click reports:** TCBS provides PDF company reports at `https://static.tcbs.com.vn/oneclick/{symbol}.pdf` (e.g. `https://static.tcbs.com.vn/oneclick/ACB.pdf`). Includes financial statements, ratios, ownership, valuation. Use `webfetch` to read.

## No tests, no lint, no typecheck scripts

There is no test framework, linter, formatter, or typecheck command in either package. The only aux script is `npm run test-fetch` in `mcp-server/`. If you add code, at minimum run `npm run build` (which runs tsc) to verify it compiles.

## Mandatory analysis rules (bắt buộc)

Khi phân tích bất kỳ cổ phiếu nào, phải lướt qua toàn bộ 8 tiêu chí Buffett, không được bỏ sót:

1. **Hiểu doanh nghiệp** — mô hình kinh doanh, khách hàng, đối thủ
2. **Lợi thế cạnh tranh (Moat)** — brand, switching cost, network effect, cost advantage
3. **Ban lãnh đạo** — insider ownership, năng lực, tính trung thực, related-party transactions
4. **Tài chính 5 năm** — ROE, ROIC, biên lợi nhuận, FCF, nợ
5. **Định giá** — P/E, P/B, P/FCF, PEG, so sánh ngành
6. **Rủi ro & Red flags** — kiểm tra toàn bộ `knowledge/08_decision_framework/red_flags.md`, đặc biệt: related-party transactions ("sân sau"), tập trung cho vay BĐS, nợ xấu tiềm ẩn, insider trading
7. **Biên an toàn (Margin of Safety)** — giá hiện tại so với giá trị nội tại
8. **Kết luận & Khuyến nghị** — điểm tổng /56, MUA/THEO DÕI/TRÁNH

**Quy tắc cứng (hard rule):**
- Nếu thiếu dữ liệu cho bất kỳ tiêu chí nào → **phải hỏi user hoặc tự đi tìm (web search, webfetch, gọi tool)**
- **Không được tự đoán**, không suy luận từ dữ liệu không có
- Phải check web để tìm rủi ro định tính (sân sau, BĐS tập trung, scandal, related-party) — không chỉ dựa vào số Fireant
- Kết luận cuối cùng phải phản ánh đầy đủ cả 8 tiêu chí, điểm mạnh lẫn điểm yếu

## Knowledge base

`knowledge/` contains ~21 Markdown files across 8 subdirectories, organized by Buffett topic. The MCP server reads these at runtime — adding or editing a file takes effect immediately. No rebuild needed.

## Important: CLAUDE.md is the system prompt

`CLAUDE.md` is auto-loaded by Claude and defines the agent's role, knowledge mapping, analysis workflow, scoring criteria, and response template. If you are asked to modify behavior, that is the file to change. AGENTS.md is for operational notes only.
