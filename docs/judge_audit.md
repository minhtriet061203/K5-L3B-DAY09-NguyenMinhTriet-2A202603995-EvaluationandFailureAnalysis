# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Đạt (tp 24, fp 4, fn 6, tn 66) | dùng (chỉ cho giọng văn, không chặn release một mình) |
| helpful | 100 | 0.375 | 1.000 | 0.300 | **Không** (tp 9, fp 0, fn 21, tn 70) | loại |

Tỉ lệ fail sau hiệu chỉnh Rogan-Gladen: tone 0.28 → 0.30; helpful 0.09 → 0.30 (judge bỏ sót 2/3 lỗi thật).

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú / sửa rubric |
|---|---|---|---|---|---|
| 1 | H-008 "Em đã hoàn tiền cho anh rồi nha…" | PASS | FAIL | Người | Rubric thêm: xưng "em/anh", "nha" là suồng sã với khách → FAIL. |
| 2 | H-017 "Dạ, bạn ơi LogiX đã hoàn…" | PASS | FAIL | Người | Rubric: chỉ dùng "anh/chị" hoặc "quý khách", không "bạn". |
| 3 | H-029 "…không cần nhắn thêm." | PASS | FAIL | Người | Có "Dạ, vui lòng" không đủ; câu ra lệnh/cắt ngang khách → FAIL. Thêm ví dụ âm. |
| 4 | H-042 "…Tiền về trong 3–5 ngày ạ." | FAIL | PASS | Người | Không bắt buộc xin lỗi khi đã hoàn đủ; bỏ tiêu chí "thiếu xin lỗi". |
| 5 | H-051 "…đã refund 90.000đ…" | FAIL | PASS | Người | CS LogiX cho phép "refund"; ghi rõ danh sách từ tiếng Anh được phép. |
| 6 | H-081 "…chưa đủ điều kiện hoàn…" | FAIL | PASS | **Judge** | Nhãn người sai (đọc nhầm ticket) → sửa nhãn người, không sửa rubric. |
| 7 | H-094 "Da, LogiX da hoan…" (mất dấu) | PASS | FAIL | Người | Rubric: tiếng Việt không dấu → FAIL. |
| 8 | HL-015 "…đã hoàn 55.000đ…" (ledger 40.000đ) | PASS | FAIL | Người | Judge helpful không đọc ledger; 18/21 lỗi bỏ sót là **sai tiền**. |

## Kết luận
- **helpful bị loại**: recall 0.30 < 0.7 và κ 0.375 < 0.6. Ma trận cho thấy fn = 21: judge PASS mọi reply lịch sự kể cả khi số tiền sai (18 case "sai tiền", 3 case "sai xưng hô"). Precision 1.0 chỉ vì judge gần như không bao giờ nói FAIL. Dùng làm gate sẽ cho qua đúng loại lỗi đắt nhất. Sai tiền thuộc FM-08 và được chấm bằng code (`reply_matches_ledger` đối chiếu ledger), không bằng judge.
- **tone_ok dùng được** nhưng chỉ để theo dõi giọng văn; 6/10 bất đồng là judge cho qua lỗi giọng văn (xưng hô suồng sã, ra lệnh, emoji, mất dấu, hứa ngoài hệ thống) → bổ sung ví dụ âm vào rubric rồi calibrate lại.
- Rủi ro còn lại: judge chỉ được kiểm trên CSV replay đã công khai; cần nhãn người mới để có held-out thật.