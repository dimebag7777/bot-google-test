# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the Flask API server with Gunicorn
CMD ["gunicorn", "--workers=2", "--threads=4", "--worker-class=gthread", "--timeout=120", "--bind=0.0.0.0:5000", "api:app"]
