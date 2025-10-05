FROM python:3.12-slim AS base

# базовые переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    PATH="/root/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/* \
 && curl -LsSf https://astral.sh/uv/install.sh | sh -s -- -y

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv pip install --system .
COPY . /app

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

VOLUME ["/app"]
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
