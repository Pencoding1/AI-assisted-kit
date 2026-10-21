# BEFORE — Decision snapshot v1.0

**Snapshot ID:** `BEFORE-DECISIONS-1.0`  
**Ngày:** 2026-10-21  
**Trạng thái:** `APPROVED_LOCKED`  
**Tên đầy đủ:** A Behavior-First, Layer-Gated Engineering Methodology for AI-Assisted Software Development

> **Canonical:** Trong bundle gốc, `BEFORE_DECISIONS.md` ở root là bản canonical. File này là snapshot portable để mang skill sang repository khác. Khi canonical đổi version, snapshot phải được cập nhật trong cùng change request; nếu lệch, dừng và báo divergence, không tự chọn bản thuận lợi cho gate.

## Quyết định cốt lõi

**D-01 — Tên/phạm vi.** Tên cuối cùng là BEFORE; mô tả đầy đủ giữ nguyên như trên. BEFORE chỉ thay thế tên `LGD` và `BF-LD`; giữ tài liệu nguồn lịch sử. Đây là working agreement + skill bundle, không phải framework kiến trúc/hệ thống sản phẩm/cam kết hiệu quả. Không cài global, không đổi provider/model.

**D-02 — Sáu phase và RGR.** Phase 0 contract definition & freeze; 1 MVP rapid implementation; 2 modularization; 3 delivery & UAT; 4 hardening & refactor; 5 tracking & repeat. RGR bên trong mini-goal là nhịp khác phase ngoài; không ánh xạ RED/GREEN/REFACTOR thành Phase 0/1/4. Refactor phần đã GREEN cần regression baseline, không cần RED giả. Phase không phải waterfall cứng.

**D-03 — Thẩm quyền.** `Project rubric/scope → Feature → Module → Implementation`. L0 feature, L1 interaction, L2 module behavior, L3 implementation là control view, không phải kiến trúc cố định. Agent đề xuất implementation trong boundary đã duyệt; không tự định nghĩa lại behavior/invariant/scope.

**D-04 — Discovery tuần tự.** Một quyết định/câu hỏi tại một thời điểm; không batch phỏng vấn. Tái sử dụng câu trả lời. Có rubric → dùng rubric + scope; chỉ có scope → dùng scope; không có cả hai → phỏng vấn BA trước Phase 0. Cần test case hoặc expected output; thiếu cả hai phải làm rõ trước implementation. Ưu tiên happy path + critical risk invariant; không bùng nổ edge case ít giá trị.

**D-05 — Vertical slice/atomic.** Slice xuyên lớp, tạo outcome độc lập có ý nghĩa. Tiêu chí dừng `[OPERATIONAL]`: outcome đã độc lập, có thể kiểm thử/kiểm chứng; chia nhỏ hơn chỉ thêm chi tiết implementation thì dừng. Không phải quote người dùng, không phải quota depth.

**D-06 — Rolling freeze.** Freeze/version/approve contract của phần sẵn sàng + upstream/dependency trực tiếp trước implementation; không freeze toàn hệ thống tương lai. Có thể code module đã sẵn sàng trong khi định nghĩa module/feature kế tiếp; không cần module N xong mới định nghĩa N+1. Không tự tạo parallel agents. Dependency chưa xác minh = `NOT VERIFIED`; mock không chứng minh integration. Global freeze một lần của bản cũ bị thay thế. Commit chỉ khi policy/quyền cho phép; không tuyên bố commit khi không có, ghi gap và tôn trọng commit gate.

**D-07 — Bounded autonomy.** Tự loop mini-goal đã duyệt, sửa fail trong scope, verify và tiếp tục không xin phê duyệt lại. Backlog mới = proposal, không phải scope. Escalate khi xung đột contract/scope; chi phí/rủi ro không tương xứng (nêu phương án gốc/thay thế/trade-off); rủi ro cao/khó đảo ngược/security/data/interface; thiếu thẩm quyền/thông tin. Trigger nghiệp vụ mới không nới lỏng safety boundary. Không silent contract/test weakening; thay đổi phải có change request (impacted cases, rationale, approval, version mới). Escalation chỉ khi xung đột có căn cứ cụ thể.

**D-08 — State và vận hành.** Persistent state Markdown, ưu tiên tài liệu hiện có. State: `BACKLOG`, `READY`, `ACTIVE`, `FIXING`, `VERIFIED`, `DONE`, `APPROVAL_NEEDED`, `BLOCKED`, `REOPENED`. `BLOCKED` có bằng chứng, phân loại `BLOCKED_USER`/`BLOCKED_EXTERNAL`; không dùng vì khó. Secret chỉ qua kênh an toàn, không ghi Markdown/prompt/log. Lỗi code/config agent sửa trong scope; rate limit/API policy phải tuân thủ; external failure không chứng minh code sai. LLM output verify schema/invariant/tiêu chí đã duyệt. Migration kiểm integrity/compatibility/recovery trước release.

