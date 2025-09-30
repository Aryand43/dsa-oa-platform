# --- Backend build stage ---
FROM python:3.11-slim AS backend

WORKDIR /app

# Copy backend code and install dependencies
COPY requirements.txt .
COPY backend/ backend/
RUN pip install --no-cache-dir -r requirements.txt

# --- Frontend build stage ---
FROM node:20-alpine AS frontend

WORKDIR /frontend

# Copy only what's needed for build
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# --- Final stage: full app image ---
FROM python:3.11-slim

WORKDIR /app

# Copy backend
COPY --from=backend /app /app

# Copy built frontend
COPY --from=frontend /frontend/dist /app/frontend_dist

# Re-install dependencies (optional if already copied from backend)
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for FastAPI static file mount
ENV FRONTEND_DIST=/app/frontend_dist

# Expose FastAPI port
EXPOSE 8000

# Run server
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000"]
