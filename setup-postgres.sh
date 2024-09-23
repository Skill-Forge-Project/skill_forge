#!/bin/bash

sleep 10

# This directory is created during the first run of PostgreSQL
if [ -f /var/lib/postgresql/data/pgdata/postgresql.conf ]; then
  echo "Appending pg_cron settings to postgresql.conf"
  
  # Append pg_cron settings
  echo "shared_preload_libraries = 'pg_cron'" >> /var/lib/postgresql/data/pgdata/postgresql.conf
  echo "cron.database_name = 'skill_forge_dev'" >> /var/lib/postgresql/data/pgdata/postgresql.conf

  # Restart PostgreSQL to apply the changes
  echo "Restarting PostgreSQL to apply changes..."
  # su - postgres -c "/usr/lib/postgresql/16/bin/pg_ctl -D /var/lib/postgresql/data/pgdata restart"
else
  echo "postgresql.conf not found, skipping pg_cron configuration."
fi
