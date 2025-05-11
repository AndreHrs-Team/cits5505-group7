#!/bin/bash

echo "[Migration] Activating virtual environment..."
source application-env/bin/activate

echo "[Migration] Running flask db upgrade..."
flask db upgrade
