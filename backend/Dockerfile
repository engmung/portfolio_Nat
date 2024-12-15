FROM arm64v8/python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install packages in specific order
RUN pip install --no-cache-dir httpx==0.24.0 && \
    pip install --no-cache-dir openai==1.3.7 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]