#!/bin/sh
set -e

# Ensure .next directory exists (will be writable since we're excluding it from volume mount)
mkdir -p /app/.next

# Execute the command
exec "$@"

