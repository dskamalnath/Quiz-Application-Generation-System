from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json
from datetime import datetime
from app import mysql
from app.models import Teacher, Student, Quiz, Question, Result, StudentAnswer

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/')
teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')
student_bp = Blueprint('student', __name__, url_prefix='/student')
quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')

# Authentication decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'user_type' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"[DECORATOR] teacher_required called. Session: {dict(session)}")
        print(f"[DECORATOR] 'user_id' in session: {'user_id' in session}")
        print(f"[DECORATOR] user_type: {session.get('user_type')}")
        if 'user_id' not in session or session.get('user_type') != 'teacher':
            print(f"[DECORATOR] Access denied. Redirecting to login.")
            return redirect(url_for('auth.login'))
        print(f"[DECORATOR] Access granted to teacher route")
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'student':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# ============ AUTH ROUTES ============
@auth_bp.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        if session.get('user_type') == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        else:
            return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        user_type = request.form.get('user_type', 'student').strip()
        
        print(f"[LOGIN] Email: {email}, Type: {user_type}")
        
        if not email or not password or not user_type:
            flash('Email, password, and user type are required', 'danger')
            return render_template('login.html')
        
        try:
            if user_type == 'teacher':
                user = Teacher.get_by_email(email)
            else:
                user = Student.get_by_email(email)
            
            print(f"[LOGIN] User data retrieved: {user}")
            
            if user and len(user) >= 4:
                print(f"[LOGIN] User found. ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
                print(f"[LOGIN] Password hash from DB: {user[3][:20]}...")
                print(f"[LOGIN] Checking password...")
                
                if check_password_hash(user[3], password):
                    print(f"[LOGIN] Password matched!")
                    session.permanent = True
                    session['user_id'] = int(user[0])
                    session['user_name'] = str(user[1])
                    session['user_email'] = str(user[2])
                    session['user_type'] = user_type
                    
                    print(f"[LOGIN] Session set. user_id={session['user_id']}, user_type={session['user_type']}")
                    print(f"[LOGIN] Full session: {dict(session)}")
                    
                    if user_type == 'teacher':
                        print(f"[LOGIN] Redirecting to teacher dashboard")
                        return redirect(url_for('teacher.dashboard'))
                    else:
                        print(f"[LOGIN] Redirecting to student dashboard")
                        return redirect(url_for('student.dashboard'))
                else:
                    print(f"[LOGIN] Password check failed!")
                    flash('Invalid email or password', 'danger')
            else:
                print(f"[LOGIN] User not found or insufficient data. User: {user}, Len: {len(user) if user else 0}")
                flash('Invalid email or password', 'danger')
        except Exception as e:
            print(f"[LOGIN] Error: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'Login error: {str(e)}', 'danger')
    
    return render_template('login.html')

@auth_bp.route('register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type = request.form.get('user_type')
        class_name = request.form.get('class')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.register'))
        
        hashed_password = generate_password_hash(password)
        
        if user_type == 'teacher':
            user_id = Teacher.create(name, email, hashed_password)
        else:
            user_id = Student.create(name, email, hashed_password, class_name)
        
        if user_id:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email already exists or registration failed', 'danger')
    
    return render_template('register.html')

@auth_bp.route('logout', methods=['POST'])
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))

# ============ TEACHER ROUTES ============
@teacher_bp.route('dashboard', methods=['GET'])
@teacher_required
def dashboard():
    try:
        print(f"[TEACHER-DASH] Session data received: {dict(session)}")
        print(f"[TEACHER-DASH] user_id type: {type(session.get('user_id'))}, value: '{session.get('user_id')}'")
        
        teacher_id = int(session.get('user_id', 0))
        if not teacher_id:
            flash('Invalid session. Please login again.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Get all quizzes for this teacher
        quizzes = Quiz.get_by_teacher(teacher_id)
        
        # If quizzes is None, make it an empty list
        if quizzes is None:
            quizzes = []
        
        dashboard_data = {
            'total_quizzes': len(quizzes),
            'quizzes': quizzes if quizzes else None
        }
        
        return render_template('teacher/dashboard.html', data=dashboard_data)
    except Exception as e:
        print(f"[TEACHER-DASH] Error in teacher dashboard: {str(e)}")
        print(f"[TEACHER-DASH] Session data: {dict(session)}")
        import traceback
        traceback.print_exc()
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))

