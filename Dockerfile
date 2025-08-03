FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY *.py ./
COPY *.md ./

# Create non-root user
RUN useradd -m -u 1000 newsletter && chown -R newsletter:newsletter /app
USER newsletter

# Expose port for webhook server
EXPOSE 5000

# Default command (can be overridden)
CMD ["python", "webhook_server.py"]
