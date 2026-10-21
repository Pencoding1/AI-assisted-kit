# Execution, gate và lifecycle

Đọc file này cho `execute-mini-goal`, `verify-gate` và `refactor-safely`.

## 1. Hai nhịp

**Nhịp ngoài — sáu phase:**

| Phase | Trọng tâm | Gate tối thiểu |
|---|---|---|
| 0 — Contract definition & freeze | Chốt behavior/expected output/invariant cho phần sẵn sàng; freeze cuốn chiếu. | Contract/version rõ; case hoặc expected output đủ; critical invariant; dependency status trung thực. |
| 1 — MVP rapid implementation | Vertical slice nhỏ nhất có giá trị; safety baseline + instrumentation cơ bản. | Acceptance + safety baseline pass; evidence thật; known debt được ghi. |
| 2 — Modularization | Làm rõ boundary đã lộ ra; không đổi behavior ngoài contract. | Test liên quan pass; interface/ownership được ghi; không có thay đổi observable ngoài contract. |
| 3 — Delivery & UAT | Người dùng/nghiệp vụ xác nhận workflow thật. | UAT case được người thật xác nhận hoặc ngoại lệ được duyệt; release safety gate đạt. |
| 4 — Hardening & refactor | Regression/reliability và cấu trúc, thay đổi nhỏ. | Behavior được bảo toàn; reliability goal đạt; không sửa test để "làm đẹp". |
| 5 — Tracking & repeat | Observation, triage, backlog/mini-goal mới. | Insight quan trọng có owner, rationale, testable outcome; proposal không tự thành scope. |

Phase không phải waterfall cứng. Feature mới có thể quay lại Phase 0 trong khi module đã release đang ở Phase 4/5. Không ép hoàn tất refactor lớn trước UAT nếu chưa có giá trị.

**Nhịp trong — RGR của mini-goal:**

- **RED:** test thể hiện behavior chưa có hoặc bug đã xác nhận; fail vì đúng lý do behavior, không vì lỗi môi trường/test.
- **GREEN:** thay đổi ít nhất cần thiết để đáp ứng test, kèm safety/regression liên quan.
- **REFACTOR:** đổi cấu trúc, giữ externally observable behavior; chạy regression sau từng bước nhỏ.

Không ánh xạ `RED/GREEN/REFACTOR` thành ba phase. Refactor phần đã GREEN không cần RED giả; cần regression baseline đủ mạnh.

## 2. Mini-goal

Một mini-goal đủ nhỏ để review diff/evidence hợp lý, đủ lớn để tạo tiến bộ. Tối thiểu:

- ID, phase, feature/parent, contract ref + version.
- Objective quan sát được.
- In-scope / out-of-scope.
- Input/output và boundary.
- Behavior criteria + critical invariant.
- Required test/regression.
- Lý do RED dự kiến (behavior thiếu hay bug đã xác nhận).
- Allowed changes/protected paths.
- Assumption/unknown.
- Required evidence.
- Risk level theo rubric dự án.
- Điểm dừng.

Dùng `assets/mini-goal.template.md`. Không cần mọi field nếu không áp dụng; không thêm field chỉ để đủ mẫu.

### 2.1. Điều kiện READY

- Contract của phần hiện tại đã freeze/approve.
- Expected output/test case đủ rõ.
- Dependency đã xác minh hoặc được đánh dấu `NOT VERIFIED` và không bị coi là tích hợp thật.
- Allowed path/quyền đủ để làm.
- Gate/evidence cần thiết xác định được.

Nếu thiếu: `APPROVAL_NEEDED`/`BLOCKED_USER`, hỏi đúng câu hiện tại. Không code thay thế.

## 3. Vòng thực thi

1. **Đọc contract/version** và xác nhận mini-goal vẫn nằm trong scope.
2. **Viết/chạy RED** (nếu behavior thực sự chưa có) và ghi lại command/exit/lý do fail.
3. **GREEN tối thiểu** trong allowed changes; không thêm cơ chế ngoài nhu cầu.
4. **Chạy safety + regression** liên quan, không chỉ test mới.
5. **Ghi evidence thật:** file/diff, command, exit, test name, output quan trọng, deviation.
6. **Chuyển trạng thái** chỉ khi gate đạt; nếu fail trong scope → `FIXING`, sửa và chạy lại không xin phê duyệt.
7. **Tiếp tục** mini-goal đã duyệt kế tiếp; không hỏi lại từng bước.

