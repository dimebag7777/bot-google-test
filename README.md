# Trading Bot - Binance Futures Technical Analysis

A full-stack trading bot application that monitors Binance Futures markets and calculates technical indicators in real-time.

## Features

- **Real-time Market Data**: Fetches live data from Binance Futures API
- **Technical Indicators**: RSI, ADX, SMA (20, 50, 200), MACD, Bollinger Bands, ATR
- **Liquidity Analysis**: Identifies and tracks the most liquid trading pairs
- **Modern UI**: React-based dashboard with real-time updates
- **Dockerized**: Easy deployment with Docker Compose

## Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- Binance Futures API credentials (optional for public data)

### Setup

1. **Clone the repository** (or navigate to the project directory)

2. **Configure environment variables:**

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your Binance API credentials:

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
INTERVAL=1h
CANDLE_LIMIT=200
UPDATE_INTERVAL=5
```

3. **Start the application:**

```bash
docker-compose up --build
```

4. **Access the application:**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:5000
   - **Health Check**: http://localhost:5000/health

### Docker Commands

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up --build

# Rebuild specific service
docker-compose build backend
docker-compose build frontend
```

## Manual Setup (Without Docker)

### Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API credentials
```

5. Run the backend:
```bash
python api.py
```

### Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

4. Access at http://localhost:3000

## Project Structure

```
.
├── backend/
│   ├── api.py              # Flask API server
│   ├── binance_api.py      # Binance API client
│   ├── indicators.py       # Technical indicators
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend Docker image
│   └── .env.example        # Environment template
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   └── components/     # React components
│   ├── Dockerfile          # Frontend Docker image
│   ├── nginx.conf          # Nginx configuration
│   └── package.json        # Node dependencies
└── docker-compose.yml      # Multi-container orchestration
```

## API Endpoints

- `GET /health` - Health check
- `GET /api/indicators` - Get all indicators data
- `GET /api/indicators/most-liquid` - Get most liquid asset indicators
- `GET /api/indicators/top` - Get top liquid assets indicators
- `GET /api/debug` - Debug endpoint for data inspection

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BINANCE_API_KEY` | Binance Futures API key | - |
| `BINANCE_API_SECRET` | Binance Futures API secret | - |
| `INTERVAL` | Kline interval (1m, 5m, 1h, etc.) | `1h` |
| `CANDLE_LIMIT` | Number of candles to fetch | `200` |
| `UPDATE_INTERVAL` | Data update interval (seconds) | `5` |

## Technical Stack

**Backend:**
- Python 3.11
- Flask (API server)
- Pandas & NumPy (data analysis)
- Requests (HTTP client)

**Frontend:**
- React 18
- Vite (build tool)
- Axios (HTTP client)

**Infrastructure:**
- Docker & Docker Compose
- Nginx (production web server)

## License

MIT
