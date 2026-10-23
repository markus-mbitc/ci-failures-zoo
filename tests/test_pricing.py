from decimal import Decimal

import pytest

from ordercalc.pricing import LineItem, calculate_total, round_to_rappen

VAT = Decimal("0.081")


def test_line_item_total() -> None:
    assert LineItem("A", Decimal("2.50"), 4).total == Decimal("10.00")


def test_line_item_rejects_zero_quantity() -> None:
    with pytest.raises(ValueError):
        LineItem("A", Decimal("1.00"), 0)


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        (Decimal("10.02"), Decimal("10.00")),
        (Decimal("10.025"), Decimal("10.05")),
        (Decimal("10.07"), Decimal("10.05")),
        (Decimal("10.08"), Decimal("10.10")),
    ],
)
def test_round_to_rappen(amount: Decimal, expected: Decimal) -> None:
    assert round_to_rappen(amount) == expected


def test_calculate_total_with_discount() -> None:
    items = [LineItem("COFFEE", Decimal("12.90"), 2), LineItem("MUG", Decimal("8.50"), 1)]
    result = calculate_total(items, vat_rate=VAT, discount_pct=Decimal("10"))
    assert result.subtotal == Decimal("34.30")
    assert result.discount == Decimal("3.43")
    assert result.total == Decimal("33.35")


def test_calculate_total_empty_order() -> None:
    assert calculate_total([], vat_rate=VAT).total == Decimal("0")


def test_calculate_total_rejects_invalid_discount() -> None:
    with pytest.raises(ValueError):
        calculate_total([], vat_rate=VAT, discount_pct=Decimal("120"))
