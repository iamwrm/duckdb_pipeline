FROM python:3.12-slim

WORKDIR /app
COPY create_data.py .
RUN pip install --no-cache-dir duckdb

CMD ["python3", "create_data.py"] 