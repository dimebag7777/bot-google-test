# Trading Bot Backend

A Python backend for fetching Binance Futures market data and calculating technical indicators (RSI, ADX, SMA) using pandas.

## Features

- Direct HTTP calls to Binance Futures API using requests library
- HMAC-SHA256 signature generation for authenticated requests
- Technical indicators using pandas: RSI, ADX, SMA
- Find most liquid trading pairs
- Get top N assets by liquidity
- Efficient pandas-based calculations for all indicators

## Docker Setup (Recommended)

### Quick Start with Docker Compose

1. Create `.env` file in the `backend` directory:

```bash
cp backend/.env.example backend/.env
```

2. Add your Binance API credentials to `backend/.env`:

```
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
```

3. Build and start both backend and frontend:

```bash
docker-compose up --build
```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

5. Stop the application:

```bash
docker-compose down
```

### Docker Commands

**Build images:**
```bash
docker-compose build
```

**Start in detached mode:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Rebuild specific service:**
```bash
docker-compose up --build backend
```

## Manual Setup

1. Create virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

4. Add your Binance Futures API keys to `.env`:

```
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
```

## Usage

### Run the bot:

```bash
python main.py
```

### Using as a module:

```python
from binance_api import BinanceAPI
from indicators import calculate_all_indicators

binance = BinanceAPI(api_key, api_secret)

# Get indicators for specific symbol
klines = binance.get_klines('BTCUSDT', '1h', 200)
indicators = calculate_all_indicators(klines)

# Get most liquid asset
most_liquid = binance.get_most_liquid_asset()

# Get top 5 liquid assets
top_assets = binance.get_top_liquid_assets(5)
```

## API Reference

### BinanceAPI

#### `get_most_liquid_asset()`

Returns the trading pair with highest 24h volume in USDT.

#### `get_top_liquid_assets(count)`

Returns top N trading pairs sorted by 24h volume.

#### `get_klines(symbol, interval, limit)`

Get candlestick data for a symbol.

#### `get_price(symbol)`

Get current price of a symbol.

### Indicators

#### `calculate_sma(prices, period)`

Calculate Simple Moving Average using pandas.

#### `calculate_rsi(prices, period)`

Calculate Relative Strength Index (0-100) using Wilder's smoothing.

#### `calculate_adx(df, period)`

Calculate Average Directional Index.

#### `calculate_all_indicators(klines, sma_periods, rsi_period, adx_period)`

Calculate all indicators from Binance klines data.

## Environment Variables

- `BINANCE_API_KEY` - Your Binance Futures API key
- `BINANCE_API_SECRET` - Your Binance Futures API secret
- `INTERVAL` - Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.) - default: 1h
- `CANDLE_LIMIT` - Number of candles to fetch (max 1500) - default: 200

## Requirements

- Python 3.7+
- pandas
- numpy
- requests
- python-dotenv

## Notes

- Uses pandas for efficient data manipulation and calculations
- HMAC-SHA256 signatures generated with Python's hmac module
- Requests library for HTTP calls to Binance API
- All calculations done using pandas Series and DataFrames
