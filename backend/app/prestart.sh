#! /usr/bin/env bash

export PYTHONPATH='/app':$PYTHONPATH

# Let the DB start
python /app/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/app/initial_data.py
