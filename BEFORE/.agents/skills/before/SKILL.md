---
name: before
description: "Điều phối phát triển AI-assisted theo BEFORE — Behavior-First, Layer-Gated: chốt hợp đồng hành vi tuần tự, triển khai mini-goal nhỏ, giữ test integrity, kiểm gate bằng evidence và biến UAT/feedback thành regression có kiểm soát. Dùng khi cần định nghĩa contract trước khi code, chạy/verify mini-goal, refactor an toàn hoặc replan từ feedback. Có thể bắt đầu bằng discovery khi chưa có contract; không thay thế review kiến trúc/bảo mật chuyên biệt."
metadata:
  short-description: "Behavior-first, layer-gated delivery"
---

# BEFORE

BEFORE là working agreement để agent tự chủ trong boundary đã duyệt, không tự định nghĩa lại điều gì là đúng. Tên đầy đủ: **A Behavior-First, Layer-Gated Engineering Methodology for AI-Assisted Software Development**.

Đọc `references/decisions.md` trước khi áp dụng. Nếu repository có `BEFORE_DECISIONS.md`, bản đó là canonical; snapshot trong skill phải đồng bộ và không được thay thế canonical khi có xung đột.

## Khi nào dùng

Dùng khi người dùng yêu cầu:

- Xác định feature/module behavior, expected output, critical invariant trước implementation.
- Chia feature thành vertical-slice mini-goal và thực thi trong scope đã duyệt.
- Kiểm quality gate, đánh giá release readiness, xử lý fail trong scope.
- Refactor phần đã GREEN mà không đổi externally observable behavior.
- Chuyển UAT/production feedback thành regression và backlog có traceability.

Không dùng để:

- Thực hiện implementation khi behavior/expected output còn mơ hồ; vẫn dùng mode define-contract để làm rõ.
- Thay thế security review, architecture review, pháp lý/compliance hoặc phê duyệt deploy.
- Tạo framework kiến trúc, service, database hay multi-agent orchestrator.

## Ràng buộc không thương lượng

1. **Một câu hỏi tại một thời điểm.** Discovery tuần tự, không gom phỏng vấn hàng loạt; tái sử dụng câu trả lời đã có.
2. **Không code khi thiếu behavior.** Cần test case cụ thể hoặc expected output. Nếu không có rubric/scope, phỏng vấn BA trước Phase 0.
3. **Thẩm quyền:** `Project rubric/scope → Feature → Module → Implementation`. L0 feature, L1 interaction, L2 module behavior, L3 implementation là control view, không phải kiến trúc cố định. Agent chỉ đề xuất implementation trong boundary đã duyệt.
4. **Rolling freeze:** chỉ freeze contract của phần sẵn sàng cùng upstream/dependency trực tiếp trước khi code. Không freeze toàn hệ thống tương lai, không bắt module N xong mới định nghĩa N+1. Dependency mới ở mức mock là `NOT VERIFIED`.
5. **Bounded autonomy:** tự loop mini-goal đã duyệt, tự sửa lỗi trong scope, tự verify và tiếp tục. Không xin phê duyệt lại từng bước. Backlog mới là `PROPOSAL`, không phải scope.
6. **Escalate có căn cứ:** xung đột contract/scope, chi phí/rủi ro không tương xứng, thay đổi rủi ro cao/khó đảo ngược/security/data/interface, hoặc thiếu thẩm quyền/thông tin. Nêu phương án gốc, thay thế và trade-off.
7. **Không làm yếu test:** không sửa expected output, bỏ assertion, skip, mock mất nghĩa, nới threshold hoặc chỉnh fixture để xanh. Thay đổi hợp lệ phải qua change request có impacted cases, rationale, approval và version mới.
8. **Evidence trước tuyên bố:** tách `VERIFIED FACT`, `INFERENCE`, `ASSUMPTION`, `PROPOSAL`, `BLOCKER`; thiếu evidence ghi `NOT VERIFIED`. Unit/acceptance xanh không đồng nghĩa release ready.
9. **Safety baseline từ Phase 1**, instrumentation cơ bản từ Phase 1. Coverage/retry/telemetry/hardening cadence phải hỏi theo dự án, không hardcode.
10. **State bằng Markdown**, ưu tiên tài liệu hiện có: `BACKLOG → READY → ACTIVE → FIXING/VERIFIED → DONE`, nhánh `APPROVAL_NEEDED`, `BLOCKED`, `REOPENED`. `BLOCKED` phải có bằng chứng và phân loại `BLOCKED_USER`/`BLOCKED_EXTERNAL`.
11. **Không ghi secret** vào Markdown, prompt, log hay test. Không tự tạo key, không giả lập live pass. Lỗi external không phải bằng chứng code sai.
12. **Không tuyên bố UAT/deploy/pilot** thay người dùng. Không tạo commit nếu policy/quyền không cho phép.

