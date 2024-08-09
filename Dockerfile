# Вказуємо базовий образ Python
FROM python:3.12-slim AS builder

# Встановлюємо необхідні пакети
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли для встановлення залежностей
COPY requirements.txt ./

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Встановлюємо Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Додаємо Poetry до системного шляху
ENV PATH="/root/.local/bin:$PATH"

# Копіюємо файли додатку
COPY ./jarvis ./jarvis

# Stage 2: Runner
FROM python:3.12-slim AS runner

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо залежності та додаток з попереднього образу
COPY --from=builder /app /app

# Встановлюємо порт
ENV PORT=8000
EXPOSE ${PORT}

# Команда запуску
CMD ["gunicorn", "--bind", ":8000", "jarvis.config.wsgi:application"]
