#!/bin/bash
# Quiz Management System - Setup Script for Linux/Mac

echo ""
echo "=============================================="
echo "Quiz Management System - Setup Script"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please download Python from: https://www.python.org/"
    exit 1
fi

echo "[1/5] Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "[2/5] Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
else
    echo ""
    echo "[2/5] Virtual environment already exists, skipping creation..."
fi

echo ""
echo "[3/5] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[4/5] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[5/5] Setup complete!"
echo ""
echo "=============================================="
echo "Starting Quiz Management System..."
echo "=============================================="
echo ""
echo "Application will run at: http://localhost:5000"
echo ""
echo "Make sure:"
echo "- XAMPP MySQL server is running"
echo "- Database 'quiz_system' is created with tables"
echo "- MySQL credentials in config.py are correct"
echo ""

python3 run.py
