# BEFORE v1 — Kiểm chứng và lock

Ngày: 2026-10-21. Root: `E:/Project/AI-assisted-kit/Layer-Gated Development`.

## Kết quả

- Skill validator: PASS (exit 0).
- Fixture A/B/D/E: PASS (exit 0); gồm các fail chủ đích quan sát được rồi GREEN, tests/contract không đổi. Không chứng minh agent tự sửa code: runner chọn các candidate đã soạn sẵn.
- Independent forward evaluation: 10 tình huống, phản hồi/hành động mô phỏng; raw report tại `evaluations/before/independent-forward-report.md`. Không có code, UAT, deployment thực thi trong lượt đó.
- Policy model và structure checks: PASS (exit 0), chỉ kiểm ví dụ deterministic/presence markers; không tính là bằng chứng LLM hay semantic sync.
- Hai file nguồn không đổi (`git diff --exit-code` = 0). Chỉ thêm file BEFORE; chưa commit/cài global/deploy.

Evidence máy đọc được: `evaluations/before/final-tool-evidence.json`, chứa argv, stdout, stderr, exit code thực của từng lệnh sau editorial review.

## Ma trận yêu cầu và acceptance criteria

| Nguồn | Rule / template | Evidence / giới hạn |
|---|---|---|
| U1 giảm review bottleneck | D-07/D-13, mini-goal/evidence templates | Forward cases 1/2; hiệu quả cần pilot |
| U2 sáu phase | D-02, execution-gates-lifecycle | Đối chiếu lifecycle; không ánh xạ RGR thành phase |
| U3 layer + mini-goal | D-03/D-05/D-06, behavior/mini-goal | Forward case 8; rolling freeze |
| U4 RGR + regression | D-02/D-10, UAT mapping | Fixture A/E; forward 5/6 |
| U5 MVP nhanh và safety | D-09, evidence template | Fixture D; forward 4 |
| U6 feedback tạo vòng tiếp | feedback-and-pilot | Forward 6; new scope vẫn PROPOSAL |
| U7 dấu vết quyết định | D-07/D-13, change request/decision log | Forward 3; không sửa contract cho xanh |
| Traceability | BEFORE_DECISIONS mapping U/P/O/C; contract/version → tests → diff → observations | Review nội dung; ID theo bảng chat |
| No overengineering | Một skill, 4 references, 8 templates; không runtime service | File inventory/usage giải thích mục đích |
| Correct RGR | Already-GREEN verify/refactor không ép RED | Fixture E; forward 1/5 |
| Bounded autonomy | Tự sửa approved scope, chỉ chặn dependency thiếu | Forward 2/8/9 |
| Test integrity | CR có approval/version/impacted cases | Forward 3/5; hash fixture tests giữ nguyên |
| Phase/layer clarity | Lifecycle ngoài, control views trong, Project → Feature → Module | Review contracts/lifecycle |
| Evidence | Truth labels và NOT VERIFIED | Raw command evidence; không claim mocks/live equivalence |
| Production awareness | Safety, migration integrity/compatibility/recovery, side effects | Fixture D; live production chưa kiểm chứng |
| Adaptation | Inspect/reuse existing repo; Markdown state | Source diff exit 0; không AGENTS override |
| Evaluation >=6 cases | Forward 1 thành công, 2 fail scope, 3 đổi semantics, 4 safety, 5 refactor, 6 feedback | 10 case mô phỏng độc lập, 4 case fixture chạy thật |
| Concise handoff | BEFORE_USAGE + SKILL.md | Invocation và limitations có trong usage |
| Yêu cầu mới | Sequential discovery, atomic behavior, rolling freeze, tên BEFORE | D-01/D-04/D-05/D-06; forward 7/8 |

## Điều chỉnh sau đánh giá độc lập