@teacher_bp.route('create-quiz', methods=['GET', 'POST'])
@teacher_required
def create_quiz():
    if request.method == 'POST':
        try:
            teacher_id = int(session.get('user_id', 0))
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            total_marks_str = request.form.get('total_marks', '0').strip()
            time_limit_str = request.form.get('time_limit', '0').strip()
            required_questions_str = request.form.get('required_questions', '0').strip()
            
            # Validate inputs
            if not title:
                flash('Quiz title is required', 'danger')
                return render_template('teacher/create_quiz.html')
            
            if not total_marks_str or not time_limit_str or not required_questions_str:
                flash('All fields are required', 'danger')
                return render_template('teacher/create_quiz.html')
            
            total_marks = int(total_marks_str)
            time_limit = int(time_limit_str)
            required_questions = int(required_questions_str)
            
            if total_marks <= 0 or time_limit <= 0 or required_questions <= 0:
                flash('Marks, time limit, and number of questions must be greater than 0', 'danger')
                return render_template('teacher/create_quiz.html')
            
            quiz_id = Quiz.create(teacher_id, title, description, total_marks, time_limit, required_questions)
            if quiz_id:
                flash('Quiz created successfully! Now add your questions.', 'success')
                return redirect(url_for('teacher.edit_quiz', quiz_id=quiz_id))
            else:
                flash('Failed to create quiz', 'danger')
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'danger')
        except Exception as e:
            print(f"Error creating quiz: {str(e)}")
            flash(f'Error creating quiz: {str(e)}', 'danger')
    
    return render_template('teacher/create_quiz.html')

@teacher_bp.route('edit-quiz/<int:quiz_id>', methods=['GET', 'POST'])
@teacher_required
def edit_quiz(quiz_id):
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz or quiz[1] != session['user_id']:
        flash('Unauthorized', 'danger')
        return redirect(url_for('teacher.dashboard'))
    
    # Handle POST request to update number of questions
    if request.method == 'POST':
        num_questions = request.form.get('num_questions')
        if num_questions:
            try:
                num_questions = int(num_questions)
                if num_questions < 1 or num_questions > 100:
                    flash('Number of questions must be between 1 and 100', 'danger')
                else:
                    # Update the quiz with new number of questions
                    cursor = mysql.connection.cursor()
                    cursor.execute('UPDATE Quiz SET Required_Questions = %s WHERE Quiz_ID = %s', (num_questions, quiz_id))
                    mysql.connection.commit()
                    cursor.close()
                    flash(f'Quiz updated! This quiz will have {num_questions} questions.', 'success')
                    quiz = Quiz.get_by_id(quiz_id)
            except (ValueError, TypeError):
                flash('Invalid number of questions', 'danger')
        else:
            flash('Please enter number of questions', 'danger')
    
    questions = Question.get_by_quiz(quiz_id)
    
    return render_template('teacher/edit_quiz.html', quiz=quiz, questions=questions)

@teacher_bp.route('add-question/<int:quiz_id>', methods=['POST'])
@teacher_required
def add_question(quiz_id):
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz or quiz[1] != session['user_id']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    question_text = request.form.get('question_text')
    options = request.form.getlist('options')
    correct_answer = request.form.get('correct_answer')
    marks = int(request.form.get('marks', 1))
    
    question_id = Question.create(quiz_id, question_text, options, correct_answer, marks)
    
    if question_id:
        return jsonify({'success': True, 'question_id': question_id})
    else:
        return jsonify({'success': False, 'message': 'Failed to add question'}), 500

@teacher_bp.route('view-results/<int:quiz_id>', methods=['GET'])
@teacher_required
def view_results(quiz_id):
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz or quiz[1] != session['user_id']:
        flash('Unauthorized', 'danger')
        return redirect(url_for('teacher.dashboard'))
    
    results = Result.get_by_quiz(quiz_id)
    
    # Calculate statistics
    stats = {
        'total_attempts': len(results) if results else 0,
        'average_score': 0,
        'highest_score': 0,
        'lowest_score': 0
    }
    
    if results:
        scores = [r[3] for r in results]
        stats['average_score'] = round(sum(scores) / len(scores), 2)
        stats['highest_score'] = max(scores)
        stats['lowest_score'] = min(scores)
    
    return render_template('teacher/view_results.html', quiz=quiz, results=results, stats=stats)

@teacher_bp.route('toggle-quiz/<int:quiz_id>', methods=['POST'])
@teacher_required
def toggle_quiz(quiz_id):
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz or quiz[1] != session['user_id']:
        return jsonify({'success': False}), 403
    
    new_status = not quiz[7]  # Toggle the status
    if Quiz.update_status(quiz_id, new_status):
        return jsonify({'success': True, 'new_status': new_status})
    return jsonify({'success': False}), 500

# ============ STUDENT ROUTES ============
@student_bp.route('dashboard', methods=['GET'])
@student_required
def dashboard():
    try:
        student_id = int(session.get('user_id', 0))
        if not student_id:
            flash('Invalid session. Please login again.', 'danger')
            return redirect(url_for('auth.login'))
        
        active_quizzes = Quiz.get_active_quizzes()
        student_results = Result.get_student_results(student_id)
        
        dashboard_data = {
            'active_quizzes': active_quizzes,
            'results': student_results
        }
        
        return render_template('student/dashboard.html', data=dashboard_data)
    except Exception as e:
        print(f"Error in student dashboard: {e}")
        flash('Error loading dashboard. Please try again.', 'danger')
        return redirect(url_for('auth.login'))

