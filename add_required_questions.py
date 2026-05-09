#!/usr/bin/env python3
"""
Script to add Required_Questions column to Quiz table
"""
import sys
sys.path.insert(0, '.')

from app import create_app, mysql

app = create_app()

with app.app_context():
    cursor = mysql.connection.cursor()
    try:
        # Try to add the column
        cursor.execute("""
            ALTER TABLE Quiz ADD COLUMN Required_Questions INT DEFAULT 0 AFTER Is_Active
        """)
        mysql.connection.commit()
        print("✓ Successfully added Required_Questions column to Quiz table")
    except Exception as e:
        if "Duplicate column name" in str(e):
            print("✓ Required_Questions column already exists")
        else:
            print(f"✗ Error: {e}")
            mysql.connection.rollback()
    finally:
        cursor.close()
