# Contract và discovery

Đọc file này cho mode `define-contract` và mỗi khi cần quyết định "behavior nào đang được kiểm soát".

## 1. Ranh giới thẩm quyền

Thứ tự thẩm quyền:

`Project rubric/scope → Feature → Module → Implementation`

- **Project rubric/scope** xác định điều gì quan trọng, ai phê duyệt, rủi ro nào bị chặn.
- **Feature** mô tả outcome người dùng/nghiệp vụ quan sát được.
- **Module** mô tả interface, dữ liệu, lỗi, side effect và invariant cần để feature hoạt động.
- **Implementation** là lựa chọn cấu trúc/thuật toán/thư viện trong boundary đã duyệt.

L0–L3 là control view, không phải kiến trúc cố định. Không tạo layer/folder/service chỉ để "đủ bốn lớp". Agent được đề xuất implementation, không được tự đổi nghĩa của outcome hoặc invariant.

## 2. Discovery tuần tự

### 2.1. Nguyên tắc

- Mỗi lần chỉ giải quyết **một quyết định hiện tại**. Không gom nhiều câu hỏi thành một bảng khảo sát.
- Trước khi hỏi, kiểm tra câu trả lời đã có trong contract, decision log, rubric hoặc tài liệu hiện có. Không hỏi lại điều đã trả lời và còn hiệu lực.
- Câu hỏi phải nêu: quyết định đang thiếu, vì sao cần cho behavior hiện tại, lựa chọn/trade-off nếu có, recommendation và safe default nếu thật sự an toàn.
- Không tự điền expected output, threshold, danh sách edge case hoặc business rule để "chạy tiếp".
- Secret không bao giờ được ghi vào Markdown/prompt/log. Nếu cần secret, yêu cầu người dùng cung cấp qua kênh an toàn đã cấu hình; ghi `BLOCKED_USER` nếu chưa có.

### 2.2. Thứ tự xử lý khi thiếu thông tin

1. Có rubric + scope → dùng rubric để xác định requirement/behavior còn thiếu trong scope hiện tại.
2. Chỉ có scope → dùng scope để nhận diện phần thiếu; không suy diễn rubric.
3. Không có cả rubric và scope → phỏng vấn BA/người có thẩm quyền **trước Phase 0**; chưa tạo contract, chưa code.
4. Có behavior nhưng thiếu test case **và** expected output → hỏi để làm rõ trước implementation.
5. Có test case hoặc expected output → chuyển thành contract case; vẫn phải xác định critical invariant nếu rủi ro đáng kể.

### 2.3. Phạm vi behavior

Ưu tiên:

- Happy path đại diện cho giá trị chính.
- Critical risk invariant: dữ liệu không mất, không trùng bản ghi, không vượt quyền, không sai tiền, không mất provenance, không nuốt lỗi, idempotency khi cần.
- Failure quan sát được ở boundary quan trọng.

Không mở rộng sang edge case ít giá trị kiểm chứng, tổ hợp hiếm hoặc chi tiết implementation. Nếu một edge case có thể làm sai invariant/business outcome, nó thuộc nhóm critical risk; nếu chỉ làm code "kín kẽ hơn", đưa vào backlog/proposal.

## 3. Tiêu chí atomic và vertical slice

Một đơn vị behavior đủ atomic khi:

- Có outcome độc lập, quan sát được.
- Có thể kiểm thử/kiểm chứng mà không cần hoàn tất behavior khác.
- Có boundary và invariant rõ.
- Nếu chia nhỏ hơn, chỉ thêm chi tiết implementation hoặc test nội bộ, không thêm khả năng kiểm chứng hay giá trị quan sát được.

Đây là **diễn giải vận hành**. Không biến nó thành quota số lớp, số file, số test hay "depth" cố định.

Vertical slice:

```text
feature outcome
  → behavior hiện tại
  → L0 acceptance tối thiểu
  → L1/L2 contract tối thiểu cho behavior đó
  → L3 implementation
  → evidence + observation
```

Slice đi xuyên các lớp cần thiết, không nhất thiết đi qua mọi lớp nếu lớp đó không có quyết định quan trọng.

## 4. Contract tối thiểu

### 4.1. Feature behavior (L0)

Phải trả lời được:

