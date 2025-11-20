#!/bin/bash

# Start script for Smart Horses Backend
echo "🐴 Starting Smart Horses Backend..."

# Check if we're in production or development
if [ "$FLASK_ENV" = "production" ]; then
    echo "🚀 Running in PRODUCTION mode"
    gunicorn wsgi:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 60
else
    echo "🔧 Running in DEVELOPMENT mode"
    python run.py
fi
