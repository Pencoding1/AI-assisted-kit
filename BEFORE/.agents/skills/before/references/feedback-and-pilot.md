# Feedback, regression và pilot

Đọc file này cho `capture-feedback/replan` và khi chuẩn bị Phase 4/5.

## 1. Nguồn feedback

| Nguồn | Cách xử lý | Không được |
|---|---|---|
| UAT case được người thật xác nhận | Tạo regression ở mức phù hợp; link case → test → contract/version. | Tự tuyên bố UAT pass; coi feedback chưa xác nhận là approved. |
| Production bug đã xác nhận | Tạo regression tái hiện bug; link issue/root cause/mini-goal. | Chỉ sửa code mà không có test/regression. |
| Characterization trên legacy | Ghi observed behavior; đánh dấu rõ chưa approved. | Khóa bug thành contract vì production đang làm vậy. |
| Feedback mới/ý tưởng feature | Đưa vào backlog `PROPOSAL`, chưa phải scope. | Tự triển khai hoặc tự thêm vào contract hiện tại. |
| Quan sát telemetry/log | Ghi observation + window + nguồn; đề xuất điều tra. | Suy ra nhân quả hoặc "đã xác nhận bug" từ tương quan. |

## 2. UAT → regression

Một UAT case chỉ trở thành baseline khi:

- Có người thật/nghiệp vụ xác nhận outcome, không phải agent tự kết luận.
- Ghi rõ input/điều kiện, expected outcome, môi trường và ngày.
- Phân biệt **approved behavior** với **observed behavior**.
- Map sang test chạy lại được ở mức phù hợp: acceptance, integration, module hoặc unit. Không bắt buộc mọi UAT là E2E.
- Nếu output không xác định: dùng invariant/schema/tolerance có lý do hoặc dataset đã adjudicate; không gán một output biến thiên làm oracle tuyệt đối.

Dùng `assets/uat-regression.template.md`. Test regression phải là test thật, chạy được, không phải mô tả bằng lời.

## 3. Production bug → regression

1. Xác nhận bug bằng evidence (log, trace, repro, dữ liệu).
2. Viết test tái hiện bug; chạy để thấy fail đúng lý do (RED hợp lệ).
3. Sửa trong scope; chạy test mới + regression liên quan + safety.
4. Link bug → test → mini-goal/contract liên quan.
5. Nếu bug cho thấy contract thiếu/sai: change request, không âm thầm đổi behavior.

Bug đã xác nhận là nguồn regression hợp lệ. Observation chưa xác nhận thì chưa.

## 4. Phân loại feedback và replan

Mỗi feedback khi triage phải rơi vào một nhóm:

- `CONFIRMED BUG` — có evidence tái hiện; sửa/regression trong scope nếu đã được duyệt, hoặc đề xuất mini-goal.
- `CONTRACT GAP` — behavior chưa rõ/contract thiếu; quay lại `define-contract`, hỏi một câu hiện tại.
- `NEW FEATURE` — proposal backlog; không tự thành scope.
- `DEBT/HARDENING` — proposal cho Phase 4/5; cần risk/impact.
- `NOISE/OBSERVATION` — ghi lại, không hành động nếu không có giá trị.

Backlog item tối thiểu: ID, loại, nguồn, impact, evidence, testable outcome, dependency, owner đề xuất, trạng thái `PROPOSAL`. Không đánh dấu `READY` nếu chưa được duyệt.

`replan` chỉ sắp xếp lại các mini-goal **đã duyệt** hoặc đề xuất backlog. Không biến backlog thành scope, không đổi expected output để khớp feedback.

## 5. Mutation testing (Phase 5)

- Chỉ sau Phase 4, khi regression baseline đủ ổn định; không phải gate bắt buộc mọi MVP/mini-goal.
- Mục tiêu: statistical convergence + risk convergence; critical logic được kiểm chứng, không chỉ nhìn mutation score.
- Bốn stop condition lịch sử được nhắc tới nhưng **không có trong artifact hiện có**. Đánh dấu `[HISTORICAL-MISSING]`; không được bịa.
- Trước khi chạy mutation phải có chính sách dừng được duyệt. Nếu thiếu, hỏi một quyết định, ví dụ: "Tiêu chí dừng nào được dùng cho lần mutation này?" Sau câu trả lời mới hỏi phần còn thiếu về scope, risk, budget hoặc mutant sống; không gộp thành một câu hỏi nhiều phần.
- Nếu chưa có chính sách: `APPROVAL_NEEDED`, không chạy mutation.
- Behavior chưa rõ phát hiện qua mutation → proposal backlog, không tự thành expected behavior.

## 6. Pilot một tháng

### 6.1. Thiết kế

- So sánh **BEFORE** với **BASELINE** trên feature thật, một tháng.
- Dùng Markdown session log; không tạo database/automation mới.
- Ghi cả chi phí soạn contract để tránh chỉ đo tốc độ code.
- Không lên lịch automation, không chạy external service trong bundle này.

### 6.2. Metric và định nghĩa

| Metric | Định nghĩa |
|---|---|
| Delivery lead time | Từ lúc bắt đầu feature đến lúc người dùng chấp nhận deploy: `T_delivery = t_accepted - t_start`; gồm thời gian chạy và chờ. |
| Human attention | Tổng thời lượng can thiệp thực tế của con người; không phải thời gian đồng hồ ước lượng. |
| Cold-start | Thời gian/chi phí để người hoặc agent mới hiểu và bắt đầu làm việc trong workflow. |
| Intervention count | Số lần con người phải can thiệp. |
| Rework | Công việc phải làm lại do lỗi/contract/implementation. |
| Accepted deployment evidence | Bằng chứng deployment được con người chấp nhận; không phải tuyên bố của agent. |
| Defect rate | Số defect / mẫu, với window đo và nguồn case xác định. |

Ghi thêm: feature, môi trường, dependency, exception, known limitation, chất lượng evidence.

### 6.3. Giới hạn

- Pilot **chưa được hoàn thành** bằng việc tạo skill. Không có metric/baseline/UAT thật trong bundle này.
- Kết quả (khi có) là quan sát, có giới hạn do độ khó feature, mẫu nhỏ và cách chọn case; không tuyên bố nhân quả hoặc "chứng minh hiệu quả" nếu thiết kế chưa đủ.
- Không so sánh bằng cảm nhận hoặc test count; không tối ưu % green.
- Human accept deploy là quyết định của con người; agent chỉ ghi evidence.

## 7. Escalation từ feedback

Chỉ escalation khi xung đột có căn cứ/bằng chứng cụ thể:

- Feedback mâu thuẫn với contract đã duyệt.
- Bug cho thấy invariant/safety bị vi phạm.
- Thay đổi cần thiết vượt scope/quyền hoặc có rủi ro cao/khó đảo ngược.
- Không đủ dữ liệu để phân biệt bug với môi trường.

Không escalation vì feedback mơ hồ, cảm tính hoặc chưa được xác nhận; ghi observation/proposal thay vì tạo quyết định giả.

## 8. Báo cáo mode này

Trả lời: feedback nào đã xác nhận, evidence nào; case nào thành regression; case nào chỉ là observed/proposal; backlog item mới (chưa duyệt); contract gap cần hỏi; mutation/pilot có được chạy hay không và vì sao; `NOT VERIFIED` còn lại.
