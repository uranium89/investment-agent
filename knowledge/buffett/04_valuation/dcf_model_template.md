# 🧮 Hướng Dẫn & Template Định Giá DCF (Discounted Cash Flow)

> DCF là phương pháp định giá tuyệt đối dựa trên nguyên tắc: "Giá trị của một doanh nghiệp bằng tổng hiện giá của các dòng tiền tự do mà nó tạo ra trong tương lai". Mặc dù Buffett và Munger hiếm khi vẽ ra bảng Excel phức tạp, họ luôn tính toán DCF trong đầu (Mental Math) để xác định Biên an toàn (Margin of Safety).

---

## 1. PHÂN LOẠI MÔ HÌNH THEO NGÀNH

AI bắt buộc phải chọn đúng mô hình định giá dựa trên đặc thù ngành của doanh nghiệp:

### 1.1 Doanh nghiệp phi tài chính (Sản xuất, Bán lẻ, Công nghệ, FMCG)
- **Mô hình sử dụng:** FCFF (Free Cash Flow to Firm) hoặc FCFE (Free Cash Flow to Equity).
- **Công thức FCFF:** `FCFF = EBIT * (1 - Tax) + D&A - CAPEX - ΔWC`
- **Tỷ suất chiết khấu:** Dùng WACC (Chi phí vốn bình quân gia quyền) cho FCFF, hoặc Ke (Chi phí vốn cổ phần) cho FCFE.

### 1.2 Doanh nghiệp Ngân hàng & Tài chính (Banking & Financials)
- **CẢNH BÁO:** KHÔNG ĐƯỢC DÙNG FCFF/FCFE cho Ngân hàng. Đối với ngân hàng, nợ (Debt) là nguyên liệu đầu vào (Deposit), dòng tiền tự do không thể tách rời khỏi cấu trúc vốn.
- **Mô hình sử dụng:** DDM (Dividend Discount Model) hoặc RI (Residual Income Model).
- **Công thức DDM:** `Value = Tổng hiện giá của các khoản Cổ tức dự kiến (Expected Dividends) + Hiện giá Giá trị cuối kỳ (Terminal Value)`.
- **Tỷ suất chiết khấu:** Ke (Chi phí vốn cổ phần - Cost of Equity).

### 1.3 Doanh nghiệp Bất động sản (Real Estate)
- **Mô hình sử dụng:** RNAV (Revalued Net Asset Value).
- **Lý do:** Dòng tiền BĐS rất khó dự báo đều đặn hàng năm do phụ thuộc vào tiến độ bàn giao dự án. Định giá từng mảnh đất/dự án theo giá trị thị trường trừ đi nợ sẽ chính xác hơn DCF.

---

## 2. QUY TRÌNH THỰC HIỆN DCF 3 KỊCH BẢN (Cho doanh nghiệp phi tài chính)

Khi thực hiện định giá trong báo cáo, AI phải lập bảng **DCF 3 Kịch bản (Tích cực 20% / Cơ sở 60% / Tiêu cực 20%)**.

### Bước 1: Ước tính FCF trong 5 năm tới (Giai đoạn tăng trưởng rõ ràng)
Dựa trên tỷ lệ tăng trưởng doanh thu và biên lợi nhuận (Net Margin) lịch sử, kết hợp với nhận định về chu kỳ ngành hiện tại.
- Kịch bản Tích cực (Bull): Tăng trưởng mạnh mẽ, biên lợi nhuận mở rộng.
- Kịch bản Cơ sở (Base): Tăng trưởng theo trung bình lịch sử hoặc theo GDP.
- Kịch bản Tiêu cực (Bear): Suy thoái, biên lợi nhuận bị nén lại, CAPEX cao.

### Bước 2: Xác định Terminal Value (Giá trị cuối kỳ)
Dùng phương pháp Tăng trưởng vĩnh viễn (Gordon Growth Model):
`TV = FCF_năm_6 / (WACC - g)`
*Trong đó `g` (Terminal Growth Rate) = Tốc độ tăng trưởng dài hạn (Thường lấy 2-3%, bằng lạm phát hoặc tăng trưởng GDP dài hạn).*

### Bước 3: Chiết khấu về Hiện tại (Present Value)
Dùng WACC (thường từ 9% - 13% tại thị trường Việt Nam tùy mức độ rủi ro doanh nghiệp).
`Giá trị Doanh nghiệp (EV) = Tổng PV của FCF 5 năm + PV của TV`

### Bước 4: Tính Giá trị Vốn chủ sở hữu (Equity Value) và Giá mỗi cổ phiếu
`Equity Value = EV + Cash & Equivalents - Total Debt`
`Giá mỗi cổ phiếu (Target Price) = Equity Value / Số lượng cổ phiếu lưu hành`

---

## 3. BẢNG SENSITIVITY ANALYSIS (Độ nhạy của định giá)

DCF cực kỳ nhạy cảm với các biến số đầu vào (Garbage In - Garbage Out). Munger đặc biệt ghét các chuyên gia phân tích dùng DCF để bóp méo giá trị. Vì vậy, luôn luôn phải chạy bảng độ nhạy (Sensitivity) quanh Kịch bản Cơ sở.

**Bảng Độ Nhạy (Minh họa cho AI khi tạo báo cáo):**

| Terminal Growth (g) \ WACC | 9.0% | 10.0% | 11.0% | 12.0% | 13.0% |
|----------------------------|-------|-------|-------|-------|-------|
| **1.0%** | | | | | |
| **2.0%** | | | [Base Price] | | |
| **3.0%** | | | | | |

*AI cần tính nhanh giá trị ở các điểm nút để người đọc thấy rủi ro nếu WACC tăng cao hoặc g giảm mạnh.*

---

## 4. CHECKLIST "INVERSION" CỦA CHARLIE MUNGER TRƯỚC KHI KẾT LUẬN DCF

Trước khi tin vào con số Target Price từ DCF, Munger sẽ hỏi:
1. "Mức Terminal Growth Rate >3% không? Nếu có, công ty này định lớn hơn cả nền kinh tế sao? Gạch bỏ!"
2. "CAPEX ước tính có đủ để duy trì tăng trưởng đó không, hay lãnh đạo đang 'xào nấu' làm giảm CAPEX để FCF dương ảo?"
3. "Tỷ suất chiết khấu (WACC) có bù đắp đủ rủi ro lạm phát và thanh khoản của Việt Nam không? Nếu dưới 9%, đó là lừa dối bản thân."
4. "Ban lãnh đạo đã từng hứa hẹn tăng trưởng 15% nhưng thực tế chỉ đạt 5%? Hãy chiết khấu mạnh dự phóng của họ."

Chỉ khi vượt qua được 4 câu hỏi này, con số DCF mới có ý nghĩa để xét Biên An Toàn (Margin of Safety).