@student_bp.route('leaderboard/<int:quiz_id>', methods=['GET'])
@student_required
def leaderboard(quiz_id):
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz:
        flash('Quiz not found', 'danger')
        return redirect(url_for('student.dashboard'))
    
    results = Result.get_by_quiz(quiz_id)
    
    return render_template('student/leaderboard.html', quiz=quiz, results=results)

# ============ QUIZ ROUTES ============
@quiz_bp.route('start/<int:quiz_id>', methods=['GET', 'POST'])
@student_required
def start_quiz(quiz_id):
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz or not quiz[7]:  # Check if quiz exists and is active
        flash('Quiz not found or not active', 'danger')
        return redirect(url_for('student.dashboard'))
    
    questions = Question.get_by_quiz(quiz_id)
    if not questions:
        flash('This quiz has no questions', 'danger')
        return redirect(url_for('student.dashboard'))
    
    if request.method == 'POST':
        return redirect(url_for('quiz.take_quiz', quiz_id=quiz_id))
    
    return render_template('student/start_quiz.html', quiz=quiz, question_count=len(questions))

@quiz_bp.route('take/<int:quiz_id>', methods=['GET', 'POST'])
@student_required
def take_quiz(quiz_id):
    quiz = Quiz.get_by_id(quiz_id)
    if not quiz or not quiz[7]:
        flash('Quiz not available', 'danger')
        return redirect(url_for('student.dashboard'))
    
    questions = Question.get_by_quiz(quiz_id)
    
    if request.method == 'POST':
        student_id = session['user_id']
        answers = request.form
        
        try:
            # Check if this student already has a result for this quiz
            existing_result = Result.get_by_student_quiz(student_id, quiz_id)
            
            if existing_result:
                # Update existing result (student is retaking the quiz)
                result_id = existing_result[0]
                print(f"[TAKE QUIZ] Updating existing result: {result_id}")
            else:
                # Create new result
                result_id = Result.create(student_id, quiz_id, 0, 0)
                print(f"[TAKE QUIZ] Created new result: {result_id}")
            
            if not result_id:
                flash('Failed to submit quiz', 'danger')
                return redirect(url_for('student.dashboard'))
            
            # Delete old answers if retaking the quiz
            if existing_result:
                from app import mysql
                cursor = mysql.connection.cursor()
                cursor.execute("DELETE FROM StudentAnswer WHERE Result_ID = %s", (result_id,))
                mysql.connection.commit()
                cursor.close()
            
            # Calculate score
            score = 0
            for question in questions:
                question_id = question[0]
                correct_answer = question[4]
                marks = question[5]
                
                selected_answer = answers.get(f'question_{question_id}')
                is_correct = selected_answer == correct_answer
                marks_obtained = marks if is_correct else 0
                
                if is_correct:
                    score += marks_obtained
                
                StudentAnswer.create(result_id, question_id, selected_answer, is_correct, marks_obtained)
            
            # Update result with final score
            from app import mysql
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE Result SET Score = %s, Submitted_At = CURRENT_TIMESTAMP WHERE Result_ID = %s", (score, result_id))
            mysql.connection.commit()
            cursor.close()
            
            # Update ranks
            Result.update_rank(quiz_id)
            
            flash('Quiz submitted successfully!', 'success')
            return redirect(url_for('quiz.view_result', result_id=result_id))
        except Exception as e:
            print(f"[TAKE QUIZ] Error: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'Error submitting quiz: {str(e)}', 'danger')
            return redirect(url_for('student.dashboard'))
    
    # Parse JSON options in questions for display
    parsed_questions = []
    if questions:
        import json
        for question in questions:
            question_list = list(question)
            try:
                # question[3] contains the JSON options
                if isinstance(question[3], str):
                    question_list[3] = json.loads(question[3])
                else:
                    question_list[3] = question[3]
            except:
                # If parsing fails, keep original
                pass
            parsed_questions.append(tuple(question_list))
    
    return render_template('student/take_quiz.html', quiz=quiz, questions=parsed_questions)

@quiz_bp.route('result/<int:result_id>', methods=['GET'])
@student_required
def view_result(result_id):
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Result WHERE Result_ID = %s", (result_id,))
    result = cursor.fetchone()
    cursor.close()
    
    if not result or result[1] != session['user_id']:
        flash('Unauthorized', 'danger')
        return redirect(url_for('student.dashboard'))
    
    quiz = Quiz.get_by_id(result[2])
    answers = StudentAnswer.get_by_result(result_id)
    
    return render_template('student/result.html', result=result, quiz=quiz, answers=answers)
