# BEFORE evaluation fixture

Thư mục này kiểm chứng **cơ chế** của bundle BEFORE bằng Python stdlib, trong workspace tạm. Không phải đánh giá năng lực agent/LLM.

## Chạy

```bash
python evaluations/before/run_fixture.py
python evaluations/before/policy_model.py
python evaluations/before/check_bundle.py
```

- `run_fixture.py`: chạy unittest thật trên candidate thật cho A, B, D, E; kiểm tra exit code, lý do fail, contract/test hash không đổi.
- `policy_model.py`: kiểm tra bất biến của decision record cho C, F, G, H, I, J. Đây là mô hình policy deterministic, **không** chạy agent.
- `check_bundle.py`: kiểm file bắt buộc, mode/reference, ID D/PI/HM có trong canonical + snapshot, và sync marker.

## Phạm vi đã kiểm chứng

| Case | Cách kiểm chứng | Ý nghĩa |
|---|---|---|
| A | RED thật (`NotImplementedError`) → GREEN thật; safety pass. | Mini-goal atomic, evidence có exit code. |
| B | Candidate lỗi rounding → fail; candidate đúng → pass; test/contract hash không đổi. | Sửa trong scope, không sửa test/contract, không xin approval lại. |
| D | Acceptance pass nhưng safety fail (`float` thay vì `int` cents) → không release-ready; sửa thì pass. | Safety invariant chặn release dù acceptance xanh. |
| E | Baseline GREEN → refactor làm đổi output → regression fail → khôi phục pass. | Không tạo RED giả; regression bảo vệ behavior. |
| C, F, G, H, I, J | Policy model deterministic. | Bất biến quyết định, không phải hành vi LLM. |

## Không kiểm chứng

- Không chạy agent/LLM nào; không có forward-eval.
- Không có UAT thật, production data, deployment, pilot metric hay người dùng thật.
- Không chứng minh skill được discover trong Codex runtime.
- Không chứng minh BEFORE hiệu quả hơn BASELINE.

## Forward evaluation

`forward-scenarios.md` chứa sáu prompt lõi và bốn prompt mở rộng cho một Codex/agent độc lập. Khi chạy:

1. Tạo workspace tạm riêng cho từng scenario; không dùng chung để tránh contamination.
2. Chỉ cung cấp artifact thô cần thiết (contract, test, repo) và prompt; không đưa đáp án, bug suspected hay kết luận mong đợi.
3. Ghi lại artifact, command/exit, hành vi quan sát và giới hạn. Không tự nhận là đã chạy nếu chưa chạy.
4. Không cho scenario chạm production, secret hay external service.

## Independent evaluation bổ sung

Xem `independent-forward-report.md`: 10 case đã được agent độc lập áp dụng skill, với hành động mô phỏng và giới hạn ghi rõ. Báo cáo validation ở root là nguồn kết quả cuối sau editorial review. Policy model chỉ là minh họa deterministic, không được tính thay cho đánh giá agent.
