FROM python:3.14-alpine

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.11.3 /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY . .

RUN uv sync --frozen

CMD ["sh", "-c", "cd src && uv run uvicorn main:app --host 0.0.0.0 --port 8000"]
