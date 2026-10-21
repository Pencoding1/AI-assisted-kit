# HANDOFF — Layer-Gated Development (LGD)

**Working agreement for AI Coding Agents · Bản ghi ý tưởng và đặc tả bàn giao cho Codex**  
**Version:** 0.1-draft · **Ngày ghi nhận:** 2026-10-21 · **Ngôn ngữ vận hành:** tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh  
**Trạng thái:** Khung ý tưởng + các quyết định người dùng đã nêu; **chưa** phải skill đã được cài đặt hoặc quy trình đã được kiểm nghiệm thực tế.

> **Cách đọc tài liệu:** `[U]` = chủ đích/yêu cầu do người dùng nêu; `[P]` = đề xuất phát triển của trợ lý, chưa được người dùng phê duyệt riêng; `[O]` = câu hỏi mở/điểm phải kiểm nghiệm. Không được tự biến `[P]` hay `[O]` thành một quyết định kiến trúc đã được phê duyệt.

## 1. Bối cảnh và vấn đề cần giải quyết

[U] Trước đây, quy trình thường là `ý tưởng → chi tiết hóa → thiết kế thuật toán → AI code từng thuật toán`. Người dùng kiểm soát được logic và biết tại sao từng cấu phần tồn tại. Khi chuyển sang AI Coding Agents (Codex/Hermes/Claude Code) và giao goal ở cấp kiến trúc/hệ thống, agent tự đưa ra nhiều quyết định bên trong, dẫn tới:

- **Review Bottleneck:** phải kiểm tra lại gần như toàn bộ sản phẩm, mất nhiều thời gian hơn lợi ích có được từ code generation.
- **Implicit assumptions:** các giả định nằm rải rác ở module/thuật toán, dễ trở thành các “magic numbers” ở tầng giải thuật hoặc những dependencies không có cơ sở nghiệp vụ.
- **Architecture drift & technical debt:** code phức tạp hơn nhu cầu; agent về sau hiểu những chi tiết tình cờ là ràng buộc bắt buộc.
- **Delivery pressure:** sản phẩm phải đi vào sử dụng rất nhanh ở cấp MVP/prototype, nhưng không được mất hoàn toàn khả năng kiểm soát, kiểm thử và cải tiến về sau.

**Mục tiêu trung tâm [U]:** chuyển từ *AI tự xây toàn hệ thống rồi con người review toàn hệ thống* sang *AI tự chủ triển khai từng đơn vị nhỏ trong phạm vi hành vi và ràng buộc đã xác định; con người chỉ cần review các quyết định quan trọng/ngoại lệ*.

## 2. Các nguyên tắc thiết kế

### 2.1. Những điểm người dùng chủ động đề xuất [U]

1. **Six-phase lifecycle:** Phase 0 Test Contracts Implementation → Phase 1 MVP Rapid Implementation → Phase 2 Modularization → Phase 3 Delivery & UAT → Phase 4 Hardening & Refactor → Phase 5 Tracking & Repeat.
2. **Layer by layer + mini-goal:** feature là cấp cao nhất; feature behavior tests định nghĩa điều người dùng cần. Bên dưới là các module, tương tác giữa module và những safety/consistency constraints cần có.
3. **Test-driven thinking:** dựa vào RED–GREEN–REFACTOR (RGR). Lấy behavioral/acceptance tests làm cơ sở delivery; khi UAT và chạy thực tế có thêm test, tái sử dụng chúng làm regression guard cho refactor.
4. **Tách tốc độ delivery và hardening:** triển khai MVP nhanh, còn những cải tiến sâu về cấu trúc và độ ổn định được thực hiện có chủ đích sau khi đã xác nhận giá trị sản phẩm; không đồng nghĩa bỏ qua tất cả safety checks trước release.
5. **Tracking tạo ra vòng lặp mới:** quan sát hệ thống đang vận hành, xác định vấn đề/feature mới và quay lại định nghĩa MVP/constraints/mini-goals tiếp theo.
6. **Không trao toàn quyền thiết kế ngầm:** các thay đổi có tác động kiến trúc, business behavior hoặc bảo đảm an toàn cần dấu vết quyết định, không để agent tự mặc định hợp lệ.

### 2.2. Những khuyến nghị đã thảo luận nhưng cần xác nhận qua pilot [P]