- Ai dùng, trong tình huống nào?
- Input/điều kiện quan sát được.
- Expected outcome, kể cả lỗi quan sát được.
- Critical invariant.
- Case cụ thể hoặc expected output do người có thẩm quyền cung cấp/xác nhận.
- Điều gì **ngoài scope**.

### 4.2. Interaction/module (L1/L2)

Chỉ ghi phần cần cho behavior hiện tại:

- Input/output/schema ở boundary.
- Error semantics và side effect.
- Ordering/idempotency/retry nếu quan trọng.
- Invariant dữ liệu/quyền/transaction.
- Dependency và trạng thái xác minh.

### 4.3. Implementation (L3)

Không cần contract chi tiết cho mọi lựa chọn code. Chỉ ghi ràng buộc thật sự ảnh hưởng behavior/invariant hoặc quyết định khó đảo ngược. Agent tự chọn chi tiết trong boundary.

### 4.4. Metadata tối thiểu

Mỗi contract nên có: `id`, `version`, `status`, `owner/approver`, `date`, `scope`, `cases/expected outputs`, `invariants`, `dependencies`, `open questions`. Không cần schema cố định nếu repository đã có format tốt hơn; dùng `assets/behavior-contract.template.md` khi chưa có.

## 5. Rolling freeze

Trước khi code một behavior/module:

1. Xác định phần **sẵn sàng** (behavior + module + upstream/dependency trực tiếp).
2. Làm rõ case/expected output và critical invariant.
3. Ghi version, trạng thái `APPROVED`/`FROZEN`, owner/approver, ngày.
4. Kiểm tra dependency: đã xác minh thật hay mới mock.
5. Chỉ freeze phần đã sẵn sàng; không freeze toàn bộ hệ thống tương lai.

Có thể:

- Triển khai module A đã freeze trong khi tuần tự định nghĩa module B.
- Định nghĩa feature N+1 trước khi implementation N xong, nếu N+1 không phụ thuộc vào chi tiết chưa chốt của N.
- Giữ dependency chưa xác minh ở `NOT VERIFIED`; mock chỉ chứng minh hợp đồng giả định, không chứng minh integration.

Không được:

- Tự tạo nhiều agent song song để lấp phần chưa định nghĩa.
- Coi "đã có mock" là "đã tích hợp".
- Freeze một contract rồi âm thầm sửa implementation cho khác contract.

## 6. Change control và commit gate

Thay đổi contract/test đã freeze phải có change request:

- Lý do và evidence.
- Decision/case/invariant bị ảnh hưởng.
- Phương án gốc, phương án thay thế, trade-off.
- Rủi ro, reversibility, owner/approver.
- Version mới và regression cần chạy.

Trước khi change request được duyệt: không sửa expected output, không bỏ assertion, không skip, không nới threshold, không chỉnh fixture để pass.

Commit:

- Chỉ commit contract đã freeze nếu repository policy và quyền cho phép.
- Nếu không được commit, ghi rõ `commit gate: NOT SATISFIED`/lý do; không tuyên bố đã commit.
- Nếu dự án yêu cầu commit trước implementation, coi đó là gate bắt buộc; không bỏ qua.

## 7. Điều kiện kết thúc `define-contract`

Chỉ chuyển sang implementation khi:

- Behavior hiện tại có outcome và boundary rõ.
- Có case cụ thể hoặc expected output đủ để viết test.
- Critical invariant đã được nêu hoặc quyết định là không có rủi ro đáng kể.
- Không còn câu hỏi behavior nghiêm trọng chưa xử lý.
- Contract/version/owner đã ghi; phần sẵn sàng đã freeze.
- Dependency status được ghi trung thực.

Nếu thiếu điều kiện: giữ `APPROVAL_NEEDED`/`BLOCKED_USER` với câu hỏi hiện tại; không code thay thế.

## 8. Báo cáo mode này

Trả lời:

- Contract/version và phần được freeze.
- Case/expected output và invariant đã dùng.
- Câu hỏi hiện tại (nếu có) và vì sao chưa thể tiến.
- Dependency `VERIFIED`/`NOT VERIFIED`.
- Điều đã là `ASSUMPTION`, điều còn `PROPOSAL`.
- Bước tiếp theo: `execute-mini-goal` hoặc chờ quyết định.
