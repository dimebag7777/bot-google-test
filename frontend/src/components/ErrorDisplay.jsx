import { AlertCircle, RefreshCw } from 'lucide-react';
import './ErrorDisplay.css';

export default function ErrorDisplay({ message, onRetry }) {
    return (
        <div className="error-container">
            <div className="error-icon">
                <AlertCircle size={48} />
            </div>
            <h3 className="error-title">Oops! Something went wrong</h3>
            <p className="error-message">{message || 'Unable to fetch market data'}</p>
            {onRetry && (
                <button className="retry-button" onClick={onRetry}>
                    <RefreshCw size={18} />
                    Retry
                </button>
            )}
        </div>
    );
}
