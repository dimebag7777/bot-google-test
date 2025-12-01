import { TrendingUp, TrendingDown } from 'lucide-react';
import './PriceCard.css';

export default function PriceCard({ asset, isFeatured = false }) {
    if (!asset) return null;

    const { symbol, liquidity } = asset;
    const price = liquidity?.price || 0;
    const priceChange = liquidity?.price_change_24h || 0;

    const formatPrice = (val) => {
        if (val >= 1) return val.toFixed(2);
        if (val >= 0.01) return val.toFixed(4);
        return val.toFixed(8);
    };

    const formatPercent = (val) => {
        const sign = val >= 0 ? '+' : '';
        return `${sign}${val.toFixed(2)}%`;
    };

    return (
        <div className={`price-card glass-card ${isFeatured ? 'featured' : ''}`}>
            <div className="price-card-header">
                <h3 className="price-symbol">{symbol}</h3>
                {isFeatured && <span className="featured-badge">Top</span>}
            </div>

            <div className="price-card-body">
                <span className="price-value-large">${formatPrice(price)}</span>
                <div className={`price-change-pill ${priceChange >= 0 ? 'positive' : 'negative'}`}>
                    {priceChange >= 0 ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
                    <span>{formatPercent(priceChange)}</span>
                </div>
            </div>
        </div>
    );
}
