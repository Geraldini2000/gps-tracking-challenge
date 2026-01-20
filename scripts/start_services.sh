#!/bin/sh

# Run Django migrations
echo "Running Django migrations..."
python api/manage.py migrate

# Start Django API in background
echo "Starting Django API on port 8000..."
python api/manage.py runserver 0.0.0.0:8000 &

# Start TCP Gateway in foreground
echo "Starting TCP Gateway on port 8888..."
python -m tcp_gateway.server
