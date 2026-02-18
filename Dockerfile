# Base image with Python 3.11
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR $APP_HOME

# Install system dependencies for GUI and XML parsing
RUN apt-get update && apt-get install -y \
    tk \
    tcl \
    python3-tk \
    libxml2-dev \
    libxslt1-dev \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY ./src ./src
COPY ./config ./config
COPY ./input ./input
COPY ./output ./output
COPY ./logs ./logs

# Expose port if needed for optional web server in future
EXPOSE 8080

# Set entrypoint for GUI launch
ENTRYPOINT ["python", "src/main.py"]
