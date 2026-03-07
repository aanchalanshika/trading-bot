import logging
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)


def place_order(client, symbol, side, order_type, quantity, price=None):
    """Place a MARKET or LIMIT order on Binance Futures Testnet."""
    try:
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        elif order_type != "MARKET":
            raise ValueError(f"Unsupported order type: {order_type}")

        logger.info("Sending order request: %s", params)

        order = client.futures_create_order(**params)

        logger.info(
            "Order response: orderId=%s status=%s executedQty=%s avgPrice=%s",
            order.get("orderId"),
            order.get("status"),
            order.get("executedQty"),
            order.get("avgPrice", "N/A"),
        )

        return order

    except BinanceAPIException as e:
        logger.error("Binance API error: [%s] %s", e.code, e.message)
        raise
    except Exception as e:
        logger.error("Order failed: %s", str(e))
        raise