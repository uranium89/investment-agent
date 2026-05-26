# Phân Tích Sức Mạnh Lợi Nhuận (Earnings Power)

## Khái Niệm Earning Power

> "Chúng tôi muốn biết một doanh nghiệp kiếm được bao nhiêu khi mọi thứ đang chạy bình thường."

Buffett không quan tâm đến lợi nhuận 1 năm cụ thể mà quan tâm đến **"Earning Power"** — khả năng kiếm tiền bình thường hóa, ổn định qua nhiều chu kỳ.

---

## Normalized Earnings (Lợi Nhuận Bình Thường Hóa)

### Tại Sao Cần Bình Thường Hóa?

Lợi nhuận 1 năm có thể bị ảnh hưởng bởi:
- Yếu tố một lần (one-time items): Thanh lý tài sản, phạt, bồi thường
- Chu kỳ kinh doanh (boom/bust cycle)
- Thay đổi kế toán
- Yếu tố thời vụ

### Cách Tính Normalized EPS:

```python
# Phương pháp 1: Trung bình chu kỳ
normalized_eps = average(EPS_last_7_to_10_years)

# Phương pháp 2: Loại bỏ extraordinary items
normalized_eps = reported_eps - one_time_gains + one_time_losses

# Phương pháp 3: Dựa trên ROE × Book Value
normalized_eps = average_ROE × book_value_per_share

# Buffett ưa thích: Owner Earnings
normalized_owner_earnings = (
    net_income
    + depreciation_amortization
    - maintenance_capex
    - working_capital_changes
)
```

---

## Xác Định Maintenance CAPEX vs Growth CAPEX

Đây là điểm khác biệt quan trọng trong phân tích Buffett:

```
Tổng CAPEX = Maintenance CAPEX + Growth CAPEX

Maintenance CAPEX: Tiền cần để giữ nguyên năng lực sản xuất hiện tại
Growth CAPEX: Tiền đầu tư để mở rộng

Ví dụ thực tế:
- Công ty báo CAPEX = 1,000 tỷ
- Khấu hao = 500 tỷ (gợi ý maintenance capex ~500 tỷ)
- Growth CAPEX = 500 tỷ

Owner Earnings = Net Income + 500 (D&A) - 500 (Maint. CAPEX)
              = Net Income (tương đương trong trường hợp này)

Lưu ý: Một số ngành có CAPEX rất thấp hơn D&A
→ Maintenance CAPEX thực sự thấp hơn D&A
→ Owner Earnings > Net Income
```

---

## Sustainable Competitive Advantages và Earning Power

### Công Thức Earning Power:

```
Sustainable Earning Power = Doanh Thu × Sustainable Net Margin

Sustainable Net Margin:
- Ngành bình thường: Trung bình margin 10 năm
- Bỏ qua năm đặc biệt tốt/xấu
- Điều chỉnh cho xu hướng dài hạn

Ví dụ VNM (Vinamilk):
- Doanh thu 2024: ~62,000 tỷ
- Net Margin 10 năm bình quân: ~17%
- Sustainable Earning Power: 62,000 × 17% = ~10,500 tỷ
```

---

## Chu Kỳ Kinh Doanh và Earning Power

### Phân Tích Chu Kỳ:

**Ngành Chu Kỳ (Cyclical Industries):**
- Thép, xi măng, hóa chất, vận tải biển
- EPS dao động rất lớn theo chu kỳ
- KHÔNG dùng EPS đỉnh chu kỳ để định giá
- Dùng EPS trung bình chu kỳ (mid-cycle EPS)

**Ngành Ổn Định (Defensive/Stable):**
- Thực phẩm, đồ uống, ngân hàng bán lẻ, tiện ích
- EPS ổn định, ít biến động
- Có thể dùng EPS hiện tại để định giá (sau khi kiểm tra)

```
Buffett nguyên tắc:
- Ngành chu kỳ: P/E thấp khi earnings cao = ĐẮT (gần đỉnh chu kỳ)
- Ngành chu kỳ: P/E cao khi earnings thấp = RẺ (gần đáy chu kỳ)

Ngược với thông thường!
```

---

## Tăng Trưởng Lợi Nhuận Bền Vững

### Công Thức:

```
Tăng Trưởng Bền Vững = ROIC × Reinvestment Rate

Trong đó:
- ROIC = Lợi nhuận / Vốn đầu tư
- Reinvestment Rate = Vốn tái đầu tư / Lợi nhuận

Ví dụ:
- ROIC = 25%
- Công ty tái đầu tư 60% lợi nhuận
- Tăng trưởng bền vững = 25% × 60% = 15%

Ý nghĩa:
- Nếu ROIC cao + tái đầu tư nhiều → Tăng trưởng cao và tạo giá trị
- Nếu ROIC thấp + tái đầu tư nhiều → Tăng trưởng phá hủy giá trị!
```

---

## Power of Compounding trong Earning Power

### Minh Họa Sức Mạnh ROE Cao:

```
Công ty A: ROE = 20%, không trả cổ tức, tái đầu tư 100%
Công ty B: ROE = 10%, không trả cổ tức, tái đầu tư 100%

Sau 10 năm:
- Book Value A tăng: (1.20)^10 = 6.19x
- Book Value B tăng: (1.10)^10 = 2.59x

Nếu P/B cuối kỳ = 2x:
- Giá A tăng: 6.19x × 2 = 12.38x
- Giá B tăng: 2.59x × 2 = 5.18x

→ ROE cao hơn 2x → Giá trị tăng hơn 2.4x sau 10 năm
```

---

## Ứng Dụng: Định Giá Dựa Trên Earning Power

### Phương Pháp EPV (Earnings Power Value):

```
Bước 1: Tính Adjusted EBIT
  = EBIT + D&A - Maintenance CAPEX - Thay đổi vốn lưu động chuẩn

Bước 2: Sau thuế
  = Adjusted EBIT × (1 - Tax Rate)

Bước 3: Chia cho chi phí vốn (WACC)
  EPV = Adjusted EBIT after tax / WACC

Bước 4: Cộng thêm tài sản dư thừa
  EPV total = EPV + Cash thặng dư - Nợ ròng

Bước 5: Chia cho số cổ phần
  EPV per share = EPV total / Shares outstanding
```

### So Sánh 3 Giá Trị:

```
Asset Value (AV): Tài sản thuần × hệ số điều chỉnh
EPV: Giá trị dựa trên sức mạnh lợi nhuận hiện tại
Intrinsic Value (IV): Giá trị bao gồm cả tăng trưởng tương lai

Phân Tích:
- AV < EPV: Doanh nghiệp tạo ra giá trị từ hoạt động (có moat)
- EPV < IV: Tăng trưởng tương lai có giá trị
- Nếu IV >> EPV >> AV → Đây là doanh nghiệp xuất sắc!
```
