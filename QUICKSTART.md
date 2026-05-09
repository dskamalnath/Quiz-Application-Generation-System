# Quick Start Guide for Quiz Management System

## Step-by-Step Setup on Windows (Using XAMPP)

### Prerequisites Checklist:
- [ ] XAMPP installed and running (Apache & MySQL)
- [ ] Python 3.8+ installed
- [ ] Git (optional)

---

## Installation

### 1. Start XAMPP Services
1. Open XAMPP Control Panel
2. Click "Start" for **Apache**
3. Click "Start" for **MySQL**
4. Open `http://localhost/phpmyadmin` in browser

### 2. Create Database
**Option A: Using phpMyAdmin (Easiest)**
1. Go to http://localhost/phpmyadmin
2. Click "SQL" tab at top
3. Open file: `database/quiz_system.sql`
4. Copy entire content
5. Paste in SQL editor
6. Click "Go" button
7. Done! ✓

**Option B: Using Terminal**
```bash
cd quiz_system
python init_db.py
```

### 3. Setup Python Environment
```bash
# Navigate to project
cd c:\Users\dskam\Desktop\DBMS\ 2.0\quiz_system

# Create virtual environment (one time only)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run Application
**Option A: Simple (Windows)**
- Double-click: `setup.bat`

**Option B: Manual**
```bash
python run.py
```

### 5. Access Application
- Open browser: `http://localhost:5000`
- Login page will appear

---

## First Time Usage

### For Teachers:
1. Click **Register**
2. Select **Teacher** as user type
3. Fill in details and register
4. Login with your credentials
5. Go to Dashboard → **Create New Quiz**
6. Add questions and publish quiz

### For Students:
1. Click **Register**
2. Select **Student** as user type
3. Fill in details with your class
4. Login with your credentials
5. Go to Dashboard → **Take Quiz**
6. Complete quiz and view results

---

## Verify Database

In phpMyAdmin, run this query to check tables:
```sql
SHOW TABLES FROM quiz_system;
```

Should show 6 tables:
- Teacher
- Student
- Quiz
- Question
- Result
- StudentAnswer

---

## Troubleshooting

### "Connection refused" Error
```
✗ Check: Is XAMPP MySQL running?
✓ Solution: Start MySQL in XAMPP Control Panel
```

### "Module not found" Error
```
✗ Check: Did you install requirements?
✓ Solution: pip install -r requirements.txt
```

### "Table doesn't exist" Error
```
✗ Check: Did you create database?
✓ Solution: Run database/quiz_system.sql in phpMyAdmin
```

### "Port 5000 already in use"
```
✗ Check: Is app already running?
✓ Solution: Change port in run.py or close existing app
```

### Database Connection Failed
```
Edit config.py and verify:
- MYSQL_HOST = 'localhost'
- MYSQL_USER = 'root'
- MYSQL_PASSWORD = ''
- MYSQL_DB = 'quiz_system'
```

---

## File Structure
```
quiz_system/
├── app/                      # Flask application
│   ├── models.py            # Database operations
│   ├── routes.py            # All routes/views
│   ├── templates/           # HTML files
│   └── static/              # CSS & JavaScript
├── database/
│   └── quiz_system.sql      # Database schema
├── config.py                # Configuration
├── run.py                   # Start application (python run.py)
├── requirements.txt         # Python packages
├── init_db.py              # Initialize database
├── setup.bat               # Windows setup script
└── README.md               # Full documentation
```

---

## Features Overview

### Teacher Dashboard
- Create multiple quizzes
- Add multiple choice questions
- Set time limits and marks
- Activate/deactivate quizzes
- View detailed performance reports
- See student rankings

### Student Dashboard
- List of available quizzes
- Previous quiz results
- Score and percentage tracking
- Rank display

### Quiz Taking
- Timer countdown
- Multiple choice options (A, B, C, D)
- Auto-submit on timer expiry
- Instant scoring

### Leaderboard
- Student rankings
- Comparative scores
- Percentages

---

## Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Run application
python run.py

# Database initialization
python init_db.py

# Deactivate virtual environment
deactivate
```

---

## Testing the Application

### Quick Test Flow:
1. **Register as Teacher**
   - Name: John Teacher
   - Email: john@teacher.com
   - Password: password123

2. **Create a Quiz**
   - Title: Sample Quiz
   - Marks: 10
   - Time: 5 minutes

3. **Add Questions**
   - Add 5 multiple choice questions
   - Mark correct answers

4. **Activate Quiz** (toggle active)

5. **Register as Student**
   - Name: Jane Student
   - Email: jane@student.com
   - Class: Class 10-A

6. **Take Quiz**
   - Answer all questions
   - View score and rank

---

## Database Schema Summary

**Teacher Table**
- Teacher_ID, Name, Email, Password, Created_At

**Student Table**
- Student_ID, Name, Email, Password, Class, Created_At

**Quiz Table**
- Quiz_ID, Teacher_ID, Title, Description, Total_Marks, Time_Limit, Is_Active, Created_At

**Question Table**
- Question_ID, Quiz_ID, Question_Text, Options (JSON), Correct_Answer, Marks

**Result Table**
- Result_ID, Student_ID, Quiz_ID, Score, Rank, Feedback, Attempt_Number, Time_Taken

**StudentAnswer Table**
- Answer_ID, Result_ID, Question_ID, Selected_Answer, Is_Correct, Marks_Obtained

---

## Next Steps

After setup, you can:
- [ ] Create sample quizzes as teacher
- [ ] Test as student
- [ ] Review results
- [ ] Check leaderboards
- [ ] Explore codebase

---

## Support Resources

- **XAMPP**: https://www.apachefriends.org/
- **Python**: https://www.python.org/
- **Flask**: https://flask.palletsprojects.com/
- **MySQL**: https://dev.mysql.com/doc/

---

**Ready to start? Run `setup.bat` (Windows) or `setup.sh` (Mac/Linux)**
