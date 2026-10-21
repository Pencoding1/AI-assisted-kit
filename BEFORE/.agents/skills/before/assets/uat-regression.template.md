# UAT → regression

- **UAT case ID:** `UAT-<...>` · **Ngày:** `<...>`
- **Feature/contract/version:** `<...>`
- **Người xác nhận:** `<vai trò + người thật>` · **Môi trường:** `<...>`
- **Trạng thái:** `CONFIRMED|REJECTED|NEEDS CLARIFICATION`

## Case

- **Input/điều kiện:** `<...>`
- **Expected outcome:** `<...>`
- **Observed outcome:** `<...>`
- **Bằng chứng:** `<path/log/ảnh — không bịa>`

## Phân biệt

- **Approved behavior:** `<điều người có thẩm quyền đã xác nhận>`
- **Observed behavior:** `<điều hệ thống đang làm>`
- **Chênh lệch:** `<...>` — nếu observed khác approved, đây là bug/contract gap, không tự thành contract.

## Regression mapping

| Test level | Test name/path | Trạng thái |
|---|---|---|
| acceptance/integration/module/unit | `<...>` | `<chưa viết/RED/GREEN>` |

- **Nondeterminism/tolerance:** `<invariant/schema/tolerance có lý do>`
- **Bug/issue link:** `<...>`
- **Mini-goal đề xuất:** `<...>` — chỉ là `PROPOSAL` nếu chưa duyệt.
