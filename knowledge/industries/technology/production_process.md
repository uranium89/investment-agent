# Ngành Công Nghệ — Chuỗi Giá Trị & Quy Trình Sản Xuất

> Phân tích chuỗi giá trị ngành CNTT từ upstream đến downstream. Không thiên vị doanh nghiệp nào.

---

## 1. CHUỖI GIÁ TRỊ NGÀNH CNTT

### 1.1 Sơ Đồ Tổng Quan

```
UPSTREAM                           MIDSTREAM                          DOWNSTREAM
─────────                          ─────────                          ──────────

Hardware/Infra ─→ Semiconductor ─→ IT Services ─→ Software/SaaS ─→ Enterprise/Consumer
  • Servers        • Design        • Outsourcing    • ERP/CRM      • BFSI
  • GPU/NPU        • Fabrication    • Consulting     • Cloud Apps   • Government
  • Network        • Packaging      • Integration    • AI/ML        • Manufacturing
  • Data Centers   • Testing        • Managed Svc    • Security     • Healthcare
                                    • BPO            • Platform     • Education
```

### 1.2 Phân Tích Từng Tầng

#### Tầng 1 — Hạ Tầng & Phần Cứng (Hardware/Infrastructure)
| Công Đoạn | Mô Tả | Ví Dụ Toàn Cầu | Tại Việt Nam |
|-----------|-------|---------------|--------------|
| Cloud infrastructure | Cung cấp compute, storage, network | AWS, Azure, GCP | FPT Cloud, Viettel Cloud, VNPT |
| Data centers | Hosting, colocation, managed hosting | Equinix, Digital Realty | FPT DC, Viettel IDC, VNPT Data |
| Network infrastructure | 5G/4G, fiber, submarine cable | Ericsson, Nokia | Viettel, VNPT, CMC |
| Enterprise hardware | Server, storage, networking | Dell, HPE, Cisco | FPT Retail (phân phối) |

#### Tầng 2 — Semiconductor
| Công Đoạn | Mô Tả | Giá Trị Gia Tăng |
|-----------|-------|------------------|
| Chip design (Front-end) | Thiết kế vi mạch, logic, layout | Cao nhất (~50% giá trị) |
| Wafer fabrication | Sản xuất wafer tại fab | Rất cao, CAPEX khổng lồ |
| Assembly & Packaging | Đóng gói chip | Trung bình |
| Testing | Kiểm tra chất lượng | Trung bình |

**Tại Việt Nam:**
- **Chip design**: 50 công ty, 7.000 kỹ sư — chủ yếu thiết kế IC cho các hãng nước ngoài
- **Fabrication**: Viettel xây fab đầu tiên tại Hòa Lạc (32nm, thử nghiệm cuối 2027)
- **Packaging & Testing**: Intel, Amkor, Hana Micron — quy mô lớn
- **FPT Semiconductor**: Thiết kế chip cho IoT, power management

#### Tầng 3 — IT Services (Dịch Vụ Công Nghệ Thông Tin)
Đây là tầng cốt lõi của các công ty IT services Việt Nam như FPT, CMC.

| Mảng Dịch Vụ | Mô Tả | Gross Margin Điển Hình | Yêu Cầu |
|-------------|-------|----------------------|---------|
| IT Outsourcing | Phát triển phần mềm theo yêu cầu (offshore/nearshore) | 25-35% | Kỹ sư đông, quản lý dự án |
| Digital Transformation | Tư vấn & triển khai chuyển đổi số (AI, cloud, automation) | 30-40% | Chuyên gia tư vấn, domain knowledge |
| System Integration | Tích hợp hệ thống (ERP, CRM, legacy modernization) | 20-30% | Kinh nghiệm platform, partner hệ thống |
| Managed Services | Vận hành, bảo trì hệ thống cho khách hàng | 25-35% | Năng lực vận hành quy mô |
| BPO (Business Process) | Gia công quy trình nghiệp vụ (kế toán, HR, v.v.) | 20-25% | Quy mô, tự động hóa |
| Consulting | Tư vấn chiến lược công nghệ | 40-50% | Thương hiệu, chuyên gia cao cấp |

**Đặc thù IT Services:**
- **Recurring**: Managed services và BPO có doanh thu định kỳ cao
- **Project-based**: Outsourcing và SI là doanh thu dự án, có tính chu kỳ
- **Labor-intensive**: Biên lợi nhuận phụ thuộc vào hiệu suất lao động và tỷ lệ utilization
- **Offshore/Nearshore**: Lợi thế cạnh tranh nhờ chênh lệch chi phí lao động

