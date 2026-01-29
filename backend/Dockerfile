FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy application code first to leverage Docker cache
COPY . .

# Create directories for chunks and merged files
RUN mkdir -p chunks merged_files

# Install Python dependencies
# Assuming requirements.txt is in the backend directory
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "score:app", "--host", "0.0.0.0", "--port", "8000"]