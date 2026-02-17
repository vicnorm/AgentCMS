# AgentCMS

AgentCMS is a lightweight Content Management System built with **Django**.  
It allows administrators to create and manage simple website pages through the Django admin panel.

This project is designed as a learning project and a foundation for building a more complete CMS over time.

---

## Features

- Page-based CMS system (`title`, `body`, `slug`)
- Publish/unpublish pages (`is_published`)
- Content managed through Django Admin
- Public page rendering with Django templates
- Automatic navigation menu showing published pages
- Shared layout using `base.html`
- Static file support (CSS)
- SQLite database by default (easy to switch later)

---

## Tech Stack

- Python 3.12+
- Django 6.0
- SQLite (development database)
- HTML Templates + Static CSS

---

## Project Structure

```text
AgentCMS/
├── cms/                     # Main CMS application
│   ├── migrations/          # Database migrations
│   ├── static/cms/          # Static files (CSS)
│   ├── templates/cms/       # HTML templates
│   ├── admin.py             # Admin configuration
│   ├── context_processors.py# Navigation menu support
│   ├── models.py            # Page model
│   ├── urls.py              # App URL routes
│   └── views.py             # Page views
│
├── config/                  # Django project configuration
│   ├── settings.py          # Main settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py / asgi.py
│
├── manage.py                # Django management entry point
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignored files
└── README.md                # Project documentation


---

## Installation Guide (Local Setup)

### 1. Clone the Repository

```bash
git clone https://github.com/vicnorm/AgentCMS.git
cd AgentCMS
2. Create a Virtual Environment
macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
Windows (CMD)
python -m venv .venv
.venv\Scripts\activate.bat
Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
3. Install Dependencies
python -m pip install -r requirements.txt
4. Apply Database Migrations
python manage.py migrate
5. Create an Admin User
python manage.py createsuperuser
Follow the prompts to create a login.

6. Start the Development Server
python manage.py runserver
Open in your browser:

Website: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/

On macOS/Linux, you may need to use:

python3 manage.py runserver
Using the CMS
Log into the admin panel
http://127.0.0.1:8000/admin/

Create a new Page

Title

Body text

Slug (URL name)

Mark as published

View the page on the site:

http://127.0.0.1:8000/<slug>/
Example:

http://127.0.0.1:8000/home/
Published pages also appear automatically in the navigation menu.
