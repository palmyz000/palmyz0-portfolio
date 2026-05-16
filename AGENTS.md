# AGENTS.md (Backend Architecture & System Logic)

## Project Summary
This project is a Web Application developed using the **Django Framework** to serve as a personal portfolio website for a Data Scientist and AI Engineer. The system is designed to handle profile data, work experience, skills, and includes various features such as a Contact Form system and special utility Tools.

## Folder Architecture
The project structure is divided into two main parts: the Project Root and the main App (`portfolio`):

- **`myresume/`**: The main Django Project folder
  - `settings.py`: The main system configuration file, including Database, Installed Apps, and Email SMTP settings.
  - `urls.py`: Top-level URL Routing.
- **`portfolio/`**: The main Django App folder managing Logic and User Interface.
  - `views.py`: Acts as the Controller for the system's logic. It contains a `DATA` variable storing all Mock Profile data and functions to handle web pages, including `contact_view` for processing POST requests from the contact form.
  - `urls.py`: URL Routing specifically for the portfolio app.
  - `templates/portfolio/`: Stores HTML Templates for each page.
  - `static/`: Stores CSS, JavaScript, and image assets (e.g., `robot_pet.js`).
- **`manage.py`**: The main command-line utility for managing the Django project.

## Coding Standard
- **Python**: Follow PEP 8 standards. Use `snake_case` for function and variable names in `views.py`.
- **Django Templates**: Separate Template files clearly by page (Modular approach) and inherit from a main structure (`base.html`).
- **JSON Handling**: Every internal API endpoint, such as the Contact form, must send and receive data in JSON format and handle Error responses with appropriate HTTP Status Codes and clear messages.

## Strict Security
- **Data Privacy & Credentials**: NEVER hardcode confidential information, such as passwords or API Keys, into the source code!
- **Current Code Observation**: The `settings.py` file currently contains a hardcoded Gmail App Password (`EMAIL_HOST_PASSWORD`). **A strict rule for all AI Agents in future development is to move these credentials to be read from environment variables (`.env`) using libraries like `python-dotenv` or `os.environ`.**
- **CSRF Protection**: Must use the `@ensure_csrf_cookie` decorator or pass a CSRF Token along with every API call that involves POST/PUT/DELETE requests from the Client side.
