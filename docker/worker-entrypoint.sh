#!/bin/sh
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" > /dev/null 2>&1; do
  sleep 1
done

echo "PostgreSQL is up."

# Run migrations (Alembic example)
echo "Running migrations..."
alembic upgrade head

# Start the worker
echo "Starting worker..."
exec python -m workers.consumer
