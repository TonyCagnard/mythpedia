#!/bin/bash

# Script to start the Django mythology project

echo "Starting Django mythology project..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start the server with gunicorn
echo "Starting server with gunicorn..."
gunicorn mythology_project.wsgi:application --bind 0.0.0.0:$PORT