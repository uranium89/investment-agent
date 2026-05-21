# Lộ trình phát triển

## Đã hoàn thành — Phase 2: Scoring Engine ✅

### Scoring Engine
- [x] VMQ30 scoring model:
  - Quality Score (ROE, D/E, FCF Yield)
  - Value Score (P/E percentile trong VN30)
  - Technical Score (trend + momentum)
  - Moat Score (định kỳ)
  - Management Score (insider transactions)
  - Macro overlay (lãi suất, VN-Index trend)
- [x] Screening gate: D/E, ROE (3 năm), Market Cap, ADTV, FCF
- [x] Portfolio construction (top ENTER signals, sector caps)
- [x] TCBS PDF parser cho balance sheet data
- [x] Pipeline real data 32 VN30 symbols → 1 ENTER (VNM), 11 HOLD

## ✅ Đã hoàn thành — Phase 3: Execution & Monitoring

### Tuần 1: Execution & OTP ✅
- [x] DNSE OTP flow integration (email OTP → trading token)
- [x] Human-in-the-loop approval workflow (file-based JSON, polling, timeout)
- [x] Order management (place → confirm → reconcile)

### Tuần 2: Monitoring ✅
- [x] Telegram alerting (trade signals, risk breach)
- [x] Grafana dashboard (P&L, drawdown, signals) — JSON panel template
- [x] Daily performance report auto-generate

### Tuần 3: Risk Management ✅
- [x] Max drawdown control (configurable 10%/15%/20%)
- [x] Black swan protocol (VN-Index -5% trigger → FREEZE_ALL)
- [x] Sector exposure monitoring (breach detection)

### Tuần 4: Paper Trading
- [ ] Chạy paper trading với dữ liệu lịch sử (script có sẵn: `paper_trading.py`)
- [ ] So sánh signal vs execution (slippage estimate)
- [ ] Điều chỉnh parameters (thresholds, weights)
- [ ] Tài liệu hóa kết quả

## Roadmap 90 ngày — Live Trading

### Tháng 2: Live — Giai đoạn 1
- [ ] Live với vốn 10-20 triệu VND (2-3 positions)
- [ ] Tight monitoring: daily review
- [ ] So sánh paper vs live performance
- [ ] Điều chỉnh scoring weights dựa trên thực tế

### Tháng 3: Scale
- [ ] Scale lên 50 triệu → 200 triệu
- [ ] Backtesting engine hoàn chỉnh
- [ ] Stress test: VN30 -30%, -40%, -50%
- [ ] AI layer: news/sentiment analysis

## KPI quan trọng

### Safety KPIs (ưu tiên cao nhất)
| Metric | Target | Ghi chú |
|---|---|---|
| Max Drawdown (6 tháng) | < 15% | Rolling window |
| Risk limit breach | 0 | Tuyệt đối |
| Win rate | 45-55% | Kỳ vọng |
| Average hold time | > 20 ngày | Chống day trading |
| Cash position | 20-30% | Luôn duy trì |

### Performance KPIs
| Metric | Target |
|---|---|
| Sharpe Ratio | > 0.8 |
| Sortino Ratio | > 1.0 |
| Alpha vs VN30 | > 3%/năm |
| Beta | 0.6-0.9 |
| Information Ratio | > 0.5 |

### Operational KPIs
| Metric | Target |
|---|---|
| Data ingestion success | > 99% |
| Signal latency | < 15 phút |
| System uptime | > 99.5% |
| Failed orders | < 1% |

## Failure modes nguy hiểm nhất

| Failure Mode | Probability | Impact | Giải pháp |
|---|---|---|---|
| DNSE OTP timeout | Cao | Cao | Retry 3 lần, fallback manual |
| FireAnt data sai/trễ | Trung bình | Cao | Cross-check, versioning |
| API key expired | Thấp | Cao | Monitoring + alert |
| Lỗi logic scoring | Trung bình | Rất cao | Backtest + code review |
| Market crash overnight | Thấp | Rất cao | Black swan protocol |
| Lỗi position sizing | Thấp | Rất cao | Double-check, max limit |
| AI hallucination signal | Trung bình | Cao | Human approval gate |
| DB corruption | Thấp | Cao | Daily backup |
| Thay đổi API không báo | Trung bình | Cao | Integration test hàng ngày |

## Những thứ tuyệt đối không được làm

```
1. ❌ KHÔNG dùng margin (vay ký quỹ)
2. ❌ KHÔNG để AI quyết định trade cuối cùng
3. ❌ KHÔNG day trade hoặc scalping
4. ❌ KHÔNG deviating khỏi risk management rules
5. ❌ KHÔNG deploy code chưa qua backtest 2 năm
6. ❌ KHÔNG giao dịch cổ phiếu ngoài VN30
7. ❌ KHÔNG bỏ qua lỗi hệ thống
```
