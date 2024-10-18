#!/bin/bash

echo "Starting build process..."

# Check if necessary environment variables are set
echo "Checking environment variables..."
if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL is not set"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY is not set"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
python -m pip install -r requirements.txt

# Set up the database
echo "Setting up the database..."
python initialize_db.py
if [ $? -ne 0 ]; then
    echo "Error: Database initialization failed"
    exit 1
fi

# Install spaCy model
echo "Installing spaCy model..."
python -m spacy download en_core_web_sm

echo "Build process completed."

# Set up the run command for Replit
echo "Setting up the run command for Replit..."
echo "python main.py" > .replit

echo "Deployment setup completed."
