import argparse
import logging
import os
import sys

try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False

from bot.client import get_client
from bot.orders import place_order
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.logging_config import setup_logging

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    if _DOTENV_AVAILABLE:
        load_dotenv()
    else:
        logging.warning("python-dotenv not installed. Reading API keys from environment variables only.")

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        epilog="Examples:\n"
               "  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01\n"
               "  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2000",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, help="Order side: BUY or SELL")
    parser.add_argument("--type", required=True, help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", type=float, required=True, help="Order quantity")
    parser.add_argument("--price", type=float, default=None, help="Limit price (required for LIMIT orders)")

    args = parser.parse_args()

    try:
        # ---- Validate inputs ----
        validate_symbol(args.symbol)
        validate_side(args.side)
        validate_order_type(args.type)
        validate_quantity(args.quantity)
        validate_price(args.price, args.type)

        # ---- Load API credentials from .env ----
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise EnvironmentError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env file"
            )

        # ---- Connect & place order ----
        client = get_client(api_key, api_secret)

        order = place_order(
            client,
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price,
        )

        # ---- Print request summary ----
        print("\n" + "=" * 40)
        print("  ORDER REQUEST SUMMARY")
        print("=" * 40)
        print(f"  Symbol   : {args.symbol}")
        print(f"  Side     : {args.side}")
        print(f"  Type     : {args.type}")
        print(f"  Quantity : {args.quantity}")
        if args.price:
            print(f"  Price    : {args.price}")

        # ---- Print response details ----
        print("\n" + "-" * 40)
        print("  ORDER RESPONSE")
        print("-" * 40)
        print(f"  Order ID     : {order.get('orderId')}")
        print(f"  Status       : {order.get('status')}")
        print(f"  Executed Qty : {order.get('executedQty')}")
        print(f"  Avg Price    : {order.get('avgPrice', 'N/A')}")
        print("\n  ✅ Order placed successfully!")
        print("=" * 40)

    except ValueError as e:
        logger.error("Validation error: %s", e)
        print(f"\n❌ Validation Error: {e}")
        sys.exit(1)

    except ConnectionError as e:
        logger.error("Connection error: %s", e)
        print(f"\n❌ Connection Error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error("Unexpected error: %s", e)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()