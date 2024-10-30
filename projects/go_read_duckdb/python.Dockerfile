FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app
COPY create_data.py .
RUN uv pip install --system duckdb

CMD ["python", "create_data.py"] 