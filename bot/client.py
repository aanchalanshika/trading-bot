import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)


def get_client(api_key, api_secret):
    """Create and return a Binance Futures Testnet client."""
    try:
        client = Client(api_key, api_secret, testnet=True)
        client.FUTURES_URL = "https://testnet.binancefuture.com"

        # Verify connection by fetching server time
        server_time = client.futures_time()
        logger.info("Connected to Binance Futures Testnet (server time: %s)", server_time["serverTime"])

        return client

    except BinanceAPIException as e:
        logger.error("Binance API error during connection: %s", e)
        raise
    except Exception as e:
        logger.error("Failed to connect to Binance Futures Testnet: %s", e)
        raise ConnectionError(f"Could not connect to Binance Futures Testnet: {e}")