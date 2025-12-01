import { useState, useEffect } from 'react';
import { TrendingUp, Clock, RefreshCw, LayoutTemplate, Maximize, LogOut } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import AssetCard from './AssetCard';
import PriceCard from './PriceCard';
import LoadingSpinner from './LoadingSpinner';
import ErrorDisplay from './ErrorDisplay';

const API_BASE_URL = 'http://localhost:5000';

function Dashboard() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastUpdate, setLastUpdate] = useState(null);
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [simpleMode, setSimpleMode] = useState(true);
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    // Fetch data from API
    const fetchData = async (isManualRefresh = false) => {
        try {
            if (isManualRefresh) {
                setIsRefreshing(true);
            } else {
                setLoading(true);
            }
            setError(null);

            const response = await fetch(`${API_BASE_URL}/api/indicators`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            setData(result);
            setLastUpdate(new Date());
        } catch (err) {
            console.error('Error fetching data:', err);
            setError(err.message);
        } finally {
            setLoading(false);
            setIsRefreshing(false);
        }
    };

    // Initial fetch and auto-refresh every 5 seconds
    useEffect(() => {
        fetchData();
        const interval = setInterval(() => fetchData(), 5000);
        return () => clearInterval(interval);
    }, []);

    // Manual refresh handler
    const handleRefresh = () => {
        fetchData(true);
    };

    // Logout handler
    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    // Format timestamp
    const formatTime = (date) => {
        if (!date) return '';
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    };

    return (
        <div className="app">
            {/* Header */}
            <header className="app-header">
                <div className="container">
                    <div className="header-content">
                        <div className="header-left">
                            <TrendingUp className="header-icon" size={32} />
                            <div className="header-text">
                                <h1 className="app-title gradient-text">Crypto Trading Dashboard</h1>
                                <p className="app-subtitle">Real-time Technical Indicators</p>
                            </div>
                        </div>

                        <div className="header-right">
                            {user && (
                                <div className="user-info">
                                    <span className="user-name">Welcome, {user.username}</span>
                                </div>
                            )}
                            {lastUpdate && (
                                <div className="last-update">
                                    <Clock size={16} />
                                    <span>Updated: {formatTime(lastUpdate)}</span>
                                </div>
                            )}
                            <button
                                className={`refresh-button ${isRefreshing ? 'refreshing' : ''}`}
                                onClick={handleRefresh}
                                disabled={isRefreshing}
                                title="Refresh data"
                            >
                                <RefreshCw size={20} className={isRefreshing ? 'spin' : ''} />
                            </button>
                            <button
                                className="icon-button"
                                onClick={() => setSimpleMode(!simpleMode)}
                                title={simpleMode ? "Switch to Detailed View" : "Switch to Simple View"}
                            >
                                {simpleMode ? <LayoutTemplate size={20} /> : <Maximize size={20} />}
                            </button>
                            <ThemeToggle />
                            <button
                                className="logout-button"
                                onClick={handleLogout}
                                title="Logout"
                            >
                                <LogOut size={20} />
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="app-main">
                <div className="container">
                    {loading && !data ? (
                        <LoadingSpinner />
                    ) : error ? (
                        <ErrorDisplay message={error} onRetry={handleRefresh} />
                    ) : data ? (
                        <>
                            {/* Most Liquid Asset */}
                            {data.most_liquid && (
                                <section className="featured-section fade-in">
                                    <h2 className="section-title">
                                        <TrendingUp size={24} />
                                        Most Liquid Asset
                                    </h2>
                                    {simpleMode ? (
                                        <PriceCard asset={data.most_liquid} isFeatured={true} />
                                    ) : (
                                        <AssetCard asset={data.most_liquid} isFeatured={true} />
                                    )}
                                </section>
                            )}

                            {/* Top Assets Grid */}
                            {data.top_assets && data.top_assets.length > 0 && (
                                <section className="top-assets-section fade-in">
                                    <h2 className="section-title">
                                        <TrendingUp size={24} />
                                        Top Liquid Assets
                                    </h2>
                                    <div className="assets-grid">
                                        {data.top_assets.map((asset, index) => (
                                            simpleMode ? (
                                                <PriceCard
                                                    key={asset.symbol || index}
                                                    asset={asset}
                                                />
                                            ) : (
                                                <AssetCard
                                                    key={asset.symbol || index}
                                                    asset={asset}
                                                />
                                            )
                                        ))}
                                    </div>
                                </section>
                            )}

                            {/* No Data Message */}
                            {!data.most_liquid && (!data.top_assets || data.top_assets.length === 0) && (
                                <div className="no-data">
                                    <p>No market data available at the moment.</p>
                                    <button className="retry-button" onClick={handleRefresh}>
                                        <RefreshCw size={18} />
                                        Refresh
                                    </button>
                                </div>
                            )}
                        </>
                    ) : null}
                </div>
            </main>

            {/* Footer */}
            <footer className="app-footer">
                <div className="container">
                    <p>Data updates automatically every 5 seconds</p>
                </div>
            </footer>
        </div>
    );
}

export default Dashboard;
