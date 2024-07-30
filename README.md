
# JARVIS

Jarvis is a versatile personal assistant application designed to help users manage their tasks, contacts, notes, and news efficiently. It also includes features for AI-powered assistance, weather updates, and currency exchange rates.

## Installation

### Using Poetry

1. Ensure you have Poetry installed. If not, you can install it using the following command:

   ```sh
   pip install poetry
   ```

2. Clone the repository:

   ```sh
   git clone <repository-url>
   ```

3. Navigate to the project directory:

   ```sh
   cd <project-directory>
   ```

4. Install the dependencies:

   ```sh
   poetry install
   ```

5. Activate the virtual environment:

   ```sh
   poetry shell
   ```

## Usage

1. Run the Docker containers:

   ```sh
   docker-compose up
   ```

2. Apply migrations:

   ```sh
   python manage.py migrate
   ```

3. Create a superuser:

   ```sh
   python manage.py createsuperuser
   ```

4. Start the development server:

   ```sh
   python manage.py runserver
   ```

5. Open your web browser and go to `http://127.0.0.1:8000/`.

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
