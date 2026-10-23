from decimal import Decimal

from ordercalc.config import get_settings


def test_settings_from_environment() -> None:
    settings = get_settings()
    assert settings.api_url.scheme == "https"
    assert settings.vat_rate == Decimal("0.081")
