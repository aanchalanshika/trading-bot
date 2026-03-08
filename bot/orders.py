import logging
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)


def place_order(client, symbol, side, order_type, quantity, price=None, stop_price=None):
    """Place a MARKET, LIMIT, or STOP_LIMIT order on Binance Futures Testnet."""
    try:
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
        }

        if order_type == "MARKET":
            params["type"] = "MARKET"

        elif order_type == "LIMIT":
            params["type"] = "LIMIT"
            params["price"] = price
            params["timeInForce"] = "GTC"

        elif order_type == "STOP_LIMIT":
            # Binance Futures API uses type=STOP for stop-limit orders
            params["type"] = "STOP"
            params["price"] = price
            params["stopPrice"] = stop_price
            params["timeInForce"] = "GTC"

        else:
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