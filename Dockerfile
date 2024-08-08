# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Встановлюємо необхідні пакети
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Копіюємо файли проекту
COPY pyproject.toml poetry.lock ./
COPY ./jarvis ./jarvis

# Встановлюємо залежності з використанням Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Stage 2: Runner
FROM python:3.12-slim AS runner

ENV PORT=8000

WORKDIR /app

# Копіюємо файли проекту з builder
COPY --from=builder /app /app

# Копіюємо .env файл
#COPY .env .env

EXPOSE ${PORT}

# Команда для запуску додатку
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "jarvis.config.wsgi:application"]