Không cần approval lặp lại cho việc đã nằm trong contract. Nhưng không được dùng autonomy để đổi contract, nới test hoặc mở rộng scope.

### 3.1. RED hợp lệ

- Behavior chưa tồn tại, hoặc bug đã được xác nhận bằng evidence.
- Test fail ở assertion/behavior mong đợi, không fail vì import sai, syntax, thiếu dependency môi trường, path sai.
- Expected output đến từ contract/case đã duyệt, không phải từ implementation hiện tại.
- Với bug: test tái hiện được bug trước khi sửa.

Nếu behavior đã thỏa contract: chạy verification/regression cần thiết và ghi nhận đã đáp ứng; không tạo RED giả, code change hoặc escalation thừa. Nếu fail vì môi trường/test lỗi, phân loại nguyên nhân; chỉ hỏi khi còn ambiguity thật về behavior. Không hạ test để có RED.

### 3.2. GREEN hợp lệ

- Thay đổi nhỏ nhất đáp ứng behavior, không thêm feature ngoài scope.
- Không sửa test/expected output để pass.
- Không mock mất phần contract đang cần chứng minh.
- Safety invariant vẫn đúng.
- Nếu phát hiện test sai: change request, không tự sửa.

### 3.3. Fail trong scope

- Lỗi implementation/config trong allowed path → tự sửa, chạy lại, ghi evidence.
- Không xin approval lại chỉ vì một lần fail.
- Nếu sửa nhiều lần vẫn fail vì thiếu thông tin/quyền → escalation có bằng chứng; không đoán budget/retry.

## 4. Verify gate

Trước khi gọi `VERIFIED` hoặc "release ready", kiểm:

- **Acceptance:** case chính + expected output pass.
- **Safety:** invariant dữ liệu/quyền/tiền/idempotency/side effect/failure handling liên quan pass.
- **Regression:** hành vi cũ liên quan không bị phá.
- **Test integrity:** không skip/weaken/mock away/sửa expected output trái phép.
- **Evidence:** command/exit/test name/diff thật; không có "pass" chưa chạy.
- **Dependency:** integration thật hay chỉ mock; mock → `NOT VERIFIED`.
- **Contract:** implementation khớp version đã freeze; deviation có change request.
- **Vận hành:** migration integrity/compatibility/recovery nếu có; side effect/rollback nếu rủi ro; instrumentation nếu cần.

Kết luận:

- `VERIFIED`: gate bắt buộc có evidence thật.
- `APPROVAL_NEEDED`: chạm contract/risk/authority boundary.
- `BLOCKED_USER`/`BLOCKED_EXTERNAL`: thiếu quyết định/quyền/dependency ngoài tầm kiểm soát, có bằng chứng cụ thể.
- `NOT VERIFIED`: chưa có evidence; không được thay bằng suy đoán.

**Unit/acceptance xanh không đồng nghĩa release ready.** Release còn cần safety, integration đúng mức, migration/recovery, deployment authority và evidence vận hành liên quan.

## 5. State machine

```text
BACKLOG → READY → ACTIVE → VERIFIED → DONE
                      │  ↑
                      ↓  │
                    FIXING
ACTIVE → APPROVAL_NEEDED → READY/ACTIVE (sau quyết định)
ACTIVE → BLOCKED → READY/ACTIVE (khi gỡ được, có evidence)
DONE → REOPENED (regression/bug có evidence)
```

- `BLOCKED` phải ghi `BLOCKED_USER` hoặc `BLOCKED_EXTERNAL` + evidence cụ thể. Không dùng `BLOCKED` cho khó khăn thông thường.
- Chỉ block công việc phụ thuộc trực tiếp vào phần thiếu. Phần độc lập vẫn có thể tiếp tục nếu approved.
- Không tự chuyển `DONE` khi mới `VERIFIED` nếu policy dự án yêu cầu thêm acceptance/commit/release bước.

## 6. Bounded autonomy và escalation

Agent được tự:

- Chia nhỏ backlog đã duyệt thành mini-goal theo dependency/impact.
- Chọn implementation trong boundary; thêm test cho logic mới/bug đã xác nhận.
- Chạy lại test, sửa fail trong scope, cập nhật evidence/known debt.
- Tạo backlog proposal từ phát hiện mới.

