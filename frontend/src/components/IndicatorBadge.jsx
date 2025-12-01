import './IndicatorBadge.css';

export default function IndicatorBadge({ label, value, type = 'neutral' }) {
    // Format value for display
    const formatValue = (val) => {
        if (typeof val === 'number') {
            if (Math.abs(val) >= 1) return val.toFixed(2);
            if (Math.abs(val) >= 0.01) return val.toFixed(4);
            return val.toFixed(8);
        }
        return val || 'N/A';
    };

    // Determine badge style based on type
    const getBadgeClass = () => {
        if (type === 'success') return 'badge badge-success';
        if (type === 'danger') return 'badge badge-danger';
        if (type === 'warning') return 'badge badge-warning';
        return 'badge badge-neutral';
    };

    return (
        <div className={getBadgeClass()}>
            <span className="badge-label">{label}:</span>
            <span className="badge-value">{formatValue(value)}</span>
        </div>
    );
}
