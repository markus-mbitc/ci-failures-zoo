"""Small CLI: calculates a sample order."""

from decimal import Decimal

from ordercalc.config import get_settings
from ordercalc.pricing import LineItem, calculate_total


def main() -> None:
    settings = get_settings()
    items = [
        LineItem(sku="COFFEE-250G", unit_price=Decimal("12.90"), quantity=2),
        LineItem(sku="MUG", unit_price=Decimal("8.50"), quantity=1),
    ]
    result = calculate_total(items, vat_rate=settings.vat_rate, discount_pct=Decimal("10"))
    print(f"API:      {settings.api_url}")
    print(f"Subtotal: CHF {result.subtotal:.2f}")
    print(f"Discount: CHF {result.discount:.2f}")
    print(f"VAT:      CHF {result.vat:.2f}")
    print(f"Total:    CHF {result.total:.2f}")


if __name__ == "__main__":
    main()
