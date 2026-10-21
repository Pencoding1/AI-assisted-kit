# FT-ORDER-001 — Tính tổng đơn hàng (fixture)

- **Version:** 1 · **Status:** `FROZEN` (fixture, không phải quyết định của người dùng)
- **Mục đích:** fixture độc lập để kiểm chứng cơ chế RED/GREEN/safety/regression của bundle.

## Cases

| Case | Input | Expected |
|---|---|---|
| A1 | `[(2, 50000), (1, 25000)]`, discount `10` | `112500` |
| A2 | `[(1, 9999)]`, discount `100` | `0` |
| A3 | `[(1, 5)]`, discount `50` | `3` (half-up) |
| A4 | discount `101` hoặc `-1` | `ValueError` |

## Invariants

- `INV-1`: tổng là `int` cents (không phải `bool`, không phải `float`), `0 <= total <= subtotal`.
- `INV-2`: quantity là `int >= 1`; unit price là `int >= 0`; input sai → `ValueError`.
- `INV-3`: discount là `int` trong `0..100`; sai → `ValueError`.
- `INV-4`: giỏ rỗng trả `0` (int).

## Không thuộc fixture

Không có UAT thật, production data, deployment hay người dùng thật. Đây là contract hư cấu phục vụ kiểm chứng kỹ thuật.
