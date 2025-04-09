FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy project requirements
COPY pyproject.toml .
COPY README.md .

# Copy application code
COPY app ./app
COPY scripts ./scripts

# Install project and dependencies
RUN pip install --no-cache-dir -e .

# Copy migration files
COPY migrations ./migrations
COPY alembic.ini .

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Command - will be overridden by docker-compose
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
