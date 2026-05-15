release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn team_task_manager.wsgi --log-file - --access-logfile - --error-logfile - --workers 4
