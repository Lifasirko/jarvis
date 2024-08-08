# Enable debugging
$ErrorActionPreference = "Stop"

# Step 1: Start Docker Compose
Write-Host "Starting Docker Compose..."
docker-compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start Docker Compose"
    Read-Host "Press any key to exit..."
    exit 1
}

# Step 2: Check for existing virtual environment
if (-Not (Test-Path -Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment"
        Read-Host "Press any key to exit..."
        exit 1
    }
} else {
    Write-Host "Virtual environment already exists."
}

# Step 3: Activate the virtual environment
Write-Host "Activating virtual environment..."
if ($env:OS -match "Windows_NT") {
    & "venv\Scripts\Activate.ps1"
} else {
    source venv/bin/activate
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to activate virtual environment"
    Read-Host "Press any key to exit..."
    exit 1
}

# Step 4: Check for Poetry and install dependencies
if (-Not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Host "Poetry is not installed. Installing Poetry..."
    pip install poetry
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install Poetry"
        Read-Host "Press any key to exit..."
        exit 1
    }
} else {
    Write-Host "Poetry is already installed."
}

# Step 5: Install dependencies with Poetry
Write-Host "Installing dependencies with Poetry..."
poetry install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies"
    Read-Host "Press any key to exit..."
    exit 1
}

# Step 6: Open project directory
Write-Host "Opening project directory..."
Set-Location -Path "jarvis"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to open project directory"
    Read-Host "Press any key to exit..."
    exit 1
}

# Step 7: Apply migrations
Write-Host "Applying migrations..."
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to apply migrations"
    Read-Host "Press any key to exit..."
    exit 1
}

# Step 8: Set up social apps
Write-Host "Setting up social apps..."
python manage.py setup_social_app
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to set up social apps"
    Read-Host "Press any key to exit..."
    exit 1
}

Write-Host "Setup completed successfully!"

# Keep the terminal window open
Read-Host "Press any key to exit..."
