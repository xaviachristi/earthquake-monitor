#!/bin/bash

# Usage: ./create_schema.sh postgres://username:password@host:port/dbname

if [ -z "$1" ]; then # checks if argument is empty - i.e. if user didn't include db url.
  echo "❌ Please provide a PostgreSQL connection URL."
  echo "Example: ./create_schema.sh postgres://postgres:postgres@localhost:5432/earthquake_db"
  exit 1
fi

echo "🔄 Running schema.sql against $1 ..."
psql "$1" -f schema.sql

if [ $? -eq 0 ]; then # checks schema ran without errors.
  echo "✅ Schema applied successfully."
else
  echo "❌ Failed to apply schema."
fi

echo "🌱 Seeding data from seed_data.sql ..."
psql "$1" -f seed_data.sql

if [ $? -eq 0 ]; then # checks seeding ran without errors.
  echo "✅ Data seeded successfully."
else
  echo "❌ Failed to seed data."
  exit 1
fi