import os
from dataclasses import dataclass

import alpaca_trade_api as tradeapi


@dataclass
class AlpacaSettings:
    key_id: str
    secret_key: str
    base_url: str = "https://paper-api.alpaca.markets"


def load_settings() -> AlpacaSettings:
    """
    Load Alpaca credentials from env vars.
    """
    return AlpacaSettings(
        key_id=os.environ["APCA_API_KEY_ID"],
        secret_key=os.environ["APCA_API_SECRET_KEY"],
        base_url=os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets"),
    )


def get_client(settings: AlpacaSettings | None = None) -> tradeapi.REST:
    """
    Build an Alpaca REST client from settings or environment.
    """
    if settings is None:
        settings = load_settings()
    return tradeapi.REST(
        settings.key_id,
        settings.secret_key,
        settings.base_url,
        api_version="v2",
    )
