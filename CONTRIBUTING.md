# Hướng Dẫn Đóng Góp Và Phát Triển Dự Án (Contributing Guide)

Kiến trúc dự án đã được chuyển sang dạng **Monorepo (npm workspaces)** và trang bị các công cụ định dạng code, kiểm tra kiểu dữ liệu tự động. Hãy tuân thủ hướng dẫn bên dưới khi phát triển hoặc đóng góp cho dự án.

---

## 🏗️ Cấu Trúc Monorepo

Dự án hiện tại được chia thành **4 workspaces**:

| Workspace | Mục đích |
|-----------|----------|
| `mcp-server` | Server MCP kết nối API Fireant (dữ liệu thị trường, cơ bản, tài chính) |
| `mcp-server-dnse` | Server MCP kết nối DNSE OpenAPI (giao dịch, nến giá OHLCV) |
| `mcp-server-buffett` | Server knowledge Warren Buffett — Chủ Tọa Hội Đồng |
| `mcp-server-munger` | Server knowledge Charlie Munger — Cố Vấn Tư Duy |

Các file cấu hình ở root (`package.json`, `tsconfig.base.json`, `.prettierrc`, `eslint.config.js`) định nghĩa quy tắc phát triển chung.

---

## ⚡ Các Lệnh Phát Triển Chính (Chạy từ Root)

Không cần `cd` vào từng thư mục như trước, bạn có thể chạy trực tiếp từ thư mục gốc của dự án:

- **Cài đặt toàn bộ dependencies:**

  ```bash
  npm install
  ```

  _(npm sẽ tự động phân bổ và cài đặt dependencies cho tất cả các workspace)._

- **Biên dịch TypeScript (Build):**

  ```bash
  npm run build
  ```

  _(Lệnh này sẽ biên dịch mã nguồn của cả hai workspace sang JS tương thích ESM trong thư mục `build/` tương ứng)._

- **Kiểm tra kiểu TypeScript (Typecheck):**

  ```bash
  npm run typecheck
  ```

- **Kiểm tra lỗi Lint (Linting):**

  ```bash
  npm run lint
  ```

- **Định dạng lại Code (Formatting):**
  ```bash
  npm run format
  ```

---

## 📝 Quy Định Viết Code & Thêm Tool Mới

Khi tạo thêm công cụ (tool) mới, vui lòng tuân thủ các quy tắc kiến trúc sau:

### 1. Luôn sử dụng `safeHandler`

Mọi tool handler đăng ký vào MCP server cần phải được bọc bởi `safeHandler` (được định nghĩa trong `src/tools/types.ts` của mỗi server).
`safeHandler` giúp:

- Bắt tất cả lỗi ném ra từ API bên thứ ba (mất mạng, hết hạn token, lỗi cú pháp).
- Định dạng lỗi thành phản hồi dạng văn bản an toàn kèm flag `isError: true` của MCP thay vì làm crash luồng Stdio của server.

Ví dụ đăng ký trong `index.ts`:

```typescript
import { safeHandler } from "./tools/types.js";

for (const tool of allTools) {
  server.registerTool(
    tool.name,
    {
      description: tool.description,
      inputSchema: tool.inputSchema,
    },
    safeHandler(tool.handler) as any,
  );
}
```

### 2. Định nghĩa kiểu dữ liệu Zod rõ ràng

Phải định nghĩa chính xác `inputSchema` bằng Zod để Client (như Claude) hiểu được các tham số bắt buộc và kiểu dữ liệu trước khi gửi request.

### 3. Graceful Startup cho DNSE API

Dự án sử dụng Zod để validate môi trường cho DNSE (`DNSE_API_KEY`, `DNSE_API_SECRET`).
Nếu thiếu các biến này, server DNSE sẽ **in cảnh báo ra stderr nhưng KHÔNG crash khi khởi động**. Lỗi chỉ được trả về khi client thực sự gọi các tool cần xác thực. Điều này giúp hệ thống hoạt động ổn định và dễ sửa lỗi cấu hình hơn.

---

## 🚀 Kiểm Tra Trước Khi Commit

Trước khi commit và push code mới, luôn chạy:

```bash
npm run format
npm run lint
npm run typecheck
npm run build
```

Đảm bảo tất cả lệnh trên đều vượt qua thành công không báo lỗi.

---

## 🧠 Thêm Cố Vấn Mới Vào Hội Đồng

Ví dụ: thêm **Peter Lynch**:

1. Tạo `knowledge/lynch/` với các file `.md` (phiết học từ `knowledge/munger/` làm template)
2. Copy `mcp-server-munger/` → `mcp-server-lynch/`
3. Đổi tất cả `munger` → `lynch`, `MUNGER` → `LYNCH` trong:
   - `package.json` (name, description)
   - `src/index.ts` (server name)
   - `src/tools/knowledge.ts` (env var, tool names, descriptions)
4. Thêm vào `workspaces` trong root `package.json`
5. Cập nhật `knowledge/buffett/08_decision_framework/council_debate_format.md` — thêm Lynch vào bảng thành viên
6. Cập nhật `CLAUDE.md` — thêm Lynch vào phần knowledge base mapping
7. Chạy `npm install && npm run build`
