#!/bin/bash

apt update && apt install postgresql-16-cron vim -y

# Check if the PostgreSQL config file exists
if [ -f /var/lib/postgresql/data/postgresql.conf ]; then
  echo "Appending pg_cron settings to postgresql.conf"
  
  # Append the pg_cron settings
  echo "shared_preload_libraries='pg_cron'" >> /var/lib/postgresql/data/postgresql.conf
  echo "cron.database_name='skill_forge_dev'" >> /var/lib/postgresql/data/postgresql.conf
else
  echo "postgresql.conf not found. Skipping append."
fi