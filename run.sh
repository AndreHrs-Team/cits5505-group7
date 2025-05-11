#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "[Run] Running install.sh..."
./install.sh

echo "[Run] Running db_migration.sh..."
./db_migration.sh

echo "[Run] Activating virtual environment..."
source application-env/bin/activate

echo "[Run] Running Flask app..."
flask run
