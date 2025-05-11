#!/bin/bash

echo "[Install] Checking if virtual environment exists..."

if [ ! -f "application-env/bin/activate" ]; then
    echo "[Install] Virtual environment not found..."
    echo "[Install] Creating virtual environment..."
    python3 -m venv application-env

    echo "[Install] Activating virtual environment..."
    source application-env/bin/activate

    echo "[Install] Installing dependencies..."
    pip install -r requirements.txt
else
    echo "[Install] Virtual environment found..."
    source application-env/bin/activate
fi
