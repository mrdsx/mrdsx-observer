FROM astral/uv:python3.14-alpine AS build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .

FROM python:3.14.6-alpine3.24
COPY --from=build /app /app
WORKDIR /app
CMD [".venv/bin/python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
