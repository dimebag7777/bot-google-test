import { TrendingUp, TrendingDown, Activity } from 'lucide-react';
import IndicatorBadge from './IndicatorBadge';
import './AssetCard.css';

export default function AssetCard({ asset, isFeatured = false }) {
    if (!asset) return null;

    const { symbol, liquidity, indicators } = asset;

    // Extract data with fallbacks
    const price = liquidity?.price || 0;
    const priceChange = liquidity?.price_change_24h || 0;
    const volume = liquidity?.volume_24h || 0;

    // Format numbers
    const formatPrice = (val) => {
        if (val >= 1) return val.toFixed(2);
        if (val >= 0.01) return val.toFixed(4);
        return val.toFixed(8);
    };

    const formatVolume = (val) => {
        if (val >= 1e9) return `$${(val / 1e9).toFixed(2)}B`;
        if (val >= 1e6) return `$${(val / 1e6).toFixed(2)}M`;
        if (val >= 1e3) return `$${(val / 1e3).toFixed(2)}K`;
        return `$${val.toFixed(2)}`;
    };

    const formatPercent = (val) => {
        const sign = val >= 0 ? '+' : '';
        return `${sign}${val.toFixed(2)}%`;
    };

    // Determine indicator types based on values
    const getRSIType = (rsi) => {
        if (rsi > 70) return 'danger';
        if (rsi < 30) return 'success';
        return 'neutral';
    };

    const getMACD = () => {
        const macd = indicators?.macd?.macd;
        const signal = indicators?.macd?.signal;
        if (macd && signal) {
            return macd > signal ? 'success' : 'danger';
        }
        return 'neutral';
    };

    return (
        <div className={`asset-card glass-card ${isFeatured ? 'featured' : ''}`}>
            {/* Header */}
            <div className="asset-header">
                <div className="asset-title-section">
                    <h3 className="asset-symbol">{symbol}</h3>
                    {isFeatured && <span className="featured-badge">Most Liquid</span>}
                </div>
                <Activity className="asset-icon" size={24} />
            </div>

            {/* Price Section */}
            <div className="asset-price-section">
                <div className="price-main">
                    <span className="price-label">Price</span>
                    <span className="price-value">${formatPrice(price)}</span>
                </div>
                <div className={`price-change ${priceChange >= 0 ? 'positive' : 'negative'}`}>
                    {priceChange >= 0 ? <TrendingUp size={18} /> : <TrendingDown size={18} />}
                    <span>{formatPercent(priceChange)}</span>
                </div>
            </div>

            {/* Volume */}
            <div className="asset-volume">
                <span className="volume-label">24h Volume</span>
                <span className="volume-value">{formatVolume(volume)}</span>
            </div>

            {/* Indicators */}
            {indicators && (
                <div className="indicators-section">
                    <h4 className="indicators-title">Technical Indicators</h4>

                    <div className="indicators-grid">
                        {/* RSI */}
                        {indicators.rsi !== undefined && indicators.rsi !== null && (
                            <IndicatorBadge
                                label="RSI"
                                value={indicators.rsi}
                                type={getRSIType(indicators.rsi)}
                            />
                        )}

                        {/* MACD */}
                        {indicators.macd && (
                            <>
                                <IndicatorBadge
                                    label="MACD"
                                    value={indicators.macd.macd}
                                    type={getMACD()}
                                />
                                <IndicatorBadge
                                    label="Signal"
                                    value={indicators.macd.signal}
                                    type="neutral"
                                />
                            </>
                        )}

                        {/* Bollinger Bands */}
                        {indicators.bollinger_bands && (
                            <>
                                <IndicatorBadge
                                    label="BB Upper"
                                    value={indicators.bollinger_bands.upper}
                                    type="neutral"
                                />
                                <IndicatorBadge
                                    label="BB Middle"
                                    value={indicators.bollinger_bands.middle}
                                    type="neutral"
                                />
                                <IndicatorBadge
                                    label="BB Lower"
                                    value={indicators.bollinger_bands.lower}
                                    type="neutral"
                                />
                            </>
                        )}

                        {/* Moving Averages - SMA */}
                        {indicators.sma?.sma20?.value !== undefined && (
                            <IndicatorBadge
                                label="SMA 20"
                                value={indicators.sma.sma20.value}
                                type="neutral"
                            />
                        )}
                        {indicators.sma?.sma50?.value !== undefined && (
                            <IndicatorBadge
                                label="SMA 50"
                                value={indicators.sma.sma50.value}
                                type="neutral"
                            />
                        )}
                        {indicators.sma?.sma200?.value !== undefined && (
                            <IndicatorBadge
                                label="SMA 200"
                                value={indicators.sma.sma200.value}
                                type="neutral"
                            />
                        )}

                        {/* ATR */}
                        {indicators.atr !== undefined && indicators.atr !== null && (
                            <IndicatorBadge
                                label="ATR"
                                value={indicators.atr}
                                type="warning"
                            />
                        )}

                        {/* ADX */}
                        {indicators.adx !== undefined && indicators.adx !== null && (
                            <IndicatorBadge
                                label="ADX"
                                value={indicators.adx}
                                type={indicators.adx > 25 ? 'success' : 'neutral'}
                            />
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
