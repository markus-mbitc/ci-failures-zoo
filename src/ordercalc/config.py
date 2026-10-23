"""Settings loaded from environment variables (prefix ORDERCALC_)."""

from decimal import Decimal

from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    api_url: HttpUrl
    vat_rate: Decimal = Decimal("0.081")

    class Config:
        env_prefix = "ORDERCALC_"


def get_settings() -> Settings:
    return Settings()
