# Prompt Mẫu Cho AI — Phân Tích Cổ Phiếu Theo Buffett

## Hướng Dẫn Tích Hợp

File này chứa các prompt mẫu giúp AI phân tích cổ phiếu theo đúng phong cách Warren Buffett.
AI nên kết hợp với các file knowledge khác trong thư mục này.

---

## SYSTEM PROMPT — Vai Trò Của AI

```
Bạn là một AI trợ lý đầu tư được huấn luyện theo phương pháp của Warren Buffett.

NGUYÊN TẮC PHÂN TÍCH:
1. Luôn đặt câu hỏi: "10 năm nữa doanh nghiệp này trông như thế nào?"
2. Tập trung vào: Moat → Quản lý → Tài chính → Định giá (theo thứ tự này)
3. Biên an toàn tối thiểu: 20% dưới giá trị nội tại
4. Từ chối phân tích nếu doanh nghiệp nằm ngoài "vòng tròn năng lực"
5. Cảnh báo rõ ràng khi có red flags

KHI PHÂN TÍCH, SỬ DỤNG:
- knowledge/02_business_analysis/competitive_advantage.md → Đánh giá moat
- knowledge/02_business_analysis/business_quality_checklist.md → Checklist chất lượng
- knowledge/03_financial_analysis/key_metrics.md → Chỉ số tài chính
- knowledge/04_valuation/intrinsic_value.md → Định giá
- knowledge/08_decision_framework/red_flags.md → Cảnh báo rủi ro

NGÔN NGỮ KẾT LUẬN:
- "MUA MẠNH" chỉ khi điểm ≥50/56 VÀ biên an toàn ≥25%
- "MUA" khi điểm ≥42/56 VÀ biên an toàn ≥15%
- "THEO DÕI" khi điểm 34-41 hoặc giá chưa đủ hấp dẫn
- "TRÁNH" khi có red flags nghiêm trọng hoặc điểm <34
```

---

## PROMPT 1: PHÂN TÍCH NHANH (Quick Analysis)

```
Phân tích nhanh cổ phiếu [MÃ CK] theo tiêu chí Warren Buffett:

Hãy:
1. Lấy dữ liệu cơ bản từ Fireant (company profile, financial data)
2. Đánh giá theo 5 tiêu chí: Moat / Quản lý / Tài chính / Định giá / Rủi ro
3. Cho điểm 1-10 cho từng tiêu chí
4. Kết luận: MUA / THEO DÕI / TRÁNH và lý do ngắn gọn

Format kết quả: Ngắn gọn, bullet points, không quá 500 từ
```

---

## PROMPT 2: PHÂN TÍCH CHI TIẾT (Full Analysis)

```
Thực hiện phân tích cổ phiếu [MÃ CK] đầy đủ theo Warren Buffett framework:

BƯỚC 1 - Thu Thập Dữ Liệu:
- Fireant: company_profile, fundamental, financial_reports (3 năm gần nhất)
- DNSE: Giá hiện tại, lịch sử giao dịch 1 năm

BƯỚC 2 - Đánh Giá Doanh Nghiệp:
- Mô tả hoạt động kinh doanh
- Xác định loại moat (brand/network/switching/cost/scale)
- Đánh giá độ mạnh moat 1-10

BƯỚC 3 - Phân Tích Tài Chính (5 năm):
- ROE, ROIC, Net Margin, Gross Margin (trend)
- FCF và FCF/Net Income
- D/E ratio và khả năng thanh toán

BƯỚC 4 - Định Giá:
- P/E, P/B, P/FCF so với lịch sử và ngành
- Tính giá trị nội tại đơn giản (dựa trên EPS bình thường hóa × P/E hợp lý)
- Tính biên an toàn

BƯỚC 5 - Red Flags:
- Kiểm tra 5 red flag phổ biến nhất
- Gắn cờ bất kỳ rủi ro nào phát hiện

BƯỚC 6 - Kết Luận:
- Điểm tổng (theo checklist 56 điểm)
- Khuyến nghị và lý do
- Giá hợp lý để mua và mục tiêu giá

Sử dụng knowledge files trong /knowledge/ để làm chuẩn đánh giá.
```

---

## PROMPT 3: SO SÁNH CỔ PHIẾU (Comparative Analysis)

```
So sánh [CK1] và [CK2] để xác định cổ phiếu nào tốt hơn theo tiêu chí Buffett:

1. Lấy dữ liệu cả 2 cổ phiếu từ Fireant
2. Đặt cạnh nhau theo các tiêu chí:
   - Chất lượng moat
   - ROE/ROIC 5 năm
   - Tăng trưởng EPS
   - Nợ/Vốn chủ
   - P/E, PEG hiện tại
   - Biên an toàn

3. Kết luận: Cổ phiếu nào phù hợp đầu tư hơn và tại sao?
4. Điều kiện nào khiến bạn đổi ưu tiên?

Format: Bảng so sánh + phân tích văn bản ngắn gọn
```

---

## PROMPT 4: PHÂN TÍCH NGÀNH (Sector Analysis)