**D-09 — Safety/instrumentation.** Safety baseline + instrumentation cơ bản từ Phase 1. Coverage/retry budget/telemetry/hardening cadence phải hỏi tuần tự theo dự án; không hardcode default/đoán budget. Chỉ block công việc phụ thuộc trực tiếp vào ngưỡng thiếu.

**D-10 — UAT/regression/test integrity.** UAT case được người thật xác nhận và production bug đã xác nhận tạo regression có link. Characterization observed ≠ approved; bug không tự thành contract. Nondeterminism dùng invariant/schema/tolerance có lý do. Không skip/bỏ assertion/mock mất nghĩa/nới threshold/sửa expected output để xanh. Agent không tự tuyên bố UAT pass hoặc deploy accepted.

**D-11 — Mutation.** Phase 5 sau Phase 4; statistical + risk convergence; critical logic được kiểm chứng, không chỉ score; không phải gate mọi MVP. Bốn stop condition lịch sử không có trong artifact → `[HISTORICAL-MISSING]`, không bịa. Phải hỏi chính sách dừng được duyệt cho dự án trước khi chạy. Behavior chưa rõ → proposal backlog.

**D-12 — Pilot.** Một tháng BEFORE vs BASELINE, Markdown session log. Metric: delivery lead time (feature start → human deployment acceptance; gồm chạy và chờ), human attention (tổng thời gian can thiệp thực tế), cold-start, intervention count, rework, accepted deployment evidence (con người chấp nhận), defect rate với window xác định. Schema lịch sử + grounded-conflict-only escalation đã duyệt. Không automation. Pilot chưa hoàn thành; không có dữ liệu/UAT thật/baseline trong bundle. Kết quả chỉ quan sát, có giới hạn; không tuyên bố nhân quả/hiệu quả. Human accept deploy không do agent tuyên bố.

**D-13 — Báo cáo/traceability.** Decision nhẹ có rationale, alternatives, reversibility, owner, goal link. Báo cáo tách `VERIFIED FACT`/`INFERENCE`/`ASSUMPTION`/`PROPOSAL`/`BLOCKER`; thiếu evidence = `NOT VERIFIED`. Unit xanh ≠ release ready. Trace `goal → contract/version → test → diff → observation`. Không áp đặt tech/folder/coverage/agent/retry.

**D-14 — Bundle.** Một skill `before`; mode: `define-contract`, `execute-mini-goal`, `verify-gate`, `refactor-safely`, `capture-feedback/replan` (mode cuối gồm hai hành động). `SKILL.md` ngắn + references + assets template; không generic boilerplate/framework/production implementation.

## Mapping rút gọn

- ID theo bảng đã trình duyệt trong chat: `U1` → D-03/D-07/D-13; `U2` → D-02; `U3` → D-03/D-05/D-06; `U4` → D-02/D-10; `U5` → D-02/D-09; `U6` → D-12/D-13; `U7` → D-03/D-07/D-13.
- `P1` → D-01 (tên cũ bị thay thế); `P2` → D-03; `P3` → D-05; `P4` → D-09; `P5` → D-06/D-07/D-10; `P6` → D-07; `P7` → D-14; `P8` → D-04/D-06 (global freeze bị thay thế); `P9` → D-08; `P10` → D-12.
- `O1` → D-05 (vận hành); `O2` → D-07/D-09 + PI-01; `O3` → D-08/D-09/D-10 + PI-02; `O4` → D-08; `O5` → D-11 + PI-04; `O6` → D-09 + PI-03; `O7` → D-12.
- `C1` rolling freeze → D-06; `C2` trạng thái phê duyệt bootstrap/handoff được giải quyết bằng phê duyệt các đề xuất còn lại trong chat → D-01 đến D-14.

## Project interview bắt buộc

Không hardcode; hỏi tuần tự khi cần: rubric/rủi ro/approver (PI-01); quality gate external API/LLM/migration (PI-02); coverage/retry/telemetry/hardening (PI-03); mutation stop policy (PI-04); UAT/deploy authority (PI-05); commit gate (PI-06); test command/paths/secure channel (PI-07); pilot baseline/window/schema (PI-08).

## Historical missing

**HM-01** Bốn mutation stop conditions không có trong artifact. **HM-02** Pilot chưa chạy. **HM-03** Không có UAT/production/deployment evidence thật. **HM-04** Chưa commit v1. **HM-05** Không có transcript nguyên văn (chỉ tóm lược phê duyệt). **HM-06** `BF-LD` không có tài liệu nguồn riêng. **HM-07** Discovery của `.agents/skills/before` trong Codex runtime phiên mới chưa được quan sát.

## Lock

`v1.0` approved 2026-10-21. Lock là governance, **không phải OS read-only/ACL**. Chỉ sửa qua change request có lý do, impacted cases, alternatives/trade-off, risk/reversibility, owner/approver, version mới, regression plan. Không sửa trực tiếp để khớp code/test. Hash được ghi trong `BEFORE_VALIDATION.md` sau review cuối; hash chỉ chứng minh toàn vẹn artifact, không chứng minh nội dung đúng. Không commit nếu chưa được phép.
