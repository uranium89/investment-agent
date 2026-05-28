# 🤖 AI Investment Agent — Hệ Thống Cố Vấn Đầu Tư Chứng Khoán Việt Nam

AI Investment Agent là một hệ thống tác tử AI thông minh được thiết kế đặc biệt cho thị trường chứng khoán Việt Nam. Dự án mô phỏng một **Hội Đồng Cố Vấn Đầu Tư** với những bộ óc vĩ đại nhất lịch sử (Warren Buffett, Charlie Munger), giúp tự động hóa quá trình thu thập dữ liệu, phân tích cơ bản, đánh giá doanh nghiệp và định giá cổ phiếu.

## 🌟 Tính Năng Nổi Bật

- **Mô phỏng Hội Đồng Cố Vấn Đầu Tư**: 
  - **Warren Buffett**: Đóng vai trò chủ tọa, đánh giá lợi thế cạnh tranh, chất lượng doanh nghiệp, định giá (DCF, Margin of Safety) và ra quyết định cuối cùng.
  - **Charlie Munger**: Đóng vai trò cố vấn tư duy, sử dụng các mô hình tư duy (Mental Models), phương pháp Inversion (Tư duy ngược) để tìm ra các rủi ro tiềm ẩn.
- **Tích hợp Dữ Liệu Thời Gian Thực**: Kết nối với các nguồn dữ liệu chứng khoán Việt Nam thông qua kiến trúc MCP (Model Context Protocol).
- **Hệ Thống Tri Thức (Knowledge Base) Đồ Sộ**: Lưu trữ các triết lý đầu tư, phương pháp định giá, và phân tích chuyên sâu về từng ngành nghề (Ngân hàng, Sữa, Thép, Bán lẻ,...).
- **Second Brain**: Hệ thống tự động lưu trữ và tra cứu các báo cáo phân tích cũ để đánh giá lại danh mục khi cần thiết.

## 🏗️ Cấu Trúc Dự Án (Monorepo)

Dự án được xây dựng theo kiến trúc Monorepo, bao gồm nhiều MCP servers độc lập:

- **`mcp-server` (Fireant MCP)**: Cung cấp 48+ công cụ (tools) để lấy dữ liệu từ Fireant (thông tin công ty, báo cáo tài chính, lịch sử giá, tin tức, cổ đông...).
- **`mcp-server-dnse` (DNSE MCP)**: Kết nối với DNSE để lấy dữ liệu thị trường (OHLC, khớp lệnh) và quản lý danh mục/đặt lệnh.
- **`mcp-server-buffett`**: Cung cấp kiến thức về phương pháp đầu tư của Warren Buffett và hệ thống lưu trữ báo cáo (Second Brain).
- **`mcp-server-munger`**: Cung cấp 100+ mô hình tư duy (Mental Models) và checklist đầu tư của Charlie Munger.
- **`mcp-server-industry`**: Cung cấp kiến thức phân tích chuyên sâu về các ngành công nghiệp tại Việt Nam.
- **`knowledge/`**: Thư mục chứa các tệp tin Markdown về triết lý đầu tư, phương pháp đánh giá và kiến thức ngành.

## 🚀 Cài Đặt & Khởi Chạy

### Yêu cầu hệ thống
- Node.js (phiên bản hỗ trợ type module)
- npm

### Các bước cài đặt

1. **Cài đặt các dependencies cho toàn bộ dự án:**
   ```bash
   npm run install:all
   ```
   *Hoặc chạy `npm install` ở thư mục gốc.*

2. **Build toàn bộ các MCP Servers:**
   ```bash
   npm run build
   ```

3. **Kiểm tra lỗi (Linting & Type Check):**
   ```bash
   npm run lint
   npm run typecheck
   ```

## 🔌 Cấu Hình MCP (Model Context Protocol)

Hệ thống cung cấp file `mcp.json` ở thư mục gốc để tích hợp dễ dàng với các AI Clients (như Claude Desktop, Cursor,...). Bạn có thể thêm cấu hình này vào client của mình:

```json
{
  "mcpServers": {
    "fireant-mcp": {
      "type": "local",
      "command": ["node", "mcp-server/build/index.js"]
    },
    "dnse-mcp": {
      "type": "local",
      "command": ["node", "mcp-server-dnse/build/index.js"]
    },
    "buffett-mcp": {
      "type": "local",
      "command": ["node", "mcp-server-buffett/build/index.js"]
    },
    "munger-mcp": {
      "type": "local",
      "command": ["node", "mcp-server-munger/build/index.js"]
    },
    "industry-mcp": {
      "type": "local",
      "command": ["node", "mcp-server-industry/build/index.js"]
    }
  }
}
```

## 🛠️ Công Nghệ Sử Dụng

- **TypeScript / Node.js**: Ngôn ngữ và môi trường chạy chính.
- **Model Context Protocol (MCP)**: Kiến trúc tiêu chuẩn giúp AI giao tiếp với các công cụ (tools) và dữ liệu bên ngoài.
- **npm workspaces**: Quản lý kiến trúc monorepo.
- **ESLint & Prettier**: Đảm bảo chất lượng và định dạng mã nguồn.

## 🤝 Hướng Dẫn Đóng Góp

Vui lòng tham khảo file `CONTRIBUTING.md` để biết thêm chi tiết về cách thức tham gia phát triển, viết thêm Knowledge Base ngành, hoặc bổ sung các MCP Tools mới. Cùng xem qua file `CLAUDE.md` để nắm rõ các quy tắc cứng của hệ thống phân tích này.
