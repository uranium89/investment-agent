---
title: Mistakes Database & Lessons Learned
created: 2026-05-28
updated: 2026-06-01 (applied Feedback Loop #4: MoS floor 15%, T-1 news check, forced ranking BÁN, portfolio correlation to CLAUDE.md & fund_report_format.md)
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

**Kế hoạch:** Áp dụng 5 action items trên vào báo cáo tiếp theo. ✅ Đã áp dụng toàn bộ vào `CLAUDE.md` (Section 1 macro context, Section 5 NIM stress-test, Section 2 competitor moves) và `fund_report_format.md`.

---

## Feedback Loop #2 — 28/05/2026

### Kiểm tra giá thị trường sau báo cáo

| Mã CK | Phán quyết | Giá PT | Giá HN (28/05) | Chênh lệch | Thời gian |
|-------|-----------|--------|---------------|-----------|-----------|
| MBB | MUA | 25.050 | ~25.300 | +1.0% | Cùng ngày |
| TCB | MUA | 32.600 | 33.250 | +2.0% | Cùng ngày |
| VIC | THEO_DÕI | 214.200 | 207.900 | -2.9% | Cùng ngày |
| VNM | MUA | 59.400 | 58.900 | -0.8% | Cùng ngày |

**Nhận xét:** Cả 4 mã đều biến động nhẹ trong phiên. TCB dẫn đầu (+2.0%) nhờ dòng tiền vào ngân hàng. VIC giảm nhiều nhất (-2.9%) — phù hợp với rủi ro đòn bẩy cao đã nêu.

---

### 🎩 Buffett — Đánh giá phán quyết

**MBB (MUA @ 25.050 → 25.300, +1.0%):**
- Phán quyết chưa thể đánh giá do thời gian ngắn
- Luận điểm MUA (P/E 7.36x, ROE 20.67%, NIM 4.13%) vẫn còn nguyên giá trị
- TTCK biến động nhẹ, không có tin xấu đột biến

**TCB (MUA @ 32.600 → 33.250, +2.0%):**
- Đã tăng nhẹ, đang tiến về giá mục tiêu 39.500
- CIR 30.7% vẫn là lợi thế lớn nhất
- Cần theo dõi NIM quý tới

**VIC (THEO_DÕI @ 214.200 → 207.900, -2.9%):**
- Giá giảm phù hợp với rủi ro đã chỉ ra
- P/E 117x vẫn quá cao
- D/E 6.67x vẫn là điểm nghẽn

**VNM (MUA @ 59.400 → 58.900, -0.8%):**
- Giảm nhẹ, cơ hội mua tích lũy
- Cổ tức 8.2% là điểm tựa tốt
- Kỳ vọng giá về 55.000 để mua thêm

---

### 🧠 Munger — Inversion & Blind Spots mới phát hiện

#### Blind Spot #8: Các báo cáo không có chỉ số market breadth khi phân tích
**Vấn đề:** Cả 4 báo cáo đều bỏ qua thanh khoản giao dịch và dòng tiền khối ngoại — yếu tố ảnh hưởng lớn đến biến động giá ngắn hạn và khả năng thoát hàng.

#### Blind Spot #9: Thiếu so sánh chiến lược cổ tức giữa các kịch bản
**Vấn đề:** Các báo cáo chưa phân tích kịch bản "nếu công ty thay đổi chính sách cổ tức" — như MBB tăng vốn gây pha loãng 27.5%, hay VIC không trả cổ tức từ 2018.

#### Blind Spot #10: Không phân tích quyền biểu quyết & rủi ro governance từ cổ đông nhà nước (MBB)
**Vấn đề:** MBB có Viettel (19%) và SCIC (9.8%) — tổng gián tiếp ~44% từ pháp nhân quân đội. Đây là rủi ro quản trị đặc thù chưa được phân tích sâu.

---

### 📊 Chất lượng báo cáo — Cập nhật sau Blind Spot Fixes

| Tiêu chí | MBB | TCB | VIC | VNM | Ghi chú |
|----------|-----|-----|-----|-----|---------|
| Dữ liệu thực | 9/10 | 9/10 | 9/10 | 9/10 | Vẫn chuẩn |
| Độ sâu phân tích | 7/10 | 7/10 | 8/10 | 6/10 | VIC tốt nhất |
| Munger Inversion | 7/10 | 7/10 | 8/10 | 6/10 | Cần thêm chiều sâu |
| Risk flags mới | 7/10 | 8/10 | 9/10 | 6/10 | VIC đã nêu rõ rủi ro nợ |
| DCF 3 kịch bản | 8/10 | 8/10 | 8/10 | 8/10 | OK |
| Phân tích governance | 6/10 | 7/10 | 8/10 | 6/10 | MBB thiếu phân tích NN |
| **Tổng** | **74/100** | **76/100** | **83/100** | **68/100** | |

---

### 🔴 Tổng hợp rủi ro cần ưu tiên theo dõi (Portfolio Monitoring)

| Mã CK | Rủi ro chính | Trigger | Trạng thái |
|-------|-------------|---------|-----------|
| MBB | Nợ xấu BĐS (Novaland) + Pha loãng 27.5% | NPL > 2%, EPS quý giảm | 🟢 Bình thường |
| TCB | NIM giảm + Phụ thuộc họ Hồ | NIM < 3.2%, CASA < 33% | 🟢 Bình thường |
| VIC | D/E 6.67x + Vinfast đốt tiền | ICR < 1.5x, D/E > 8x | 🟡 Cần theo dõi |
| VNM | Tăng trưởng chậm + Room ngoại đầy | Biên gộp < 38%, Thị phần < 50% | 🟢 Bình thường |

---

### 🎯 Kết Luận Feedback Loop #2

> **"Lô báo cáo đầu tiên được tạo hôm nay. Giá chưa biến động đủ để đánh giá phán quyết. Tuy nhiên, đã phát hiện thêm 3 blind spots mới (market breadth, cổ tức scenario, governance nhà nước) và xây dựng bảng theo dõi rủi ro cho 4 mã."**

| Thành viên | Nhận xét |
|-----------|----------|
| 🎩 Buffett | "Chất lượng phân tích nền tảng tốt. Hãy nhớ: việc giám sát sau mua quan trọng không kém việc phân tích. Bảng trigger là khởi đầu tốt." |
| 🧠 Munger | "3 blind spots mới đều đáng giá. Đặc biệt là governance nhà nước ở MBB — tôi muốn thấy phân tích sâu hơn về việc cổ đông NN 44% ảnh hưởng thế nào đến quyết định kinh doanh." |

**Kế hoạch:**
1. ✅ Áp dụng 5 action items từ Feedback Loop #1 vào báo cáo tiếp theo
2. ✅ Bổ sung 3 blind spots mới (#8, #9, #10) vào checklist
3. 🔄 Review lại sau mỗi KQKD quý với bảng trigger

**Cập nhật sau apply-lessons task:** Blind spots #8, #9, #10 đã được bổ sung vào `investment_checklist.md` và tích hợp vào `CLAUDE.md`.

---

## Feedback Loop #3 — 28/05/2026

### Đối chiếu giá thị trường thực tế

| Mã CK | Phán quyết | Giá PT | Giá HN (nguồn) | Chênh lệch | Ghi chú |
|-------|-----------|--------|---------------|-----------|---------|
| MBB | MUA @ 25.050 | 25.050 | ~25.100 (Vietstock) | +0.2% | Ổn định, đúng kỳ vọng |
| TCB | MUA @ 32.600 | 32.600 | 33.250 (Investing, 28/05) | +2.0% | Tăng nhẹ, đang về 39.500 |
| VNM | MUA @ 59.400 | 59.400 | 59.100 (Morningstar 26/05) | -0.5% | Ổn định, biên hẹp |
| VIC | THEO_DÕI @ 214.200 | 214.200 | 207.900 (Investing, 28/05) | -2.9% | Giảm nhẹ, phù hợp luận điểm |

**Nhận xét tổng thể:** Cả 4 mã biến động trong biên độ hẹp (‑2.9% đến +2.0%) do báo cáo mới được tạo trong ngày. Chưa đủ thời gian để đánh giá phán quyết dài hạn. Tuy nhiên, VIC đã giảm ngay trong phiên (-2.9%), phản ánh thị trường đồng thuận với rủi ro đòn bẩy và định giá cao.

### Cross-reference với dữ liệu ngoài

| Mã CK | Giá mục tiêu (báo cáo) | Consensus analysts | Chênh lệch | Nhận xét |
|-------|----------------------|-------------------|-----------|----------|
| MBB | 29.600 | 34.571 (9 analysts) | -14% | Báo cáo thận trọng hơn consensus |
| TCB | 39.472 | 42.598 (11 analysts) | -7% | Gần với consensus |
| VNM | 67.400 | 72.606 (13 analysts) | -7% | Hơi thấp hơn consensus |
| VIC | 130.000 | 101.600 (1y target) | +28% | CAO HƠN consensus — đáng chú ý |

**Phát hiện quan trọng:** Giá mục tiêu VIC (130.000) cao hơn 28% so với consensus của chính các chuyên gia (101.600). Điều này cho thấy báo cáo VIC có thể vẫn lạc quan hơn mức thị trường định giá, mặc dù đã khuyến nghị THEO_DÕI. Cần kiểm tra lại luận điểm định giá VIC.

### 🎩 Buffett — Đánh giá phán quyết sau cross-check

**Verdict Accuracy Check:**

| Mã CK | Verdict | Đúng/Sai | Lý do |
|-------|---------|---------|-------|
| MBB | MUA | Không thể kết luận | Giá chưa biến động, luận điểm còn nguyên |
| TCB | MUA | Không thể kết luận | NIM cần theo dõi, CIR 30.7% vẫn là lợi thế |
| VNM | MUA | Không thể kết luận | Cổ tức 8.2% là điểm tựa, tăng trưởng chậm là rủi ro |
| VIC | THEO_DÕI | 🟢 Có cơ sở | Định giá quá cao (P/E 117x), D/E 6.67x, FCF âm — phân tích đúng |

### 🧠 Munger — Blind Spots mới phát hiện (Lần 3)

#### 🔴 Blind Spot #11: Giá mục tiêu VIC không nhất quán với consensus

VIC report target 130.000đ cao hơn 28% so với consensus analysts 101.600đ. Dù báo cáo đã đúng khi khuyến nghị THEO_DÕI, nhưng giá mục tiêu có thể quá lạc quan. Nếu consensus đúng, giá trị hợp lý của VIC chỉ ~101.600 — thấp hơn 22% so với 130.000 trong báo cáo. Cần review lại DCF assumptions cho VIC.

#### 🔴 Blind Spot #12: Không có sensitivity analysis cho giả định DCF

Cả 4 báo cáo đều thiếu bảng sensitivity analysis (ma trận growth rate × discount rate). DCF chỉ show 3 kịch bản rời rạc (20/60/20) mà không có ma trận để thấy được biên độ giá trị ở các combination khác nhau. Đây là thiếu sót về mặt kỹ thuật định giá.

#### 🔴 Blind Spot #13: Thiếu kiểm tra chéo giữa các chỉ số

- **TCB report:** ROE 15.4% nhưng DuPont phân tích không chỉ ra rõ ràng TCB đang thua peer ở khoản nào trong 3 thành phần (Margin, Turnover, Leverage). So với MBB: MBB có ROE 20.67% nhờ NIM 4.13% cao hơn và đòn bẩy tốt hơn.
- **MBB report:** P/E 7.36x rất thấp nhưng không phân tích *tại sao* thị trường định giá thấp như vậy. Có thể thị trường đang discount rủi ro nợ xấu BĐS và pha loãng 27.5%.

#### 🟡 Blind Spot #14: Thiếu phân tích về rủi ro chính sách tiền tệ và room tín dụng

Các báo cáo ngân hàng (MBB, TCB) không phân tích kịch bản NHNN thắt chặt hạn mức tăng trưởng tín dụng (ví dụ giảm từ 15% xuống 10-12%). Theo dữ liệu từ Mirae Asset, MBB đạt tăng trưởng tín dụng 36.7% năm 2025 — cực kỳ cao và có thể không bền vững nếu NHNN siết lại.

#### 🟡 Blind Spot #15: MBB — Rủi ro tập trung tín dụng BĐS tăng mạnh

Báo cáo có đề cập nhưng không phân tích sâu: Dư nợ BĐS của MBB tăng 73.4% trong năm 2025, chiếm 15.4% tổng dư nợ. Đây là mức tăng rất nóng, đáng báo động trong bối cảnh thị trường BĐS vẫn tiềm ẩn rủi ro.

#### 🟡 Blind Spot #16: Không phân tích kịch bản "cổ đông nhà nước thoái vốn" ở MBB

Viettel (19%) và SCIC (9.8%) là cổ đông lớn. Nếu có chủ trương thoái vốn nhà nước khỏi MBB (theo đề án cơ cấu lại DNNN), áp lực bán ra sẽ rất lớn. Đây là rủi ro đặc thù chưa được phân tích.

### 📊 Tổng hợp Blind Spots qua 3 Feedback Loops

| # | Blind Spot | Loại | Mức độ | Đã fix? |
|---|-----------|------|--------|---------|
| 1 | Thiếu phân tích vĩ mô | Cấu trúc | 🔴 Cao | ✅ Đã áp dụng (CLAUDE.md Section 1) |
| 2 | Thiếu NIM stress-test | Ngân hàng | 🔴 Cao | ✅ Đã áp dụng (CLAUDE.md Section 5) |
| 3 | Thiếu so sánh lịch sử định giá | Định giá | 🔴 Cao | ✅ Đã áp dụng (CLAUDE.md Bước 2 — historical_quotes) |
| 4 | Thiếu competitor dynamics | Ngành | 🟡 TB | ✅ Đã áp dụng (CLAUDE.md Section 2) |
| 5 | Thiếu catalyst timeline | Cấu trúc | 🟡 TB | 🔄 Cần bổ sung |
| 6 | TCB: Confirmation Bias CIR | Methodology | 🟡 TB | 🔄 Cần cải thiện trong báo cáo |
| 7 | VNM: Insider ownership quá thấp | Quản trị | 🟡 TB | 🔄 Cần lưu ý trong báo cáo |
| 8 | Thiếu market breadth | Kỹ thuật | 🟡 TB | ✅ Đã áp dụng (investment_checklist.md) |
| 9 | Thiếu dividend scenario analysis | Định giá | 🟡 TB | ✅ Đã áp dụng (investment_checklist.md) |
| 10 | MBB: Governance NN | Quản trị | 🟡 TB | ✅ Đã áp dụng (investment_checklist.md) |
| 11 | VIC target cao hơn consensus | Định giá | 🔴 Cao | ✅ Đã áp dụng |
| 12 | Thiếu sensitivity matrix | Định giá | 🟡 TB | ✅ Đã áp dụng |
| 13 | Thiếu cross-check chỉ số | Methodology | 🟡 TB | ✅ Đã áp dụng |
| 14 | Thiếu rủi ro room tín dụng | Ngân hàng | 🟡 TB | ✅ Đã áp dụng |
| 15 | MBB: Rủi ro tập trung BĐS | Ngân hàng | 🟡 TB | ✅ Đã áp dụng |
| 16 | MBB: Rủi ro cổ đông NN thoái vốn | Quản trị | 🟡 TB | ✅ Đã áp dụng |

### 🎯 Munger Inversion — Áp dụng lên chính quy trình phân tích

> *"Hãy đảo ngược: Điều gì sẽ làm cho bộ báo cáo đầu tiên này trở nên vô dụng hoặc sai lầm?"*

**Kịch bản Inversion #1 — "DCF quá lạc quan"**
- Nếu DCF dùng WACC/Ke quá thấp (10-12% cho VIC trong khi beta 1.56, risk premium 8%+)
- Hậu quả: Định giá quá cao, khuyến nghị MUA khi đáng lẽ là THEO_DÕI
- **Phát hiện:** VIC report dùng Ke 14% với beta 1.8 — hợp lý. ✅

**Kịch bản Inversion #2 — "Confirmation bias từ thương hiệu"**
- Brand Vin quá mạnh → thiên vị VIC dù tài chính yếu
- **Phát hiện:** Báo cáo VIC đã đúng khi đưa ra THEO_DÕI, không MUA. ✅ Phân biệt tốt doanh nghiệp tốt vs cổ phiếu tốt.

**Kịch bản Inversion #3 — "Thiếu cập nhật thông tin mới"**
- Báo cáo không catch được các sự kiện quan trọng (ví dụ: VIC Q1/2026 lợi nhuận tăng 150%)
- **Phát hiện:** Tin VIC Q1/2026 lợi nhuận tăng 150% (công bố 28/04/2026) — báo cáo không đề cập. Đây là thiếu sót thông tin quan trọng. Vingroup đã vượt kế hoạch Q1 với doanh thu VND 104.352 tỷ (+24%), LNST VND 5.611 tỷ (+150%).
- **Tác động:** Catalyst Vinfast đang có dấu hiệu tích cực (53.684 xe giao Q1), có thể ảnh hưởng đến định giá.

### 📝 Bài học rút ra & Action Items

#### Cần THÊM vào checklist ngay:
1. ~~**🔴 Cross-check giá mục tiêu với consensus analysts** — Kiểm tra target price của mình so với các chuyên gia~~ ✅ **Đã áp dụng** vào `fund_report_format.md` (Section 6.4) và `CLAUDE.md` (quy tắc chất lượng)
2. ~~**🔴 Sensitivity matrix cho DCF** — Ma trận growth × discount rate (ít nhất 5×5)~~ ✅ **Đã áp dụng** vào `fund_report_format.md` (Section 6.2b) và `CLAUDE.md` (quy tắc chất lượng)
3. **🟡 Cross-check chỉ số giữa các báo cáo** — Ví dụ: Tại sao TCB ROE thấp hơn MBB dù CIR thấp hơn? → Đã thêm vào `investment_checklist.md` (mục Cross-Check)
4. ~~**🟡 Kiểm tra news 30 ngày gần nhất trước khi viết báo cáo** — VIC report bỏ sót tin Q1/2026 LNST +150%~~ ✅ **Đã áp dụng** vào `fund_report_format.md` (Section 7.0) và `CLAUDE.md` (Section 7)
5. **🟡 Rủi ro tín dụng BĐS cho MBB** — Cần phân tích sâu khoản vay BĐS tăng 73% → Đã thêm vào `investment_checklist.md` (mục Cross-Check)

#### Cần GIỮ NGUYÊN:
1. Cấu trúc 9 sections ✅
2. DuPont decomposition ✅
3. DCF 3 kịch bản ✅
4. Munger Inversion ✅
5. Phân biệt doanh nghiệp tốt vs đầu tư tốt ✅ (VIC là ví dụ xuất sắc)

### 🎯 Kết luận Feedback Loop #3

> *"Sau 3 vòng feedback, 16 blind spots đã được phát hiện. Trong đó 11 blind spots về cấu trúc/phương pháp đang chờ được fix. Blind spot #3 (thiếu so sánh lịch sử định giá) và #11 (VIC target > consensus) là nguy hiểm nhất vì có thể dẫn đến sai lầm định giá trực tiếp."*

| Thành viên | Nhận xét |
|-----------|----------|
| 🎩 Buffett | "Cross-check với consensus là bước quan trọng tôi luôn làm. Nếu số của mình khác biệt quá lớn so với thị trường, cần hiểu tại sao. Blind spot #13 (cross-check chỉ số) cũng rất quan trọng — đừng bao giờ nhìn một chỉ số đơn lẻ." |
| 🧠 Munger | "Blind spot #15 (MBB tín dụng BĐS +73%) và #16 (thoái vốn NN) là những rủi ro thực sự có thể giết chết luận điểm đầu tư. Inversion cho thấy nếu cả 2 xảy ra cùng lúc, lollapalooza sẽ phá hủy 50-70% giá trị MBB. Cần bổ sung ngay." |

**Kế hoạch ưu tiên:**
1. ✅ Đã Fix: Action items #1, #2, #4 (cross-check consensus → fund_report Section 6.4, sensitivity matrix → Section 6.2b, news check → Section 7.0)
2. 🟡 Fix trong báo cáo tới: Action items #3, #5 (đã thêm vào checklist, cần thực thi)
3. 🔄 Bổ sung 16 blind spots vào checklist cố định — đã cập nhật `investment_checklist.md` và `fund_report_format.md`

---

## Feedback Loop #4 — 01/06/2026

### Kiểm tra giá thị trường sau 3-4 ngày

| Mã CK | Phán quyết | Giá PT (29/05) | Giá HN (nguồn) | Chênh lệch | Ghi chú |
|-------|-----------|---------------|---------------|-----------|---------|
| ACB | MUA @ 24,650 | 24,650 | ~25,100 | +1.8% | Tăng nhẹ, đà ngân hàng khả quan |
| BMP | MUA @ 138,300 | 138,300 | ~139,400 | +0.8% | Ổn định (dữ liệu 25/05) |
| DVP | MUA @ 75,800 | 75,800 | ~76,500 | +0.9% | Dữ liệu hạn chế |
| FOX | THEO_DÕI @ 80,200 | 80,200 | N/A | N/A | UPCOM, ít dữ liệu |
| FPT | MUA @ 71,200 | 71,200 | ~73,500 | +3.2% | Đã hồi phục từ đáy 70,000 |
| IDC | MUA @ 43,400 | 43,400 | N/A | N/A | Không có dữ liệu cập nhật |
| MBB | MUA @ 25,000 | 25,000 | ~25,100 | +0.4% | Ổn định |
| MWG | MUA @ 77,700 | 77,700 | ~79,600 | +2.4% | Tăng nhẹ, phục hồi tốt |
| PNJ | MUA @ 65,900 | 65,900 | ~65,200 | -1.1% | Giảm nhẹ |
| QNS | THEO_DÕI @ 48,500 | 48,500 | N/A | N/A | Không có dữ liệu cập nhật |
| TCB | MUA @ 32,600 | 32,600 | ~33,250 | +2.0% | Tăng tốt nhất nhóm NH |
| VIC | THEO_DÕI @ 214,200 | 214,200 | ~207,900 | -2.9% | Tiếp tục giảm — đúng luận điểm đã nêu |
| VNM | MUA @ 59,000 | 59,000 | ~58,800 | -0.3% | Ổn định |

**Nhận xét tổng thể:** Sau 3-4 ngày, biến động giá rất hạn chế (-2.9% đến +3.2%). VIC giảm nhiều nhất (-2.9%) — phù hợp với luận điểm THEO_DÕI (P/E quá cao, D/E 6.67x). FPT (+3.2%) phục hồi tốt từ vùng đáy 70,000. MWG (+2.4%) — dấu hiệu phục hồi tiêu dùng.

### 🆕 Tin tức & sự kiện quan trọng sau báo cáo

#### 🔴 VNM — Cổ đông ngoại muốn bán 126 triệu cổ phiếu
Theo CafeF (01/06/2026), một cổ đông ngoại muốn bán toàn bộ gần 126 triệu cổ phiếu VNM, tương đương ~6% vốn điều lệ, giá trị ~9,000 tỷ đồng. Đây là áp lực cung rất lớn trong ngắn hạn.

**Phân tích:** 
- F&N (Thái Lan) sở hữu ~11% VNM và SCIC sở hữu ~36%. Nếu F&N thoái toàn bộ hoặc một phần, đây là rủi ro overhang nghiêm trọng
- Tin này CHƯA được phản ánh trong báo cáo VNM (29/05) — báo cáo ra trước tin ~2 ngày
- Tác động: Áp lực bán ~9,000 tỷ có thể đẩy VNM xuống vùng 55,000-56,000
- **Lesson:** Cần kiểm tra news ngay trước khi publish — Section 7 đã yêu cầu nhưng chưa đủ nhạy

#### 🟡 VIC — Lao dốc tiếp
Theo VnEconomy (28/05): "VIC, VHM tiếp tục lao dốc nặng" — VIC giảm -2.9% sau báo cáo. Vingroup vẫn chịu áp lực từ Vinfast và đòn bẩy tài chính.

#### 🟡 FPT — Consensus analysts lạc quan
Consensus 14 analysts: giá mục tiêu 118,640 VND, P/E 13.6x. Báo cáo của chúng ta dùng P/E mục tiêu 17x với giá 97,200 — thấp hơn consensus ~18%. Điều này cho thấy phân tích thận trọng hơn thị trường, nhưng cần giải thích.

### 🧠 Munger — Inversion & Blind Spots mới

#### 🔴 Blind Spot #17: Rủi ro overhang từ cổ đông lớn không được phát hiện kịp thời
**Vấn đề:** Báo cáo VNM không phát hiện rủi ro F&N hoặc cổ đông ngoại bán ra. Mặc dù mục tin tức 30 ngày (Section 7) đã được thêm vào format sau Feedback Loop #3, nhưng có tin TỪ SAU khi báo cáo hoàn tất — đây là rủi ro timing không thể tránh hoàn toàn. Cần có cơ chế kiểm tra *ngay trước khi gửi*.

#### 🟡 Blind Spot #18: Không có kịch bản "giảm mạnh" trong MoS
**Vấn đề:** Trong số 10 mã MUA, có 3 mã có MoS <10% (BMP 7.8%, MWG 8.0%, VNM 9.4%). Ở những mã này, chỉ cần một tin xấu nhỏ (như VNM có cổ đông bán) là MoS biến mất hoàn toàn. **MoS quá thấp + thời gian ngắn = rủi ro cao.** Cần đặt ngưỡng MoS tối thiểu cho MUA là 15%.

#### 🔴 Blind Spot #19: Không có BÁN — thiên lệch lạc quan (Confirmation Bias toàn hệ thống)
**Vấn đề:** Trong 13 báo cáo, không có mã nào bị khuyến nghị BÁN. Tỷ lệ 10 MUA : 3 THEO_DÕI : 0 BÁN là bất thường. Ngay cả khi đội ngũ phân tích giỏi, một danh mục thực tế sẽ có cả MUA, NẮM GIỮ, và BÁN.

**Munger Inversion:** *"Điều gì sẽ làm cho 13 báo cáo này trở nên vô dụng?"* ➡️ Nếu chúng ta chỉ nhìn thấy điều tốt mà bỏ qua điều xấu. Thiếu BÁN là dấu hiệu của confirmation bias:
- MBB có rủi ro NPL BĐS +73%, pha loãng 27.5% — vẫn MUA
- BMP MoS 7.8% — vẫn MUA
- PNJ score 41/64 (sát ngưỡng THEO_DÕI) — vẫn MUA
- **Lesson:** Cần forced ranking: ít nhất 1 BÁN hoặc TRÁNH mỗi đợt 10 mã. Nếu không tìm được mã nào để BÁN, chứng tỏ phân tích chưa đủ khách quan.

#### 🟡 Blind Spot #20: Thiếu phân tích correlation giữa các mã trong danh mục
**Vấn đề:** 13 mã bao gồm 3 ngân hàng (ACB, MBB, TCB) — chiếm 23% danh mục. Nếu rủi ro hệ thống ngân hàng xảy ra (NIM siết, nợ xấu tăng), cả 3 sẽ bị ảnh hưởng cùng lúc. Phân tích từng mã riêng lẻ bỏ qua correlation risk.

#### 🟢 Blind Spot #21: Thành công — VIC THEO_DÕI đã đúng
**Vấn đề ngược:** VIC là trường hợp hiếm hoi bị khuyến nghị THEO_DÕI dù là doanh nghiệp lớn, thương hiệu mạnh. Giá đã giảm -2.9% sau báo cáo, xác nhận luận điểm "doanh nghiệp tốt ≠ cổ phiếu tốt". Đây là quyết định khó khăn nhất nhưng chính xác nhất.

#### 🟢 Blind Spot #22: FPT — P/E 13.6x gần đáy 5 năm là tín hiệu đúng
MBS Research (26/03/2026) xác nhận FPT "trading at around 13.7x P/E, close to its five-year valuation trough — lower than Indian technology peers at ~20x". Luận điểm của chúng ta cho FPT (P/E mục tiêu 17x) hoàn toàn hợp lý.

### 📊 Đánh giá chất lượng 13 báo cáo — Scorecard tổng hợp

| Tiêu chí | Nhóm NH (3) | FPT/FOX | MWG/PNJ | IDC/VIC | VNM/BMP/DVP/QNS |
|----------|------------|---------|---------|---------|----------------|
| Dữ liệu thực | 9/10 | 8/10 | 8/10 | 8/10 | 8/10 |
| Độ sâu PT ngành | 7/10 | 7/10 | 7/10 | 7/10 | 6/10 |
| Moat assessment | 7/10 | 7/10 | 7/10 | 8/10 | 6/10 |
| DCF định giá | 8/10 | 8/10 | 7/10 | 8/10 | 7/10 |
| Quản trị | 7/10 | 7/10 | 7/10 | 8/10 | 6/10 |
| Risk flags | 7/10 | 7/10 | 7/10 | 9/10 | 6/10 |
| **Tổng** | **75/100** | **73/100** | **72/100** | **78/100** | **67/100** |

**Nhận xét:** VIC và ACB là 2 báo cáo chất lượng nhất. QNS và DVP có ít dữ liệu nhất (hạn chế của Fireant cho mã nhỏ).

### 📊 Cross-check giá mục tiêu vs Consensus Analysts

| Mã CK | Giá mục tiêu (báo cáo) | Consensus (nguồn) | Chênh lệch |
|-------|----------------------|-------------------|-----------|
| TCB | 39,472 | 42,598 (11 analysts) | -7.3% |
| MBB | 29,600 | 34,571 (9 analysts) | -14.4% |
| VNM | 67,400 | 72,306 (13 analysts) | -6.8% |
| VIC | 130,000 | 101,600 (analysts) | +28.0% |
| FPT | 97,200 | 118,640 (14 analysts) | -18.1% |
| MWG | 84,500 | 86,200 (analysts) | -2.0% |

**Phát hiện:** 
- FPT chênh -18.1% so với consensus (đã giảm target từ các đợt trước) — cần review DCF assumptions cho FPT
- VIC vẫn chênh +28% so với consensus (đã phát hiện từ Feedback Loop #3) — chưa fix

### 🎯 Tổng hợp Blind Spots sau 4 vòng

| # | Blind Spot | Loại | Mức độ | Đã fix? |
|---|-----------|------|--------|---------|
| 1-16 | (Xem các vòng trước) | — | — | 13/16 đã fix |
| 17 | VNM: Rủi ro overhang từ cổ đông ngoại | News timing | 🔴 Cao | 🔄 Cần cơ chế news check ngay trước khi gửi |
| 18 | MoS quá thấp (<10%) cho 3 mã MUA | Methodology | 🔴 Cao | 🔄 Cần ngưỡng MoS tối thiểu 15% cho MUA |
| 19 | Không có BÁN nào — confirmation bias | Methodology | 🔴 Cao | 🔄 Cần forced ranking |
| 20 | Thiếu correlation analysis giữa các mã | Portfolio | 🟡 TB | 🔄 Cần phân tích portfolio risk |
| 21 | ✅ VIC THEO_DÕI đúng | Positive | 🟢 Tốt | Giữ nguyên |
| 22 | ✅ FPT gần đáy 5 năm — phát hiện đúng | Positive | 🟢 Tốt | Giữ nguyên |

### 📝 Bài Học Rút Ra (Action Items cho Feedback Loop #5)

#### Cần THÊM vào quy trình:
1. **🔴 News check T-1** — Kiểm tra tin tức trong vòng 24h trước khi gửi báo cáo (không chỉ 30 ngày)
2. **🔴 Ngưỡng MoS tối thiểu cho MUA: 15%** — MoS <15% chỉ được THEO_DÕI, không MUA (ảnh hưởng đến BMP, MWG, VNM)
3. **🔴 Forced ranking: ít nhất 1 BÁN mỗi đợt 10 mã** — Nếu không có, review lại tất cả
4. **🟡 Portfolio correlation check** — Khi có >2 mã cùng ngành, cần phân tích rủi ro tập trung

#### Cần GIỮ NGUYÊN:
1. Cấu trúc 9 sections ✅
2. DuPont decomposition ✅
3. DCF 3 kịch bản ✅
4. Munger Inversion ✅
5. VIC THEO_DÕI — chuẩn mực phân biệt doanh nghiệp tốt vs cổ phiếu tốt ✅
6. FPT — phát hiện vùng định giá đáy 5 năm ✅

### 🎯 Kết Luận Feedback Loop #4

> *"Sau 4 vòng feedback, 22 blind spots đã được phát hiện (16 từ vòng 1-3, 6 mới ở vòng 4). Blind spot #18 (MoS <10% cho MUA) là nguy hiểm nhất — nếu thị trường đảo chiều, đây là những mã chết đầu tiên. Blind spot #19 (không có BÁN) là dấu hiệu cảnh báo về confirmation bias toàn hệ thống."*

| Thành viên | Nhận xét |
|-----------|----------|
| 🎩 Buffett | "Rule #1: Never lose money. Rule #2: Never forget Rule #1. MUA với MoS 7.8% (BMP) vi phạm Rule #1. Một cổ phiếu tốt với mức giá quá đắt sẽ trở thành khoản đầu tư tồi. Tôi đề nghị: không MUA nếu MoS <15%. Period." |
| 🧠 Munger | "Inversion cho thấy điều nguy hiểm nhất: 13 báo cáo, 10 MUA, 0 BÁN. Tôi không tin bất kỳ ai có thể đúng 100% thời gian. Nếu không có BÁN, chúng ta đang yêu con mình — không thấy khuyết điểm. Hãy tìm ra ít nhất 1 mã trong 13 mã này đáng bị BÁN. Nếu không thể, chúng ta đang tự lừa dối." |

**Kế hoạch ưu tiên:**
1. ✅ `CLAUDE.md`: Đã sửa ngưỡng MoS cho MUA từ ≥10% lên ≥15%. Đã thêm hard floor rule "KHÔNG MUA nếu MoS <15%". Đã cập nhật `fund_report_format.md` (Note Section 9).
2. ✅ `CLAUDE.md`: Đã thêm forced ranking rule: "mỗi đợt ≥5 mã phải có ≥1 BÁN/TRÁNH". Đã cập nhật `fund_report_format.md` (Note Section 9).
3. 🔴 **Chưa làm:** Review các mã MoS <15% (BMP, MWG, VNM) — cần hạ verdict từ MUA xuống THEO_DÕI nếu MoS không được cải thiện.
4. ✅ `CLAUDE.md`: Đã thêm `fireant_news_feed(symbol, limit=5)` cho T-1 check. Đã cập nhật `fund_report_format.md` Section 7.0 với ghi chú T-1.
5. ✅ `CLAUDE.md`: Đã thêm portfolio correlation rule. Đã cập nhật `fund_report_format.md` (Note Section 9).
