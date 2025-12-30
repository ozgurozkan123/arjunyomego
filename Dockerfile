FROM python:3.11-slim

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (cache-friendly)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV HOST=0.0.0.0
EXPOSE 8000

CMD ["python", "server.py"]
