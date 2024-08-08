# Вказуємо базовий образ Python
FROM python:3.12-slim AS builder

# Встановлюємо необхідні пакети
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Встановлюємо робочу директорію
WORKDIR /app

# Додаємо Poetry до системного шляху
ENV PATH="/root/.local/bin:$PATH"

# Копіюємо файли для встановлення залежностей
COPY pyproject.toml poetry.lock ./

# Встановлюємо залежності
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Копіюємо файли додатку
COPY ./jarvis ./jarvis

# Stage 2: Runner
FROM python:3.12-slim AS runner

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо залежності та додаток з попереднього образу
COPY --from=builder /app /app

# Копіюємо .env файл
#COPY .env .env

# Встановлюємо порт
ENV PORT=8000
EXPOSE ${PORT}

# Команда запуску
CMD ["poetry", "run", "gunicorn", "--bind", ":8000", "jarvis.config.wsgi:application"]
