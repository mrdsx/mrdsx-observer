FROM astral/uv:python3.14-alpine

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

WORKDIR /app
COPY . .

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]