"""
Database Helper Script - Use this to initialize your database
Run this before starting the application for the first time
"""

import mysql.connector
from mysql.connector import Error

def create_database():
    """Create quiz_system database and tables"""
    
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'quiz_system'
    }
    
    # SQL schema
    sql_file_path = 'database/quiz_system.sql'
    
    try:
        # Connect to MySQL
        print("Connecting to MySQL...")
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        
        cursor = conn.cursor()
        
        # Read SQL file
        print("Reading database schema...")
        with open(sql_file_path, 'r') as f:
            sql_statements = f.read()
        
        # Execute SQL statements
        print("Creating database and tables...")
        for statement in sql_statements.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        print("✓ Database created successfully!")
        
        # Verify tables
        cursor.execute("SHOW TABLES FROM quiz_system")
        tables = cursor.fetchall()
        print(f"\n✓ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure XAMPP MySQL is running")
        print("2. Check default password is empty for root user")
        print("3. Verify MySQL is accessible at localhost:3306")
        return False
    
    return True

if __name__ == '__main__':
    print("Quiz Management System - Database Setup")
    print("=" * 50)
    print()
    
    if create_database():
        print("\n" + "=" * 50)
        print("Database setup complete!")
        print("You can now run: python run.py")
    else:
        print("\nDatabase setup failed. Please fix the errors above.")