Phải dừng/escalate khi:

- Cần đổi behavior, expected output, invariant, public interface hoặc persisted schema.
- Thay đổi security/secret/authorization/compliance/PII/production có rủi ro cao.
- Migration khó rollback hoặc có nguy cơ mất dữ liệu thật.
- Chi phí/rủi ro không tương xứng lợi ích; phải trình bày phương án gốc, thay thế, trade-off.
- Cần dependency/quyền/ngân sách chưa được duyệt.
- Gate fail sau khi đã tự xử lý trong giới hạn hợp lý, hoặc thiếu thông tin khiến không thể xác nhận.

Cách escalate:

- Nêu **một** quyết định hiện tại.
- Nêu 1–3 lựa chọn nếu hữu ích, impact, recommendation, safe default.
- Gắn evidence/căn cứ cụ thể; không escalate xung đột chỉ vì phỏng đoán.
- Không gom nhiều quyết định không liên quan.

Gate security fail luôn chặn release. Sửa lỗi để khôi phục approved authorization trong allowed scope có thể tự làm nếu không tạo rủi ro mới đáng kể; thay policy/quyền, mở rộng access hoặc sửa rủi ro cao phải escalation. Tách gate thất bại khỏi rủi ro của phương án sửa.

## 7. Refactor an toàn

Trước refactor:

1. Xác nhận phần liên quan đang GREEN.
2. Chạy regression baseline; ghi command/exit.
3. Nếu legacy/characterization: ghi observed behavior và phân biệt rõ với approved behavior. Bug quan sát được không tự thành contract.
4. Xác định externally observable behavior cần giữ: output, error, side effect, ordering, schema, performance invariant (nếu có).

Trong refactor:

- Thay đổi nhỏ, chạy regression sau mỗi bước.
- Không đổi output/error/side effect ngoài contract.
- Không tạo RED giả; không sửa test để khớp cấu trúc mới nếu behavior không đổi.
- Nếu phát hiện behavior hiện tại sai contract: change request hoặc bug fix có test/evidence, không âm thầm "chuẩn hóa".

Sau refactor:

- Regression pass.
- Diff chỉ là cấu trúc/implementation trong allowed path.
- Ghi evidence trước/sau và xác nhận không đổi observable behavior.

Nếu refactor làm đổi output: test regression phải fail; khôi phục behavior tương thích hoặc trình change request. Không cập nhật expected output để pass.

## 8. External API, LLM output và lỗi môi trường

- Phân biệt lỗi code/config với lỗi external: HTTP 401/403 do thiếu quyền/key, rate limit, timeout, DNS, môi trường.
- Thiếu key/quyền/cấu hình chỉ người dùng cung cấp được: state `BLOCKED`, reason `BLOCKED_USER`, yêu cầu qua kênh an toàn. Provider/service ngoài quyền xử lý: state `BLOCKED`, reason `BLOCKED_EXTERNAL`. Không kết luận chỉ từ HTTP status; URL sai do code/config thì `FIXING`. External failure không chứng minh code sai.
- Tuân thủ rate-limit/retry policy của dự án; không tự tăng retry hoặc tạo key.
- Không đưa secret vào log/Markdown/test.
- Không tuyên bố live pass nếu chưa gọi thật; mock chỉ là `NOT VERIFIED`.
- Với output LLM: kiểm schema, invariant, tiêu chí đã duyệt và tolerance hợp lý; một sample đúng không phải oracle.

## 9. Commit và release

- Commit chỉ khi repo policy/quyền cho phép; nếu không, ghi gap và không tuyên bố.
- Trước release: migration integrity/compatibility/recovery, rollback/side effect, safety gate, evidence vận hành.
- Deploy acceptance phải do con người/owner xác nhận; agent không tự tuyên bố "đã được chấp nhận".
- Không chạy hành động không thể đảo ngược chỉ dựa trên assumption.

## 10. Báo cáo mode này

Theo thứ tự: trạng thái → contract/version → diff/artifact → command + exit + kết quả → acceptance/safety/regression → `VERIFIED FACT`/`INFERENCE`/`ASSUMPTION`/`PROPOSAL`/`BLOCKER` → `NOT VERIFIED`/gap → bước tiếp theo.
