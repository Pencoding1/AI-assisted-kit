# Project rubric / cấu hình BEFORE

> Điền từ project interview. Không dùng giá trị mặc định cho các mục đánh dấu `(hỏi dự án)`.

- **Project:** `<tên>`
- **Scope hiện tại:** `<feature/module/behavior>`; **ngoài scope:** `<...>`
- **Owner/approver:** `<vai trò + người>`
- **Ngôn ngữ/test framework:** `<...>`

## Rubric rủi ro (hỏi dự án)

| Mức | Tiêu chí | Cần escalation/review |
|---|---|---|
| normal | `<...>` | `<...>` |
| high | `<...>` | `<...>` |
| critical | `<...>` | `<...>` |

## Gate và môi trường (hỏi dự án)

- **Test command:** `<...>`
- **Safety/regression command:** `<...>`
- **Coverage:** `<ngưỡng hoặc "không đặt">`
- **Retry/rate-limit policy:** `<...>`
- **Telemetry/instrumentation:** `<...>`
- **Hardening cadence:** `<...>`
- **Migration/recovery gate:** `<...>`

## Quyền và boundary

- **Allowed paths:** `<...>`
- **Protected paths/actions:** `<...>`
- **Commit gate:** `<bắt buộc/không; người cho phép>`
- **Deploy/UAT authority:** `<...>`
- **Kênh nhận secret an toàn:** `<...>` — không ghi secret vào file này.

## Pilot (nếu có)

- **Baseline:** `<workflow/feature so sánh>`
- **Window đo defect:** `<...>`
- **Session log schema:** `<...>`
- **Human accept deploy:** `<người/kênh>`

## Open interview

| ID | Câu hỏi hiện tại | Trạng thái |
|---|---|---|
| PI-`<...>` | `<một câu>` | `<chờ trả lời/đã chốt>` |
