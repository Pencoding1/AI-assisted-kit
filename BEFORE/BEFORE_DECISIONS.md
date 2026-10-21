# BEFORE — Quyết định đã phê duyệt và khóa v1

**Tên:** BEFORE  
**Tên đầy đủ:** A Behavior-First, Layer-Gated Engineering Methodology for AI-Assisted Software Development  
**Phiên bản quyết định:** 1.0 — `APPROVED_LOCKED`  
**Ngày khóa:** 2026-10-21  
**Task:** `BEFORE-V1-20261021`  
**Ngôn ngữ:** tiếng Việt; thuật ngữ kỹ thuật giữ nguyên tiếng Anh.

> Tài liệu này là bản ghi quyết định, không phải transcript. Các nhãn `[USER-APPROVED]`, `[OPERATIONAL]`, `[PROJECT-INTERVIEW]`, `[HISTORICAL-MISSING]` phân biệt nguồn và mức thẩm quyền. Không có câu trích dẫn nguyên văn nào được tạo ra trong tài liệu này.

Theo brief `BEFORE-V1-20261021`, người dùng đã phê duyệt toàn bộ proposal còn lại trong danh sách trước. Các proposal của handoff được ánh xạ ở mục 5; không proposal nào ngoài danh sách đó được coi là đã duyệt.

## 0. Cách đọc và thẩm quyền

| Nhãn | Ý nghĩa | Được dùng để làm gì |
|---|---|---|
| `[USER-APPROVED]` | Nội dung người dùng đã phê duyệt trong danh sách quyết định của brief `BEFORE-V1-20261021`; đây là bản tóm lược phê duyệt, không phải bản ghi lời nói nguyên văn. | Ràng buộc thực thi của bundle. |
| `[OPERATIONAL]` | Cách diễn giải vận hành do agent soạn để thi hành quyết định đã duyệt; không phải phát biểu của người dùng. | Tiêu chí thao tác; có thể sửa bằng change request nếu sai. |
| `[PROJECT-INTERVIEW]` | Điểm phải hỏi tuần tự cho từng dự án; không được hardcode default. | Đầu vào cấu hình dự án. |
| `[HISTORICAL-MISSING]` | Dữ liệu lịch sử được nhắc tới nhưng không có trong artifact hiện có. | Ghi gap; không được bịa hoặc coi là đã xác minh. |

**Thẩm quyền:** quyết định người dùng đã duyệt là ràng buộc; cấu hình dự án được người dùng duyệt cụ thể hóa ràng buộc đó. Diễn giải `[OPERATIONAL]` không được lấn át quyết định hoặc cấu hình đã được duyệt. Khi xung đột, hỏi một quyết định hiện tại; không tự nâng proposal thành approved scope.

## 1. Tên, phạm vi và supersession

### D-01 — Tên và phạm vi bundle `[USER-APPROVED]`

- Tên cuối cùng là **BEFORE**.
- Tên đầy đủ, giữ chính xác: **A Behavior-First, Layer-Gated Engineering Methodology for AI-Assisted Software Development**.
- BEFORE thay thế **chỉ tên** `LGD` và `BF-LD`. Các tài liệu nguồn lịch sử (`LGD_HANDOFF.md`, `CODEX_BOOTSTRAP_PROMPT.md`) được giữ nguyên, không viết lại để hợp thức hóa tên mới.
- Đây là working agreement + skill bundle để điều phối công việc AI-assisted. Không phải framework kiến trúc, không phải hệ thống sản phẩm, không phải cam kết hiệu quả đã được chứng minh.
- Bundle không cài đặt global, không tạo dịch vụ/database/orchestrator, không thay đổi provider/model.

### D-02 — Sáu phase và RGR `[USER-APPROVED]`

Lifecycle ngoài gồm sáu phase:

