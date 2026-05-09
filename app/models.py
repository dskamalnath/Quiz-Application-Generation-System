from app import mysql
from datetime import datetime
import json

class Teacher:
    @staticmethod
    def create(name, email, password):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO Teacher (Name, Email, Password) VALUES (%s, %s, %s)",
                         (name, email, password))
            mysql.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            mysql.connection.rollback()
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Teacher WHERE Email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    @staticmethod
    def get_by_id(teacher_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Teacher WHERE Teacher_ID = %s", (teacher_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

class Student:
    @staticmethod
    def create(name, email, password, class_name):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO Student (Name, Email, Password, Class) VALUES (%s, %s, %s, %s)",
                         (name, email, password, class_name))
            mysql.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            mysql.connection.rollback()
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Student WHERE Email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    @staticmethod
    def get_by_id(student_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Student WHERE Student_ID = %s", (student_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

class Quiz:
    @staticmethod
    def create(teacher_id, title, description, total_marks, time_limit, required_questions=None):
        cursor = mysql.connection.cursor()
        try:
            if required_questions is None:
                cursor.execute("""INSERT INTO Quiz (Teacher_ID, Title, Description, Total_Marks, Time_Limit) 
                               VALUES (%s, %s, %s, %s, %s)""",
                             (teacher_id, title, description, total_marks, time_limit))
            else:
                cursor.execute("""INSERT INTO Quiz (Teacher_ID, Title, Description, Total_Marks, Time_Limit, Required_Questions) 
                               VALUES (%s, %s, %s, %s, %s, %s)""",
                             (teacher_id, title, description, total_marks, time_limit, required_questions))
            mysql.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            mysql.connection.rollback()
            print(f"Database error in Quiz.create: {str(e)}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_id(quiz_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Quiz WHERE Quiz_ID = %s", (quiz_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    @staticmethod
    def get_by_teacher(teacher_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Quiz WHERE Teacher_ID = %s ORDER BY Created_At DESC", (teacher_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @staticmethod
    def get_active_quizzes():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Quiz WHERE Is_Active = TRUE ORDER BY Created_At DESC")
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @staticmethod
    def update_status(quiz_id, is_active):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("UPDATE Quiz SET Is_Active = %s WHERE Quiz_ID = %s", (is_active, quiz_id))
            mysql.connection.commit()
            return True
        except:
            mysql.connection.rollback()
            return False
        finally:
            cursor.close()

class Question:
    @staticmethod
    def create(quiz_id, question_text, options, correct_answer, marks):
        cursor = mysql.connection.cursor()
        try:
            options_json = json.dumps(options) if isinstance(options, list) else options
            cursor.execute("""INSERT INTO Question (Quiz_ID, Question_Text, Options, Correct_Answer, Marks) 
                           VALUES (%s, %s, %s, %s, %s)""",
                         (quiz_id, question_text, options_json, correct_answer, marks))
            mysql.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            mysql.connection.rollback()
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_quiz(quiz_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Question WHERE Quiz_ID = %s", (quiz_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @staticmethod
    def get_by_id(question_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Question WHERE Question_ID = %s", (question_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    @staticmethod
    def count_by_quiz(quiz_id):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Question WHERE Quiz_ID = %s", (quiz_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            cursor.close()

class Result:
    @staticmethod
    def create(student_id, quiz_id, score, time_taken):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("""INSERT INTO Result (Student_ID, Quiz_ID, Score, Time_Taken) 
                           VALUES (%s, %s, %s, %s)""",
                         (student_id, quiz_id, score, time_taken))
            mysql.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"[Result.create] Error: {str(e)}")
            import traceback
            traceback.print_exc()
            mysql.connection.rollback()
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_student_quiz(student_id, quiz_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Result WHERE Student_ID = %s AND Quiz_ID = %s", 
                      (student_id, quiz_id))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    @staticmethod
    def get_by_quiz(quiz_id):
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT r.*, s.Name, s.Email FROM Result r 
                        JOIN Student s ON r.Student_ID = s.Student_ID 
                        WHERE r.Quiz_ID = %s 
                        ORDER BY r.Score DESC, r.Submitted_At DESC""", (quiz_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @staticmethod
    def get_student_results(student_id):
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT r.*, q.Title, q.Total_Marks FROM Result r 
                        JOIN Quiz q ON r.Quiz_ID = q.Quiz_ID 
                        WHERE r.Student_ID = %s 
                        ORDER BY r.Submitted_At DESC""", (student_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @staticmethod
    def update_rank(quiz_id):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("""UPDATE Result SET Rank = (
                           SELECT COUNT(*) + 1 FROM Result r2 
                           WHERE r2.Quiz_ID = %s AND r2.Score > Result.Score
                        ) WHERE Quiz_ID = %s""", (quiz_id, quiz_id))
            mysql.connection.commit()
            return True
        except:
            mysql.connection.rollback()
            return False
        finally:
            cursor.close()

class StudentAnswer:
    @staticmethod
    def create(result_id, question_id, selected_answer, is_correct, marks_obtained):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("""INSERT INTO StudentAnswer (Result_ID, Question_ID, Selected_Answer, Is_Correct, Marks_Obtained) 
                           VALUES (%s, %s, %s, %s, %s)""",
                         (result_id, question_id, selected_answer, is_correct, marks_obtained))
            mysql.connection.commit()
            return True
        except:
            mysql.connection.rollback()
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_result(result_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM StudentAnswer WHERE Result_ID = %s", (result_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
