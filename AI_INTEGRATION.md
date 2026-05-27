# 🤖 Investment Agent — Hướng Dẫn Tích Hợp AI

## Kiến Trúc Tổng Quan

```
┌─────────────────────────────────────────────────────────────┐
│                    AI (Claude / Gemini / GPT)                │
├─────────────────────────────────────────────────────────────┤
│  CLAUDE.md → System prompt / Vai trò & hướng dẫn           │
├──────────────────────┬──────────────────────────────────────┤
│   Fireant MCP        │    DNSE MCP                          │
│   (48+ tools)        │    (giá real-time, portfolio)        │
│   - Dữ liệu BCTC     │    - OHLCV                          │
│   - Chỉ số tài chính │    - Giá khớp lệnh                  │
│   - Tin tức, posts   │    - Lệnh đặt (auth)                │
├──────────────────────┴──────────────────────────────────────┤
│   Warren Buffett Knowledge Tools (buffett_*)                │
│   - buffett_knowledge_list   → Xem danh sách files         │
│   - buffett_knowledge_read   → Đọc bất kỳ file nào         │
│   - buffett_analyze_stock    → Framework phân tích cổ phiếu │
│   - buffett_sector_guide     → Hướng dẫn phân tích ngành   │
│   - buffett_valuation_guide  → Phương pháp định giá        │
├─────────────────────────────────────────────────────────────┤
│   knowledge/ directory (21 files, 4200+ lines)              │
│   → Toàn bộ kiến thức Warren Buffett                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Cách AI Tự Động Hiểu Project

### 1. CLAUDE.md (Tự Động Load)

**File [`CLAUDE.md`](./CLAUDE.md) được Claude đọc tự động** khi bạn mở project trong Claude Code/Desktop.

Nó chứa:
- Vai trò của AI (trợ lý đầu tư theo Buffett)
- Mapping: Câu hỏi → File knowledge tương ứng
- Quy trình phân tích chuẩn 5 bước
- Bảng tiêu chuẩn đánh giá nhanh
- Template kết quả chuẩn

**AI platform khác** (Cursor, Windsurf, v.v.) cũng đọc `CLAUDE.md` hoặc file tương đương.

---

### 2. MCP Tools — Buffett Knowledge (Tự Động)

Khi MCP server được kết nối, AI có thể **gọi tools** để đọc knowledge base:

```
AI: "Phân tích VCB cho tôi"
  → Gọi: buffett_analyze_stock({ symbol: "VCB" })
  → Nhận: Full checklist + tiêu chuẩn + hướng dẫn thu thập data
  → Gọi: fireant_fundamental({ symbol: "VCB" })
  → Gọi: fireant_financial_data({ symbol: "VCB" })
  → Gọi: fireant_holders({ symbol: "VCB" })
  → Tổng hợp → Đưa ra phân tích theo Buffett framework
```

---

## Cài Đặt MCP Server

### Build

```bash
cd mcp-server
npm install
npm run build
```

### Cấu Hình Claude Desktop

Mở file: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "investment-agent": {
      "command": "node",
      "args": ["/Users/vinhpham/Documents/Github/investment-agent/mcp-server/build/index.js"]
    },
    "dnse": {
      "command": "node",
      "args": ["/Users/vinhpham/Documents/Github/investment-agent/mcp-server-dnse/build/index.js"]
    }
  }
}
```

### Cấu Hình cho AI IDE khác (Cursor, Windsurf, Zed)

```json
{
  "mcpServers": {
    "investment-agent": {
      "command": "node",
      "args": ["./mcp-server/build/index.js"]
    }
  }
}
```

---

## Các Tool Mới — Buffett Knowledge

