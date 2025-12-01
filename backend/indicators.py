import pandas as pd
import numpy as np
from typing import Dict, List, Optional


def calculate_sma(prices: pd.Series, period: int) -> Optional[float]:
    """
    Calculate Simple Moving Average (SMA)
    
    Args:
        prices: Series of prices
        period: Number of periods for SMA
        
    Returns:
        SMA value or None if insufficient data
    """
    if len(prices) < period:
        return None
    return prices.tail(period).mean()


def calculate_all_smas(prices: pd.Series, periods: List[int] = None) -> Dict[str, Optional[float]]:
    """
    Calculate all SMAs for different periods
    
    Args:
        prices: Series of prices
        periods: List of periods to calculate
        
    Returns:
        Dictionary with SMA values
    """
    if periods is None:
        periods = [20, 50, 200]
    
    smas = {}
    for period in periods:
        smas[f"sma{period}"] = calculate_sma(prices, period)
    return smas


def calculate_rsi(prices: pd.Series, period: int = 14) -> Optional[float]:
    """
    Calculate Relative Strength Index (RSI)
    
    Args:
        prices: Series of prices
        period: Number of periods (typically 14)
        
    Returns:
        RSI value (0-100) or None if insufficient data
    """
    if len(prices) < period + 1:
        return None
    
    # Calculate price changes
    deltas = prices.diff()
    
    # Separate gains and losses
    gains = deltas.clip(lower=0)
    losses = -deltas.clip(upper=0)
    
    # Calculate smoothed averages (Wilder's smoothing)
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()
    
    # Smooth using exponential moving average
    avg_gain = avg_gain.ewm(span=period, adjust=False).mean()
    avg_loss = avg_loss.ewm(span=period, adjust=False).mean()
    
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None


def calculate_atr(df: pd.DataFrame, period: int = 14) -> Optional[float]:
    """
    Calculate Average True Range (ATR)
    
    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        period: Number of periods (typically 14)
        
    Returns:
        ATR value or None if insufficient data
    """
    if len(df) < period:
        return None
    
    # Calculate true ranges
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift(1))
    low_close = abs(df['low'] - df['close'].shift(1))
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    
    # Calculate ATR using smoothed average
    atr = true_range.rolling(window=period).mean()
    atr = atr.ewm(span=period, adjust=False).mean()
    
    return float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else None


def calculate_adx(df: pd.DataFrame, period: int = 14) -> Optional[float]:
    """
    Calculate ADX (Average Directional Index)
    
    Args:
        df: DataFrame with 'high', 'low', 'close' columns
        period: Number of periods (typically 14)
        
    Returns:
        ADX value or None if insufficient data
    """
    if len(df) < period * 2:
        return None
    
    # Calculate directional movements
    high_diff = df['high'].diff()
    low_diff = -df['low'].diff()
    
    plus_dm = pd.Series(0.0, index=df.index)
    minus_dm = pd.Series(0.0, index=df.index)
    
    for i in range(1, len(df)):
        if high_diff.iloc[i] > 0 and high_diff.iloc[i] > low_diff.iloc[i]:
            plus_dm.iloc[i] = high_diff.iloc[i]
        if low_diff.iloc[i] > 0 and low_diff.iloc[i] > high_diff.iloc[i]:
            minus_dm.iloc[i] = low_diff.iloc[i]
    
    # Calculate true range
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift(1))
    low_close = abs(df['low'] - df['close'].shift(1))
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    
    # Smooth directional movements and true range
    smoothed_plus_dm = plus_dm.rolling(window=period).sum().ewm(span=period, adjust=False).mean()
    smoothed_minus_dm = minus_dm.rolling(window=period).sum().ewm(span=period, adjust=False).mean()
    smoothed_tr = true_range.rolling(window=period).sum().ewm(span=period, adjust=False).mean()
    
    # Calculate directional indicators
    di_plus = (smoothed_plus_dm / smoothed_tr) * 100
    di_minus = (smoothed_minus_dm / smoothed_tr) * 100
    
    # Calculate DX
    dx = (abs(di_plus - di_minus) / (di_plus + di_minus)) * 100
    
    # ADX is smoothed DX
    adx = dx.ewm(span=period, adjust=False).mean()
    
    return float(adx.iloc[-1]) if not pd.isna(adx.iloc[-1]) else None


