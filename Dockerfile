FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /build/

RUN poetry config virtualenvs.in-project true && \
    poetry install -n --no-root --without dev

COPY api/version.py /build/
COPY .git /build/.git/
RUN pip install gitpython && python version.py

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --gid 1000 api \
    && adduser --gid 1000 --uid 1000 --disabled-password --no-create-home api

USER api

EXPOSE 8002

COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build/VERSION /app/
COPY alembic /app/alembic
COPY alembic.ini /app/
COPY api /app/api/

ENV PATH="/app/.venv/bin:$PATH"

HEALTHCHECK --interval=20s --timeout=5s --retries=1 \
    CMD curl -fI http://localhost:${PORT:-8003}/status

CMD python -m alembic upgrade head && python -m api
