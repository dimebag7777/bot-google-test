import hmac
import hashlib
import time
import requests
from typing import Dict, List, Optional
from urllib.parse import urlencode

BASE_URL = "https://fapi.binance.com"


class BinanceAPI:
    """Binance Futures API client without third-party dependencies"""

    def __init__(self, api_key: str = "", api_secret: str = ""):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()

    def _generate_signature(self, query_string: str) -> str:
        """Generate HMAC-SHA256 signature for authenticated requests"""
        return hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()

    def _request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Dict = None,
        requires_auth: bool = False
    ) -> Dict:
        """Make HTTP request to Binance API"""
        if params is None:
            params = {}

        url = f"{BASE_URL}{endpoint}"

        if requires_auth:
            params["timestamp"] = int(time.time() * 1000)
            query_string = urlencode(params)
            signature = self._generate_signature(query_string)
            params["signature"] = signature

        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            headers["X-MBX-APIKEY"] = self.api_key

        try:
            response = self.session.request(
                method,
                url,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def get_exchange_info(self) -> Dict:
        """Get exchange information"""
        return self._request("/fapi/v1/exchangeInfo")

    def get_trading_symbols(self) -> set:
        """Get set of symbols that are currently TRADING"""
        try:
            info = self.get_exchange_info()
            return {
                s["symbol"] for s in info.get("symbols", [])
                if s.get("status") == "TRADING"
            }
        except Exception:
            return set()

    def get_24h_ticker_price_change(self) -> List[Dict]:
        """Get 24h ticker data for all symbols"""
        return self._request("/fapi/v1/ticker/24hr")

    def get_klines(
        self,
        symbol: str,
        interval: str = "1h",
        limit: int = 100
    ) -> List[List]:
        """
        Get klines (candlestick) data
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            limit: Number of klines to return (default 500, max 1500)
        
        Returns:
            List of klines
        """
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }
        result = self._request("/fapi/v1/klines", params=params)
        return result

    def get_mark_price(self, symbol: str = None) -> Dict:
        """Get mark price for a symbol or all symbols (no auth required)"""
        params = {}
        if symbol:
            params["symbol"] = symbol
            result = self._request("/fapi/v1/premiumIndex", params=params)
            return result if isinstance(result, dict) else {}
        return {}

    def get_all_mark_prices(self) -> List[Dict]:
        """Get mark prices for all symbols"""
        result = self._request("/fapi/v1/premiumIndex")
        return result if isinstance(result, list) else []

    def get_price(self, symbol: str) -> Dict:
        """Get current price of a symbol"""
        params = {"symbol": symbol}
        return self._request("/fapi/v1/ticker/price", params=params)

    def get_most_liquid_asset(self) -> Dict:
        """Get the most liquid asset (highest 24h volume in USDT)"""
        try:
            tickers = self.get_24h_ticker_price_change()

            # Filter USDT pairs and get highest volume
            usdt_pairs = [
                ticker for ticker in tickers
                if isinstance(ticker, dict) and ticker.get("symbol", "").endswith("USDT")
            ]

            if not usdt_pairs:
                raise Exception("No USDT trading pairs found")

            # Get trading symbols
            trading_symbols = self.get_trading_symbols()

            # Filter for trading symbols only
            active_usdt_pairs = [
                p for p in usdt_pairs 
                if p.get("symbol") in trading_symbols
            ]
            
            if not active_usdt_pairs:
                # Fallback to original list if filter fails (unlikely)
                active_usdt_pairs = usdt_pairs

            # Sort by quote asset volume (24h volume in USDT)
            most_liquid = max(
                active_usdt_pairs,
                key=lambda x: float(x.get("quoteVolume") or 0)
            )

            # Get mark price for this symbol
            symbol = most_liquid.get("symbol")
            try:
                mark_price_data = self.get_mark_price(symbol)
                if mark_price_data and "markPrice" in mark_price_data:
                    most_liquid["markPrice"] = mark_price_data.get("markPrice")
            except Exception:
                pass
            return most_liquid

        except Exception as e:
            raise Exception(f"Failed to get most liquid asset: {str(e)}")

    def get_top_liquid_assets(self, count: int = 10) -> List[Dict]:
        """Get multiple symbols sorted by liquidity"""
        try:
            tickers = self.get_24h_ticker_price_change()

            usdt_pairs = [
                ticker for ticker in tickers
                if ticker.get("symbol", "").endswith("USDT")
            ]

            # Get trading symbols
            trading_symbols = self.get_trading_symbols()

            # Filter for trading symbols only
            active_usdt_pairs = [
                p for p in usdt_pairs 
                if p.get("symbol") in trading_symbols
            ]

            # Sort by quote asset volume and get top N
            sorted_pairs = sorted(
                active_usdt_pairs,
                key=lambda x: float(x.get("quoteVolume") or 0),
                reverse=True
            )[:count]

            # Get mark prices for these symbols
            mark_prices = {}
            try:
                all_mark_prices = self.get_all_mark_prices()
                for mp in all_mark_prices:
                    symbol = mp.get("symbol")
                    mark_price = float(mp.get("markPrice", 0))
                    mark_prices[symbol] = mark_price
            except Exception:
                pass

            results = []
            for ticker in sorted_pairs:
                symbol = ticker.get("symbol", "")
                price = mark_prices.get(symbol, float(ticker.get("lastPrice", 0)))
                
                results.append({
                    "symbol": symbol,
                    "price": price,
                    "volume_24h": float(ticker.get("quoteVolume") or 0),
                    "price_change_24h": float(ticker.get("priceChangePercent", 0)),
                })

            return results

        except Exception as e:
            raise Exception(f"Failed to get top liquid assets: {str(e)}")
