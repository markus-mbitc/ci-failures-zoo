"""Client for a (fictional) exchange-rate API."""

from decimal import Decimal

import requests


def fetch_rate(api_url: str, currency: str, timeout_s: float = 5.0) -> Decimal:
    """Return the CHF exchange rate for the given currency."""
    response = requests.get(f"{api_url}/rates/{currency}", timeout=timeout_s)
    response.raise_for_status()
    return Decimal(str(response.json()["chf"]))