#### Tầng 4 — Software & Platform (Phần Mềm & Nền Tảng)
| Mảng | Mô Tả | Gross Margin | Mức Độ Recurring |
|------|-------|-------------|------------------|
| SaaS (Software as a Service) | Phần mềm đăng ký theo tháng/năm | 60-80% | Rất cao |
| Platform Engineering | Xây dựng nền tảng số, low-code | 50-70% | Cao |
| AI/ML Solutions | Giải pháp AI, xử lý dữ liệu | 40-60% | Trung bình-Cao |
| Cybersecurity | Phần mềm bảo mật, SOC | 50-70% | Cao |
| ERP/Enterprise Apps | Phần mềm quản trị doanh nghiệp | 40-60% | Trung bình |

#### Tầng 5 — Hạ Tầng Viễn Thông (Telecom)
| Mảng | Mô Tả | Margin | Đặc Điểm |
|------|-------|--------|---------|
| Băng rộng cố định | Internet cáp quang đến hộ gia đình | 35-45% | Recurring, cạnh tranh giá |
| Di động | 4G/5G services | 30-40% | Recurring, CAPEX lớn |
| Data Center | Cho thuê chỗ, cloud | 40-50% | Recurring, CAPEX lớn |

---

## 2. QUY TRÌNH SẢN XUẤT PHẦN MỀM (Software Development)

Đây là quy trình cốt lõi của ngành — từ yêu cầu khách hàng → sản phẩm phần mềm.

### 2.1 Vòng Đời Phát Triển Phần Mềm (SDLC)

```
Requirements → Design → Development → Testing → Deployment → Maintenance
      ↑            ↑           ↑            ↑            ↑            ↑
   BA/PO       Solution    Developer    QA/Tester    DevOps       Support
               Architect
```

| Giai Đoạn | Thời Gian | Chi Phí | Giá Trị Gia Tăng |
|-----------|-----------|---------|------------------|
| Requirements & Analysis | 10-15% | 5-10% | Cao (domain knowledge) |
| Solution Design | 10-15% | 10-15% | Rất cao (kiến trúc) |
| Development (coding) | 40-50% | 30-40% | Trung bình (có thể thay thế) |
| Testing | 15-20% | 15-20% | Trung bình (cần automation) |
| Deployment | 5-10% | 5-10% | Cao (DevOps) |
| Maintenance | 15-25% | 20-30% | Cao (recurring) |

### 2.2 Các Mô Hình Phát Triển

| Mô Hình | Đặc Điểm | Phù Hợp Với |
|---------|---------|------------|
| Waterfall | Tuần tự, tài liệu đầy đủ | Dự án chính phủ, fixed-price |
| Agile/Scrum | Lặp, linh hoạt | Offshore/outsourcing, sản phẩm |
| DevOps | CI/CD, tự động hóa liên tục | Cloud-native, SaaS |
| Low-code/No-code | Kéo thả, ít code | Nội bộ doanh nghiệp |

### 2.3 Các Yếu Tố Kỹ Thuật Ảnh Hưởng Đến Kinh Tế

| Yếu Tố | Tác Động Đến Chi Phí | Ghi Chú |
|--------|---------------------|---------|
| Chọn tech stack (Java vs .NET vs Python) | Chênh lệch 20-30% chi phí nhân sự | Java/.NET đắt hơn Python/JS |
| Mức độ tự động hóa | Giảm 30-40% thời gian testing | Cần đầu tư ban đầu |
| Cloud-native design | Giảm 50-60% chi phí infra | Tăng chi phí platform |
| AI-assisted coding | Tăng 20-40% năng suất developer | Đang mới nổi |

---

## 3. CHUỖI GIÁ TRỊ VIỄN THÔNG (Telecommunications)

### 3.1 Cấu Trúc Ngành Viễn Thông VN

```
Hạ tầng (TowerCo, Fiber) → Mạng lõi (Core Network) → Dịch vụ (Service) → Khách hàng
                              ↓
                        Data Center → Cloud Services
```

| Tầng | Mô Tả | Thị Trường VN |
|------|-------|--------------|
| Hạ tầng thụ động | Cột, trạm BTS, cáp quang | Viettel, VNPT, CMC |
| Mạng lõi | Core network, 5G/4G | Viettel (dẫn đầu 5G), VNPT |
| Dịch vụ viễn thông | Di động, internet, IPTV | Viettel, VNPT, MobiFone |
| Data Center/Cloud | Cho thuê chỗ, cloud services | FPT, Viettel, VNPT, CMC |

---

## 4. CHUỖI GIÁ TRỊ GIÁO DỤC CÔNG NGHỆ (EdTech)

| Công Đoạn | Mô Tả | Biên Lợi Nhuận |
|-----------|-------|---------------|
| Đào tạo ĐH/Cao đẳng | Cử nhân, kỹ sư CNTT | 15-25% |
| Đào tạo ngắn hạn | Coding bootcamp, chứng chỉ | 25-35% |
| Nền tảng học trực tuyến | E-learning platforms | 40-60% |
| Xuất khẩu giáo dục | Du học, hợp tác quốc tế | 10-20% |