1. Dùng tên tạm **Layer-Gated Development (LGD)**, không khẳng định đây là một framework được tiêu chuẩn hóa.
2. Chia layer kiểm soát thành `L0 Feature Behavior`, `L1 Module Interaction`, `L2 Module Behavior`, `L3 Implementation`.
3. Triển khai theo **vertical slices**: Triển khai từng module đảm bảo chúng pass các behavior đã được xác định rồi mới triển khai tiếp các module khác.
4. Đầu tư một **Safety Test Baseline** tối thiểu ngay từ MVP; tracking/instrumentation căn bản có từ Phase 1 thay vì đợi Phase 5.
5. `Approved contracts` nên có versioning/change process, không phải “bất biến vĩnh viễn”. Quyết định khó đảo ngược = chi phí/rủi ro đảo ngược lớn, không phải bị cấm thay đổi.
6. Dùng **Bounded Autonomy**: agent tự thực hiện mini-goals và tự xử lý lỗi trong scope; chỉ escalation khi vướng blocker thật hoặc quyết định vượt quyền đã giao.
7. Bắt đầu bằng **một skill điều phối gọn** và các tài liệu tham chiếu/templates; chỉ tách thành nhiều skills khi có trigger/input/output tách biệt rõ. Không tạo orchestration framework mới chỉ để chạy quy trình.
8. **Behavior-Driven Test Contract & Layer-Gated Freeze:** Phase 0 được thực hiện tuần tự theo từng layer, bắt đầu từ toàn bộ Feature Behavior Contracts, sau đó đến Module Interaction Contracts và dừng trước Implementation. Mỗi test contract chỉ cần xác định luồng thành công, hành vi mong đợi tại từng bước và dữ liệu đầu ra mẫu (nếu cần). Người dùng có thể cung cấp test case cụ thể hoặc chỉ mô tả expected output; nếu thiếu cả hai, agent bắt buộc phải phỏng vấn để làm rõ trước khi tiếp tục. Agent có trách nhiệm đánh giá mức độ đầy đủ dựa trên rubric, mục tiêu và behavior tổng thể của hệ thống, tránh đề xuất các edge cases không mang lại giá trị kiểm chứng đáng kể. Khi người dùng xác nhận kết thúc Phase 0, toàn bộ test contracts phải được **freeze, version và commit** trước khi chuyển sang implementation. Mọi thay đổi sau đó phải tuân theo contract change control.
## 3. Ngôn ngữ dùng chung

- **Feature:** khả năng người dùng/kinh doanh cần, gắn với hành vi quan sát được.
- **Behavior Contract:** input, điều kiện và expected outcome; ví dụ Gherkin, pytest acceptance, API/CLI examples.
- **Module Contract:** các interface, schema, error semantics, side effects và bất biến giữa các module.
- **Invariant:** điều luôn đúng qua các lần chạy (dữ liệu không bị mất, retry không tạo bản ghi trùng, quyền truy cập không bị vượt).
- **Mini-goal:** đơn vị triển khai nhỏ có scope, test, evidence, điểm dừng rõ ràng.
- **Quality Gate:** điều kiện có bằng chứng để cho phép bước tiếp theo; một bài test chưa chạy không được ghi là pass.
- **UAT:** người dùng/nghiệp vụ xác thực use cases và outcome thực tế.
- **Regression Suite:** bộ kiểm chứng nhằm phát hiện hành vi từng đúng bị phá vỡ bởi thay đổi sau đó.
- **Characterization Test:** ghi nhận hành vi hệ thống hiện tại khi chuẩn bị refactor; hành vi quan sát được **không tự động** là hành vi được nghiệp vụ chấp thuận.
- **Escalation:** yêu cầu quyết định từ người dùng khi vượt contract, đụng vùng rủi ro cao, hoặc không thể xác minh.

## 4. Hai trục điều phối: lifecycle × layer

### Trục A: Six-phase lifecycle (vòng ngoài)

