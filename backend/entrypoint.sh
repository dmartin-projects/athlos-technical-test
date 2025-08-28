#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --no-input

echo "Installing requirements"
pip install --upgrade pip
if [ "$ENVIRONMENT" = "production" ]; then
    pip install --no-cache-dir --upgrade -r requirements/production.txt
else
    pip install --no-cache-dir --upgrade -r requirements/development.txt
fi

# Start server
if [ "$ENVIRONMENT" = "production" ]; then
    echo "Starting production server with Gunicorn"
    gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
else
    echo "Starting development server"
    python3 manage.py runserver 0.0.0.0:8000
fi