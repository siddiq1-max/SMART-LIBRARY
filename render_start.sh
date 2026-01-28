#!/bin/bash

# Initialize Database (Create Tables if not exist)
echo "Initializing Database..."
python -c "from app import create_app, db; app=create_app(); app.app_context().push(); db.create_all()"

# Seed Data (Add books if empty)
echo "Seeding Data..."
python seed_data.py

# Start Application
echo "Starting Gunicorn..."
gunicorn run:app
