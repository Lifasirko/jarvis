# Вказуємо базовий образ Python
FROM python:3.12-slim

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

# Копіюємо файли додатку
COPY . .

# Встановлюємо порт
ENV PORT=8000
EXPOSE ${PORT}

# Команда запуску
CMD ["gunicorn", "--bind", ":8000", "jarvis.config.wsgi:application"]
