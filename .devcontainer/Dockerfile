# .devcontainer/Dockerfile

FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (CPU-only)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /workspace

# Copy backend requirements file for dependency install
COPY backend/requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt


# Copy all backend code
COPY backend /workspace/backend


# Expose FastAPI port
EXPOSE 8000

# Default command when container starts
CMD ["bash", "-c", "uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload"]