| Phase | Tên | Mục đích tối thiểu |
|---|---|---|
| 0 | Contract definition & freeze | Xác định behavior, expected output và critical invariant cho phần đã sẵn sàng; freeze đúng phần đó trước implementation. |
| 1 | MVP rapid implementation | Triển khai vertical slice nhỏ nhất có giá trị, kèm safety baseline và instrumentation cơ bản. |
| 2 | Modularization | Làm rõ boundary/interface đã lộ ra trong quá trình triển khai; không đổi behavior ngoài contract. |
| 3 | Delivery & UAT | Người dùng/nghiệp vụ xác nhận use case thật; chốt release decision và evidence. |
| 4 | Hardening & refactor | Củng cố regression/reliability và cấu trúc bằng thay đổi nhỏ có kiểm chứng. |
| 5 | Tracking & repeat | Thu observation, triage feedback, tạo backlog/mini-goal và quay lại vòng tiếp theo. |

- Vòng **RGR bên trong mini-goal** là một nhịp khác với sáu phase ngoài. Không được ánh xạ máy móc `RED = Phase 0`, `GREEN = Phase 1`, `REFACTOR = Phase 4`.
- Refactor một phần **đã GREEN** không bắt buộc tạo RED giả. Điều kiện là có regression baseline đủ bảo vệ hành vi quan sát được trước khi refactor.
- Phase không phải waterfall cứng: feature mới có thể quay lại Phase 0 trong khi module đã release đang ở Phase 4/5.

### D-03 — Thứ bậc thẩm quyền và bốn control view `[USER-APPROVED]`

Thứ bậc thẩm quyền:

`Project rubric/scope → Feature → Module → Implementation`

Bốn lớp là **control view**, không phải kiến trúc cố định hay sơ đồ thư mục bắt buộc:

| View | Câu hỏi kiểm soát |
|---|---|
| L0 — Feature behavior | Người dùng/nghiệp vụ quan sát được gì? |
| L1 — Interaction | Các capability/module kết nối, trao đổi dữ liệu và lỗi thế nào? |
| L2 — Module behavior | Module hành xử đúng trong luồng thường, lỗi và side effect ra sao? |
| L3 — Implementation | Dùng cấu trúc/thuật toán/thư viện nào? |

- Agent được đề xuất implementation trong boundary đã duyệt; không được tự định nghĩa lại behavior, expected output, invariant hoặc scope nghiệp vụ.
- L0–L3 không bắt buộc mọi dự án phải tạo đủ tài liệu cho mọi lớp. Chỉ tạo contract tối thiểu đủ kiểm soát behavior/invariant đang triển khai.

## 2. Khám phá hành vi và hợp đồng

### D-04 — Discovery tuần tự, một quyết định tại một thời điểm `[USER-APPROVED]`

- Khám phá behavior diễn ra tuần tự. Tại mỗi thời điểm chỉ hỏi **một** quyết định/câu hỏi hiện tại; không gom nhiều câu hỏi thành một buổi phỏng vấn hàng loạt.
- Câu trả lời đã có được tái sử dụng; không hỏi lại chỉ vì mở mode/phiên khác nếu câu trả lời đã được ghi và vẫn còn hiệu lực.
- Nếu có rubric: dùng rubric + scope để xác định phần thiếu. Nếu không có rubric: dùng scope để nhận diện requirement còn thiếu. Nếu không có cả rubric và scope: phải phỏng vấn BA/người có thẩm quyền **trước Phase 0**.
- Người dùng cung cấp test case cụ thể **hoặc** expected output. Nếu thiếu cả hai: phải làm rõ trước khi implementation; không tự bịa expected output.
- Ưu tiên happy path + critical risk invariant. Không mở rộng sang edge case ít giá trị kiểm chứng hoặc biến Phase 0 thành benchmark/labeling quá sớm.

### D-05 — Vertical slice và tiêu chí "atomic" `[USER-APPROVED]` + `[OPERATIONAL]`

