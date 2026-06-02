# Django Notes CRUD App

A simple Notes Management application built using Django that allows users to create, view, edit, and delete notes.

## Features

* Create new notes
* View all saved notes
* Edit existing notes
* Delete notes
* Title and content validation
* Success and error messages
* Bootstrap-based UI
* SQLite database integration

## Tech Stack

* Python
* Django
* HTML
* CSS
* Bootstrap
* SQLite

## Project Structure

```text
mysite/
├── manage.py
├── mysite/
├── notes/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── static/
│   └── migrations/
├── requirements.txt
└── .gitignore
```

## Database Model

### Note

| Field      | Type          |
| ---------- | ------------- |
| title      | CharField     |
| content    | TextField     |
| created_at | DateTimeField |

## Installation

1. Clone the repository

```bash
git clone https://github.com/isjn227-pickymty/django-notes-crud-app.git
```

2. Navigate to the project directory

```bash
cd django-notes-crud-app
```

3. Create a virtual environment

```bash
python -m venv venv
```

4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Apply migrations

```bash
python manage.py migrate
```

7. Run the development server

```bash
python manage.py runserver
```

8. Open in browser

```text
http://127.0.0.1:8000/
```

## Future Improvements

* User Authentication (Login/Register)
* User-specific Notes
* Search Functionality
* Categories and Tags
* REST API using Django REST Framework
* Deployment on Render

## Learning Outcomes

This project helped me understand:

* Django Models
* Views and URLs
* Template Inheritance
* Forms and POST Requests
* CRUD Operations
* Django ORM
* Migrations
* Static Files
* Django Messages Framework

## Author

Ishita Jain
