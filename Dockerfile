FROM python:3.11-slim

# Install system dependencies 
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the pre-compiled uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# cache the dependency layer
COPY pyproject.toml README.md ./

RUN mkdir src && touch src/__init__.py

RUN uv pip install --system -e . pydantic duckdb pyarrow requests dbt-duckdb prefect pytest ruff

COPY . .

CMD ["python", "-m", "src.orchestration.pipeline"]