| Phase | Mục đích | Đầu ra tối thiểu | Gate chuyển pha |
|---|---|---|---|
| **0 — Test Contract Definition & Freeze** | Lần lượt xác định behavior và expected output cho từng feature, hoàn thành toàn bộ Feature Contracts rồi chuyển sang Module Interaction Contracts. Agent phỏng vấn khi thiếu expected output, tự giới hạn các đề xuất edge cases theo rubric và scope. Dừng tại module layer, chưa triển khai production code. | Người dùng xác nhận hoàn tất; toàn bộ approved contracts được freeze, version và commit. Không còn behavioral ambiguity nghiêm trọng chưa được xử lý. |
| **1 — MVP Rapid Implementation** | Triển khai vertical slice tối thiểu, ưu tiên time-to-value; tránh kiến trúc thừa | Working feature, implementation diff, test results, trace/log cơ bản, known debt | Acceptance + safety baseline pass; chưa pass thì không tuyên bố ready |
| **2 — Modularization** | Chuẩn hóa boundaries đã lộ rõ khi triển khai, tách trách nhiệm ở mức cần thiết cho UAT và thay đổi tiếp | Interfaces/ownership rõ, module/integration tests, updated decision record | Behavior không bị thay đổi ngoài contract; mọi test liên quan pass |
| **3 — Delivery & UAT** | Người dùng/đơn vị nghiệp vụ đánh giá workflow thực, hoàn thiện acceptance | UAT scenarios, feedback/bug list, release decision, evidence | UAT pass hoặc ngoại lệ được chấp thuận rõ; release safety gate đạt |
| **4 — Hardening & Refactor** | Củng cố test baseline từ UAT/prod, xử lý reliability risks, cải thiện cấu trúc theo từng thay đổi nhỏ | Regression suite, technical-debt decisions, refactor diffs, evidence | Behavior bảo toàn và các reliability goals đạt; không sửa test để “làm đẹp” kết quả |
| **5 — Tracking & Repeat** | Đo hiệu quả và ổn định; nhận diện gap, phân loại feedback; chọn vòng feature/mini-goal mới | Telemetry/observations, issue triage, prioritized mini-goal backlog, revised contracts nếu cần | Các insight quan trọng gắn vào backlog có owner, rationale, testable outcome |

**Không nên hiểu các phase là một thác nước cứng:** bộ test và log phải có từ đầu; phase 4 có thể thực hiện theo luồng độc lập cho module đã release, đồng thời feature mới quay về phase 0. Không áp đặt refactor lớn để hoàn thành Phase 2 trước khi UAT.

### Trục B: Constraint layers (mỗi mini-goal)

| Layer | Câu hỏi | Contract cần có | Quyền quyết định |
|---|---|---|---|
| **L0 Feature Behavior** | Người dùng thấy hệ thống làm gì? | Acceptance tests, UAT scenarios, business invariants | User/product owner chấp thuận ý nghĩa |
| **L1 Module Interaction** | Các capability kết nối thế nào? | Inputs/outputs, schemas, retries, errors, integration contracts | Agent đề xuất; escalation cho breaking/high-risk decisions |
| **L2 Module Behavior** | Module đúng trong trường hợp thường và lỗi như thế nào? | Unit/integration cases, side effects, failure policy | Agent trong scope, chịu gate test |
| **L3 Implementation** | Dùng thuật toán, thư viện, cấu trúc code nào? | Code quality, direct tests, minimum required evidence | Agent tự quyết trong giới hạn được duyệt |

**Quy tắc phân rã:** `Feature goal → một behavior nhỏ → L0 acceptance → L1/L2 tối thiểu cho behavior đó → L3 implementation → evidence`. Lặp với behavior kế tiếp. Không cần đóng băng tất cả L1/L2/L3 cho cả hệ thống.

## 5. RED–GREEN–REFACTOR đúng nghĩa trong lifecycle

- **RED:** viết test thể hiện một yêu cầu hoặc bug đã được xác nhận; test phải fail vì đúng behavior chưa được triển khai (không phải do lỗi môi trường/test sai).
- **GREEN:** thay đổi ít nhất cần thiết để đáp ứng test, cùng với kiểm tra baseline an toàn liên quan.
- **REFACTOR:** thay đổi cấu trúc nhưng *không thay đổi externally observable behavior*; chạy lại regression sau các bước nhỏ.

**Hai nhịp khác nhau:** vòng `RGR nhỏ` trong mini-goal và `hardening/refactor lớn hơn` tại Phase 4. Không được đánh đồng RGR thành “RED là Phase 0, GREEN là Phase 1, REFACTOR là Phase 4”. Khi chỉ refactor một tính năng vốn đã GREEN, không bắt buộc tạo một test mới để ép RED; điều kiện là có regression baseline đủ bảo vệ thay đổi.

