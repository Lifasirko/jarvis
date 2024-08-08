# Використовуємо офіційний образ Python з Docker Hub
FROM python:3.12-slim

# Встановлюємо залежності системи
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли проекту в контейнер
COPY . .

# Виставляємо змінні середовища
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"

# Встановлюємо залежності з використанням Poetry
RUN poetry install

# Перехід до директорії jarvis
WORKDIR /app/jarvis

# Відкриваємо порт 8000 для доступу до додатку
EXPOSE 8000

# Запускаємо команду для старту сервера
CMD ["poetry", "run", "uvicorn", "jarvis.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
