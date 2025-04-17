FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files and install
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-root

# Copy the rest of the app
COPY . .