- Vertical slice đi xuyên các lớp và tạo ra outcome có ý nghĩa, không phải một lớp kỹ thuật đơn lẻ.
- **Tiêu chí dừng phân rã `[OPERATIONAL]`:** dừng khi behavior hiện tại đã có một outcome độc lập, có ý nghĩa và có thể kiểm thử/kiểm chứng; nếu chia nhỏ hơn chỉ tạo thêm chi tiết implementation mà không tạo thêm khả năng kiểm chứng hay giá trị quan sát được, thì không chia tiếp.
- Đây là diễn giải vận hành cho câu hỏi mở O1, **không phải phát biểu nguyên văn của người dùng** và không phải một con số depth cố định. Không được biến tiêu chí này thành quota số lớp, số test hay số file.

### D-06 — Rolling contract freeze `[USER-APPROVED]`

- Trước khi implementation một module/behavior, phải approve + version + freeze **contract của phần sẵn sàng đó** cùng contract upstream/dependency liên quan trực tiếp.
- Không freeze toàn bộ hệ thống tương lai. Có thể triển khai module đã sẵn sàng trong khi tuần tự định nghĩa module/feature kế tiếp.
- Không yêu cầu implementation module N hoàn tất trước khi định nghĩa N+1. Không tự tạo nhiều agent chạy song song để lấp khoảng trống định nghĩa.
- Dependency chưa được xác minh giữ trạng thái `NOT VERIFIED`. Mock/stub **không** chứng minh integration.
- Quy tắc freeze toàn cục một lần trong Phase 0 của bản LGD cũ bị thay thế bởi rolling freeze này; phần discovery tuần tự vẫn giữ.
- Chỉ commit contract đã freeze khi policy repository và quyền hiện có cho phép. Nếu không commit được, ghi rõ khoảng trống `commit gate`, không tuyên bố "đã commit", và không bỏ qua commit gate mà dự án yêu cầu.

### D-07 — Bounded autonomy và escalation `[USER-APPROVED]`

Agent được tự chủ trong scope đã duyệt:

- Loop qua các mini-goal đã được duyệt; tự sửa lỗi trong scope; tự chạy lại verification và tiếp tục mà không xin phê duyệt lại từng mini-goal.
- Được tạo backlog item mới từ phát hiện trong quá trình làm. **Backlog mới là proposal, không phải scope đã duyệt.**
- Được chuyển trạng thái khi evidence thật đáp ứng gate, theo state machine ở D-08.

Phải dừng/escalate khi:

- Có xung đột contract hoặc scope.
- Chi phí/rủi ro không tương xứng lợi ích; phải trình bày phương án gốc, phương án thay thế và trade-off, không tự đổi mục tiêu.
- Thay đổi rủi ro cao, khó đảo ngược, ảnh hưởng security/data/interface, hoặc vượt thẩm quyền.
- Thiếu thông tin/quyền khiến không thể xác minh.

Quy tắc bổ sung:

- Trigger nghiệp vụ mới chỉ bổ sung vào backlog/ proposal; không tự nới lỏng safety boundary đang có.
- Không silent contract/test weakening. Mọi thay đổi behavior/expected output/test quan trọng phải đi qua change request có lý do, impacted cases, rationale, người phê duyệt và version mới.
- Escalation phải dựa trên xung đột có căn cứ/bằng chứng cụ thể, không dựa trên phỏng đoán.

## 3. Trạng thái, an toàn và bằng chứng

### D-08 — Persistent state và kỷ luật vận hành `[USER-APPROVED]`

