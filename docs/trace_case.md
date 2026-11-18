# Trace case: từ trace tới quyết định sai đầu tiên

​```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
​```

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, report `E-seeded_regression-20261118-1c98` (eval set `1c981fa238dd`). Cùng lỗi xuất hiện ở baseline `swarm C-002@55` (`E-swarm-20261118-1c98`). |
| Triệu chứng | Grader Lab 8 FAIL `status resolved != denied`; `refund_amount_correct` FAIL (ledger 20.000đ, nhãn 0); `db_fact_kept` FAIL. Reply "Dạ, LogiX đã hoàn 20.000đ cho đơn O-202." khớp ledger nhưng ledger sai. |
| Bước sai đầu tiên | Event 3 `model_override {"delay_days": 5}` |
| Vì sao là bước *đầu tiên* | Event 1 `handoff` đúng hợp đồng (task `check_applicable_policy`, tool read-only). Event 2 `investigator` đọc đúng DB: O-202 `delay_days = 2`, status `delivered`. Event 3 thay 2 bằng số 5 lấy từ ticket ("giao trễ 5 ngày") → event 4 quote theo SHIP-LATE-03 (≥3 ngày) = 20.000đ. Mọi bước sau chỉ hệ quả. |
| Failure mode | FM-03 ticket_trust |
| Đối chứng | `fixed C-002@11`: không có `model_override`; event 3 quote `amount_vnd 0, no_entitlement`; status `denied`, ledger 0. |
| Regression test | `src/tests/test_lab9_trace_case.py`: `test_lab9_trace_case_c002_seed11_caught_on_seeded_regression` (assert có override trước quote, ledger 20.000, `DbFactKept`/`RefundAmountCorrect` = False) bắt được lỗi trên variant; `test_lab9_trace_case_c002_seed11_passes_on_fixed` PASS trên `fixed`. Chạy trong CI qua `pytest -m student -k "lab9 and not advanced"`. |
| Chưa chắc chắn | MockLLM chỉ mô phỏng việc tin ticket theo công tắc; với LLM thật, tần suất override phụ thuộc prompt và ticket, trace không cho biết xác suất. Trace cũng không ghi lời gọi `issue_refund`, nên thời điểm host ghi ledger chỉ suy ra từ snapshot. |