Đã làm rõ: behavior vốn đúng chỉ verify; thiếu key phân loại theo người có quyền xử lý; security gate fail chặn release nhưng fix an toàn trong scope không mặc định cần approval; mutation hỏi từng quyết định. Đã sửa metric về `T_delivery = t_accepted - t_start` (feature start → human deploy acceptance, gồm chạy/chờ), và phục hồi U1–U7/C2 theo ID đã trình duyệt trong chat. Đây là sửa bản dựng để khớp quyết định đã duyệt, không tự tạo quyết định nghiệp vụ mới.

## Failed attempts và giới hạn

- Launcher OpenCode cũ có `--dir` không còn hợp lệ (exit 1); đọc help và chạy lại bằng cwd đúng, exit 0. Session: `ses_ea23ee201ffegmHiy6vcCmgHCJ`.
- Một lượt fixture trong sandbox fail vì quyền ghi TEMP (exit 1); rerun với TEMP trong writable workspace pass. Lượt final dùng quyền ghi thư mục dự án đã được phép.
- Validator/generator mặc định Windows có lỗi encoding; validator final chạy `-X utf8`. UI metadata optional không cần cho v1, không giữ file lỗi.
- Chưa kiểm chứng Codex discovery trong phiên mới, UAT thật, live API/production, pilot một tháng. Không dùng unit/fixture pass để claim release hoặc hiệu quả thực nghiệm.
- Bốn mutation stop conditions lịch sử vẫn không có; hỏi policy theo dự án trước khi chạy mutation. Coverage/retry/telemetry/hardening tiếp tục là interview tuần tự theo dự án.
- Lock là governance snapshot v1.0 với hash, không phải OS read-only/ACL. Thay đổi quyết định cần change request được duyệt + version mới, đồng bộ portable snapshot. Không tự tạo git commit.

## SHA256 cuối

Hash được tính trên byte thực sau editorial review. Manifest không hash chính báo cáo này để tránh tự tham chiếu. Hash phát hiện artifact đổi, không chứng minh quyết định đúng; thay đổi template/code qua review phù hợp, thay đổi quyết định qua CR/version.

