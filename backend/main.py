import os
import json
import logging
import time
from datetime import datetime
from dotenv import load_dotenv
from binance_api import BinanceAPI
from indicators import calculate_all_indicators

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")
INTERVAL = os.getenv("INTERVAL", "1h")
CANDLE_LIMIT = int(os.getenv("CANDLE_LIMIT", 200))
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", 5))  # seconds

# Initialize API client
binance = BinanceAPI(API_KEY, API_SECRET)


def get_symbol_indicators(symbol: str) -> dict:
    """Get indicators for a specific symbol"""
    try:
        logger.info(f"Fetching klines for {symbol}...")
        klines = binance.get_klines(symbol, INTERVAL, CANDLE_LIMIT)

        indicators = calculate_all_indicators(klines)

        return {
            "symbol": symbol,
            "interval": INTERVAL,
            "indicators": indicators,
        }
    except Exception as e:
        logger.error(f"Error fetching indicators for {symbol}: {str(e)}")
        return None


def get_most_liquid_indicators() -> dict:
    """Get indicators for the most liquid asset"""
    try:
        logger.info("Finding most liquid asset...")
        most_liquid = binance.get_most_liquid_asset()

        symbol = most_liquid.get("symbol", "UNKNOWN")
        volume = float(most_liquid.get("quoteAssetVolume") or most_liquid.get("volume") or 0)
        
        logger.info(
            f"Most liquid asset: {symbol} "
            f"(Volume: ${volume:,.0f})"
        )

        return get_symbol_indicators(symbol)
    except Exception as e:
        logger.error(f"Error getting most liquid indicators: {str(e)}")
        return None


def get_top_liquid_indicators(count: int = 5) -> list:
    """Get indicators for multiple top liquid assets"""
    try:
        logger.info(f"Fetching top {count} liquid assets...")
        top_assets = binance.get_top_liquid_assets(count)

        results = []
        for asset in top_assets:
            logger.info(f"Fetching indicators for {asset['symbol']}...")
            result = get_symbol_indicators(asset["symbol"])
            if result:
                result["liquidity"] = asset
                results.append(result)

        return results
    except Exception as e:
        logger.error(f"Error getting top liquid indicators: {str(e)}")
        return []


def main():
    """Main execution with loop"""
    logger.info("=== Trading Bot Backend ===\n")
    logger.info(f"Updating every {UPDATE_INTERVAL} seconds\n")

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"\n[{timestamp}] --- Most Liquid Asset ---")
            most_liquid = get_most_liquid_indicators()
            if most_liquid:
                print(json.dumps(most_liquid, indent=2))

            logger.info(f"\n[{timestamp}] --- Top 5 Liquid Assets ---")
            top_liquid = get_top_liquid_indicators(5)
            if top_liquid:
                print(json.dumps(top_liquid, indent=2))

            logger.info(f"\nNext update in {UPDATE_INTERVAL} seconds...")
            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        logger.info("\n\nBot stopped by user")


if __name__ == "__main__":
    main()
