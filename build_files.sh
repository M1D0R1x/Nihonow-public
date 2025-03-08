#!/bin/bash

# Use the Vercel-provided Python binary
python3.9 -m pip install -r requirements.txt

# Run migrations
python3.9 manage.py migrate

# Collect static files
python3.9 manage.py collectstatic --noinput

# Create a build directory for Vercel
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/
