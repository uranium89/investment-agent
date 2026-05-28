# Ngành Ngân Hàng — Chuỗi Giá Trị & Quy Trình Sản Xuất

## Chuỗi Giá Trị Ngân Hàng Thương Mại

```
[Huy động vốn] → [Quản lý rủi ro] → [Cấp tín dụng] → [Thu hồi & dịch vụ]
       ↓                  ↓                 ↓                  ↓
   Tiền gửi,        Thẩm định,       Cho vay, đầu tư,     Xử lý nợ,
   phát hành        chấm điểm        bảo lãnh, mở L/C    thanh toán, tư vấn
```

## 1. Huy Động Vốn (Funding)

### Nguồn Vốn
| Loại | Tỷ Trọng | Chi Phí | Đặc Điểm |
|------|----------|---------|----------|
| Tiền gửi KH (CASA) | ~20-35% | 0-0.5%/năm | Rẻ nhất, ổn định |
| Tiền gửi có kỳ hạn | ~40-55% | 4-6%/năm | Chi phí trung bình |
| Tiền gửi TCTD khác | ~5-10% | 3-5%/năm | Ngắn hạn |
| Phát hành giấy tờ có giá | ~5-10% | 5-7%/năm | Chi phí cao |
| Vốn tự có | ~8-12% | Cost of equity ~12-15% | Đắt nhất |

### Yếu Tố Quan Trọng
- **CASA ratio** — tỷ lệ tiền gửi không kỳ hạn: quyết định chi phí vốn
- CASA cao → chi phí vốn thấp → NIM cao hơn
- CASA phụ thuộc vào: mạng lưới chi nhánh, chất lượng dịch vụ, uy tín thương hiệu

## 2. Quản Lý Rủi Ro (Risk Management)

### Các Loại Rủi Ro Chính
| Rủi Ro | Mô Tả | Công Cụ Quản Lý |
|--------|-------|-----------------|
| Tín dụng | Khách hàng không trả nợ | Thẩm định, chấm điểm tín dụng, tài sản đảm bảo, trích lập dự phòng |
| Thị trường | Biến động lãi suất, tỷ giá | ALM, hedging, gap management |
| Thanh khoản | Mất khả năng chi trả | Dự trữ thanh khoản, LDR < 80% |
| Tác nghiệp | Sai sót quy trình, gian lận | Kiểm soát nội bộ, Basel III operational risk |
| Pháp lý | Thay đổi quy định, kiện tụng | Pháp chế, tuân thủ |

### Quy Trình Thẩm Định Tín Dụng
```
Tiếp nhận hồ sơ → Thẩm định (6C) → Chấm điểm → Phê duyệt → Giải ngân → Giám sát → Thu hồi
```

**6C tín dụng:**
- Character (tư cách)
- Capacity (khả năng trả nợ)
- Capital (vốn tự có)
- Collateral (tài sản đảm bảo)
- Conditions (điều kiện thị trường)
- Cash flow (dòng tiền)

## 3. Cấp Tín Dụng (Lending)

### Các Sản Phẩm Cho Vay

| Phân Khúc | Sản Phẩm | Lãi Suất | Rủi Ro |
|-----------|----------|----------|--------|
| Bán lẻ | Vay mua nhà, vay tiêu dùng, thẻ tín dụng | 8-15%/năm | NPL 1-3% |
| SME | Vay vốn lưu động, vay đầu tư | 8-12%/năm | NPL 2-5% |
| Corporate | Vay dự án, vay hợp vốn, phát hành trái phiếu | 6-10%/năm | NPL 0.5-2% |

### Biên Lợi Nhuận Theo Sản Phẩm
| Sản Phẩm | NIM ước tính | Rủi ro/RWA |
|----------|-------------|------------|
| Cho vay bán lẻ tiêu dùng | 6-8% | Cao |
| Cho vay mua nhà | 3-4% | Thấp (có TSĐB) |
| Cho vay SME | 4-6% | Cao |
| Cho vay doanh nghiệp lớn | 1.5-2.5% | Thấp |
| Thẻ tín dụng | 15-20% | Rất cao |
| Bảo lãnh / L/C | 1-3% (phí) | Thấp |

## 4. Thu Nhập Ngoài Lãi (Non-Interest Income)

| Mảng | Tỷ Trọng | Biên LN | Tăng Trưởng |
|------|----------|---------|-------------|
| Phí dịch vụ thanh toán | 25-35% | ~90% | 15-20%/năm |
| Bảo hiểm (bancassurance) | 15-25% | ~90% | 20-30%/năm |
| Kinh doanh ngoại hối | 10-15% | 50-70% | 10-15%/năm |
| Dịch vụ chứng khoán | 5-10% | 60-80% | 15-25%/năm |
| Thu nhập khác (phí, xử lý nợ) | 15-25% | — | Biến động |

## Công Nghệ & Số Hóa

### Hệ Sinh Thái Ngân Hàng Số
- **Core banking**: T24 (Temenos), SilverLake, Oracle FLEXCUBE, in-house
- **Kênh số**: Mobile banking, Internet banking, Chatbot AI, API banking
- **Chi phí vận hành số**: Mở tài khoản online (tốn 5k vs 50k qua chi nhánh)
- **Tác động**: Ngân hàng số hóa mạnh có CIR 30-35% so với CIR 45-55% của ngân hàng truyền thống

## Tạo Giá Trị

**Vị trí tạo giá trị cao nhất:**
- Quản lý CASA (huy động vốn rẻ) + Bancassurance (phí thuần, không tốn vốn)
- Cho vay bán lẻ (NIM cao) nếu quản trị rủi ro tốt
- Số hóa giúp giảm CIR — mỗi 1% CIR giảm ~0.5% ROE tăng
