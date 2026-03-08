# AgentCMS

AgentCMS is a lightweight Content Management System built with **Django**.  
It allows administrators to create and manage simple website pages through the Django admin panel.

---

## Features

- Page-based CMS system (`title`, `body`, `slug`)
- Publish/unpublish pages (`is_published`)
- Content managed through Django Admin
- Public page rendering with Django templates
- Automatic navigation menu showing published pages
- Shared layout using `base.html`
- Static file support (CSS)
- SQLite database (possibility to switch to Postgresql)

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
```

---

## Installation Guide (Local Setup)

### 1. Clone the Repository

```bash
git clone https://github.com/vicnorm/AgentCMS.git
cd AgentCMS
```

### 2. Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (CMD)**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create an Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create a login.

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open in your browser:

- Website: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

On macOS/Linux, you may need to use:

```bash
python3 manage.py runserver
```

## Using the CMS

1. Log into the admin panel: http://127.0.0.1:8000/admin/
2. Create a new **Page** with:
   - Title
   - Body text
   - Slug (URL name)
   - Mark as published
3. View the page on the site:

```text
http://127.0.0.1:8000/<slug>/
```

Example:

```text
http://127.0.0.1:8000/home/
```

Published pages also appear automatically in the navigation menu.
