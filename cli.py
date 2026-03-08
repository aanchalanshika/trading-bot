import argparse
import logging
import os
import sys

try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    _COLOR = True
except ImportError:
    _COLOR = False

from bot.client import get_client
from bot.orders import place_order
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_stop_price,
)
from bot.logging_config import setup_logging

logger = logging.getLogger(__name__)


def _c(text, code):
    return f"{code}{text}{Style.RESET_ALL}" if _COLOR else text

def green(t):  return _c(t, Fore.GREEN)
def red(t):    return _c(t, Fore.RED)
def yellow(t): return _c(t, Fore.YELLOW)
def cyan(t):   return _c(t, Fore.CYAN)
def bold(t):   return _c(t, Style.BRIGHT)

def prompt_inputs():
    """Ask the user for order details one field at a time."""
    print("\n" + bold(cyan("=" * 44)))
    print(bold(cyan("   BINANCE FUTURES TESTNET  —  TRADING BOT")))
    print(bold(cyan("=" * 44)) + "\n")

    symbol     = input(yellow("  Symbol     (e.g. BTCUSDT)              : ")).strip().upper()
    side       = input(yellow("  Side       (BUY / SELL)                : ")).strip().upper()
    order_type = input(yellow("  Order type (MARKET / LIMIT / STOP_LIMIT): ")).strip().upper()
    qty_raw    = input(yellow("  Quantity                                : ")).strip()

    price_raw      = None
    stop_price_raw = None

    if order_type in ("LIMIT", "STOP_LIMIT"):
        price_raw = input(yellow("  Limit price                             : ")).strip()
    if order_type == "STOP_LIMIT":
        stop_price_raw = input(yellow("  Stop trigger price                      : ")).strip()

    def _float(val):
        try:
            return float(val) if val else None
        except ValueError:
            return val  # let the validator produce the proper error message

    return symbol, side, order_type, _float(qty_raw), _float(price_raw), _float(stop_price_raw)


def main():
    setup_logging()
    if _DOTENV_AVAILABLE:
        load_dotenv()
    else:
        logging.warning("python-dotenv not installed. Reading API keys from environment only.")

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        epilog=(
            "Examples:\n"
            "  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01\n"
            "  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2000\n"
            "  python cli.py --symbol BTCUSDT --side SELL --type STOP_LIMIT "
            "--quantity 0.01 --price 29000 --stop-price 29500\n"
            "  python cli.py          (no args → interactive mode)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--symbol",     help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side",       help="Order side: BUY or SELL")
    parser.add_argument("--type",       help="Order type: MARKET, LIMIT, or STOP_LIMIT")
    parser.add_argument("--quantity",   type=float, help="Order quantity")
    parser.add_argument("--price",      type=float, default=None,
                        help="Limit price (required for LIMIT and STOP_LIMIT orders)")
    parser.add_argument("--stop-price", type=float, default=None, dest="stop_price",
                        help="Stop trigger price (required for STOP_LIMIT orders)")

    args = parser.parse_args()
    interactive = not any([args.symbol, args.side, args.type, args.quantity])

    if interactive:
        try:
            symbol, side, order_type, quantity, price, stop_price = prompt_inputs()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{yellow('  Cancelled.')}")
            sys.exit(0)
    else:
        if not all([args.symbol, args.side, args.type, args.quantity]):
            print(red("  ERROR: --symbol, --side, --type, and --quantity are all required."))
            parser.print_help()
            sys.exit(1)
        symbol     = args.symbol
        side       = args.side
        order_type = args.type
        quantity   = args.quantity
        price      = args.price
        stop_price = args.stop_price

    try:
        
        validate_symbol(symbol)
        validate_side(side)
        validate_order_type(order_type)
        validate_quantity(quantity)
        validate_price(price, order_type)
        validate_stop_price(stop_price, order_type)

        api_key    = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise EnvironmentError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env file"
            )

        
        client = get_client(api_key, api_secret)
        order  = place_order(client, symbol, side, order_type, quantity, price, stop_price)

       
        print("\n" + bold(cyan("=" * 44)))
        print(bold(cyan("  ORDER REQUEST SUMMARY")))
        print(bold(cyan("=" * 44)))
        print(f"  Symbol     : {bold(symbol)}")
        print(f"  Side       : {green(side) if side == 'BUY' else red(side)}")
        print(f"  Type       : {yellow(order_type)}")
        print(f"  Quantity   : {quantity}")
        if price:
            print(f"  Limit Price: {price}")
        if stop_price:
            print(f"  Stop Price : {stop_price}")

        
        print("\n" + "-" * 44)
        print(bold("  ORDER RESPONSE"))
        print("-" * 44)
        print(f"  Order ID     : {order.get('orderId')}")
        print(f"  Status       : {green(order.get('status', 'N/A'))}")
        print(f"  Executed Qty : {order.get('executedQty')}")
        print(f"  Avg Price    : {order.get('avgPrice', 'N/A')}")
        print(f"\n  {green('Order placed successfully.')}")
        print(bold(cyan("=" * 44)))

    except ValueError as e:
        logger.error("Validation error: %s", e)
        print(f"\n  {red('Validation Error:')} {e}")
        sys.exit(1)

    except ConnectionError as e:
        logger.error("Connection error: %s", e)
        print(f"\n  {red('Connection Error:')} {e}")
        sys.exit(1)

    except Exception as e:
        logger.error("Unexpected error: %s", e)
        print(f"\n  {red('Error:')} {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()