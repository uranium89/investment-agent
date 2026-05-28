# 🏛️ Hội Đồng Cố Vấn Đầu Tư

Bộ tài liệu tổng hợp kiến thức đầu tư từ các nhà đầu tư huyền thoại thế giới.
Mỗi nhà đầu tư có thư mục riêng và MCP server riêng, cho phép AI tham khảo từng "cố vấn" một cách độc lập.

## 👥 Thành Viên Hội Đồng

| Cố Vấn | Thư Mục | MCP Server | Chuyên Môn |
|--------|---------|------------|------------|
| **Warren Buffett** | `buffett/` | `mcp-server-buffett` | Value investing, Moat, Margin of safety |
| **Charlie Munger** | `munger/` | `mcp-server-munger` | Mental models, Inversion, Multidisciplinary thinking |

> **Thêm cố vấn mới**: Tạo thư mục `<tên>/` + copy pattern MCP server → tự động hoạt động.

---

## 📂 Cấu Trúc Thư Mục

```
knowledge/
├── README.md                    ← File này (tổng quan hội đồng)
│
├── buffett/                     ← Warren Buffett
│   ├── README.md
│   ├── 01_philosophy/           ← Triết lý đầu tư
│   ├── 02_business_analysis/    ← Phân tích doanh nghiệp & Moat
│   ├── 03_financial_analysis/   ← Phân tích tài chính
│   ├── 04_valuation/            ← Định giá nội tại
│   ├── 05_portfolio_management/ ← Quản lý danh mục
│   ├── 06_market_psychology/    ← Tâm lý thị trường
│   ├── 07_sector_analysis/      ← Phân tích ngành
│   └── 08_decision_framework/   ← Checklist & quyết định
│
└── munger/                      ← Charlie Munger
    ├── README.md
    ├── 01_philosophy/           ← Triết lý đa ngành
    ├── 02_mental_models/        ← 100+ mô hình tư duy
    ├── 03_investing_principles/ ← Nguyên tắc đầu tư
    ├── 04_decision_making/      ← Ra quyết định & checklist
    └── 05_quotes_wisdom/        ← Câu nói & bài học
```

---

## 🎯 Hướng Dẫn Sử Dụng

### Khi phân tích cổ phiếu:
1. **Góc nhìn Buffett** → Dùng `buffett_analyze_stock` — tập trung vào moat, tài chính, định giá
2. **Góc nhìn Munger** → Dùng `munger_analyze_stock` — tập trung vào mental models, inversion, incentives

### Khi nghiên cứu nguyên tắc:
- `buffett_read` → Đọc file cụ thể trong `knowledge/buffett/`
- `munger_read` → Đọc file cụ thể trong `knowledge/munger/`

---

_Cập nhật lần cuối: 2026-05-28_
