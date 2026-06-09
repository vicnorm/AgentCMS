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
- REST API for exposing CMS page data as JSON
- KNIME integration through GET and POST endpoints
- Temporary endpoint for viewing latest data received from KNIME

---

## Tech Stack

- Python 3.12+
- Django 6.0
- SQLite (development database)
- HTML Templates + Static CSS
- Django REST Framework
- KNIME Analytics Platform

---

## Project Structure

```text
AgentCMS/
|-- cms/                                      # Main Django CMS application
|   |-- migrations/                           # Database migrations for Page and builder fields
|   |-- static/cms/                           # CMS styles and Django builder integration script
|   |   |-- builder_integration.js
|   |   `-- style.css
|   |-- templates/cms/                        # Django templates for pages and builder editor
|   |   |-- base.html
|   |   |-- builder_editor.html
|   |   |-- index.html
|   |   `-- page_detail.html
|   |-- admin.py                              # Django admin configuration
|   |-- apps.py                               # CMS app configuration
|   |-- builder_adapter.py                    # Builder payload validation and rendering
|   |-- context_processors.py                 # Navigation menu support
|   |-- models.py                             # Page model and builder content fields
|   |-- tests.py                              # CMS and builder endpoint tests
|   |-- urls.py                               # CMS URL routes
|   `-- views.py                              # Page and builder views
|
|-- config/                                   # Django project configuration
|   |-- asgi.py
|   |-- settings.py                           # Settings, installed apps, static files, TinyMCE
|   |-- urls.py                               # Root URL configuration
|   `-- wsgi.py
|
|-- api/                                      # REST API for KNIME integration
|   |-- migrations/
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- serializers.py                        # Page model JSON serialization
|   |-- tests.py
|   |-- urls.py                               # API routes
|   `-- views.py                              # GET/POST integration views
|
|-- frontend/
|   `-- Web-Design-Studio/                    # Standalone visual web builder
|       |-- README.md                         # Builder-specific documentation
|       `-- web_design_studio/
|           |-- css/studio_style.css          # Builder UI styles
|           |-- data/                         # HTML, JS, API component libraries and spreadsheets
|           |-- img/design_it_logo.png        # Builder image assets
|           |-- js/app.js                     # Builder entry script
|           |-- js/modules/                   # Builder managers for canvas, export, history, etc.
|           |-- excel_to_json2.py             # Spreadsheet-to-JSON component conversion
|           `-- index.html                    # Standalone builder entry point
|
|-- .gitignore                                # Ignored local/generated files
|-- manage.py                                 # Django management entry point
|-- requirements.txt                          # Python dependencies
`-- README.md                                 # Project documentation
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

---

## API Purpose

The API makes it possible to use AgentCMS as a data source for external workflow tools.

The intended data flow is:

```text
AgentCMS → KNIME → AgentCMS
```

### AgentCMS API and KNIME Integration

AgentCMS includes a simple REST API that allows external tools such as **KNIME** to retrieve CMS page data, process it, and send results back to AgentCMS.

### Testing the KNIME Integration

Assuming AgentCMS is already running locally, the integration can be tested with this API endpoint:

```text
http://127.0.0.1:8000/api/knime/pages/
```

View latest KNIME data can be showed with this API endpoint:

```text
GET /api/knime/latest/
```