- Persistent state dùng Markdown, ưu tiên tài liệu hiện có của repository; không tạo planning database/đồ thị service mới.
- State chuẩn: `BACKLOG`, `READY`, `ACTIVE`, `FIXING`, `VERIFIED`, `DONE`, `APPROVAL_NEEDED`, `BLOCKED`, `REOPENED`.
- `BLOCKED` phải kèm bằng chứng cụ thể và phân loại tối thiểu `BLOCKED_USER` hoặc `BLOCKED_EXTERNAL`. Không gọi `BLOCKED` chỉ vì công việc khó.
- Secret phải được yêu cầu từ người dùng qua cơ chế an toàn; **không bao giờ** ghi secret vào Markdown, prompt, log hay test fixture.
- Lỗi code/config do agent sửa trong scope. Rate limit/API policy phải tuân thủ; không tự tạo key, không giả lập live pass.
- Lỗi external/environment không phải bằng chứng code sai. Phải phân biệt `BLOCKED_EXTERNAL`/environment với defect trong code.
- Với output LLM: verify schema, invariant và tiêu chí đã duyệt; không coi một sample "trông đúng" là oracle.
- Migration phải có kiểm chứng integrity, compatibility và recovery trước release.

### D-09 — Safety baseline, instrumentation và cấu hình theo dự án `[USER-APPROVED]`

- Safety baseline tối thiểu và instrumentation cơ bản có từ Phase 1, không đợi Phase 5.
- Coverage threshold, retry budget, telemetry detail, hardening cadence và các ngưỡng tương tự là **project-specific**. Phải hỏi tuần tự cho từng dự án; không hardcode default, không đoán budget.
- Khi thiếu cấu hình, chỉ block công việc phụ thuộc trực tiếp vào ngưỡng đó. Không block toàn bộ dự án nếu phần đang làm không cần ngưỡng đó.

### D-10 — UAT, regression và test integrity `[USER-APPROVED]`

- UAT case đã được người dùng/nghiệp vụ xác nhận và production bug đã được xác nhận phải tạo regression case liên kết tới nguồn.
- Characterization chỉ ghi nhận hành vi **quan sát được**; observed behavior **không tự động** là behavior đã được phê duyệt. Bug không được khóa thành contract chỉ vì production đang làm vậy.
- Output không xác định (nondeterministic) phải kiểm theo invariant, schema hoặc tolerance có lý do; không dùng một output biến thiên làm oracle tuyệt đối.
- Không skip test, bỏ assertion, mock mất ý nghĩa contract, nới threshold hoặc sửa expected output chỉ để đạt GREEN.
- UAT phải do người thật xác nhận. Agent không được tự tuyên bố UAT pass, không được tự tuyên bố deploy đã được chấp nhận.

### D-11 — Mutation testing và điều kiện dừng `[USER-APPROVED]` + `[HISTORICAL-MISSING]`

- Mutation testing là hoạt động của Phase 5, sau Phase 4; không phải gate bắt buộc cho mọi MVP/mini-goal.
- Mục tiêu là statistical convergence và risk convergence; critical logic phải được kiểm chứng, không chỉ chạy theo một mutation score.
- Bốn stop condition lịch sử được nhắc tới nhưng **không có trong artifact hiện có**: đánh dấu `[HISTORICAL-MISSING]`, không được bịa nội dung.
- Trước khi chạy mutation, phải hỏi và nhận chính sách dừng đã được duyệt cho dự án (theo D-04: một câu hỏi tại một thời điểm). Không suy ra bốn điều kiện đó.
- Behavior chưa rõ phát hiện trong quá trình mutation → proposal backlog, không tự thành expected behavior.

## 4. Pilot và báo cáo

### D-12 — Pilot một tháng và đo lường `[USER-APPROVED]` + `[HISTORICAL-MISSING]`

- Thiết kế pilot: một tháng, so sánh **BEFORE** với **BASELINE**, dùng Markdown session log.
- Metric tối thiểu và định nghĩa:
  - **Delivery lead time:** từ thời điểm bắt đầu feature đến thời điểm người dùng chấp nhận deploy; T_delivery = t_accepted - t_start, gồm cả thời gian agent chạy và chờ.
  - **Human attention:** tổng thời lượng can thiệp thực tế của con người, không phải thời gian đồng hồ ước lượng.
  - **Cold-start:** thời gian/chi phí để một người hoặc agent mới hiểu và bắt đầu làm việc trong workflow.
  - **Intervention count:** số lần con người phải can thiệp.
  - **Rework:** công việc phải làm lại do lỗi/contract/implementation.
  - **Accepted deployment evidence:** bằng chứng deployment đã được con người chấp nhận; không phải tuyên bố của agent.
  - **Defect rate:** phải ghi rõ window đo và nguồn case.
