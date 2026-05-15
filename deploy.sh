#!/bin/bash
# Deploy script for Railway

set -e

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist (optional)
# python manage.py shell < create_superuser.py

echo "Deployment completed successfully!"