## 6. Mini-goal contract tối thiểu

Một mini-goal phải đủ nhỏ để có thể xem diff và evidence hợp lý, nhưng đủ lớn để tạo tiến bộ hữu ích. Dùng schema có thể biểu diễn bằng Markdown/YAML, không ép hệ thống quản lý phức tạp.

```yaml
id: MG-EXTRACT-001
phase: 1
parent_feature: FT-NEWS-EXTRACTION
objective: "Trích xuất nội dung bài viết từ HTML; tránh menu blob"
in_scope:
  - "HTML extractor và test liên quan"
out_of_scope:
  - "Không sửa scheduler, notification, classifier"
inputs:
  - "raw_html"
  - "source_url"
outputs:
  - "normalized_text"
  - "content_status"
  - "source_metadata"
behavior_criteria:
  - "Bài viết hợp lệ trả nội dung chính"
  - "Menu-only document không được đánh nhãn bài viết hợp lệ"
critical_invariants:
  - "Giữ provenance/source_url"
  - "Không im lặng nuốt lỗi extraction"
required_tests:
  - "valid_article"
  - "menu_blob"
  - "empty_page"
  - "source_metadata_preserved"
allowed_changes:
  - "src/extractor/**"
  - "tests/extractor/**"
assumptions:
  - "Chưa chốt policy với trang web render bằng JavaScript"
unknowns:
  - "Expected status với HTML không thể parse: cần xác nhận trong phase 0"
required_evidence:
  - "diff_or_commit"
  - "test_run_with_exit_status"
  - "assumptions_and_exceptions"
risk_level: "normal" # normal|high|critical, theo rubric dự án
status: "ready"
```

**Lưu ý:** YAML chỉ là mẫu khởi tạo; không nên đặt số lượng field cố định hoặc những threshold tùy tiện thành ràng buộc của tất cả dự án. Đối với việc chưa xác định behavior, giải quyết unknowns trước khi biến nó thành expected outcome cứng.

## 7. Test strategy & bảo vệ UAT sau refactor

1. **Acceptance/feature tests:** kiểm tra các hành vi đã thống nhất; là cơ sở UAT và delivery.
2. **Module/unit/integration tests:** bảo vệ logic và tương tác ở layer L1/L2.
3. **Safety baseline từ trước release:** các invariant về dữ liệu, quyền hạn, transaction, idempotency, side effects, failure handling (chọn theo rủi ro thực của feature).
4. **UAT-derived regression tests:** sau UAT, chuyển các tình huống đã xác nhận thành test có thể chạy lại ở mức thích hợp; không bắt buộc mọi UAT phải là E2E.
5. **Production-derived cases:** mỗi bug hoặc edge case quan trọng được xác nhận tạo ra case mới và liên kết tới issue/root cause.
6. **Characterization tests:** trước refactor trên legacy code, ghi lại hành vi hiện hành và phân biệt rõ observed behavior với approved behavior; bug không được khóa thành contract chỉ vì production đã làm vậy.
7. **Non-deterministic outputs:** test theo invariants, schema, tolerances có lý do hoặc dataset đã adjudicate; không gán output biến thiên là oracle tuyệt đối.

**Red test integrity:** không sửa expected outputs, bỏ assertion, skip test, mock mất ý nghĩa, nới threshold hoặc chỉnh fixtures chỉ để test xanh. Nếu test thực sự sai hoặc yêu cầu thay đổi thì tạo `contract change request` ghi: lý do, impacted cases, version mới, quyền xác nhận, bằng chứng.

## 8. Autonomy & escalation policy

### Agent được phép tự thực hiện trong scope được duyệt

- Chia backlog thành mini-goals, ưu tiên theo dependency và impact đã được chỉ định.
- Chọn implementation chi tiết; tạo/thêm test cho logic mới và bug đã được xác nhận.
- Tự chạy lại test, sửa lỗi, phản biện kết quả, cập nhật evidence và known technical debt.
- Tạo các backlog items mới từ vấn đề tìm thấy; **không tự mở rộng approved scope** chỉ bằng việc thêm backlog.
- Chuyển mini-goal `VERIFIED → DONE` khi đủ gate/evidence, rồi thực hiện mini-goal tiếp theo mà không hỏi lại mỗi lần.

