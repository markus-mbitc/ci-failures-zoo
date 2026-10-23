"""Pricing: subtotal, discount, VAT and rounding to 5 Rappen (CHF 0.05)."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

FIVE_RAPPEN = Decimal("0.05")


@dataclass(frozen=True)
class LineItem:
    sku: str
    unit_price: Decimal
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(f"quantity must be positive, got {self.quantity}")
        if self.unit_price < 0:
            raise ValueError(f"unit_price must not be negative, got {self.unit_price}")

    @property
    def total(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass(frozen=True)
class OrderTotal:
    subtotal: Decimal
    discount: Decimal
    vat: Decimal
    total: Decimal


def round_to_rappen(amount: Decimal) -> Decimal:
    """Round half up to the nearest 5 Rappen (CHF 0.05)."""
    return (amount / FIVE_RAPPEN).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * FIVE_RAPPEN


def format_chf(amount: Decimal) -> Decimal:
    """Format an amount for display, e.g. CHF 33.35."""
    return f"CHF {amount:.2f}"


def calculate_total(
    items: list[LineItem], vat_rate: Decimal, discount_pct: Decimal = Decimal("0")
) -> OrderTotal:
    if not Decimal("0") <= discount_pct <= Decimal("100"):
        raise ValueError(f"discount_pct must be between 0 and 100, got {discount_pct}")
    subtotal = sum((item.total for item in items), Decimal("0"))
    discount = subtotal * discount_pct / Decimal("100")
    net = subtotal - discount
    vat = net * vat_rate
    return OrderTotal(
        subtotal=subtotal,
        discount=discount,
        vat=vat,
        total=round_to_rappen(net + vat),
    )
