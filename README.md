# Quiz Management System Setup Guide

## Project Overview
A complete Quiz Management System built with Flask and MySQL where:
- **Teachers** can create quizzes, add questions, and view student performance
- **Students** can take quizzes, view their scores, and see leaderboards
- System tracks ranks, scores, and detailed answers

## Prerequisites
1. **XAMPP** - Download from https://www.apachefriends.org/
2. **Python 3.8+** - Download from https://www.python.org/
3. **Git** (optional) - Download from https://git-scm.com/

## Installation Steps

### Step 1: Start XAMPP
1. Open XAMPP Control Panel
2. Click "Start" next to Apache and MySQL
3. Open http://localhost/phpmyadmin in your browser

### Step 2: Create Database
1. In phpMyAdmin, go to "SQL" tab
2. Copy the entire content of `database/quiz_system.sql`
3. Paste it in the SQL editor and execute
4. Verify the database and tables are created

### Step 3: Setup Flask Application
```bash
# Navigate to project directory
cd c:\Users\dskam\Desktop\DBMS\ 2.0\quiz_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Database Connection
Edit `config.py` and update MySQL credentials if needed:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Default XAMPP password is empty
MYSQL_DB = 'quiz_system'
```

### Step 5: Run the Application
```bash
python run.py
```

Application will be available at: **http://localhost:5000**

## Database Schema

### Tables:
1. **Teacher** - Teacher account information
2. **Student** - Student account information
3. **Quiz** - Quiz details created by teachers
4. **Question** - Questions in each quiz with options and correct answers
5. **Result** - Student quiz results and scores
6. **StudentAnswer** - Individual student answers for review

## File Structure
```
quiz_system/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models
│   ├── routes.py            # All routes and logic
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── teacher/
│   │   │   ├── dashboard.html
│   │   │   ├── create_quiz.html
│   │   │   ├── edit_quiz.html
│   │   │   └── view_results.html
│   │   └── student/
│   │       ├── dashboard.html
│   │       ├── start_quiz.html
│   │       ├── take_quiz.html
│   │       ├── result.html
│   │       └── leaderboard.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── database/
│   └── quiz_system.sql      # Database schema
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features

### For Teachers:
- ✅ Create multiple quizzes
- ✅ Add multiple choice questions (A, B, C, D)
- ✅ Set marks per question
- ✅ Set time limit for quiz
- ✅ Activate/Deactivate quizzes
- ✅ View overall performance analytics
- ✅ See student results and rankings

### For Students:
- ✅ Register and login
- ✅ View available quizzes
- ✅ Take quizzes with timer
- ✅ View their scores and percentages
- ✅ See their rank/position
- ✅ View leaderboard for each quiz
- ✅ Review submitted answers

### System Features:
- ✅ Secure password hashing
- ✅ Session management
- ✅ Real-time timer countdown
- ✅ Automatic rank calculation
- ✅ Comprehensive statistics
- ✅ Responsive design with Bootstrap 5

## Default Credentials (After Setup)
You'll need to register new teacher and student accounts first.

## Troubleshooting

### MySQL Connection Error
- Ensure XAMPP MySQL is running
- Check credentials in config.py
- Verify database exists: SELECT * FROM quiz_system.Quiz;

### Module Not Found
```bash
pip install -r requirements.txt
```

### Port 5000 Already in Use
```bash
python run.py --port 5001
```

### Template Not Found
- Ensure templates folder exists at `app/templates`
- Check template file names match exactly

## API Endpoints

### Authentication
- `GET /` - Root redirect
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `POST /logout` - User logout

### Teacher Routes
- `GET /teacher/dashboard` - Teacher dashboard
- `GET/POST /teacher/create-quiz` - Create quiz
- `GET/POST /teacher/edit-quiz/<quiz_id>` - Edit quiz
- `POST /teacher/add-question/<quiz_id>` - Add question
- `GET /teacher/view-results/<quiz_id>` - View results
- `POST /teacher/toggle-quiz/<quiz_id>` - Activate/Deactivate

### Student Routes
- `GET /student/dashboard` - Student dashboard
- `GET /student/leaderboard/<quiz_id>` - View leaderboard

### Quiz Routes
- `GET/POST /quiz/start/<quiz_id>` - Start quiz
- `GET/POST /quiz/take/<quiz_id>` - Take quiz
- `GET /quiz/result/<result_id>` - View result

## Security Notes
- Passwords are hashed using Werkzeug security
- Session management with Flask sessions
- CSRF protection recommended for production
- Change SECRET_KEY in config.py for production

## Future Enhancements
- [ ] Email notifications
- [ ] Quiz scheduling
- [ ] Question banks
- [ ] Random question selection
- [ ] Negative marking
- [ ] Admin dashboard
- [ ] Export results to CSV
- [ ] Two-factor authentication

## Support
For issues or questions, check the database schema and ensure all tables are created properly.

## License
This project is provided as-is for educational purposes.
