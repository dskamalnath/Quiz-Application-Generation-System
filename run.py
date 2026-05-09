#!/usr/bin/env python
"""
Quiz Management System - Main Application Entry Point
"""

import os
import sys
from app import create_app, mysql

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Test database connection
@app.shell_context_processor
def make_shell_context():
    return {'mysql': mysql}

if __name__ == '__main__':
    # Test MySQL connection
    with app.app_context():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            print("✓ Database connection successful!")
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            print("\nPlease ensure:")
            print("1. XAMPP MySQL server is running")
            print("2. Database 'quiz_system' exists")
            print("3. MySQL credentials in config.py are correct")
            sys.exit(1)
    
    # Run Flask development server
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
