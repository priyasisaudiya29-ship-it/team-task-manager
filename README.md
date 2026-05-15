# Team Task Manager

A Django-based task management application that enables teams to organize, track, and collaborate on projects and tasks efficiently.

## Features

- **User Authentication**: Secure login and signup functionality
- **Project Management**: Create, view, and manage multiple projects
- **Task Management**: Create and organize tasks within projects
- **Dashboard**: Central hub to view all projects and tasks
- **REST API**: RESTful API endpoints for programmatic access
- **Admin Interface**: Django admin panel for system administration

## Tech Stack

- **Backend**: Django
- **Database**: SQLite (default)
- **API Framework**: Django REST Framework
- **Frontend**: Django Templates with HTML/CSS
- **Static Files Management**: Django Static Files

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/PriyaSisaudiya/team-task-manager.git
   cd team-task-manager
   ```

2. **Create and activate a virtual environment**

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install django djangorestframework
   ```

4. **Apply database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files** (if needed)
   ```bash
   python manage.py collectstatic
   ```

## Running the Project

1. **Start the development server**

   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   - Web interface: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## Project Structure

```
team-task-manager/
├── core/                    # Main application
│   ├── models.py           # Database models (Projects, Tasks, Users)
│   ├── views.py            # View functions for templates
│   ├── api_views.py        # API view classes
│   ├── serializers.py      # DRF serializers
│   ├── urls.py             # URL routing
│   ├── forms.py            # Django forms
│   ├── templates/          # HTML templates
│   ├── static/             # Static assets (CSS, JS)
│   └── migrations/         # Database migrations
├── team_task_manager/      # Project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Root URL configuration
│   ├── asgi.py             # ASGI configuration
│   └── wsgi.py             # WSGI configuration
├── manage.py               # Django management script
└── db.sqlite3              # SQLite database
```

## Available Pages

- `/` - Dashboard
- `/login` - User login
- `/signup` - User registration
- `/projects` - Project list
- `/projects/<id>/` - Project detail
- `/projects/new/` - Create new project
- `/tasks/new/` - Create new task
- `/admin/` - Admin panel

## API Endpoints

The application includes REST API endpoints for programmatic access. See `core/api_views.py` for available endpoints.

## Development

- **Create new migrations**: `python manage.py makemigrations`
- **Run migrations**: `python manage.py migrate`
- **Run tests**: `python manage.py test`
- **Create superuser**: `python manage.py createsuperuser`

## Database

The project uses SQLite by default (`db.sqlite3`). To use PostgreSQL or MySQL, update the `DATABASES` configuration in `team_task_manager/settings.py`.

## Troubleshooting

### Static files not loading

Run: `python manage.py collectstatic --noinput`

### Database errors

Try resetting migrations:

```bash
python manage.py migrate --fake-initial
```

### Port already in use

Run on a different port: `python manage.py runserver 8001`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on the GitHub repository.

---

**Created**: May 2026  
**Version**: 1.0.0
