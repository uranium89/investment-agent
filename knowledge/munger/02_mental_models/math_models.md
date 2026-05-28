# Math & Probability Models — Compound Interest, Decision Trees, Bayes

> *"Sức mạnh của compound interest là lực lượng mạnh nhất trong vũ trụ."* (thường được gán cho Einstein, được Munger hay trích dẫn)

---

## 1. Compound Interest (Lãi Kép)

### Định Nghĩa

Lãi sinh ra từ lãi. Số tiền tăng theo hàm số mũ theo thời gian.

```
Giá trị = P × (1 + r)^n
P = vốn gốc, r = lãi suất, n = số năm
```

### Sức Mạnh Của Thời Gian

| ROE / Năm | 10 năm | 20 năm | 30 năm |
|-----------|--------|--------|--------|
| 15% | 4.0x | 16.4x | 66.2x |
| 20% | 6.2x | 38.3x | 237x |
| 25% | 9.3x | 86.7x | 807x |

**Bài học**: ROE 25% duy trì 30 năm = vốn tăng 807 lần. Đây là lý do Munger & Buffett tìm kiếm doanh nghiệp có khả năng compound cao trong thời gian dài.

### Áp Dụng Trong Đầu Tư

**Công ty compound tốt có:**
- ROE cao (>20%) và **bền vững** qua nhiều năm
- Có thể tái đầu tư lợi nhuận vào cơ hội sinh lời cao
- Không cần phân phối nhiều cổ tức (vì tự compound tốt hơn)

**Câu hỏi:**
- ROE của công ty này có thể duy trì trong 10-20 năm không?
- Công ty có đang tái đầu tư hiệu quả không (ROIC > WACC)?
- Có bao nhiêu năm runway tăng trưởng còn lại?

### The Rule of 72

Chia 72 cho lãi suất = số năm để tiền nhân đôi:
- 12%/năm → 72/12 = 6 năm nhân đôi
- 20%/năm → 72/20 = 3.6 năm nhân đôi
- 25%/năm → 72/25 = 2.9 năm nhân đôi

---

## 2. Probability & Expected Value

> *"Bạn không cần dự đoán đúng mọi lúc. Bạn cần expected value dương theo thời gian."*

### Expected Value

```
EV = Σ (Probability × Outcome)
```

**Ví dụ:**
- 70% xác suất cổ phiếu tăng 50% = +35%
- 30% xác suất cổ phiếu giảm 30% = -9%
- **Expected Value = 35% - 9% = +26%** → Đáng mua

### Áp Dụng Trong Đầu Tư

Munger không cần chắc chắn 100%. Ông cần **expected value cao và asymmetric** (tiềm năng lãi lớn hơn nhiều tiềm năng lỗ).

**Asymmetric bets:**
- Cổ phiếu undervalued: tiềm năng tăng 100%, nguy cơ mất 30% (với margin of safety)
- EV = 60%(100%) + 40%(-30%) = 48% → Excellent

**Kelly Criterion** (cỡ đặt cược tối ưu):
```
Kelly % = (bp - q) / b
b = tỷ lệ lãi/lỗ, p = xác suất thắng, q = xác suất thua
```
Munger thường dùng "half Kelly" để an toàn hơn.

---

## 3. Regression to the Mean (Hồi Về Trung Bình)

### Định Nghĩa

Các kết quả cực đoan (rất tốt hoặc rất xấu) có xu hướng trở về mức trung bình theo thời gian.

### Áp Dụng Trong Đầu Tư

**ROE cực cao → Cẩn thận:**
- ROE 50% hiếm khi duy trì dài hạn (trừ công ty đặc biệt như Berkshire)
- Cạnh tranh sẽ gia tăng khi thấy lợi nhuận cao

**Lỗ cực nặng → Có thể là cơ hội:**
- Ngành đang đáy chu kỳ → có thể recover về mức bình thường
- Công ty gặp sự cố một lần → thường recover

**Câu hỏi:**
- Margin/ROE hiện tại có bền vững hay đang ở cực đoan?
- Nếu về mức trung bình, giá trị công ty là bao nhiêu?
- Điều gì ngăn cản regression to mean?

---

## 4. Decision Trees (Cây Quyết Định)

### Định Nghĩa

Vẽ ra tất cả các kết quả có thể xảy ra với xác suất tương ứng, tính expected value.

### Ví Dụ: Phân Tích Mua Cổ Phiếu

```
Mua cổ phiếu X (giá 50,000 VNĐ)
├── Kịch bản tốt (40%): EPS tăng 20%/năm → giá 90,000 (+80%)
├── Kịch bản trung bình (40%): EPS tăng 10%/năm → giá 65,000 (+30%)
└── Kịch bản xấu (20%): EPS flat/giảm → giá 35,000 (-30%)

EV = 40%(+80%) + 40%(+30%) + 20%(-30%)
   = 32% + 12% - 6%
   = +38% → Hấp dẫn nếu thời gian giữ 3-5 năm
```

### Cách Xây Dựng Decision Tree Tốt

1. **Xác định kịch bản**: Bull / Base / Bear
2. **Ước tính xác suất**: Phải tổng = 100%, tránh optimism bias
3. **Tính giá trị mỗi kịch bản**: Dùng DCF hoặc P/E target
4. **Tính EV**: Weighted average
5. **Kiểm tra**: EV có đủ hấp dẫn so với opportunity cost?

---

## 5. Bayes' Theorem (Cập Nhật Xác Suất)

### Định Nghĩa

Cập nhật xác suất của một giả thuyết khi có thông tin mới.

```
P(A|B) = P(B|A) × P(A) / P(B)
```

### Áp Dụng Đơn Giản

**Prior belief**: "Công ty X có 60% khả năng là đầu tư tốt"

**New information**: "CEO vừa bán 30% cổ phần của mình"

**Bayesian update**: Xác suất giảm xuống có thể còn 30-40%

**Nguyên tắc:**
- Bắt đầu với prior dựa trên phân tích cơ bản
- Cập nhật liên tục khi có thông tin mới
- **Không bỏ qua evidence mới** chỉ vì nó xung đột với thesis

**Dấu hiệu cần update mạnh:**
- Insider selling lớn
- Kết quả quarterly miss liên tục
- Regulatory investigation mới
- Thay đổi lãnh đạo đột ngột

---

## 6. The Pareto Principle (Quy Tắc 80/20)

### Áp Dụng Trong Đầu Tư

- 80% lợi nhuận thường đến từ 20% số khoản đầu tư
- 80% rủi ro thường đến từ 20% nguồn rủi ro
- **Tập trung vào 20% quan trọng nhất**, không phân tán quá nhiều

**Implication cho portfolio:**
- Concentration beats diversification (trong giới hạn)
- Tập trung nghiên cứu sâu vào vài công ty hơn là research nông nhiều công ty

---

## Tóm Tắt — Checklist Math Models

```
□ Compound: ROE có thể duy trì bao nhiêu năm? 10 năm → x?
□ EV: Expected value có dương và asymmetric không?
□ Regression: ROE/margin hiện tại có bền vững hay sẽ hồi về mean?
□ Decision tree: Tôi đã vẽ bull/base/bear scenarios chưa?
□ Bayes: Tôi có đang cập nhật view khi có thông tin mới không?
□ Pareto: Tôi có đang focus vào 20% yếu tố quan trọng nhất không?
```
