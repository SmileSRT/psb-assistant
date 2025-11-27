# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Create necessary directories
RUN mkdir -p feature_repo/data

# Copy application files
COPY app/ app/
COPY feature_repo/ feature_repo/

# Set environment variables
ENV PYTHONPATH=/app
ENV FEAST_USAGE=False

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "cd /app && python -c 'from app.main import load_feast_data; load_feast_data()' && uvicorn app.main:app --host 0.0.0.0 --port 8000"] 