FROM python:3.11-slim

LABEL maintainer="OpenStack Cloud Platform"
LABEL description="OpenStack Cloud Platform - Cloud computing SDK and CLI"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /workspace/project

# Copy requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose ports
EXPOSE 8080 5000

# Default command
CMD ["python3", "-c", "
from openstack_sdk import OpenStackClient
client = OpenStackClient(mock_mode=True)
print('OpenStack Cloud Platform ready!')
print('Run: python3 cloud_cli.py --help')
"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "from openstack_sdk import OpenStackClient; print('OK')" || exit 1