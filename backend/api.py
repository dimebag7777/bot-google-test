from flask import Flask, jsonify
from flask_cors import CORS
import os
import threading
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print(f"DEBUG: .env loaded. DB_HOST={os.getenv('DB_HOST')}")
print(f"DEBUG: Current working directory: {os.getcwd()}")
print(f"DEBUG: Directory contents: {os.listdir('.')}")

from binance_api import BinanceAPI
from indicators import calculate_all_indicators
from auth import auth_bp
from database import init_database

# Configuration
API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")
INTERVAL = os.getenv("INTERVAL", "1h")
CANDLE_LIMIT = int(os.getenv("CANDLE_LIMIT", 200))
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", 5))

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register authentication blueprint
app.register_blueprint(auth_bp)

# Initialize database
init_database()

# Initialize API client
binance = BinanceAPI(API_KEY, API_SECRET)

# Global data storage
current_data = {
    "most_liquid": None,
    "top_assets": [],
    "timestamp": None,
    "error": None
}

def get_symbol_indicators(symbol: str) -> dict:
    """Get indicators for a specific symbol"""
    try:
        klines = binance.get_klines(symbol, INTERVAL, CANDLE_LIMIT)
        indicators = calculate_all_indicators(klines)
        

        return {
            "symbol": symbol,
            "interval": INTERVAL,
            "indicators": indicators,
        }
    except Exception as e:
        # Silently handle errors
        return None


def get_most_liquid_indicators() -> dict:
    """Get indicators for the most liquid asset"""
    try:
        most_liquid = binance.get_most_liquid_asset()
        symbol = most_liquid.get("symbol", "UNKNOWN")
        
        result = get_symbol_indicators(symbol)
        if result:
            # Attach liquidity data with mark price (from most_liquid)
            liquidity_price = float(most_liquid.get("markPrice", most_liquid.get("lastPrice", 0)))
            klines_price = result.get("indicators", {}).get("last_price", 0)
            
            # Use liquidity/mark price if klines price is 0
            final_price = klines_price if klines_price > 0 else liquidity_price
            
            result["liquidity"] = {
                "symbol": most_liquid.get("symbol", ""),
                "price": final_price,
                "volume_24h": float(most_liquid.get("quoteVolume", 0)),
                "price_change_24h": float(most_liquid.get("priceChangePercent", 0)),
            }

        return result
    except Exception as e:
        # Silently handle errors
        return None


def get_top_liquid_indicators(count: int = 5) -> list:
    """Get indicators for multiple top liquid assets"""
    try:
        top_assets = binance.get_top_liquid_assets(count)


        results = []
        for asset in top_assets:
            result = get_symbol_indicators(asset["symbol"])
            if result:
                # Attach liquidity data - this includes the price from mark price endpoint
                liquidity_price = asset.get("price", 0)
                klines_price = result.get("indicators", {}).get("last_price", 0)
                
                # Use liquidity price if klines price is 0
                final_price = klines_price if klines_price > 0 else liquidity_price
                
                result["liquidity"] = {
                    "symbol": asset.get("symbol", ""),
                    "price": final_price,
                    "volume_24h": float(asset.get("volume_24h", 0)),
                    "price_change_24h": float(asset.get("price_change_24h", 0)),
                }

                results.append(result)


        return results
    except Exception as e:
        # Silently handle errors
        return []


def update_data():
    """Background thread to update data continuously"""
    global current_data
    
    while True:
        try:
            # Updating indicators silently
            most_liquid = get_most_liquid_indicators()
            top_assets = get_top_liquid_indicators(5)
            
            current_data = {
                "most_liquid": most_liquid,
                "top_assets": top_assets,
                "timestamp": datetime.now().isoformat(),
                "error": None
            }

        except Exception as e:
            current_data["error"] = str(e)
            # Silently handle errors

        time.sleep(UPDATE_INTERVAL)


# API Routes

@app.route('/api/indicators', methods=['GET'])
def get_indicators():
    """Get current indicators data"""
    return jsonify(current_data)


@app.route('/api/indicators/most-liquid', methods=['GET'])
def get_most_liquid():
    """Get most liquid asset indicators"""
    return jsonify(current_data.get("most_liquid"))


@app.route('/api/indicators/top', methods=['GET'])
def get_top():
    """Get top assets indicators"""
    data = current_data.get("top_assets", [])

    return jsonify(data)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/debug', methods=['GET'])
def debug_data():
    """Debug endpoint to check current data"""
    return jsonify({
        "current_data": current_data,
        "top_assets_count": len(current_data.get("top_assets", [])),
        "first_asset": current_data.get("top_assets", [])[0] if current_data.get("top_assets") else None
    })


if __name__ == "__main__":
    # Start background update thread
    update_thread = threading.Thread(target=update_data, daemon=True)
    update_thread.start()

    # Starting Trading Bot API Server on http://0.0.0.0:5000
    
    app.run(host="0.0.0.0", port=5000, debug=False)
