# CONTEXT
Tôi muốn tiêu chuẩn hóa hợp đồng làm việc giữa tôi và AI Coding Agents thông qua một reusable Codex Skill. Tài liệu nguồn là `LGD_HANDOFF.md` (Layer-Gated Development, LGD), ghi lại bối cảnh, những ý tưởng tôi đã chủ động đề xuất, các bổ sung đang ở trạng thái đề xuất, workflow 6 phases, layer contracts, mini-goal, RGR, review/quality gates, bounded autonomy và continuous feedback.

Trước tiên, hãy đọc toàn bộ LGD_HANDOFF.md và kiểm tra các quy ước/skills có sẵn trong repository. Đọc documentation hiện hành của Codex Skills/SKILL.md, hoặc dùng `$skill-creator` nếu có sẵn. Hãy phân biệt `[U]` = user intent/requirements, `[P]` = proposal, `[O]` = unresolved. Không suy diễn các đề xuất thành quyết định được chốt.

# PRIMARY GOAL
Xây dựng một Codex Skill v1 có thể sử dụng lại trong những repository khác nhau nhằm điều phối quy trình Layer-Gated Development, với khả năng:
- Định nghĩa và kiểm chứng feature behavior / critical invariants trước implementation.
- Phân rã feature thành vertical-slice mini-goals có module contracts tối thiểu.
- Thực hiện RED–GREEN–REFACTOR hợp lý trong các mini-goals, đồng thời giữ 6-phase lifecycle ngoài.
- Tự loop qua các mini-goals đã được cho phép, không yêu cầu approval lặp lại; thu thập evidence và chỉ escalate những thay đổi vượt contract/risk boundary.
- Tái sử dụng UAT, production-confirmed bugs và characterization để tạo regression baseline, hỗ trợ refactor mà không silently change approved behavior.
- Dùng tracking/feedback để tạo backlog tiếp theo, giữ traceability goal → contract → tests → code → observed results.

# EXECUTION CONSTRAINTS
1. Nhiệm vụ phiên này chỉ là xây Skill + templates + tài liệu sử dụng + kiểm chứng skill. KHÔNG triển khai hệ thống sản phẩm nghiệp vụ hoặc xây orchestrator/service/database mới.
2. Inspect before create. Tận dụng cấu trúc repo hiện hữu; không ghi đè AGENTS.md, files khác hoặc skill đang tồn tại nếu chưa đủ quyền/phạm vi.
3. Khởi đầu với một focused skill có SKILL.md (YAML frontmatter name/description) cùng references/assets tối thiểu. Chỉ tách thành nhiều skills khi chứng minh được trigger và acceptance criteria riêng cho từng skill.
4. Không áp đặt technology stack, folder convention, coverage threshold, fixed retry counts hay số lượng agents. Tránh hidden assumptions, magic numbers và quy định không có causal justification.
5. Các dự án ứng dụng skill phải duy trì quyền tự động trong approved scope. Escalate chỉ khi gặp genuine blocker hoặc materially risky/irreversible change; không dừng ở từng mini-goal để xin phép.
6. Không làm suy yếu test để biến RED thành GREEN. Nếu test/behavior contract sai, trình bày contract change request và xin quyết định phù hợp.
7. Không claim verification khi chưa có tool evidence. Phân biệt VERIFIED FACT / INFERENCE / ASSUMPTION / PROPOSAL / BLOCKER.
8. Có thể cập nhật backlog từ khám phá trong quá trình triển khai nhưng không được tự động coi backlog mới là scope đã được phê duyệt.

# WORK PLAN
A. Read & reconcile: trích xuất working agreements, xác định phần bắt buộc, phần proposal, unresolved; đọc skills standard và conventions repo.
B. Minimal design: xác định skill entrypoint, triggers, modes, reference files và template ownership, sao cho ít file và context overhead nhất.
C. Implement: tạo SKILL.md, templates/contracts, quality gate/evidence protocol, autonomy/escalation policy, and usage notes.
D. Validate: chạy schema/frontmatter validation nếu tool có sẵn; làm ít nhất sáu scenario-based forward tests: (1) successful mini-goal; (2) failed but in-scope goal tự sửa; (3) unauthorized contract modification; (4) safety gate fail; (5) unsafe refactor regression; (6) Phase 5 feedback tạo backlog. Có thể dùng toy fixtures và kiểm tra thủ công minh bạch nếu không có test harness; không giả mạo kết quả.
E. Audit & refine: phát hiện contradictory instructions, over-engineering, missing boundaries, ambiguous exit gates; sửa đến khi acceptance criteria của LGD_HANDOFF.md đạt hoặc báo blocker cụ thể.

# AUTONOMY & LOOP
Duy trì backlog của chính nhiệm vụ tạo skill trong repo hoặc báo cáo phiên. Tự phát hiện sub-goals, thực hiện tuần tự, tự validate rồi fix. Không yêu cầu tôi approve từng sub-goal. Chỉ dừng hỏi nếu phải thay đổi hành vi tôi đã chốt, phá dữ liệu/file hiện hữu, tăng chi phí/rủi ro quan trọng hoặc thiếu thông tin mà không có safe choice hợp lý. Không sửa LGD_HANDOFF.md để hợp thức hóa sai lệch; nếu đề nghị cập nhật, ghi rõ diff và lý do.

# FINAL DELIVERY FORMAT
1. Danh sách files đã tạo/sửa và chức năng từng file.
2. Cách invoke skill, cùng một ví dụ đơn giản cho một feature cụ thể.
3. Matrix mapping [U] requirements và acceptance criteria trong handoff → rule/template/evaluation tương ứng.
4. Evidence của validation, bao gồm các test đã chạy, fail và còn thiếu.
5. Những câu hỏi mở/risks cần thảo luận ở phiên sau; tuyệt đối không ngụy tạo trạng thái completed.

# ACCEPTANCE GATE
Phải thỏa các acceptance criteria ở mục 13.3 của LGD_HANDOFF.md trước khi tự tuyên bố hoàn thành. Nếu điều kiện nào không thể đạt, nêu rõ blocker/evidence và phương án xử lý thay vì tuyên bố thành công.
