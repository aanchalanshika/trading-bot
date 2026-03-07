def validate_symbol(symbol):
    """Validate trading symbol format."""
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string (e.g., BTCUSDT)")
    if not symbol.isalpha() or not symbol.isupper():
        raise ValueError(f"Invalid symbol '{symbol}'. Must be uppercase letters only (e.g., BTCUSDT)")


def validate_side(side):
    """Validate order side."""
    if side not in ["BUY", "SELL"]:
        raise ValueError(f"Invalid side '{side}'. Must be BUY or SELL")


def validate_order_type(order_type):
    """Validate order type."""
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError(f"Invalid order type '{order_type}'. Must be MARKET or LIMIT")


def validate_quantity(quantity):
    """Validate order quantity."""
    if quantity is None or quantity <= 0:
        raise ValueError("Quantity must be a positive number")


def validate_price(price, order_type):
    """Validate price — required for LIMIT orders."""
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price is required and must be positive for LIMIT orders")
    return True