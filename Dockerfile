FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.1 /uv /uvx /bin/

COPY . /api

WORKDIR /api

RUN uv sync --frozen --no-cache

CMD ["uv", "run", "uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8080"]