| File | SHA256 |
|---|---|
| `BEFORE_DECISIONS.md` | `a7425744c06b55253f8f817e7a44c4946f64d8d553b2380be86f06a54fb96810` |
| `BEFORE_USAGE.md` | `d463a0bb791b48c3541546297d246c80fa4adccaeb9277b1330aa201a906a9a7` |
| `.agents/skills/before/assets/behavior-contract.template.md` | `278cee646b0fd37f7f4bc7fbe6b5a433647deb9f8fa1b34972a61cbb2693c422` |
| `.agents/skills/before/assets/change-request.template.md` | `6b0b14782fccd4e556253affe1bb9f9ee64f4a5c64a288e00ec88f2c49d565bc` |
| `.agents/skills/before/assets/decision-assumption.template.md` | `d29a1407fc8a6449ae7bdb8810e1484ec4b39c15f52c98e600f9147b9f27b6a3` |
| `.agents/skills/before/assets/evidence.template.md` | `d0e5fbbc12da784691d98c14011819afd3ae37b1160ce12e6bb625d312979184` |
| `.agents/skills/before/assets/mini-goal.template.md` | `115a986366c45d16897710aaa7a289a4c7bb50e58ba2ee1c9bf455853831ede6` |
| `.agents/skills/before/assets/pilot-log.template.md` | `9b921fe3524e59623c03d8c005347fc28b1d8da6726397ddc8e4bbc3c7e44821` |
| `.agents/skills/before/assets/project-rubric.template.md` | `c1f3e45ae846e1f7d5a394a2387f0617835b1894df1b5dbd4cf658e9630a2ced` |
| `.agents/skills/before/assets/uat-regression.template.md` | `88bc586351640be8ccf33ed211538f98bce058a5c7f28746d13199579c8fd54a` |
| `.agents/skills/before/references/contract-and-discovery.md` | `7800bd5fc101750cf106bdd3b2d9a19e151f5ae6a95581d0706687bd5bd2dfe5` |
| `.agents/skills/before/references/decisions.md` | `0b7c8cc708a740c124ced2bb3b93bf8dc89b0481dda6b9088029ca5ddcf30fc8` |
| `.agents/skills/before/references/execution-gates-lifecycle.md` | `209205d5cc3cdb9b6c2382c403ac3beadcfd8e33e77907d7b0ffd08154c0030c` |
| `.agents/skills/before/references/feedback-and-pilot.md` | `047cfb7281eeec13818b84c47312778818683985bf74a298c7ccb1771b1d1ae6` |
| `.agents/skills/before/SKILL.md` | `1738fad5d9abb4979fcf7b40a4b8b87c933244aa893f387660b6210d005870d7` |
| `evaluations/before/check_bundle.py` | `39de67cca390313ed1bb5e138f948f0f487e331a03071cf57de75b777b0f3749` |
| `evaluations/before/final-tool-evidence.json` | `8c89daf85825155e5a6f393a0d7edbd3a0986f20ae4dd55acdcec1d09e474b7e` |
| `evaluations/before/fixture/app/__init__.py` | `c3abcb081df5cbfd551c3ce8dc24feecae3212116e587b5a432f59a7cb5bcc38` |
| `evaluations/before/fixture/candidates/baseline.py` | `816531d2cc1c2dae838934fa6e5ad4cbaac51596acffba30d051d4289392c7bd` |
| `evaluations/before/fixture/candidates/buggy.py` | `b52ac18e6a28dae8101cb8e8cc423bd7c28bf2945b16b8ade8e754a57c8d21cd` |
| `evaluations/before/fixture/candidates/good.py` | `3cb5182bd11e69d10a7a1f8f8a82463dd6d86221e4e9d076dd4ebd2eed04a7f2` |
| `evaluations/before/fixture/candidates/refactor_bad.py` | `6c5fa2163b81bd29a901c7ecba860c875cf86fdc570c38bed1825751f81b463d` |
| `evaluations/before/fixture/candidates/unsafe.py` | `b012d514e6f25adc38dfc904af418e24084ab619749467391c6afe84ef3e2d08` |
| `evaluations/before/fixture/contract.md` | `46425459dae5889904d80c98c0ae2d8cbc98898679ec7f69b198f689ad77a3f3` |
| `evaluations/before/fixture/tests/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `evaluations/before/fixture/tests/acceptance/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `evaluations/before/fixture/tests/acceptance/test_order_total.py` | `a6c2ded51088e8a9e2d2fa6248a74e05d336c33db444cf73d001fb29225b1f40` |
| `evaluations/before/fixture/tests/safety/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `evaluations/before/fixture/tests/safety/test_order_total.py` | `b38ea8102a234a79b671f7fa8d812f069aeaa29f23cbbffd20890fe7c657b856` |
| `evaluations/before/forward-scenarios.md` | `f3168ea342a0504a180394fc9e6041b908051397bd1edeeb0c7dad1e7711c44e` |
| `evaluations/before/independent-forward-followup.md` | `09f7e0a3d14ce64f85531339f1648e60d5af3d0f7d71585eebf6df8677e55bfd` |
| `evaluations/before/independent-forward-report.md` | `10f40b0bb9d6efdf81a3ddea5f9fc82ced7ed85277dacba7c636b6cd23530a03` |
| `evaluations/before/policy_model.py` | `d69daf933571e2f219f990ca400a7d39704f7a8d282796d341bec2de34ccd52d` |
| `evaluations/before/README.md` | `090945928f8614ae13df636f804d33c24119265b8ce3330844574a2d28b8fc7a` |
| `evaluations/before/run_fixture.py` | `b06cd84dcafad1c38bf1855b284b810304edac925ecb41c78f2e01929befb63d` |
