# Quản trị rủi ro

Được thiết kế bởi Ray Dalio, phản biện bởi Benjamin Graham và Charlie Munger.

## Nguyên tắc cốt lõi

> **Luật số 1:** Không bao giờ default.
> **Luật số 2:** Nhớ luật số 1.
> — Charlie Munger

## 1. Max Drawdown Control

| Portfolio Drawdown | Hành động |
|---|---|
| > 10% | Giảm position về 75%, rà soát toàn bộ danh mục |
| > 15% | Giảm về 50% (tăng cash), chỉ giữ defensive positions |
| > 20% | Đóng toàn bộ, chỉ giữ VNM, VCB (defensive) |

## 2. Position Limits

| Loại limit | Giới hạn |
|---|---|
| Single position | Không quá 10% danh mục |
| Top 5 positions | Không quá 40% tổng thể |
| Ngành tài chính | Không quá 40% |
| Ngành bất động sản | Không quá 20% |

## 3. Liquidity Filter

- Chỉ mua cổ phiếu có ADTV > 30 tỷ/ngày trong 20 phiên
- Không mua quá 10% khối lượng giao dịch trung bình 1 ngày
- Kiểm tra thanh khoản trước mỗi lệnh EXIT

## 4. Volatility Targeting

- Target portfolio volatility: 15-20%/năm
- Nếu VN30 index volatility > 30% → giảm 20% position
- Position sizing dùng ATR:

```
Position = RiskCapital / (ATR × Multiplier)

Trong đó:
  RiskCapital = 1% của portfolio mỗi trade
  Multiplier = 1.5 (cá nhân), 2.0 (defensive)
```

## 5. Black Swan Protocol

| Trigger | Hành động |
|---|---|
| VN-Index giảm > 3% trong 1 ngày | Tự động rà soát toàn bộ danh mục |
| VN-Index giảm > 5% trong 1 ngày | Bán toàn bộ, vào cash |
| VN-Index tăng > 3%/ngày + overbought | Chốt lời 30% |
| Có tin tức về khủng hoảng ngân hàng | Giảm financial exposure về 0 |

## 6. Stop Loss — Chiến lược của Hội đồng

**Tranh luận giữa Graham và Soros:**

- **Graham:** Stop loss = bán tháo. Nếu đã mua với margin of safety, giá xuống là cơ hội mua thêm.
- **Soros:** Thị trường Việt Nam có gap risk và limit-down. Black swan thật sự.

**Kết luận:**
- **Không** stop loss trên từng cổ phiếu nếu lý do đầu tư còn
- **Có** stop loss ở cấp độ danh mục (drawdown control)
- **Không** bao giờ dùng margin
- **Cash** luôn 20-30% — đó là stop loss tốt nhất

## 7. Kelly Criterion (Half-Kelly)

```
f* = (bp - q) / b

Trong đó:
  b = tỷ lệ lợi nhuận/thua lỗ
  p = xác suất thắng
  q = 1 - p = xác suất thua

Half-Kelly: f = f* / 2
```

Ví dụ VN30: win rate ~55%, risk/reward ~1.5
- Full Kelly: ~25%
- Half-Kelly: ~12.5% → dùng cho position sizing

## 8. Stress Test Scenarios

| Kịch bản | VN-Index | Portfolio expected |
|---|---|---|
| Bình thường | ±5% | ±4% |
| Correction | -15% | -10% (còn 5% cash buffer) |
| Bear market | -30% | -18% (còn 20% cash) |
| Crisis (COVID-style) | -40% | -25% (còn 30% cash) |
| Black swan | -50% | -30% (black swan protocol kích hoạt) |

## 9. Monitoring Checklist Hàng Ngày

- [ ] Drawdown hiện tại
- [ ] Sector exposure
- [ ] Top 5 position size
- [ ] Cash level
- [ ] VN-Index volatility (20-day)
- [ ] Có vi phạm risk limits không
- [ ] Số lệnh failed / total
