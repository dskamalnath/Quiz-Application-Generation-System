-- Quiz Management System Database Schema
-- MySQL Database

CREATE DATABASE IF NOT EXISTS quiz_system;
USE quiz_system;

-- Teacher Table
CREATE TABLE IF NOT EXISTS Teacher (
    Teacher_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Student Table
CREATE TABLE IF NOT EXISTS Student (
    Student_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Class VARCHAR(50),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quiz Table
CREATE TABLE IF NOT EXISTS Quiz (
    Quiz_ID INT AUTO_INCREMENT PRIMARY KEY,
    Teacher_ID INT NOT NULL,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    Total_Marks INT NOT NULL,
    Time_Limit INT NOT NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Is_Active BOOLEAN DEFAULT TRUE,
    Required_Questions INT DEFAULT 0,
    FOREIGN KEY (Teacher_ID) REFERENCES Teacher(Teacher_ID) ON DELETE CASCADE
);

-- Question Table
CREATE TABLE IF NOT EXISTS Question (
    Question_ID INT AUTO_INCREMENT PRIMARY KEY,
    Quiz_ID INT NOT NULL,
    Question_Text TEXT NOT NULL,
    Options JSON NOT NULL,
    Correct_Answer VARCHAR(255) NOT NULL,
    Marks INT NOT NULL DEFAULT 1,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Quiz_ID) REFERENCES Quiz(Quiz_ID) ON DELETE CASCADE
);

-- Result Table
CREATE TABLE IF NOT EXISTS Result (
    Result_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID INT NOT NULL,
    Quiz_ID INT NOT NULL,
    Score INT NOT NULL DEFAULT 0,
    Rank INT,
    Feedback TEXT,
    Attempt_Number INT DEFAULT 1,
    Submitted_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Time_Taken INT,
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID) ON DELETE CASCADE,
    FOREIGN KEY (Quiz_ID) REFERENCES Quiz(Quiz_ID) ON DELETE CASCADE,
    UNIQUE KEY unique_attempt (Student_ID, Quiz_ID, Attempt_Number)
);

-- Student Attempt Table (for tracking individual answers)
CREATE TABLE IF NOT EXISTS StudentAnswer (
    Answer_ID INT AUTO_INCREMENT PRIMARY KEY,
    Result_ID INT NOT NULL,
    Question_ID INT NOT NULL,
    Selected_Answer VARCHAR(255),
    Is_Correct BOOLEAN,
    Marks_Obtained INT,
    Answered_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Result_ID) REFERENCES Result(Result_ID) ON DELETE CASCADE,
    FOREIGN KEY (Question_ID) REFERENCES Question(Question_ID) ON DELETE CASCADE
);

-- Create Indexes for better performance
CREATE INDEX idx_teacher_email ON Teacher(Email);
CREATE INDEX idx_student_email ON Student(Email);
CREATE INDEX idx_quiz_teacher ON Quiz(Teacher_ID);
CREATE INDEX idx_question_quiz ON Question(Quiz_ID);
CREATE INDEX idx_result_student ON Result(Student_ID);
CREATE INDEX idx_result_quiz ON Result(Quiz_ID);
CREATE INDEX idx_studentanswer_result ON StudentAnswer(Result_ID);
