# Виведення відладкових повідомлень
set -x

# Запуск Docker Compose
echo "Starting Docker Compose..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "Failed to start Docker Compose"
    read -p "Press any key to exit..."
    exit 1
fi

# Перевірка наявності віртуального середовища
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment"
        read -p "Press any key to exit..."
        exit 1
    fi
else
    echo "Virtual environment already exists."
fi

# Визначення операційної системи
OS=$(uname -s | tr '[:upper:]' '[:lower:]')

# Активування віртуального середовища
echo "Activating virtual environment..."
if [[ "$OS" == "linux" ]] || [[ "$OS" == "darwin" ]]; then
    source venv/bin/activate
elif [[ "$OS" == "mingw"* ]]; then
    source venv/Scripts/activate
else
    echo "Unsupported OS: $OS"
    read -p "Press any key to exit..."
    exit 1
fi

if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment"
    read -p "Press any key to exit..."
    exit 1
fi

# Перевірка наявності Poetry
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing Poetry..."
    pip install poetry
    if [ $? -ne 0 ]; then
        echo "Failed to install Poetry"
        read -p "Press any key to exit..."
        exit 1
    fi
else
    echo "Poetry is already installed."
fi

# Встановлення залежностей з використанням Poetry
echo "Installing dependencies with Poetry..."
poetry install
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies"
    read -p "Press any key to exit..."
    exit 1
fi

# Перехід в директорію проекту
echo "Opening project directory..."
cd jarvis
if [ $? -ne 0 ]; then
    echo "Failed to open project directory"
    read -p "Press any key to exit..."
    exit 1
fi

# Виконання міграцій
echo "Applying migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Failed to apply migrations"
    read -p "Press any key to exit..."
    exit 1
fi

# Налаштування соціальних додатків
echo "Setting up social apps..."
python manage.py setup_social_app
if [ $? -ne 0 ]; then
    echo "Failed to set up social apps"
    read -p "Press any key to exit..."
    exit 1
fi

echo "Setup completed successfully!"

# Вимкнення відладкових повідомлень
set +x

# Утримання вікна відкритим до натискання клавіші
read -p "Press any key to exit..."