def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Optional[Dict]:
    """
    Calculate MACD (Moving Average Convergence Divergence)
    
    Args:
        prices: Series of prices
        fast: Fast EMA period (typically 12)
        slow: Slow EMA period (typically 26)
        signal: Signal line period (typically 9)
        
    Returns:
        Dictionary with MACD, Signal, and Histogram values
    """
    if len(prices) < slow:
        return None
    
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_histogram = macd - macd_signal
    
    return {
        "macd": float(macd.iloc[-1]) if not pd.isna(macd.iloc[-1]) else None,
        "signal": float(macd_signal.iloc[-1]) if not pd.isna(macd_signal.iloc[-1]) else None,
        "histogram": float(macd_histogram.iloc[-1]) if not pd.isna(macd_histogram.iloc[-1]) else None,
    }


def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2.0) -> Optional[Dict]:
    """
    Calculate Bollinger Bands
    
    Args:
        prices: Series of prices
        period: Period for moving average (typically 20)
        std_dev: Number of standard deviations (typically 2.0)
        
    Returns:
        Dictionary with upper, middle, and lower band values
    """
    if len(prices) < period:
        return None
    
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    
    return {
        "upper": float(upper_band.iloc[-1]) if not pd.isna(upper_band.iloc[-1]) else None,
        "middle": float(sma.iloc[-1]) if not pd.isna(sma.iloc[-1]) else None,
        "lower": float(lower_band.iloc[-1]) if not pd.isna(lower_band.iloc[-1]) else None,
    }


def calculate_all_indicators(
    klines: List[List],
    sma_periods: List[int] = None,
    rsi_period: int = 14,
    adx_period: int = 14
) -> Dict:
    """
    Calculate all indicators from klines data
    
    Args:
        klines: List of klines from Binance API
        sma_periods: Periods for SMA calculation
        rsi_period: Period for RSI calculation
        adx_period: Period for ADX calculation
        
    Returns:
        Dictionary with all indicators
    """
    if sma_periods is None:
        sma_periods = [20, 50, 200]
    
    if not klines or len(klines) == 0:
        print("[ERROR] No klines data provided")
        return {
            "sma": {},
            "rsi": None,
            "adx": None,
            "last_price": 0,
            "timestamp": 0,
        }
    
    # Convert klines to DataFrame
    df = pd.DataFrame(
        klines,
        columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ]
    )
    
    # Convert to numeric types
    df['open'] = pd.to_numeric(df['open'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['close'] = pd.to_numeric(df['close'])
    df['volume'] = pd.to_numeric(df['volume'])
    
    # Calculate indicators
    closes = df['close']
    last_price = float(closes.iloc[-1])
    
    smas = calculate_all_smas(closes, sma_periods)
    rsi = calculate_rsi(closes, rsi_period)
    adx = calculate_adx(df, adx_period)
    macd = calculate_macd(closes)
    bollinger = calculate_bollinger_bands(closes)
    atr = calculate_atr(df)
    
    # Format SMA values with human-readable comparisons
    sma_analysis = {}
    for period, sma_value in smas.items():
        if sma_value is not None:
            sma_value = float(sma_value)
            diff = last_price - sma_value
            diff_percent = (diff / sma_value * 100) if sma_value != 0 else 0
            
            sma_analysis[period] = {
                "value": round(sma_value, 8),
                "difference": round(diff, 8),
                "difference_percent": round(diff_percent, 2),
                "status": "above" if diff > 0 else "below" if diff < 0 else "equal",
            }
        else:
            sma_analysis[period] = None
    
    return {
        "sma": sma_analysis,
        "rsi": round(rsi, 2) if rsi is not None else None,
        "adx": round(adx, 2) if adx is not None else None,
        "macd": macd,
        "bollinger_bands": bollinger,
        "atr": round(atr, 8) if atr is not None else None,
        "last_price": round(last_price, 8),
        "timestamp": int(df['close_time'].iloc[-1]),
    }
