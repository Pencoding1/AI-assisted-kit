# BEFORE — Hướng dẫn sử dụng

BEFORE = **A Behavior-First, Layer-Gated Engineering Methodology for AI-Assisted Software Development**.

Bundle này gồm một skill điều phối `before`, các reference progressive disclosure, template nhỏ và một fixture kiểm chứng deterministic. Nó không phải framework kiến trúc, không phải hệ thống sản phẩm và không chứng minh hiệu quả thực nghiệm.

## 1. Vị trí và tích hợp

Skill nằm tại:

```text
.agents/skills/before/
  SKILL.md
  references/
  assets/
```

### Vì sao `.agents/skills`

- `LGD_HANDOFF.md` §13.2 gợi ý cấu trúc `.agents/skills/layer-gated-development/` và yêu cầu kiểm tra convention thực tế trước khi chọn đường dẫn.
- `CODEX_BOOTSTRAP_PROMPT.md` yêu cầu **inspect before create**, không ghi đè cấu trúc hiện có.
- Trong project này không có `AGENTS.md`, không có `.agents/skills` trước khi tạo, và không có skill nội bộ nào khác. `.agents/skills` là path repo-scoped, portable, không cài global và không đụng `$CODEX_HOME`.
- Đây là lựa chọn theo nguồn + bootstrap, **không phải** bằng chứng rằng mọi Codex runtime sẽ tự discover path này. Phải kiểm tra runtime đích.
- UI metadata `agents/openai.yaml` là optional và **không được đính kèm**: lần thử generator mặc định gặp lỗi encoding Windows. Có thể dùng chế độ Python UTF-8 khi cần tạo metadata; v1 không cần file này. `SKILL.md` vẫn có `metadata.short-description`; không có file UI metadata lỗi.

### Tích hợp vào project khác

1. Copy nguyên thư mục `.agents/skills/before/` vào repository đích.
2. Nếu repo đích dùng convention khác (`$CODEX_HOME/skills`, `.codex/skills`, v.v.), kiểm tra tài liệu runtime hiện hành rồi đặt đúng chỗ. **Không tự cài global** trong bundle này; nếu runtime chỉ hỗ trợ global, dừng và xin phép người dùng vì đó là thay đổi ngoài scope.
3. Nếu muốn nhắc agent dùng skill, thêm **một dòng ngắn** vào `AGENTS.md` của repo đích — chỉ khi có quyền và cần thiết:

   ```text
   Khi làm việc theo BEFORE, dùng $before và tuân thủ contract/evidence trong skill.
   ```

   Task tạo bundle này **không sửa `AGENTS.md`**.
4. Không sửa `LGD_HANDOFF.md`/`CODEX_BOOTSTRAP_PROMPT.md` để hợp thức hóa bundle.

### Discovery cần reload/phiên mới

Sau khi copy hoặc sửa skill:

- Reload/khởi động **phiên mới** để runtime scan lại skill.
- Kiểm tra bằng một prompt vô hại, ví dụ `$before define-contract ...`, và ghi lại hành vi quan sát.
- **Không hứa phiên hiện tại sẽ tự nhận skill.** Việc skill xuất hiện trong danh sách của harness đang tạo bundle không chứng minh Codex runtime đích sẽ discover/invoke đúng.
- Trạng thái discovery trong bundle này: `NOT VERIFIED` (xem `BEFORE_VALIDATION.md`).

## 2. Cách gọi

Năm tên mode (sáu entry action, vì `capture-feedback/replan` gồm hai hành động):

```text
$before define-contract ...
$before execute-mini-goal ...
$before verify-gate ...
$before refactor-safely ...
$before capture-feedback/replan ...
```

Ví dụ:

```text
$before define-contract cho feature FT-CHECKOUT-001.
Chỉ hỏi tôi một câu tại một thời điểm; dùng rubric/scope hiện có; chưa code.
```

```text
$before execute-mini-goal MG-CHECKOUT-003 theo contract FT-CHECKOUT-001 v2.
Tự sửa fail trong scope, không đổi test/contract, ghi command + exit + evidence.
```

```text
$before verify-gate cho MG-CHECKOUT-003.
Kiểm acceptance, safety, regression, integration thật hay chỉ mock; nếu thiếu evidence ghi NOT VERIFIED.
```

```text
$before refactor-safely module tính tiền đã GREEN.
Chạy regression baseline trước; không tạo RED giả; không đổi observable behavior.
```

