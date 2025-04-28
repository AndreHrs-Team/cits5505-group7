#!/bin/bash
set -e  # Exit immediately if any command fails

echo "Checking if virtual environment exists..."
if [ ! -f "./application-env/bin/activate" ]; then
    echo "Virtual environment not found..."
    echo "Creating virtual environment..."
    python3 -m venv application-env

    echo "Activating virtual environment..."
    source application-env/bin/activate

    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Virtual environment found..."
    # Activate it (optional here if you just want to acknowledge)
    source application-env/bin/activate
fi
