# Multi-stage Docker build for DreamDirector
FROM node:18-alpine AS frontend-builder

# Build frontend
WORKDIR /app/frontend
COPY package*.json ./
RUN npm install

COPY src/ ./src/
COPY index.html ./
COPY vite.config.js ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

RUN npm run build

# Python backend stage  
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
COPY agents/requirements.txt ./agents/
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r agents/requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY agents/ ./agents/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./static

# Create directories for generated files
RUN mkdir -p /app/media /app/generated

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Start command - use shell to expand PORT environment variable
CMD sh -c "python -m uvicorn backend.app:app --host 0.0.0.0 --port ${PORT:-8000}" 