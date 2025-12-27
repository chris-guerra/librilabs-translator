#!/bin/bash
# Setup test database for Docker environment
# This script creates the test database if it doesn't exist

set -e

POSTGRES_USER=${POSTGRES_USER:-librilabs}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-librilabs_dev}
POSTGRES_DB=${POSTGRES_DB:-librilabs_translator}
TEST_DB_NAME="${POSTGRES_DB}_test"
POSTGRES_HOST=${POSTGRES_HOST:-postgres}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

echo "Setting up test database: $TEST_DB_NAME"

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d postgres -c '\q' 2>/dev/null; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

# Create test database if it doesn't exist
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d postgres <<EOF
SELECT 'CREATE DATABASE $TEST_DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$TEST_DB_NAME')\gexec
EOF

echo "Test database $TEST_DB_NAME is ready!"

