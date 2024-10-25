FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY requirements.txt /build/requirements.txt

RUN uv pip install --system -r /build/requirements.txt

ENTRYPOINT ["/bin/bash"]

