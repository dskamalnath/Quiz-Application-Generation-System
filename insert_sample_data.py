"""
Sample Data Insertion Script
Insert this sample data to test the application
"""

import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

def insert_sample_data():
    """Insert sample data for testing"""
    
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'quiz_system'
    }
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("Inserting sample data...")
        
        # Insert Teachers
        teacher_data = [
            ('Dr. Smith', 'smith@teacher.com', generate_password_hash('password123')),
            ('Prof. Johnson', 'johnson@teacher.com', generate_password_hash('password123')),
        ]
        
        cursor.executemany(
            "INSERT INTO Teacher (Name, Email, Password) VALUES (%s, %s, %s)",
            teacher_data
        )
        conn.commit()
        print("✓ Inserted 2 sample teachers")
        
        # Insert Students
        student_data = [
            ('Alice Johnson', 'alice@student.com', generate_password_hash('password123'), 'Class 10-A'),
            ('Bob Smith', 'bob@student.com', generate_password_hash('password123'), 'Class 10-A'),
            ('Charlie Brown', 'charlie@student.com', generate_password_hash('password123'), 'Class 10-B'),
            ('Diana Prince', 'diana@student.com', generate_password_hash('password123'), 'Class 10-B'),
        ]
        
        cursor.executemany(
            "INSERT INTO Student (Name, Email, Password, Class) VALUES (%s, %s, %s, %s)",
            student_data
        )
        conn.commit()
        print("✓ Inserted 4 sample students")
        
        # Insert Sample Quiz
        cursor.execute(
            "INSERT INTO Quiz (Teacher_ID, Title, Description, Total_Marks, Time_Limit, Is_Active) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (1, 'General Knowledge Quiz', 'Test your general knowledge with these 5 questions', 5, 10, True)
        )
        conn.commit()
        quiz_id = cursor.lastrowid
        print(f"✓ Inserted 1 sample quiz (ID: {quiz_id})")
        
        # Insert Questions
        questions = [
            (quiz_id, 'What is the capital of France?', '["Paris", "London", "Berlin", "Madrid"]', '0', 1),
            (quiz_id, 'Which planet is closest to the Sun?', '["Venus", "Mercury", "Earth", "Mars"]', '1', 1),
            (quiz_id, 'What is the largest ocean?', '["Atlantic", "Indian", "Arctic", "Pacific"]', '3', 1),
            (quiz_id, 'Who wrote Romeo and Juliet?', '["William Shakespeare", "Jane Austen", "Charles Dickens", "Mark Twain"]', '0', 1),
            (quiz_id, 'What is 2 + 2?', '["3", "4", "5", "6"]', '1', 1),
        ]
        
        cursor.executemany(
            "INSERT INTO Question (Quiz_ID, Question_Text, Options, Correct_Answer, Marks) "
            "VALUES (%s, %s, %s, %s, %s)",
            questions
        )
        conn.commit()
        print("✓ Inserted 5 sample questions")
        
        # Insert Sample Results
        results = [
            (1, quiz_id, 4, 1, 8),  # Alice: 4/5
            (2, quiz_id, 3, 2, 7),  # Bob: 3/5
            (3, quiz_id, 5, 1, 9),  # Charlie: 5/5
            (4, quiz_id, 2, 3, 10), # Diana: 2/5
        ]
        
        for student_id, q_id, score, rank, time_taken in results:
            cursor.execute(
                "INSERT INTO Result (Student_ID, Quiz_ID, Score, Rank, Time_Taken) "
                "VALUES (%s, %s, %s, %s, %s)",
                (student_id, q_id, score, rank, time_taken)
            )
        conn.commit()
        print("✓ Inserted 4 sample results")
        
        print("\n" + "=" * 50)
        print("Sample data inserted successfully!")
        print("=" * 50)
        print("\nTest Credentials:")
        print("-" * 50)
        print("Teacher Login:")
        print("  Email: smith@teacher.com")
        print("  Password: password123")
        print()
        print("Student Login:")
        print("  Email: alice@student.com")
        print("  Password: password123")
        print("-" * 50)
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"✗ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("Quiz Management System - Sample Data Insertion")
    print("=" * 50)
    print()
    
    if insert_sample_data():
        print("\nYou can now log in and test the application!")
    else:
        print("\nFailed to insert sample data. Please check errors above.")
