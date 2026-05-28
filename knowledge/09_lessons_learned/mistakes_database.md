---
title: Mistakes Database & Lessons Learned
created: 2026-05-28
updated: 2026-05-28
---

# 📚 Mistakes Database & Lessons Learned

> *"All I want to know is where I'm going to die, so I'll never go there." — Charlie Munger*

## Feedback Loop #1 — 28/05/2026

### Phân tích 4 báo cáo đầu tiên

| Mã CK | Phán quyết | Giá PT | Giá HN | Chênh lệch | Thời gian |
|-------|-----------|--------|--------|-----------|-----------|
| MBB | MUA | 25.050 | 25.100 | +0.2% | 0 ngày |
| TCB | MUA | 32.600 | 32.600 | 0% | 0 ngày |
| VIC | THEO_DÕI | 214.200 | 216.000 | +0.8% | 0 ngày |
| VNM | MUA | 59.400 | 59.300 | -0.2% | 0 ngày |

**Nhận xét:** Cả 4 báo cáo đều mới được tạo trong ngày. Giá chưa kịp biến động đáng kể. Feedback loop này tập trung vào đánh giá chất lượng phân tích và phát hiện blind spots.

---

## 🎩 Buffett — Đánh giá chất lượng phân tích

### Điểm mạnh đã làm tốt:
1. ✅ **Cấu trúc chuẩn 9 sections** — cả 4 báo cáo đều đúng format
2. ✅ **Dữ liệu thực từ Fireant** — không bịa số, có số liệu cụ thể
3. ✅ **DuPont Decomposition** — có phân tích ROE thành 3 phần, nhấn mạnh chất lượng
4. ✅ **DCF 3 kịch bản** — có phân bổ xác suất 20/60/20
5. ✅ **Munger Inversion** — có ít nhất 3 kịch bản đảo ngược
6. ✅ **Phân biệt doanh nghiệp tốt vs cổ phiếu tốt** — VIC: doanh nghiệp tốt, giá quá đắt

### Điểm yếu cần cải thiện:
1. ❌ **Thiếu biểu đồ trực quan** — toàn bảng số, không có trend chart
2. ❌ **Cơ cấu doanh thu chưa có breakdown quá khứ** — chỉ có 1 năm, thiếu so sánh 5 năm
3. ❌ **Porter's 5 Forces thiếu điểm số tổng hợp** — mới chỉ liệt kê, chưa có điểm để so ngành
4. ❌ **Không có WACC/Ke tính toán chi tiết** — DCF thiếu giải thích suất chiết khấu
5. ❌ **Moat assessment thiếu peer benchmark** — chấm điểm moat nhưng chưa so với đối thủ

---

## 🧠 Munger — Inversion & Blind Spots

### 🔴 Blind Spot #1 — Thiếu phân tích vĩ mô
**Vấn đề:** Cả 4 báo cáo đều không có section về môi trường vĩ mô (lãi suất, tỷ giá, tăng trưởng GDP, lạm phát) — những yếu tố ảnh hưởng trực tiếp đến định giá.
- MBB/TCB (ngân hàng): Lãi suất ảnh hưởng NIM, room tín dụng ảnh hưởng tăng trưởng
- VIC (BĐS): Lãi suất ảnh hưởng sức mua, thanh khoản thị trường
- VNM (sữa): Giá nguyên liệu nhập khẩu phụ thuộc tỷ giá USD/VND

### 🔴 Blind Spot #2 — Thiếu phân tích kịch bản lãi suất
**Vấn đề:** Các báo cáo ngân hàng không stress-test NIM ở các kịch bản lãi suất khác nhau. DCF dùng một Ke duy nhất.

### 🔴 Blind Spot #3 — Thiếu so sánh lịch sử định giá
**Vấn đề:** P/E hiện tại so với P/E 5 năm? P/B hiện tại so với trung bình lịch sử? Thiếu context này làm giảm độ sâu của phân tích.

### 🔴 Blind Spot #4 — Không phân tích competitor dynamics động
**Vấn đề:** Porter's 5 Forces là tĩnh. Không phân tích competitor đang làm gì (TH True Milk, Nestlé đang mở rộng thế nào? ACB, VPBank đang chiếm thị phần ra sao?).

### 🔴 Blind Spot #5 — Thiếu catalyst timeline cụ thể
**Vấn đề:** Catalyst liệt kê nhưng thiếu timeline và điều kiện cụ thể để kích hoạt.

