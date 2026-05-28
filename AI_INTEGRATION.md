# 🤖 Investment Agent — Hướng Dẫn Tích Hợp AI

## Kiến Trúc Tổng Quan

```
┌──────────────────────────────────────────────────────────────────┐
│              AI (Claude / Gemini / GPT)                          │
├──────────────────────────────────────────────────────────────────┤
│  CLAUDE.md → System prompt: "Mô phỏng Hội Đồng Cố Vấn Đầu Tư"  │
├─────────────────┬────────────────┬──────────────────────────────┤
│   Fireant MCP   │   DNSE MCP     │  🏛️ Hội Đồng Cố Vấn          │
│   (48+ tools)   │  (giá, orders) │                              │
│   - BCTC        │  - OHLCV       │  🎩 Buffett (Chủ Tọa)        │
│   - Chỉ số TC   │  - Khớp lệnh   │     buffett_*  tools         │
│   - Tin tức     │  - Đặt lệnh    │                              │
│                 │                │  🧠 Munger (Cố Vấn)          │
│                 │                │     munger_* tools            │
└─────────────────┴────────────────┴──────────────────────────────┘
```

---

## Cách Hoạt Động — Phiên Họp Hội Đồng

Khi người dùng yêu cầu phân tích cổ phiếu, AI **không phân tích đơn độc** mà tổ chức một phiên họp hội đồng:

```
Người dùng: "Phân tích VCB"

AI (với tư cách hội đồng):
  1. Thu thập dữ liệu: fireant_* + dnse_* tools
  2. Mở phiên họp:
     🎩 Buffett: "Tôi thấy moat của VCB rất mạnh ở CASA..."
     🧠 Munger: "Hãy đảo ngược — điều gì sẽ phá hủy khoản đầu tư này?"
     🗳️ Biểu quyết: Buffett → MUA | Munger → THEO DÕI (với điều kiện)
  3. Phân tích kỹ thuật: Scorecard 56 điểm, tài chính, định giá
  4. Kết luận: Buffett (Chủ Tọa) ra phán quyết chính thức
```

---

## Cài Đặt MCP Servers

### Build tất cả từ root

```bash
npm install
npm run build
```

### Cấu Hình Claude Desktop

Mở: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fireant": {
      "command": "node",
      "args": ["/absolute/path/to/investment-agent/mcp-server/build/index.js"]
    },
    "dnse": {
      "command": "node",
      "args": ["/absolute/path/to/investment-agent/mcp-server-dnse/build/index.js"],
      "env": {
        "DNSE_API_KEY": "your-key",
        "DNSE_API_SECRET": "your-secret"
      }
    },
    "buffett": {
      "command": "node",
      "args": ["/absolute/path/to/investment-agent/mcp-server-buffett/build/index.js"]
    },
    "munger": {
      "command": "node",
      "args": ["/absolute/path/to/investment-agent/mcp-server-munger/build/index.js"]
    }
  }
}
```

---

## Tools Theo Từng Server

### 🎩 Buffett MCP Server (`mcp-server-buffett`)

| Tool | Mô Tả | Khi Dùng |
|------|-------|----------|
| `buffett_list` | Liệt kê tất cả knowledge files | Khám phá knowledge base |
| `buffett_read` | Đọc bất kỳ file knowledge nào | Tham khảo chi tiết |
| `buffett_analyze_stock` | Framework phân tích + council format | Bắt đầu phiên họp hội đồng |
| `buffett_sector_guide` | Hướng dẫn ngành | Phân tích ngành cụ thể |
| `buffett_valuation_guide` | Phương pháp định giá | Tính intrinsic value |

### 🧠 Munger MCP Server (`mcp-server-munger`)

| Tool | Mô Tả | Khi Dùng |
|------|-------|----------|
| `munger_list` | Liệt kê tất cả knowledge files | Khám phá Munger knowledge |
| `munger_read` | Đọc bất kỳ file knowledge nào | Tham khảo chi tiết |
| `munger_analyze_stock` | Framework Munger (inversion-first) | Cross-check với Buffett |
| `munger_mental_models` | Mental models theo ngành | psychology/physics/economics/math/biology |
| `munger_checklist` | Checklist đầy đủ Munger | Bias check + mistake avoidance |

---

## Ví Dụ Tương Tác

### Phân Tích Cổ Phiếu (Hội Đồng)

```
Người dùng: "Hội đồng hãy phân tích VCB"

→ buffett_analyze_stock({ symbol: "VCB" })  ← Load council format
→ fireant_fundamental("VCB")
→ fireant_financial_data("VCB")
→ fireant_company_profile("VCB")
→ fireant_holders("VCB")
→ Tổ chức phiên họp → Output: Phiên Họp Hội Đồng đầy đủ
```

### Hỏi Về Mental Model

```
Người dùng: "Munger giải thích về inversion trong đầu tư"

→ munger_read('03_investing_principles/inversion_in_investing.md')
→ Trả lời bằng giọng Munger, có trích dẫn quote gốc
```

### Đánh Giá Danh Mục

```
Người dùng: "Danh mục: VCB 30%, FPT 25%, VNM 20%, Cash 25%"

→ buffett_read('05_portfolio_management/concentration_strategy.md')
→ munger_checklist()
→ Phân tích từng cổ phiếu nhanh theo hội đồng
→ Buffett kết luận phân bổ có hợp lý không
```

---

## Cập Nhật Knowledge Base

Thêm file `.md` mới vào `knowledge/buffett/` hoặc `knowledge/munger/` → AI tự động nhận ra, không cần rebuild.

```bash
# Ví dụ: thêm bài học về Buffett và Coca-Cola
echo "# Buffett & Coca-Cola" > knowledge/buffett/01_philosophy/coca_cola_case.md
```

---

## Cấu Trúc Files

```
investment-agent/
├── CLAUDE.md                    ← 🤖 System prompt (tự động load)
├── AI_INTEGRATION.md            ← 📖 File này
├── CONTRIBUTING.md              ← 🔧 Hướng dẫn phát triển
├── AGENTS.md                    ← ⚙️ Operational notes
│
├── knowledge/
│   ├── README.md                ← Tổng quan Hội Đồng Cố Vấn
│   ├── buffett/                 ← 🎩 Warren Buffett (22 files)
│   │   └── 08_decision_framework/
│   │       └── council_debate_format.md  ← 🏛️ Format phiên họp
│   └── munger/                  ← 🧠 Charlie Munger (16 files)
│
├── mcp-server/                  ← 🔌 Fireant API
├── mcp-server-dnse/             ← 🔌 DNSE API (giá, giao dịch)
├── mcp-server-buffett/          ← 🎩 Buffett knowledge server
└── mcp-server-munger/           ← 🧠 Munger knowledge server
```
