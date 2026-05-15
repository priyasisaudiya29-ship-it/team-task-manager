#!/usr/bin/env python
"""
Local Validation Script - Run before deployment to Railway
Tests all configurations and dependencies
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_task_manager.settings')
django.setup()

from django.core.management import call_command
from django.apps import apps
from django.conf import settings
import importlib

print("=" * 60)
print("TEAM TASK MANAGER - DEPLOYMENT VALIDATION")
print("=" * 60)

errors = []
warnings = []

# 1. Check Python Version
print("\n✓ Python Environment")
print(f"  Python: {sys.version}")

# 2. Check Django Installation
print(f"  Django: {django.get_version()}")

# 3. Check Required Apps
print("\n✓ Installed Apps")
for app in settings.INSTALLED_APPS:
    print(f"  - {app}")

# 4. Check Database
print("\n✓ Database Configuration")
print(f"  Engine: {settings.DATABASES['default']['ENGINE']}")
print(f"  Name: {settings.DATABASES['default']['NAME']}")

# 5. Run Migrations Check
print("\n✓ Migrations Status")
try:
    call_command('migrate', '--check', verbosity=0)
    print("  ✓ All migrations applied")
except Exception as e:
    errors.append(f"Migration check failed: {str(e)}")

# 6. Check Templates
print("\n✓ Template Directories")
for template_dir in settings.TEMPLATES[0]['DIRS']:
    if os.path.exists(template_dir):
        print(f"  ✓ {template_dir}")
    else:
        warnings.append(f"Template directory not found: {template_dir}")

# 7. Check Static Files
print("\n✓ Static Files Configuration")
print(f"  STATIC_URL: {settings.STATIC_URL}")
print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")

# 8. Test Models
print("\n✓ Model Validation")
try:
    from core.models import Project, Task
    print("  ✓ Project model loaded")
    print("  ✓ Task model loaded")
except ImportError as e:
    errors.append(f"Model import error: {str(e)}")

# 9. Test Views
print("\n✓ Views Validation")
try:
    from core import views
    print("  ✓ Views module loaded")
    required_views = ['dashboard', 'project_list', 'project_create', 'task_create']
    for view in required_views:
        if hasattr(views, view):
            print(f"    ✓ {view}")
        else:
            warnings.append(f"View not found: {view}")
except ImportError as e:
    errors.append(f"Views import error: {str(e)}")

# 10. Test Serializers
print("\n✓ REST API Serializers")
try:
    from core.serializers import ProjectSerializer, TaskSerializer
    print("  ✓ ProjectSerializer loaded")
    print("  ✓ TaskSerializer loaded")
except ImportError as e:
    errors.append(f"Serializer import error: {str(e)}")

# 11. Check Required Packages
print("\n✓ Required Packages")
required_packages = [
    'django',
    'rest_framework',
    'decouple',
    'gunicorn',
    'whitenoise',
]

for package in required_packages:
    try:
        module = importlib.import_module(package)
        print(f"  ✓ {package}")
    except ImportError:
        errors.append(f"Missing package: {package}")

# 12. Environment Variables
print("\n✓ Environment Variables")
env_vars = ['DEBUG', 'SECRET_KEY', 'ALLOWED_HOSTS']
for var in env_vars:
    val = os.getenv(var, '(not set)')
    if var == 'SECRET_KEY' and val != '(not set)':
        val = '*' * 10  # Hide secret key
    print(f"  {var}: {val}")

# 13. Run Checks
print("\n✓ Django System Checks")
try:
    call_command('check', verbosity=0)
    print("  ✓ No system errors found")
except Exception as e:
    errors.append(f"System check failed: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)

if errors:
    print(f"\n❌ ERRORS FOUND ({len(errors)}):")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

if warnings:
    print(f"\n⚠️  WARNINGS ({len(warnings)}):")
    for warning in warnings:
        print(f"  - {warning}")

print("\n✅ VALIDATION PASSED - Ready for deployment!")
print("\nNext steps:")
print("  1. git add .")
print("  2. git commit -m 'Final deployment prep'")
print("  3. git push origin main")
print("  4. Deploy to Railway")
print("\n" + "=" * 60)
