FROM astral/uv:python3.14-alpine

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .

CMD ["./.venv/bin/python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