## Chọn mode

| Mode | Dùng khi | Đọc |
|---|---|---|
| `define-contract` | Cần làm rõ behavior, expected output, invariant, boundary trước code. | `references/contract-and-discovery.md` |
| `execute-mini-goal` | Contract của phần hiện tại đã sẵn sàng; cần triển khai một vertical slice nhỏ. | `references/execution-gates-lifecycle.md` |
| `verify-gate` | Cần đánh giá evidence, release readiness hoặc xử lý fail trong scope. | `references/execution-gates-lifecycle.md` |
| `refactor-safely` | Cần đổi cấu trúc phần đã GREEN mà giữ observable behavior. | `references/execution-gates-lifecycle.md` |
| `capture-feedback/replan` | Có UAT/production feedback, bug đã xác nhận hoặc cần backlog vòng tiếp. | `references/feedback-and-pilot.md` |

`capture-feedback/replan` là một mode với hai hành động: ghi nhận feedback (`capture-feedback`) và cập nhật backlog/proposal (`replan`); không tự mở rộng scope. Sáu entry action: `define-contract`, `execute-mini-goal`, `verify-gate`, `refactor-safely`, `capture-feedback`, `replan` — gom thành năm tên mode như bảng trên.

## Vòng làm việc tối thiểu

1. **Xác định mode** và đọc đúng reference; không nạp toàn bộ tài liệu nếu không cần.
2. **Kiểm tra đầu vào:** contract/version, scope, expected output/test case, invariant, dependency status, quyền và môi trường.
3. **Nếu thiếu quyết định:** hỏi đúng một câu hiện tại, kèm lựa chọn/trade-off nếu hữu ích; chỉ dừng implementation phụ thuộc quyết định đó. Phần độc lập đã approved vẫn tiếp tục.
4. **Thực thi một mini-goal:** nếu behavior thiếu, viết RED đúng lý do rồi GREEN tối thiểu; nếu đã đúng, verify và ghi nhận mà không tạo RED giả hay sửa code vô ích. Chạy safety và ghi output/exit thật.
5. **Verify:** đối chiếu acceptance + safety + invariant; ghi deviations, assumptions, `NOT VERIFIED`; chỉ chuyển `VERIFIED` khi evidence thật.
6. **Tiếp tục hoặc escalate:** nếu còn mini-goal đã duyệt thì tiếp tục không hỏi lại; nếu chạm boundary thì `APPROVAL_NEEDED`/`BLOCKED` kèm bằng chứng.

Khi refactor phần đã GREEN: chạy regression baseline trước, thay đổi nhỏ, chạy lại; **không tạo RED giả**. RED chỉ hợp lệ khi behavior thực sự chưa tồn tại hoặc bug đã được xác nhận.

## Template

Dùng trong `assets/`, copy rồi điền; không coi template là contract đã duyệt:

| File | Mục đích |
|---|---|
| `project-rubric.template.md` | Cấu hình rubric/scope, quyền, gate, test command, path, commit policy của dự án. |
| `behavior-contract.template.md` | Feature/module behavior, expected output, invariant, dependency, trạng thái freeze. |
| `mini-goal.template.md` | Scope, test, invariant, evidence và điểm dừng của một đơn vị triển khai. |
| `evidence.template.md` | Diff/command/exit/test result, truth labels và release readiness. |
| `change-request.template.md` | Yêu cầu đổi contract/test đã duyệt, impacted cases và version mới. |
| `decision-assumption.template.md` | Quyết định/giả định nhẹ với rationale, alternative, reversibility, owner. |
| `uat-regression.template.md` | Map UAT case đã xác nhận sang regression, phân biệt observed và approved. |
| `pilot-log.template.md` | Session log BEFORE/BASELINE, metric, intervention, deploy evidence, limitation. |

## Báo cáo

Trả lời ngắn theo: mode/trạng thái → artifact đã đọc/ghi → hành động → command + exit + kết quả thật → `VERIFIED FACT` / `INFERENCE` / `ASSUMPTION` / `PROPOSAL` / `BLOCKER` → `NOT VERIFIED`/gap → bước tiếp theo. Không mô tả "đã pass" nếu chưa chạy; không gọi "production ready" từ unit test.
