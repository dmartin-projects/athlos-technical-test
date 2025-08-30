#!/bin/bash

# Activate virtual environment
export PATH="/py/bin:$PATH"

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting development server"
if [ "$DEBUG_MODE" = "true" ]; then
    echo "Starting with debugpy on port 5678"
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client manage.py runserver 0.0.0.0:8000 --noreload
else
    python manage.py runserver 0.0.0.0:8000
fi