```text
$before capture-feedback/replan từ bug production đã có repro.
Tạo regression, phân loại backlog; không tự mở rộng scope.
```

Nếu runtime không hỗ trợ cú pháp `$before`, gọi skill theo cơ chế của runtime đó; nội dung mode không đổi.

## 3. Chức năng từng file

| Path | Chức năng |
|---|---|
| `BEFORE_DECISIONS.md` | Canonical decision record v1.0: quyết định đã duyệt, mapping nguồn, project interview, historical missing, lock policy. |
| `BEFORE_USAGE.md` | File này: tích hợp, invocation, discovery, ví dụ end-to-end, purpose của từng file. |
| `BEFORE_VALIDATION.md` | Command/exit/kết quả validation thật, hash snapshot, giới hạn và independent forward-eval dạng mô phỏng. |
| `.agents/skills/before/SKILL.md` | Entrypoint ngắn: trigger, ràng buộc, chọn mode, template, báo cáo. |
| `.agents/skills/before/references/contract-and-discovery.md` | Discovery tuần tự, authority, atomic/vertical slice, rolling freeze, change control. |
| `.agents/skills/before/references/execution-gates-lifecycle.md` | Sáu phase, RGR, mini-goal, verify gate, state machine, bounded autonomy, refactor an toàn. |
| `.agents/skills/before/references/feedback-and-pilot.md` | UAT/production → regression, characterization, mutation, pilot metric/limitation. |
| `.agents/skills/before/references/decisions.md` | Snapshot portable của decision record; root canonical, phải sync khi version đổi. |
| `.agents/skills/before/assets/project-rubric.template.md` | Cấu hình rubric/scope/quyền/gate/test command/commit/secret channel của dự án. |
| `.agents/skills/before/assets/behavior-contract.template.md` | Feature/module behavior, case/expected output, invariant, dependency, freeze. |
| `.agents/skills/before/assets/mini-goal.template.md` | Scope, test, invariant, evidence, điểm dừng của một mini-goal. |
| `.agents/skills/before/assets/evidence.template.md` | Diff/command/exit/test result, truth labels, release readiness. |
| `.agents/skills/before/assets/change-request.template.md` | Yêu cầu đổi contract/test đã duyệt, impacted cases, alternatives, version mới. |
| `.agents/skills/before/assets/decision-assumption.template.md` | Decision/assumption nhẹ với rationale, reversibility, owner, goal link. |
| `.agents/skills/before/assets/uat-regression.template.md` | Map UAT case sang regression; phân biệt approved và observed. |
| `.agents/skills/before/assets/pilot-log.template.md` | Session log BEFORE/BASELINE với metric, intervention, deploy evidence, limitation. |
| `evaluations/before/README.md` | Cách chạy fixture, phạm vi đã/chưa kiểm chứng, hướng dẫn forward-eval. |
| `evaluations/before/run_fixture.py` | Chạy unittest thật cho A/B/D/E; kiểm exit, lý do fail, hash contract/test. |
| `evaluations/before/policy_model.py` | Mô hình policy deterministic cho C/F/G/H/I/J; không phải LLM eval. |
| `evaluations/before/check_bundle.py` | Kiểm cấu trúc bundle, mode/reference/template và sync marker D/PI/HM giữa canonical và snapshot. |
| `evaluations/before/fixture/` | Contract hư cấu FT-ORDER-001, candidate baseline/good/buggy/unsafe/refactor_bad, acceptance/safety tests. |
| `evaluations/before/independent-forward-report.md` | Bản đánh giá độc lập trên 10 tình huống; hành động mô phỏng, không claim tool execution. |
| `evaluations/before/forward-scenarios.md` | Sáu prompt lõi + bốn prompt mở rộng cho Codex độc lập. |

## 4. Ví dụ end-to-end: FT-ORDER-001

> **Cảnh báo hư cấu:** feature, tên vai trò, UAT và bối cảnh dưới đây là **hư cấu kỹ thuật**. Không có người dùng/nghiệp vụ thật nào đã xác nhận; không có production data, deployment hay pilot metric. Không được trích dẫn mục này như UAT đã được chấp nhận.

### 4.1. Contract và discovery

Feature: tính tổng đơn hàng bằng integer cents, giảm giá theo phần trăm, làm tròn half-up.

Rubric giả định: tiền là critical invariant; test command là `python -m unittest`; allowed path là `app/order_total.py`, `tests/`; commit gate chưa cấp.

