# Binance Futures Testnet Trading Bot

A Python trading bot that places **Market**, **Limit**, and **Stop-Limit** orders on [Binance Futures Testnet (USDT-M)](https://testnet.binancefuture.com), with an enhanced interactive CLI and colored output.

---

## Setup

### 1. Prerequisites

- Python 3.8+
- A [Binance Futures Testnet](https://testnet.binancefuture.com) account with API credentials

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Create a `.env` file in the project root (see `.env.example`):

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

> **Note:** Never commit your `.env` file to version control. It is already listed in `.gitignore`.

---

## How to Run

### Option 1 — Interactive Mode (Recommended)

Run with no arguments and the bot will ask you for each input one by one:

```bash
python cli.py
```

Example session:

```
============================================
   BINANCE FUTURES TESTNET  —  TRADING BOT
============================================

  Symbol     (e.g. BTCUSDT)              : BTCUSDT
  Side       (BUY / SELL)                : BUY
  Order type (MARKET / LIMIT / STOP_LIMIT): MARKET
  Quantity                                : 0.01
```

---

### Option 2 — Flag Mode (One-liner)

#### Place a Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

#### Place a Limit Order

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2000
```

#### Place a Stop-Limit Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_LIMIT --quantity 0.01 --price 29000 --stop-price 29500
```

> A Stop-Limit order means: **if** BTC price hits `--stop-price` (29500), **then** place a limit order at `--price` (29000).

#### View Help

```bash
python cli.py --help
```

---

## CLI Arguments

| Argument        | Required        | Description                                         |
|-----------------|-----------------|-----------------------------------------------------|
| `--symbol`      | Yes             | Trading pair (e.g., `BTCUSDT`, `ETHUSDT`)           |
| `--side`        | Yes             | `BUY` or `SELL`                                     |
| `--type`        | Yes             | `MARKET`, `LIMIT`, or `STOP_LIMIT`                  |
| `--quantity`    | Yes             | Order quantity (positive number)                    |
| `--price`       | LIMIT/STOP_LIMIT| Limit price for LIMIT and STOP_LIMIT orders         |
| `--stop-price`  | STOP_LIMIT      | Stop trigger price — activates the limit order      |

> **Tip:** Omit all arguments to launch **interactive mode** which prompts you for each field.

---

## Enhanced CLI Features

- **Interactive mode** — run `python cli.py` with no flags for a guided prompt
- **Colored output** — BUY shown in green, SELL in red, errors highlighted in red
- **Stop-Limit orders** — third order type using `--type STOP_LIMIT` with `--price` and `--stop-price`
- **Clear error messages** — validation errors show exactly what went wrong

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance client wrapper (connection & config)
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup (file + console)
├── cli.py                 # CLI entry point (argparse)
├── .env                   # API keys (not committed)
├── .gitignore
├── requirements.txt
├── trading_bot.log        # Auto-generated log file
└── README.md
```

---

## Logging

All API requests, responses, and errors are logged to:

- **`trading_bot.log`** — persistent log file
- **Console (stdout)** — real-time output during execution

---

## Assumptions

- This bot targets the **Binance Futures Testnet (USDT-M)** only — base URL: `https://testnet.binancefuture.com`
- API keys are generated from the Binance Futures Testnet dashboard
- The `python-binance` library is used as the API client
- LIMIT orders use `timeInForce=GTC` (Good Till Cancelled) by default
- Symbols must be uppercase (e.g., `BTCUSDT`, not `btcusdt`)
- No real funds are at risk — all orders are placed on testnet

---

## Example Output

```
========================================
  ORDER REQUEST SUMMARY
========================================
  Symbol   : BTCUSDT
  Side     : BUY
  Type     : MARKET
  Quantity : 0.01

----------------------------------------
  ORDER RESPONSE
----------------------------------------
  Order ID     : 123456789
  Status       : FILLED
  Executed Qty : 0.01000
  Avg Price    : 87000.00

  Order placed successfully!
========================================
```

---

## Error Handling

The bot handles:

- **Invalid input** — wrong symbol format, missing price for LIMIT, bad quantity
- **API errors** — Binance-specific error codes and messages
- **Network failures** — connection timeouts, unreachable endpoints

All errors are logged with context and shown to the user with clear messages.
