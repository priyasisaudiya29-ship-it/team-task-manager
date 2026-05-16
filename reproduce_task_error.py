import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_task_manager.settings')
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from core.models import Project

user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
if created or not user.has_usable_password():
    user.set_password('testpass123')
    user.save()
project, _ = Project.objects.get_or_create(name='Test Project', owner=user, defaults={'description': 'Test project', 'status': 'active'})
project.members.add(user)
project.save()

client = Client()
if not client.login(username='testuser', password='testpass123'):
    raise SystemExit('Login failed')

response = client.post(f'/projects/{project.id}/tasks/create/', {
    'title': 'Test Task',
    'description': 'A test task',
    'assigned_to': str(user.id),
    'status': 'todo',
    'priority': 'medium',
    'due_date': '2099-12-31',
})
print('Status code:', response.status_code)
print('Redirects:', response.redirect_chain)
print('Content:', response.content.decode('utf-8')[:1000])