Câu hỏi discovery đầu tiên (một câu):

> "Giảm giá áp dụng trên subtotal trước hay sau khi làm tròn từng dòng?"

Giả định trả lời: "Trên subtotal; làm tròn một lần ở tổng." Ghi vào contract. Không hỏi thêm edge case không ảnh hưởng invariant.

Contract rút gọn:

| Case | Input | Expected |
|---|---|---|
| A1 | `[(2, 50000), (1, 25000)]`, discount `10` | `112500` |
| A2 | `[(1, 9999)]`, discount `100` | `0` |
| A3 | `[(1, 5)]`, discount `50` | `3` |
| A4 | discount `101`/`-1` | `ValueError` |

Invariant: tổng là `int` cents, `0 <= total <= subtotal`; quantity `int >= 1`; unit price `int >= 0`; discount `int 0..100`.

### 4.2. RED → GREEN thật từ fixture

```text
python evaluations/before/run_fixture.py
```

Kết quả thật (rút gọn):

- A-RED: `exit=1`; `NotImplementedError: FT-ORDER-001 behavior not implemented`; `FAILED (errors=4)`.
- A-GREEN: `exit=0`; `OK`.
- A-SAFETY: `exit=0`; `OK`.

RED hợp lệ vì behavior chưa tồn tại, không phải vì test/môi trường sai. GREEN là implementation integer cents; contract/test hash không đổi.

### 4.3. UAT hư cấu và mapping

**UAT-ORDER-001 — HƯ CẤU, KHÔNG PHẢI UAT THẬT.**

- Vai trò: "kế toán giả định" (không có người thật).
- Case: đơn 2 × 50.000 + 1 × 25.000, giảm 10% → 112.500.
- Kết quả ghi nhận: "khớp expected trong ví dụ hư cấu".
- Người xác nhận: **không có**; trạng thái: `FICTIONAL / NOT ACCEPTED`.
- Không có deployment, không có production, không có defect rate.

Mapping giả định (chưa phải regression thật):

| UAT hư cấu | Test map | Trạng thái |
|---|---|---|
| A1 | `tests.acceptance.test_order_total.OrderTotalAcceptance.test_two_items_ten_percent_discount` | fixture pass |
| A3 | `...test_half_up_rounding` | fixture pass |
| Invariant tiền | `tests.safety.test_order_total...test_total_is_integer_cents` | fixture pass |

### 4.4. Refactor

`refactor_bad` đổi half-up thành floor. Kết quả thật:

- E-BASELINE (good): `exit=0`, `OK` — đã GREEN trước refactor.
- E-BAD-REFACTOR: `exit=1`, `AssertionError: 2 != 3`, `FAILED (failures=1)`.
- E-RESTORE: `exit=0`, `OK`.

Không có RED giả: baseline đã GREEN; regression bắt thay đổi observable output. Không sửa expected `3` thành `2`.

### 4.5. Exception và escalation

`unsafe` trả đúng giá trị nhưng dùng `float`:

- D-ACCEPTANCE: `exit=0`, `OK` — acceptance xanh.
- D-SAFETY: `exit=1`, `<class 'float'> is not <class 'int'>`, `FAILED (failures=2)`.
- Kết luận: **không release ready**; sửa về integer cents (D-FIX `exit=0`) hoặc block nếu không sửa được trong scope.

Nếu nghiệp vụ thực sự muốn banker's rounding thay vì half-up, đó là thay đổi contract: tạo change request với impacted case A3, rationale, alternatives, approval, version mới. Không tự sửa test.

### 4.6. Trace

```text
goal FT-ORDER-001
  → contract v1 (cases A1-A4, invariants)
  → MG-ORDER-001 (baseline → good)
  → acceptance/safety commands + exit
  → UAT hư cấu (không accepted) / regression mapping dự kiến
  → refactor (regression bắt output change)
  → exception D (safety block, fixed)
```

## 5. Giới hạn

- Fixture chỉ chứng minh cơ chế deterministic; không chứng minh LLM sẽ tuân thủ skill.
- Đã có lượt independent forward-eval trên 10 tình huống: hành động/response được mô phỏng, không phải 10 lượt implementation chạy thật. Xem `evaluations/before/independent-forward-report.md`.
- Chưa có UAT thật, production bug thật, deployment, pilot metric.
- Chưa chứng minh discovery trong Codex runtime đích.
- Chưa commit; commit gate vẫn là gap nếu repo yêu cầu.