### Chỉ escalation khi thực sự cần

- Business behavior, acceptance contract hoặc ràng buộc quan trọng cần thay đổi.
- Public interface/persisted schema thay đổi phá tương thích, migration khó rollback, dữ liệu thật có nguy cơ bị mất.
- Security, secrets, authorization, compliance, PII hoặc tác động production có rủi ro cao.
- Phát sinh dependency mới có chi phí hoặc rủi ro đáng kể, phá ranh giới scope hoặc cần quyền truy cập bổ sung.
- Thiếu thông tin khiến expected behavior không thể xác nhận, gate không đạt sau khi tự xử lý trong giới hạn hợp lý.

**Chống ping-pong:** gom các câu hỏi quyết định liên quan; nêu 1–3 lựa chọn, impact, recommendation và safe default nếu có. Không xin phê duyệt lại cho những việc đã nằm trong approved contract. `Blocked` phải có bằng chứng cụ thể; không gọi blocked chỉ vì khó.

**Cấm:** tuyên bố test pass khi chưa chạy; xóa/skip test để qua gate; tự thay đổi contract được duyệt; làm side effect không được cho phép; tự tạo kiến trúc ngoài scope; chạy các hành động không thể đảo ngược chỉ dựa trên một giả định.

## 9. State machine đề xuất [P]

`BACKLOG → READY → ACTIVE → VERIFIED → DONE`

`ACTIVE → FIXING → ACTIVE` khi kiểm tra không đạt nhưng vẫn nằm trong scope.

`ACTIVE → APPROVAL_NEEDED` khi contract/risk/authority boundary bị chạm; `ACTIVE → BLOCKED` nếu thiếu external dependency ngoài quyền xử lý. `APPROVAL_NEEDED → READY/ACTIVE` sau khi có quyết định. `DONE → REOPENED` khi phát hiện regression có bằng chứng.

Chỉ `VERIFIED` khi các required gates có evidence thật. Evidence tối thiểu: ID goal/contract version, code diff/commit, test names và exit status, known limitations, assumptions/decisions. Không dùng số lần retry cố định thiếu căn cứ: giới hạn thời gian/chi phí/retry phải cấu hình theo dự án và môi trường chạy.

## 10. Giảm Review Bottleneck có hệ thống

**Review objects thay cho review toàn bộ codebase:**

- Feature-level: review behavior/outcome, critical invariants và scope boundary.
- Mini-goal-level: review **diff + test/evidence + deviations**, không tự động đọc lại tất cả module.
- Cross-cutting/high-risk: vẫn cần code review/architecture review trực tiếp khi liên quan auth, data integrity, public contracts, irreversible side effects, performance/cost-sensitive pathways.

**Decision record nhẹ:** `ID, quyết định, lý do, alternatives, impact, reversibility, owner/approver, link goal`. Không yêu cầu ADR dài cho mọi biến cục bộ; ghi các quyết định khiến agent sau này dễ hiểu sai thành một ràng buộc hệ thống.

**Minimum metrics (định nghĩa rõ window và baseline khi đo):** `human review time/feature`, `time-to-acceptance`, `post-UAT defect rate`, `unplanned rework`. Khi có release pipeline, có thể mở rộng bằng các chỉ số DORA; không tối ưu test count hay % green đơn thuần.

## 11. Sự thật phải được phân biệt trong báo cáo của agent

Báo cáo phải tách:

- `VERIFIED FACT` — bằng chứng từ test run, file, diff hoặc telemetry.
- `INFERENCE` — suy luận từ code/test/data chưa chứng minh đầy đủ.
- `ASSUMPTION` — điều được giả định để triển khai trong phạm vi được phép.
- `PROPOSAL` — đề xuất ngoài contract, chưa được duyệt.
- `BLOCKER/ESCALATION` — điều ngăn tiến độ hoặc cần quyết định.

Không được tạo summary kiểu “system production ready” chỉ vì unit tests xanh. Khi gate thiếu dữ liệu phải ghi `NOT VERIFIED`.

## 12. Áp dụng qua dự án — cấu hình thay vì kiến trúc hóa quá mức

