import random
from decimal import Decimal

from ordercalc.pricing import LineItem, calculate_total

VAT = Decimal("0.081")
APPROVAL_LIMIT = Decimal("180.00")


def test_bulk_order_stays_below_approval_limit() -> None:
    items = [
        LineItem(sku=f"SKU-{n}", unit_price=Decimal("9.90"), quantity=random.randint(1, 10))
        for n in range(3)
    ]
    result = calculate_total(items, vat_rate=VAT)
    assert result.total < APPROVAL_LIMIT
