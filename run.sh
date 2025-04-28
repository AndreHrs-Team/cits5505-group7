#!/bin/bash
set -e  # Exit immediately if any command fails

# Run install.sh first
./install.sh

echo "Moving into backend folder..."
cd backend

echo "Activating virtual environment..."
source ../application-env/bin/activate

echo "Running Flask app..."
flask run
