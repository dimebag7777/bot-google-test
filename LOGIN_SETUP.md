# Login System Setup Guide

## Quick Start

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 3. Configure Environment Variables
Copy the example environment file and update with your settings:
```bash
cd backend
cp .env.example .env
```

Edit `.env` and set:
- `JWT_SECRET` - A strong secret key for JWT tokens
- `DB_PASSWORD` - MySQL root password (default: rootpassword)
- Binance API keys if needed

### 4. Start with Docker (Recommended)
```bash
# From project root
docker-compose up --build
```

This will start:
- MySQL database on port 3306
- Backend API on port 5000
- Frontend on port 3000

### 5. Access the Application
Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

You'll be redirected to the login page. Create a new account to get started!

## Manual Setup (Without Docker)

### 1. Start MySQL
Make sure MySQL is running on your system and create the database:
```sql
CREATE DATABASE trading_bot_db;
```

### 2. Update Environment
Edit `backend/.env` and set `DB_HOST=localhost`

### 3. Start Backend
```bash
cd backend
python api.py
```

### 4. Start Frontend
```bash
cd frontend
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/verify` - Verify token
- `POST /api/auth/logout` - Logout user

### Trading Data (Protected)
- `GET /api/indicators` - Get all indicators
- `GET /api/indicators/most-liquid` - Get most liquid asset
- `GET /api/indicators/top` - Get top assets

## Features

✅ **Secure Authentication**
- JWT token-based authentication
- Bcrypt password hashing
- 6-character minimum password requirement

✅ **Beautiful UI**
- Modern glassmorphism design
- Responsive layout for mobile devices
- Smooth animations and transitions

✅ **Protected Routes**
- Dashboard requires authentication
- Automatic redirect to login
- Token persistence in localStorage

✅ **MySQL Database**
- User data storage
- Indexed queries for performance
- Docker volume for data persistence

## Troubleshooting

### Database Connection Issues
If you see database connection errors:
1. Ensure MySQL container is running: `docker ps`
2. Check MySQL logs: `docker logs trading-bot-mysql`
3. Verify environment variables in `.env`

### Frontend Can't Connect to Backend
1. Ensure backend is running on port 5000
2. Check CORS settings in `backend/api.py`
3. Verify API_URL in `frontend/src/contexts/AuthContext.jsx`

### Token Expired
Tokens expire after 24 hours by default. Simply log in again to get a new token.
