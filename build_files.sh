#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create a build directory for Vercel
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/
