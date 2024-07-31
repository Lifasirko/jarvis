
# JARVIS

Jarvis is a versatile personal assistant application designed to help users manage their tasks, contacts, notes, and news efficiently. It also includes features for AI-powered assistance, weather updates, and currency exchange rates.

## Installation

To run the project, follow these steps:

1. **Clone the repository**:
   ```sh
   git clone https://github.com/Lifasirko/jarvis
   ```

2. **Fill the .env file**:
   - Create a `.env` file in the root directory of the project and fill it with the appropriate settings.

3. **Install Poetry**:
   - Run the following command to install Poetry:
     ```sh
     pip install poetry
     ```

4. **Run Docker Compose**:
   - Bring up the necessary services using Docker Compose:
     ```sh
     docker-compose up -d
     ```

5. **Navigate to the project directory**:
   ```sh
   cd .\jarvis

6. **Apply migrations**:
   - Run database migrations:
     ```sh
     python manage.py migrate
     ```

7. **Create a superuser**:
   - Create a superuser for accessing the admin panel:
     ```sh
     python manage.py createsuperuser
     ```

## Usage

1. **Run the server**:
   - Start the development server:
     ```sh
     python manage.py runserver 8000
     ```

2. **Access the project**:
   - Open a web browser and go to:
     ```
     http://127.0.0.1:8000
     ```
   - For admin panel access, go to:
     ```
     http://127.0.0.1:8000/admin
     ```


## Project Structure

The project is divided into several main parts:

### Core

Contains core functionalities and common utilities for the project.

- **Admin:** Administrative site configuration.
- **Apps:** Configuration for the core application.
- **ChatGPT Service:** Integration with ChatGPT for AI capabilities.
- **Forms:** Forms used across the application.
- **Models:** Database models for the core functionalities.
- **RSS Feed:** RSS feed parsing and handling.
- **Templates:** Common HTML templates for core pages (404, 500, base, etc.).
- **Views:** Core views for handling requests and responses.

### Notes

Manages notes and related functionalities.

- **Admin:** Administrative site configuration for notes.
- **Apps:** Configuration for the notes application.
- **Forms:** Forms related to notes.
- **Models:** Database models for notes.
- **Templates:** HTML templates specific to notes (note list, note detail, etc.).
- **Views:** Views for handling notes-related requests and responses.

### Contacts

Manages contacts and related functionalities.

- **Admin:** Administrative site configuration for contacts.
- **Apps:** Configuration for the contacts application.
- **Forms:** Forms related to contacts.
- **Models:** Database models for contacts.
- **Templates:** HTML templates specific to contacts (contact list, add contact, etc.).
- **Views:** Views for handling contacts-related requests and responses.

### News

Handles news and related functionalities.

- **Admin:** Administrative site configuration for news.
- **Apps:** Configuration for the news application.
- **Management Commands:** Custom management commands for news (e.g., updating news).
- **Models:** Database models for news.
- **Templates:** HTML templates specific to news (news list, news detail, etc.).
- **Views:** Views for handling news-related requests and responses.

### Task Manager

Manages tasks and related functionalities.

- **Admin:** Administrative site configuration for tasks.
- **Apps:** Configuration for the task manager application.
- **Forms:** Forms related to tasks.
- **Models:** Database models for tasks.
- **Templates:** HTML templates specific to tasks (task list, task detail, etc.).
- **Views:** Views for handling tasks-related requests and responses.

## General Features

- **AI Integration:** Uses ChatGPT for AI capabilities.
- **Weather Information:** Provides weather updates.
- **Currency Exchange Rates:** Fetches and displays current exchange rates.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
