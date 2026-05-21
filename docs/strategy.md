# Chiến lược đầu tư VMQ30

**VMQ30** = VN30 Quality-Momentum Hybrid Model — chiến lược được Hội đồng Đầu tư thống nhất.

## Triết lý

> "Hệ thống này không được thiết kế để giàu nhanh. Nó được thiết kế để không nghèo khi về già." — Warren Buffett

## Scoring Framework

### 1. Screening Gate (loại ngay nếu không đạt)

| Tiêu chí | Điều kiện | Ngoại lệ |
|---|---|---|
| D/E | < 1.5 | Ngân hàng (rules riêng) |
| ROE (3 năm) | > 10% liên tiếp | Không |
| Market cap | > 5,000 tỷ | Không |
| ADTV | > 30 tỷ/ngày | Không |
| FCF | Dương 2/3 năm gần nhất | Không |

### 2. Fundamental Score (50%)

#### Quality Score (25%)
| Chỉ số | Trọng số | Cách tính |
|---|---|---|
| ROE | 40% | ROE > 15% = 10, >12% = 7, >10% = 5 |
| D/E | 30% | < 0.5 = 10, <1.0 = 7, <1.5 = 5 |
| FCF Yield | 30% | > 4% = 10, > 2% = 7, > 0% = 5 |

#### Value Score (15%)
- P/E percentile trong VN30 (2 năm): thấp nhất = 10, cao nhất = 0
- P/B < 2 bonus +2 điểm

#### Moat Score (5%)
Đánh giá định kỳ bởi chuyên gia (update 6 tháng/lần):
- Độc quyền tự nhiên (VNM, VCB) = 10
- Lợi thế quy mô (MWG, FPT) = 7
- Brand power (PNJ, SAB) = 5
- Không có moat = 0

#### Management Score (5%)
Dữ liệu từ FireAnt:
- CEO mua cổ phiếu quỹ = bonus
- ESOP pha loãng > 5%/năm = trừ điểm
- Giao dịch nội bộ bất thường = trừ điểm

### 3. Technical Score (25%)

#### Trend Score (15%)
| Tín hiệu | Điểm |
|---|---|
| Price > EMA50 | +3 |
| Price > EMA200 | +3 |
| EMA50 > EMA200 (golden cross) | +3 |
| ADX > 20 (có xu hướng) | +3 |
| Volume > SMA20 | +3 |

#### Momentum Score (10%)
- RSI(14): 30-40 (oversold) = +5, 40-60 = +3, >70 = -3
- MACD histogram dương = +3
- MACD vừa cắt lên signal = +2

### 4. Macro Overlay (±20% tổng exposure)

| Điều kiện vĩ mô | Adjustment |
|---|---|
| Lãi suất điều hành giảm | +10% |
| Lãi suất điều hành tăng | -10% |
| VN-Index > MA200 (uptrend) | +10% |
| VN-Index < MA200 (downtrend) | -10% |
| Rủi ro tỷ giá cao | -10% |
| Tổng adjustment tối đa | ±20% |

## Portfolio Construction

1. **Chọn cổ phiếu**: Top 10 scoring symbols (sau screening)
2. **Trọng số**: proportional to score, điều chỉnh bởi sector limit
3. **Sector limits**:
   - Tài chính (ngân hàng, chứng khoán, bảo hiểm): max 40%
   - Bất động sản: max 20%
   - Mỗi single position: max 10%
4. **Cash**: luôn giữ 20-30% danh mục

## Rebalancing

- **Định kỳ**: 1 tháng/lần (vào phiên đầu tháng)
- **Đột xuất**: khi có cổ phiếu vi phạm screening gate
- **Emergency**: khi drawdown > 10% → review toàn bộ

## Signal Types

| Signal | Hành động | Mô tả |
|---|---|---|
| ENTER | Mua mới | Score > threshold, cash available |
| EXIT | Bán hết | Score < threshold, hoặc vi phạm risk rule |
| ADD | Mua thêm | Score cải thiện, giá giảm nhưng fundamentals tốt |
| REDUCE | Bán bớt | Score giảm, hoặc cần rebalance sector |
| HOLD | Giữ | Không có tín hiệu tốt hơn |