| Tool | Mô Tả | Khi Dùng |
|------|--------|---------|
| `buffett_knowledge_list` | Liệt kê tất cả files | Khám phá knowledge base |
| `buffett_knowledge_read` | Đọc bất kỳ file nào | Tham khảo nội dung cụ thể |
| `buffett_analyze_stock` | Framework phân tích + checklist | Bắt đầu phân tích cổ phiếu |
| `buffett_sector_guide` | Hướng dẫn ngành | Phân tích ngành cụ thể |
| `buffett_valuation_guide` | Phương pháp định giá | Tính intrinsic value |

---

## Ví Dụ Tương Tác Với AI

### Phân Tích Cổ Phiếu Đơn Lẻ

```
Người dùng: "Phân tích VCB theo phong cách Warren Buffett"

AI sẽ:
1. Gọi buffett_analyze_stock({ symbol: "VCB" }) → nhận framework
2. Gọi fireant_fundamental("VCB") → P/E, P/B, ROE, v.v.
3. Gọi fireant_financial_data("VCB") → BCTC chi tiết
4. Gọi fireant_company_profile("VCB") → mô tả doanh nghiệp
5. Gọi fireant_holders("VCB") → cơ cấu cổ đông
6. Đối chiếu với tiêu chuẩn Buffett → Chấm điểm
7. Tính giá trị nội tại và biên an toàn
8. Kết luận: MUA/THEO DÕI/TRÁNH với lý do cụ thể
```

### Tìm Cổ Phiếu Tốt

```
Người dùng: "Tìm cổ phiếu tốt theo tiêu chí Buffett"

AI sẽ:
1. Đọc buffett_sector_guide() → biết ngành nào ưu tiên
2. Gọi fireant_screener với tiêu chí: ROE>15%, D/E<1.5
3. Lọc và xếp hạng theo Buffett framework
4. Đề xuất top 3-5 cổ phiếu để phân tích sâu
```

### Đánh Giá Danh Mục

```
Người dùng: "Danh mục của tôi: VCB 30%, FPT 25%, VNM 20%, MSN 15%, Cash 10%"

AI sẽ:
1. Đọc buffett_knowledge_read("05_portfolio_management/concentration_strategy.md")
2. Phân tích từng cổ phiếu nhanh
3. Đánh giá tổng thể danh mục (đủ tập trung? ngành? tỷ trọng?)
4. Đề xuất điều chỉnh nếu cần
```

---

## Cấu Trúc Files

```
investment-agent/
├── CLAUDE.md                    ← 🤖 AI đọc file này tự động (system prompt)
├── AI_INTEGRATION.md            ← 📖 File này
│
├── knowledge/                   ← 📚 Warren Buffett knowledge base
│   ├── README.md
│   ├── 01_philosophy/           ← Triết lý đầu tư
│   ├── 02_business_analysis/    ← Phân tích doanh nghiệp
│   ├── 03_financial_analysis/   ← Phân tích tài chính
│   ├── 04_valuation/            ← Định giá
│   ├── 05_portfolio_management/ ← Quản lý danh mục
│   ├── 06_market_psychology/    ← Tâm lý thị trường
│   ├── 07_sector_analysis/      ← Phân tích ngành
│   └── 08_decision_framework/   ← Framework quyết định
│
├── mcp-server/                  ← 🔌 MCP server (Fireant + Buffett tools)
│   └── src/tools/
│       ├── symbols.ts           ← Fireant stock tools
│       ├── icb.ts               ← Industry tools
│       ├── knowledge.ts         ← ✨ Buffett knowledge tools (MỚI)
│       └── ...
│
└── mcp-server-dnse/             ← 🔌 DNSE MCP server (giá real-time)
```

---

## Cập Nhật Knowledge Base

Để thêm kiến thức mới:

```bash
# Thêm file mới vào thư mục phù hợp
echo "# Nội dung mới" > knowledge/01_philosophy/new_topic.md

# AI sẽ tự động nhận ra file qua buffett_knowledge_list tool
```

Không cần rebuild MCP server — knowledge tools đọc file trực tiếp.
