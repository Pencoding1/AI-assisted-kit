# Mini-goal

- **ID:** `MG-<...>` · **Phase:** `<0-5>` · **Status:** `BACKLOG|READY|ACTIVE|FIXING|VERIFIED|DONE|BLOCKED|APPROVAL_NEEDED`
- **Parent:** `<feature/module>` · **Contract/version:** `<...>`
- **Risk:** `normal|high|critical` theo rubric dự án

## Objective

`<Một outcome quan sát được, đủ nhỏ để review diff/evidence.>`

## Scope

- **In scope:** `<paths/behavior>`
- **Out of scope:** `<...>`
- **Allowed changes:** `<...>`
- **Protected paths/actions:** `<...>`

## Behavior và invariant

| Behavior/case | Expected outcome | Test |
|---|---|---|
| `<...>` | `<...>` | `<tên test>` |

- **Critical invariant:** `<...>`
- **RED dự kiến:** `behavior chưa có | bug đã xác nhận` — `<bằng chứng>`

## Dependency và giả định

- **Dependency:** `<ID>` — `VERIFIED|NOT VERIFIED|MOCK ONLY`
- **Assumption:** `<...>`
- **Unknown:** `<...>` — nếu ảnh hưởng expected output, dừng và hỏi.

## Evidence bắt buộc

- [ ] Diff/artifact path
- [ ] Command + exit cho RED
- [ ] Command + exit cho GREEN
- [ ] Safety/regression result
- [ ] Output/observation thực
- [ ] Deviation/known limitation

## Điểm dừng

`<Khi nào VERIFIED; khi nào APPROVAL_NEEDED/BLOCKED; không tự mở rộng scope.>`