Core working agreement phải độc lập framework/ngôn ngữ và dùng được trên Python, TypeScript, C++ hoặc tool nội bộ. Các phần project-specific (test commands, allowed paths, risky actions, dependency policy, environments, hard/soft gates) nên được ghi một lần dưới cấu hình/hướng dẫn repository hiện có.

Đừng buộc mỗi repository tạo một đồ thị service, planning database, multi-agent orchestrator, hay cấu trúc thư mục mới. Agent phải **inspect before create**; kế thừa conventions, test runner và docs có sẵn; giữ footprint nhỏ nhất đủ đạt goal.

## 13. Yêu cầu bàn giao cho Codex — xây Skill v1

**Nhiệm vụ:** tạo skill sử dụng được trong Codex nhằm khiến các phiên sau tuân thủ working agreement trên. Không triển khai phần mềm nghiệp vụ trong lần tạo skill này.

### 13.1. Kết quả kỳ vọng

- **Một skill đầu mối** có `SKILL.md` với frontmatter chuẩn `name`, `description`, trigger rõ ràng; dùng `references/` cho quy trình dài, `assets/` cho templates, `scripts/` chỉ khi có thao tác định lượng/deterministic đáng tự động hóa.
- **Entry points/modes** tối thiểu: `define-contract`, `execute-mini-goal`, `verify-gate`, `refactor-safely`, `capture-feedback/replan` (có thể gom trong một skill v1; không bắt buộc tách năm skill).
- **Các template nhỏ:** feature/behavior contract, mini-goal contract, gate evidence, contract change request, decision/assumption log, UAT-to-regression mapping.
- **Một ví dụ end-to-end** trên toy feature hoặc fixture độc lập, chứng minh `RED → GREEN`, handoff UAT, regression/refactor và exception/escalation.
- **Kiểm chứng skill:** test/forward-eval ít nhất các tình huống green, fail trong scope, thay đổi contract trái phép, safety gate fail, refactor làm đổi behavior, feedback sinh mini-goal mới.
- **Hướng dẫn tích hợp tối thiểu:** vị trí skill được Codex hiện hành hỗ trợ và cách viện dẫn từ `AGENTS.md` (chỉ thêm/ghi đè file khi được cho phép và cần thiết).

### 13.2. Định hướng cấu trúc (ví dụ, không phải bắt buộc)

```text
.agents/skills/layer-gated-development/
  SKILL.md
  references/
    lifecycle-and-gates.md
    layer-contracts.md
    autonomy-and-escalation.md
  assets/
    feature-contract.template.md
    mini-goal.template.md
    gate-evidence.template.md
    contract-change.template.md
```

Codex phải đọc tài liệu skills hiện hành trước khi quyết định đường dẫn thực tế; không giả định cấu trúc trên hợp lệ trong mọi runtime. Nếu `skill-creator` sẵn có, ưu tiên dùng để khởi tạo rồi tinh giản. Tài liệu chính thức: <https://developers.openai.com/plugins/build/skills>, <https://learn.chatgpt.com/docs/build-skills>, <https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex>.

### 13.3. Acceptance criteria của nhiệm vụ tạo skill

- [ ] **Traceability:** mọi user principle [U] ở Mục 2 được biểu diễn bằng quy tắc hoặc workflow của skill; [P] không bị đóng vai trò là quyết định người dùng đã phê duyệt.
- [ ] **No overengineering:** không phụ thuộc một server, database, framework, orchestrator hoặc nhiều subagents nếu không thực sự cần; mô tả rõ tại sao mỗi file tồn tại.
- [ ] **Correct RGR:** hiểu inner loop khác outer phases; một refactor vốn GREEN không bị ép tạo test RED giả.
- [ ] **Bounded autonomy:** agent tự loop approved mini-goals; escalation đúng boundary; không hỏi người dùng phê duyệt từng bước.
- [ ] **Test integrity:** skill cấm silent contract edit/test weakening; có đường đi hợp lệ cho contract change.
- [ ] **Phase/layer clarity:** six-phase lifecycle, four-layer contracts và vertical slice không mâu thuẫn nhau.
- [ ] **Evidence:** không cho phép đánh dấu verified khi chưa chạy validation; ghi rõ missing evidence.
- [ ] **Production awareness:** safety gates, runtime evidence và rollback/side-effect policy ở mức phù hợp, không mặc định unit green = release ready.
- [ ] **Adaptation:** áp dụng được cho repository đã có conventions; không chiếm quyền ghi đè docs/cấu trúc hiện hành.
- [ ] **Evaluation:** có bằng chứng test ít nhất sáu tình huống ở 13.1; ghi những gì đã chạy/chưa chạy.
- [ ] **Concise handoff:** đầu ra gồm đường dẫn skill thực tế, cách dùng, khác biệt với tài liệu nguồn, known limitations và file diff.

