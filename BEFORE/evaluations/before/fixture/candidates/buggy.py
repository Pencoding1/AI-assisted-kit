"""In-scope bug: banker's rounding instead of half-up."""


def _require_int(value, name, minimum, maximum=None):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an int")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name} must be <= {maximum}")


def invoice_total_cents(items, discount_percent):
    _require_int(discount_percent, "discount_percent", 0, 100)

    subtotal = 0
    for item in items:
        try:
            quantity, unit_price_cents = item
        except (TypeError, ValueError):
            raise ValueError("each item must be a (quantity, unit_price_cents) pair")
        _require_int(quantity, "quantity", 1)
        _require_int(unit_price_cents, "unit_price_cents", 0)
        subtotal += quantity * unit_price_cents

    return round(subtotal * (100 - discount_percent) / 100)
