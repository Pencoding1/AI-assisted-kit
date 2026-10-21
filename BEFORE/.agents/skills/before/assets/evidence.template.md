# Gate evidence

- **Goal/Mini-goal:** `<ID>` · **Contract/version:** `<...>`
- **Ngày/chạy bởi:** `<...>` · **Môi trường:** `<...>`

## Artifact

- **Diff/file:** `<đường dẫn thật>`
- **Commit:** `<hash nếu có; nếu không: "không có — lý do">`
- **Allowed path check:** `<...>`

## Command và kết quả

| Mục đích | Command | Exit | Kết quả quan trọng |
|---|---|---|---|
| RED | `<...>` | `<...>` | `<...>` |
| GREEN/acceptance | `<...>` | `<...>` | `<...>` |
| Safety | `<...>` | `<...>` | `<...>` |
| Regression | `<...>` | `<...>` | `<...>` |

## Đánh giá

- **Acceptance:** `PASS|FAIL|NOT RUN` — `<bằng chứng>`
- **Safety/invariant:** `PASS|FAIL|NOT RUN` — `<bằng chứng>`
- **Regression:** `PASS|FAIL|NOT RUN` — `<bằng chứng>`
- **Integration thật:** `VERIFIED|NOT VERIFIED` — `<mock chỉ là NOT VERIFIED>`
- **Test integrity:** `OK|VIOLATION` — `<không skip/weaken>`
- **Release readiness:** `READY|NOT READY|NOT VERIFIED` — `<lý do>`

## Truth labels

- **VERIFIED FACT:** `<...>`
- **INFERENCE:** `<...>`
- **ASSUMPTION:** `<...>`
- **PROPOSAL:** `<...>`
- **BLOCKER:** `<...>`
- **NOT VERIFIED:** `<...>`

## Deviation / limitation

`<...>`