## 14. Những vấn đề còn mở [O]

Những điểm dưới đây **không ngăn Codex tạo Skill v1**; dùng lựa chọn bảo thủ, project-configurable và ghi rõ assumptions thay vì tự ngầm hardcode.

1. Phase 0 cần độ chi tiết feature acceptance đến đâu để không biến thành benchmark/labeling quá sớm?
2. Khi nào một architectural decision đủ rủi ro để bắt buộc escalated review? Rubric mặc định và ngoại lệ theo loại dự án.
3. Quality Gate cần cấu hình chi tiết ra sao cho module tích hợp nhiều external APIs, nondeterministic LLM outputs, data migrations?
4. Format lưu persistent state nên là Markdown/YAML/issue tracker? Ưu tiên dùng tool/repo hiện có; tránh lock-in.
5. Có cần kỹ thuật đánh giá độ chất lượng test như mutation testing sau khi test baseline ổn định? Không mặc định mọi mini-goal phải chạy.
6. Ngưỡng về test coverage, retry budget, telemetry và tần suất hardening? Không đặt magic number ở mức quy trình.
7. Đánh giá hiệu quả thực nghiệm so với full-autonomy agent coding trên một feature thật như thế nào?

## 15. Pilot đề xuất [P]

Pilot một feature có behavior đã rõ (ví dụ HTML content extraction với menu-blob detection), không phải toàn bộ hệ thống crawling. Thiết lập baseline `human review time`, `time-to-acceptance`, `rework`, `post-UAT defects`. Dùng LGD để tạo acceptance, giao vài mini-goal theo vertical slices, ghi lại exceptions, chạy UAT và thử một refactor có regression. So sánh với workflow trước, bao gồm chi phí soạn contract để tránh thiên lệch chỉ đo tốc độ coding.

## 16. Định hướng nguồn tham khảo

**Nguồn người dùng đã cung cấp để hình thành ý tưởng:**

- AI coding/verification bottleneck: <https://arealisticdreamer.com/ai-code-30-phut-he-thong-mat-2-tieng-tu-kiem-tra-nhau>
- TDD introduction: <https://viblo.asia/p/tong-quan-ve-tdd-gDVK2WzeZLj>
- TDD introduction: <https://viblo.asia/p/test-driven-development-gioi-thieu-6J3ZgneMKmB>
- IBM TDD: <https://www.ibm.com/think/topics/test-driven-development>
- TDD overview: <https://en.wikipedia.org/wiki/Test-driven_development>

**Tài liệu định dạng Skill/Codex (đã đối chiếu ngày 2026-10-21):**

- <https://developers.openai.com/plugins/build/skills>
- <https://learn.chatgpt.com/docs/build-skills>
- <https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex>
- <https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md>

**Ghi chú provenance:** `[U]` được tóm lược từ những phát biểu của người dùng trong cuộc trao đổi, không phải từ tài liệu bên ngoài; `[P]` là đề xuất thiết kế. Các lý thuyết TDD, characterization/regression, contract test và agent skills là bối cảnh tham khảo, không được xem như bằng chứng LGD đã đạt hiệu quả.

---

## Quyết định quan trọng nhất để Codex không đánh mất

> Người dùng muốn AI tự động **làm việc**, không tự động **định nghĩa lại điều gì là đúng**. Hợp đồng hành vi và các ràng buộc quan trọng tạo nên quyền kiểm soát; các mini-goal, gates và evidence giúp giảm phạm vi review; feedback từ vận hành tạo ra vòng lặp phát triển tiếp theo. Tối ưu hóa là giảm review bottleneck **mà không tăng rủi ro và rework**, không phải tối đa hóa số lượng code hoặc test tự sinh.