- Schema pilot lịch sử và đề xuất "grounded-conflict-only escalation" đã được phê duyệt: chỉ escalate xung đột có bằng chứng/căn cứ cụ thể.
- Không lên lịch automation, không chạy external service trong task này.
- **Pilot một tháng chưa được hoàn thành** bằng việc xây skill. Không có dữ liệu pilot, UAT thật, production hay baseline thật trong bundle này.
- Kết quả pilot (khi có) chỉ là quan sát, có giới hạn do độ khó feature và cách chọn mẫu; không được tuyên bố quan hệ nhân quả hoặc "chứng minh hiệu quả" nếu thiết kế chưa đủ.

### D-13 — Báo cáo, traceability và chống over-engineering `[USER-APPROVED]`

- Quyết định kiến trúc/nghiệp vụ/rủi ro ở mức nhẹ, có: rationale, alternatives, reversibility, owner/approver, link tới goal. Không cần ADR dài cho biến cục bộ.
- Mọi báo cáo phải phân biệt: `VERIFIED FACT`, `INFERENCE`, `ASSUMPTION`, `PROPOSAL`, `BLOCKER`.
- Thiếu evidence → ghi `NOT VERIFIED`. Unit test xanh **không** đồng nghĩa release ready.
- Trace tối thiểu: `goal → contract/version → test → diff → observation`.
- Không áp đặt technology stack, folder convention, coverage threshold, số agent, retry count hay mutation score cố định.

### D-14 — Hình dạng bundle v1 `[USER-APPROVED]`

- Một skill điều phối tên `before`, không tách thành năm skill.
- Năm tên mode: `define-contract`, `execute-mini-goal`, `verify-gate`, `refactor-safely`, `capture-feedback/replan`. Mode cuối gồm hai hành động `capture-feedback` và `replan` nhưng chỉ chiếm một tên mode.
- Sáu entry action tương ứng: `define-contract`, `execute-mini-goal`, `verify-gate`, `refactor-safely`, `capture-feedback`, `replan`; gom thành năm tên mode như trên.
- `SKILL.md` ngắn, frontmatter chuẩn; reference progressive disclosure; asset là template nhỏ.
- Không tạo generic process boilerplate, không tạo architecture framework, không triển khai production system trong task này.

## 5. Ánh xạ nguồn lịch sử

Các ID dưới đây giữ cách đánh số trong danh sách đã trình người dùng duyệt trong chat; không đánh số lại theo mục 2.1 của handoff. Bản handoff có sáu nguyên tắc, còn bảng chat tách mục tiêu trung tâm thành U1 nên có bảy ID.

### 5.1. User intent

| ID trong chat | Nội dung đã duyệt | Quyết định |
|---|---|---|
| U1 | Giảm review bottleneck; tự chủ trong boundary, review ngoại lệ | D-03, D-07, D-13 |
| U2 | Sáu phase | D-02 |
| U3 | Layer và mini-goal; feature/module/interactions/invariants | D-03, D-05, D-06 |
| U4 | RGR và UAT/production regression | D-02, D-10 |
| U5 | Delivery nhanh tách hardening, vẫn có safety | D-02, D-09 |
| U6 | Tracking tạo vòng lặp phát triển | D-12, D-13 |
| U7 | Không trao toàn quyền thiết kế ngầm; quyết định quan trọng có dấu vết | D-03, D-07, D-13 |

### 5.2. Proposal

