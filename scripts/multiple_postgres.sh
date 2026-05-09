#!/bin/bash
set -e

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
    echo "Creating multiple databases: $POSTGRES_MULTIPLE_DATABASES"
    for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
        # Check if database exists first
        DB_EXISTS=$(psql -U "$POSTGRES_USER" -tAc "SELECT 1 FROM pg_database WHERE datname='$db'")
        
        if [ "$DB_EXISTS" != "1" ]; then
            psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
                CREATE DATABASE $db;
                GRANT ALL PRIVILEGES ON DATABASE $db TO $POSTGRES_USER;
EOSQL
        else
            echo "Database '$db' already exists, skipping."
        fi
    done
fi
