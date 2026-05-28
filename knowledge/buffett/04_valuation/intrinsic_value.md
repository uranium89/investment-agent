# Định Giá Nội Tại (Intrinsic Value) — Phương Pháp Buffett

## Khái Niệm Cơ Bản

> "Giá trị nội tại là giá trị thực sự của một doanh nghiệp — số tiền mà một nhà đầu tư hiểu biết sẽ trả cho toàn bộ doanh nghiệp đó, với thông tin đầy đủ về tất cả các sự kiện tương lai."

### Định Nghĩa Chính Xác:

```
Giá Trị Nội Tại = Tổng giá trị hiện tại của tất cả dòng tiền
                  mà doanh nghiệp sẽ tạo ra trong suốt vòng đời còn lại
                  của nó, được chiết khấu về thời điểm hiện tại
```

---

## Phương Pháp 1: DCF Đơn Giản Hóa (Buffett Style)

Buffett không dùng DCF phức tạp. Ông dùng phiên bản đơn giản hóa:

### Bước 1: Xác Định Owner Earnings Hiện Tại

```
Owner Earnings = Net Income
               + Khấu hao (D&A)
               - Maintenance CAPEX (CAPEX cần thiết để duy trì)
               - Thay đổi vốn lưu động bình thường
```

### Bước 2: Dự Báo Tăng Trưởng (2 Giai Đoạn)

```
Giai đoạn 1 (năm 1-10): Tăng trưởng cao
Giai đoạn 2 (năm 10+): Tăng trưởng ổn định (terminal growth)

Lưu ý Buffett:
- Terminal growth KHÔNG bao giờ cao hơn GDP dài hạn (~3-4%)
- Hãy bảo thủ trong dự báo
```

### Bước 3: Chiết Khấu về Hiện Tại

```python
# Công thức tính giá trị hiện tại
def calculate_intrinsic_value(
    owner_earnings,      # Lợi nhuận chủ sở hữu hiện tại
    growth_rate_1,       # Tăng trưởng giai đoạn 1 (10 năm đầu)
    growth_rate_2,       # Tăng trưởng cuối (terminal)
    discount_rate,       # Tỷ lệ chiết khấu (thường 10-12%)
    years_phase1=10
):
    pv = 0
    current = owner_earnings

    # Giai đoạn 1: 10 năm tăng trưởng cao
    for year in range(1, years_phase1 + 1):
        current *= (1 + growth_rate_1)
        pv += current / (1 + discount_rate) ** year

    # Giai đoạn 2: Terminal Value
    terminal_value = current * (1 + growth_rate_2) / (discount_rate - growth_rate_2)
    pv += terminal_value / (1 + discount_rate) ** years_phase1

    return pv
```

### Bước 4: Tính Giá Trị Nội Tại Trên Cổ Phần

```
IV per share = Tổng Giá Trị Nội Tại / Số Cổ Phần Lưu Hành
```

---

## Phương Pháp 2: Earnings Power Value (EPV)

_(Phương pháp của Bruce Greenwald, được Buffett áp dụng)_

```
EPV = Normalized EBIT × (1 - Tax Rate) / WACC
    = NOPAT / WACC
```

**Ưu điểm:** Không cần dự báo tăng trưởng, dựa vào hiện tại

**Ý nghĩa:**

- EPV > Assets Value → Có lợi thế cạnh tranh
- EPV ≈ Assets Value → Doanh nghiệp bình thường, không có lợi thế
- EPV < Assets Value → Ngành đang suy giảm

---

## Phương Pháp 3: So Sánh Lịch Sử (Historical Comparison)

```
Mức định giá hợp lý = Trung bình P/E lịch sử × EPS hiện tại

Ví dụ:
- P/E lịch sử 10 năm: 15x
- EPS hiện tại: 10,000 VNĐ
- Giá hợp lý: 150,000 VNĐ
```

**Điều Chỉnh:**

- Nếu triển vọng tốt hơn quá khứ → P/E cao hơn
- Nếu triển vọng xấu hơn → P/E thấp hơn
- Lãi suất thay đổi → Điều chỉnh tương ứng

---

## Phương Pháp 4: "10-Year Test" của Buffett

Buffett thường dùng tư duy đơn giản:

