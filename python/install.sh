#!/bin/bash

# Wispbyte Python Service Installation Script
# This script installs required dependencies and starts the application.
# Assumes Python 3.8+ is installed and the app.py file is in the current directory.

set -e  # Exit on any error

echo "🚀 Starting Wispbyte Python Service Installation..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment (optional but recommended)
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install dependencies with versions
echo "📥 Installing dependencies..."
pip install \
    flask==3.0.3 \
    psutil==6.0.0

echo "✅ Dependencies installed successfully!"

# Optional: Create requirements.txt for future use
echo "📝 Generating requirements.txt..."
pip freeze > requirements.txt

# Start the application
echo "🏃 Starting the application on port 14659..."
echo "Press Ctrl+C to stop."
python app.py
