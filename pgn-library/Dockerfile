# NMEA 2000 PGN Library Docker Image
# Serves the library files via HTTP for easy consumption

FROM python:3.11-alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy library files
COPY dist/ ./dist/
COPY scripts/ ./scripts/

# Simple HTTP server on port 8080
EXPOSE 8080

CMD ["python", "-m", "http.server", "8080", "--directory", "dist"]