### 🟡 Blind Spot #6 — TCB report: Confirmation Bias từ CIR
Báo cáo TCB dành quá nhiều sự chú ý vào CIR 30.7% (ấn tượng) mà ít phân tích:
- Tại sao ROE TCB chỉ 15.4% trong khi MBB 20.67%?
- CASA đang tăng hay giảm?
- NIM giảm từ 4.4% về 3.88% — xu hướng này có tiếp diễn?

### 🟡 Blind Spot #7 — VNM report: Insider ownership quá thấp
CEO Mai Kiều Liên chỉ sở hữu 0.3% — đây là red flag về alignment. Báo cáo ghi nhận (1/4) nhưng không phân tích sâu hậu quả của việc không có insider ownership.

---

## 📊 Scorecard chất lượng phân tích

| Tiêu chí | MBB | TCB | VIC | VNM | Ghi chú |
|----------|-----|-----|-----|-----|---------|
| Dữ liệu thực | 9/10 | 9/10 | 9/10 | 9/10 | Đầy đủ, chính xác |
| Độ sâu phân tích | 7/10 | 7/10 | 8/10 | 6/10 | VIC sâu nhất, VNM hời hợt |
| Munger Inversion | 7/10 | 7/10 | 8/10 | 6/10 | 3 kịch bản tối thiểu |
| DCF 3 kịch bản | 8/10 | 8/10 | 8/10 | 8/10 | Đều có |
| DuPont | 8/10 | 8/10 | 9/10 | 8/10 | VIC xuất sắc |
| Phân tích ngành | 7/10 | 7/10 | 8/10 | 6/10 | VNM quá sơ sài |
| Moat assessment | 7/10 | 7/10 | 9/10 | 7/10 | VIC rất tốt |
| Quản trị | 7/10 | 7/10 | 8/10 | 6/10 | VNM thiếu insider analysis |
| Định giá | 8/10 | 8/10 | 8/10 | 7/10 | Thiếu so sánh lịch sử |
| Risk & Inversion | 7/10 | 7/10 | 8/10 | 6/10 | VNM quá nhẹ nhàng |
| **Tổng** | **75/100** | **75/100** | **83/100** | **69/100** | |

---

## 📝 Bài Học Rút Ra (Action Items)

### Cần THÊM vào checklist phân tích:
1. **Macro context box** — Lãi suất, tỷ giá, GDP, lạm phát ở đầu mỗi báo cáo
2. **Historical valuation range** — P/E, P/B 5 năm để biết đang ở vùng nào
3. **NIM stress-test** — Với ngân hàng: NIM ở các kịch bản lãi suất ±1%, ±2%
4. **Competitor moves** — Đối thủ đang làm gì (1 đoạn ngắn)
5. **Ke/WACC calculation** — Giải thích suất chiết khấu dùng trong DCF

### Cần CẢI THIỆN:
1. **VNM report** — Cần sâu hơn về rủi ro cạnh tranh và insider ownership
2. **TCB report** — Cần giải thích ROE thấp hơn peer
3. **Biểu đồ** — Thêm ít nhất 1 biểu đồ xu hướng cho mỗi báo cáo

### Cần GIỮ NGUYÊN:
1. Cấu trúc 9 sections ✅
2. DuPont decomposition ✅
3. DCF 3 kịch bản ✅
4. Munger Inversion ✅
5. Phân biệt doanh nghiệp tốt vs đầu tư tốt ✅
6. Dữ liệu thực từ Fireant ✅

---

## 🎯 Kết Luận Feedback Loop #1

> **"Chưa có sai lầm nào để học vì đây là lô báo cáo đầu tiên. Nhưng đã phát hiện 7 blind spots tiềm ẩn — nếu không sửa, chúng sẽ trở thành sai lầm thật sự trong tương lai."**

| Thành viên | Nhận xét |
|-----------|----------|
| 🎩 Buffett | "Chất lượng nền tảng tốt. Blind spot vĩ mô là nguy hiểm nhất — tôi luôn đọc báo cáo kinh tế trước khi nhìn vào báo cáo tài chính." |
| 🧠 Munger | "Inversion cho thấy điểm yếu nhất là thiếu historical context. Không biết quá khứ thì không hiểu hiện tại. Thêm historical P/E range vào checklist." |

**Kế hoạch:** Áp dụng 5 action items trên vào báo cáo tiếp theo.