```
Câu hỏi: "10 năm nữa công ty này sẽ kiếm được bao nhiêu?"

Nếu tôi tự tin:
- EPS hiện tại: 5,000 VNĐ
- Tăng trưởng: 15%/năm × 10 năm
- EPS sau 10 năm: 5,000 × (1.15)^10 = 20,228 VNĐ
- P/E ổn định: 15x
- Giá sau 10 năm: 20,228 × 15 = 303,420 VNĐ

Nếu mua ở 100,000 VNĐ hôm nay:
- Lợi nhuận từ tăng giá: 303,420 - 100,000 = +203%
- IRR ≈ 11.7%/năm (chưa tính cổ tức)
```

---

## Tỷ Lệ Chiết Khấu Buffett Dùng

Buffett không tiết lộ tỷ lệ chiết khấu cụ thể, nhưng từ các bài viết và phân tích:

### Trái Phiếu Chính Phủ Mỹ (Risk-Free Rate):

- Khi lãi suất thấp (2-3%): Buffett chấp nhận IRR thấp hơn
- Khi lãi suất cao (5-7%): Yêu cầu IRR cao hơn

### Tỷ Lệ Chiết Khấu Thực Tế Buffett Dùng:

- **Cổ phiếu tốt nhất**: 10% (= yêu cầu tối thiểu)
- **Cổ phiếu trung bình**: 12-15%
- **Tương đương trái phiếu dài hạn Mỹ + 5-6%**

### Tại Việt Nam:

```
Tỷ lệ chiết khấu hợp lý VN =
  Lãi suất TPCP 10 năm (hiện ~5-6%)
  + Premium rủi ro vốn cổ phần (~5-7%)
  + Premium rủi ro thanh khoản (~1-2%)
  = ~11-15%

Đề xuất sử dụng: 12% cho cổ phiếu VN tốt
```

---

## Tình Huống Ví Dụ — Vietcombank (VCB)

### Dữ Liệu Giả Định (chỉ mang tính minh họa):

- EPS 2024: 8,000 VNĐ
- ROE: 22%
- Tăng trưởng EPS dự báo: 15%/năm (5 năm), 10% (5 năm tiếp)
- Terminal growth: 5%
- Discount rate: 12%

### Tính Toán Sơ Bộ:

```
Owner Earnings ≈ EPS × FCF ratio = 8,000 × 0.85 = 6,800 VNĐ

Giai đoạn 1 (5 năm, 15%):
Year 1-5 PV ≈ 6,800 × [Σ(1.15)^n / (1.12)^n] ≈ 34,000 VNĐ

Giai đoạn 2 (5 năm, 10%):
Year 6-10 PV ≈ ...

Terminal Value:
EPS năm 10 ≈ 6,800 × (1.15)^5 × (1.10)^5 ≈ 22,000
TV = 22,000 × 1.05 / (0.12 - 0.05) = 330,000
PV of TV = 330,000 / (1.12)^10 ≈ 106,000 VNĐ

Giá Trị Nội Tại ≈ 140,000-150,000 VNĐ/cổ phiếu (giả định)
```

---

## Sai Lầm Thường Gặp Khi Định Giá

### 1. Quá Lạc Quan Về Tăng Trưởng

- Nhiều người dự báo 20-30% mãi mãi → Không thực tế
- Buffett nguyên tắc: Tăng trưởng terminal không vượt 4-5%

### 2. Quá Chú Trọng Vào Số Liệu

- DCF rất nhạy cảm với các giả định nhỏ
- ±1% tỷ lệ chiết khấu = ±20% giá trị nội tại

### 3. Quên Cộng Tiền Mặt và Trừ Nợ

```
Giá trị nội tại trên cổ phần =
  Giá trị hoạt động (DCF)
  + Tiền mặt thặng dư
  - Nợ thuần
  -----------------------------------
  Chia cho: Số cổ phần lưu hành
```

### 4. Không Xem Xét Rủi Ro Cụ Thể

- Doanh nghiệp có rủi ro cao → Dùng discount rate cao hơn
- Doanh nghiệp dự đoán được → Có thể dùng discount rate thấp hơn

---

## Nguyên Tắc Bảo Thủ Của Buffett

> "Tôi thà bị đúng gần đúng còn hơn sai chính xác."

### Áp Dụng:

1. Luôn dùng dự báo bảo thủ (lower bound)
2. Tính biên an toàn ≥ 25% trên giá trị nội tại
3. Kết quả tốt: Bạn mua rẻ hơn giá trị
4. Kết quả bảo thủ: Bạn vẫn không mất nhiều tiền