| ID | Nội dung nguồn | Trạng thái v1 | Quyết định |
|---|---|---|---|
| P1 | Tên tạm LGD | Bị thay thế bởi BEFORE (chỉ tên) | D-01 |
| P2 | L0–L3 control layers | Đã duyệt, là control view không phải kiến trúc | D-03 |
| P3 | Vertical slices | Đã duyệt, kèm tiêu chí atomic vận hành | D-05 |
| P4 | Safety baseline + instrumentation sớm | Đã duyệt từ Phase 1; ngưỡng theo dự án | D-09 |
| P5 | Contract versioning/change process | Đã duyệt | D-06, D-07, D-10 |
| P6 | Bounded autonomy | Đã duyệt | D-07 |
| P7 | Một skill điều phối + references/templates | Đã duyệt và hiện thực trong bundle v1 | D-14 |
| P8 | Phase 0 tuần tự + freeze/version/commit toàn bộ trước implementation | Tuần tự giữ; **freeze toàn cục bị thay thế** bởi rolling freeze; commit có điều kiện | D-04, D-06 |
| P9 | State machine đề xuất | Đã duyệt, bổ sung phân loại BLOCKED có bằng chứng | D-08 |
| P10 | Pilot đề xuất | Đã duyệt thành pilot một tháng, chưa thực hiện | D-12 |

### 5.3. Câu hỏi mở

| ID | Nội dung nguồn | Trạng thái v1 | Quyết định |
|---|---|---|---|
| O1 | Phase 0 cần chi tiết acceptance đến đâu? | Giải quyết **ở mức vận hành** bằng tiêu chí atomic/minimal; không có con số depth | D-05 |
| O2 | Khi nào architectural decision đủ rủi ro để escalate? | Nguyên tắc đã duyệt; rubric/ngưỡng cụ thể vẫn là project interview | D-07, D-09; PI-01 |
| O3 | Quality gate cho external APIs, LLM nondeterministic, migration? | Nguyên tắc đã duyệt; cấu hình chi tiết theo dự án | D-08, D-09, D-10; PI-02 |
| O4 | Format persistent state? | Markdown, ưu tiên tài liệu hiện có | D-08 |
| O5 | Có cần mutation testing? | Phase 5, sau Phase 4; không phải gate mọi MVP; stop policy phải hỏi | D-11; PI-04 |
| O6 | Ngưỡng coverage/retry/telemetry/hardening? | Không hardcode; hỏi tuần tự theo dự án | D-09; PI-03 |
| O7 | Đánh giá hiệu quả so với full-autonomy thế nào? | Pilot một tháng, quan sát, không tuyên bố nhân quả | D-12 |

### 5.4. Clarification của phiên phê duyệt

| ID | Nội dung | Trạng thái v1 | Quyết định |
|---|---|---|---|
| C1 | Rolling freeze: freeze phần sẵn sàng, không freeze toàn hệ thống; thay thế global freeze ban đầu | Đã duyệt | D-06 |
| C2 | Đồng bộ trạng thái phê duyệt giữa bootstrap và handoff: các đề xuất còn lại đã được người dùng duyệt trong chat | Đã giải quyết; ngoại lệ/supersession nêu rõ từng mục | D-01 đến D-14 |

## 6. Sổ project interview

Các mục này **không được trả lời bằng default**. Hỏi tuần tự, một câu tại một thời điểm, khi công việc hiện tại thực sự cần.

| ID | Câu hỏi cần chốt cho dự án | Liên quan |
|---|---|---|
| PI-01 | Rubric rủi ro, ngưỡng escalation và người có thẩm quyền phê duyệt của dự án là gì? | O2, D-07 |
| PI-02 | Quality gate cụ thể cho external API, output LLM không xác định và migration là gì? | O3, D-08, D-09 |
| PI-03 | Coverage, retry budget, telemetry và hardening cadence của dự án là gì? | O6, D-09 |
| PI-04 | Chính sách dừng mutation testing đã được duyệt là gì? | O5, D-11 |
| PI-05 | Ai là người xác nhận UAT và ai có quyền chấp nhận deploy? | D-10, D-12 |
| PI-06 | Repo có commit gate bắt buộc không; ai cho phép commit? | D-06 |
| PI-07 | Test command, allowed/protected paths, môi trường và kênh an toàn để nhận secret là gì? | D-08, D-09 |
| PI-08 | Baseline, window đo defect và schema session log cụ thể của pilot là gì? | D-12 |