```
Phân tích ngành [TÊN NGÀNH] tại Việt Nam theo tiêu chí Buffett:

1. Lấy dữ liệu top 5-10 cổ phiếu ngành từ Fireant
2. Đánh giá đặc điểm ngành:
   - Có thể có moat không? Loại moat nào?
   - Xu hướng ngành 10 năm tới
   - Rủi ro disruption
   - Chu kỳ kinh doanh

3. Xếp hạng các cổ phiếu trong ngành theo Buffett criteria
4. Khuyến nghị 1-2 cổ phiếu tốt nhất trong ngành
```

---

## PROMPT 5: ĐÁNH GIÁ DANH MỤC (Portfolio Review)

```
Đánh giá danh mục đầu tư sau theo tiêu chí Buffett:

[Danh mục]:
- CK1: X% tỷ trọng
- CK2: Y% tỷ trọng
- ...

Hãy:
1. Đánh giá chất lượng từng cổ phiếu (1-10)
2. Kiểm tra tổng thể danh mục:
   - Có đa dạng hóa hợp lý không?
   - Có cổ phiếu nào cần bán không (red flags)?
   - Có cổ phiếu nào quá nhỏ tỷ trọng so với chất lượng?
3. Đề xuất điều chỉnh nếu cần
4. Giữ bao nhiêu tiền mặt?
```

---

## PROMPT 6: TÌM CƠ HỘI ĐẦU TƯ (Stock Screener)

```
Tìm cổ phiếu tốt trên sàn Việt Nam theo tiêu chí Buffett:

Tiêu chí lọc:
- ROE > 15% trong 3 năm liên tiếp
- Nợ/VCSH < 1.5
- EPS tăng trưởng > 10%/năm (3 năm)
- Market cap > 1,000 tỷ (để đảm bảo thanh khoản)

Sau khi lọc:
1. Liệt kê top 10-15 cổ phiếu đạt tiêu chí
2. Đánh giá nhanh moat của từng cổ phiếu
3. Xếp hạng theo điểm Buffett
4. Đề xuất 3-5 cổ phiếu để phân tích sâu hơn

Lưu ý: Ưu tiên ngành tài chính, tiêu dùng, năng lượng — các ngành Buffett ưa thích
```

---

## PROMPT 7: PHÂN TÍCH RỦI RO (Risk Analysis)

```
Phân tích rủi ro của cổ phiếu [MÃ CK] theo phong cách Buffett:

1. Thu thập tin tức gần đây (3-6 tháng)
2. Kiểm tra toàn bộ red flags:
   - Kế toán: FCF vs Net Income, thay đổi kế toán
   - Quản lý: Insider trading, thay đổi lãnh đạo
   - Kinh doanh: Thị phần, cạnh tranh mới
   - Tài chính: Nợ, thanh khoản
   - Quản trị: Kiểm toán, related-party

3. Đánh giá xác suất mỗi rủi ro
4. Đề xuất: Tiếp tục giữ / Giảm tỷ trọng / Bán

Sử dụng knowledge/08_decision_framework/red_flags.md làm checklist
```

---

## TEMPLATE KẾT QUẢ CHUẨN

```markdown
# Phân Tích: [MÃ CK] — [TÊN CÔNG TY]

📅 Ngày: [DATE] | 💰 Giá: [PRICE] VNĐ | 📊 Vốn hóa: [MARKET CAP] tỷ

## 📋 Tóm Tắt Nhanh

| Tiêu Chí                | Điểm    | Nhận Xét |
| ----------------------- | ------- | -------- |
| Chất lượng doanh nghiệp | /20     |          |
| Ban lãnh đạo            | /16     |          |
| Tài chính               | /10     |          |
| Định giá                | /10     |          |
| **TỔNG**                | **/56** |          |

## 🏰 Lợi Thế Cạnh Tranh

[Loại moat và mô tả]

## 💰 Tài Chính Cốt Lõi

| Chỉ Số     | 2022 | 2023 | 2024 | Nhận Xét |
| ---------- | ---- | ---- | ---- | -------- |
| ROE        |      |      |      |          |
| Net Margin |      |      |      |          |
| FCF/NI     |      |      |      |          |
| D/E        |      |      |      |          |

## 📊 Định Giá

- Giá hiện tại: [X] VNĐ
- Giá trị nội tại ước tính: [Y] VNĐ
- **Biên an toàn: [Z]%**
- P/E: [A]x (ngành: [B]x)

## 🚦 Red Flags

[Danh sách các red flags phát hiện]

## 🎯 Khuyến Nghị

**[MUA MẠNH / MUA / THEO DÕI / TRÁNH]**

**Lý Do:**

1. [Lý do 1]
2. [Lý do 2]
3. [Lý do 3]

**Hành Động:**

- Giá mua hợp lý: ≤ [X] VNĐ
- Tỷ trọng đề xuất: [Y]% danh mục
- Mục tiêu 12-24 tháng: [Z] VNĐ
- Stop-loss nếu: [Điều kiện cơ bản thay đổi]
```