## 7. Sổ dữ liệu lịch sử còn thiếu

| ID | Gap | Hệ quả |
|---|---|---|
| HM-01 | Bốn stop condition lịch sử của mutation testing không có trong artifact hiện có | Không được bịa; phải lấy chính sách dừng được duyệt trước khi chạy mutation. |
| HM-02 | Pilot một tháng chưa chạy | Không có metric, baseline hay kết luận hiệu quả. |
| HM-03 | Không có UAT thật, production bug thật hoặc deployment evidence trong bundle | Mọi ví dụ UAT là hư cấu, phải ghi rõ. |
| HM-04 | Chưa có commit cho v1 | Không tuyên bố "đã commit"; commit gate vẫn mở nếu repo yêu cầu. |
| HM-05 | Không có transcript nguyên văn; các phê duyệt đến từ chat; brief là bản tóm lược phục vụ executor | Không tạo quote, không gán lời nói cho người dùng. |
| HM-06 | Tên `BF-LD` chỉ xuất hiện trong phạm vi supersession của brief, không có tài liệu nguồn riêng trong cwd | Chỉ ghi nhận supersession tên; không suy diễn lịch sử. |
| HM-07 | Việc Codex runtime trong phiên mới có discover `.agents/skills/before` hay không chưa được quan sát | Discovery là `NOT VERIFIED`; cần reload/phiên mới và ghi kết quả quan sát. |

## 8. Chính sách khóa

- **Lock là governance, không phải OS read-only.** Không đặt file attribute read-only, không đổi ACL/quyền, không mã hóa. Việc khóa nằm ở quy tắc: chỉ sửa qua change request được duyệt.
- Bản này là bản canonical đã khóa `v1.0`, được phê duyệt ngày **2026-10-21**.
- Mọi thay đổi nội dung phải có change request gồm: lý do, decision/case bị ảnh hưởng, alternatives/trade-off, rủi ro/reversibility, owner/approver, version mới và kế hoạch regression.
- Không sửa trực tiếp để "cho khớp" implementation hoặc test. Nếu code/test khác contract đã duyệt, code/test phải sửa hoặc một change request phải được trình.
- `BEFORE_DECISIONS.md` ở root là bản canonical. `references/decisions.md` trong skill là snapshot portable phục vụ di chuyển skill sang repository khác; khi canonical đổi phiên bản, snapshot phải được đồng bộ trong cùng change request. Nếu phát hiện lệch, dừng và báo divergence; không tự chọn bản có lợi cho việc pass gate.
- SHA256 của các file thuộc snapshot được ghi trong `BEFORE_VALIDATION.md` **sau lần review cuối**. Hash chỉ chứng minh tính toàn vẹn của artifact tại thời điểm ghi, không chứng minh nội dung đúng.
- Git commit chỉ được tạo nếu repository policy và quyền cho phép. Trong task này không commit; xem HM-04.

## 9. Điều không được suy diễn

- Không suy diễn rằng BEFORE đã được chứng minh hiệu quả, nhanh hơn, ít lỗi hơn hoặc tốt hơn full-autonomy.
- Giữ sáu phase làm lifecycle; không suy diễn rằng mỗi phase cần một bộ tài liệu riêng hoặc mọi dự án cần đủ bốn lớp tài liệu, mutation gate cho MVP, coverage threshold hay multi-agent.
- Không suy diễn rằng UAT hư cấu trong tài liệu usage là UAT thật hoặc đã được người dùng chấp nhận.
- Không suy diễn rằng việc skill được tạo trong phiên này chứng minh nó sẽ được discover/invoke đúng trong Codex runtime khác.
- Không suy diễn rằng "unit tests xanh" hoặc "acceptance xanh" đồng nghĩa release ready.
