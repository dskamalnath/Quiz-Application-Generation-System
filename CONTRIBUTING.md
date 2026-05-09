# Contributing to Quiz Management System

Thank you for considering contributing to the Quiz Management System! We appreciate your interest in improving this project.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:
- Using welcoming and inclusive language
- Being respectful of differing opinions, viewpoints, and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## How Can I Contribute?

### 1. Report Bugs 🐛

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**
- **Include your environment details** (OS, Python version, MySQL version)

### 2. Suggest Enhancements 💡

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the expected behavior**
- **Explain why this enhancement would be useful**

### 3. Submit Pull Requests 🔧

Before you begin writing code, please search the pull request list to see if a feature or fix has already been proposed.

#### Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/quiz-system.git
   cd quiz-system
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the coding style guidelines below
   - Write meaningful commit messages
   - Add comments for complex logic

4. **Test Your Changes**
   ```bash
   python -m pytest tests/
   ```

5. **Commit Your Changes**
   ```bash
   git commit -m "Add brief description of changes"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Include screenshots for UI changes

## Development Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/quiz-system.git
cd quiz-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
mysql -u root -p < database/quiz_system.sql

# Run tests
python -m pytest

# Run application
python run.py
```

## Coding Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (not tabs)
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep lines under 100 characters

#### Example:
```python
def calculate_quiz_percentage(total_marks, obtained_marks):
    """
    Calculate quiz percentage for a student.
    
    Args:
        total_marks (int): Total marks of the quiz
        obtained_marks (int): Marks obtained by student
        
    Returns:
        float: Percentage score
    """
    if total_marks == 0:
        return 0
    return (obtained_marks / total_marks) * 100
```

### HTML/CSS Style

- Use lowercase for tag and attribute names
- Use semantic HTML5 elements
- Use CSS classes for styling, avoid inline styles
- Maintain consistent indentation (2 spaces for HTML)
- Add comments for complex CSS rules

#### Example:
```html
<div class="quiz-container">
    <h1 class="quiz-title">{{ quiz.title }}</h1>
    <p class="quiz-description">{{ quiz.description }}</p>
</div>
```

### JavaScript Style

- Use ES6+ features
- Use meaningful variable names
- Add comments for complex logic
- Use const/let instead of var
- Use semicolons consistently

#### Example:
```javascript
const submitQuiz = (quizId) => {
    // Validate quiz completion
    if (!validateQuizCompletion(quizId)) {
        showError('Please answer all questions');
        return;
    }
    
    // Submit quiz data
    submitQuizData(quizId);
};
```

## Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` - Improve structure/format
  - ⚡ `:zap:` - Improve performance
  - 🐛 `:bug:` - Fix bug
  - ✨ `:sparkles:` - New feature
  - 📚 `:books:` - Documentation
  - 🔒 `:lock:` - Security fix
  - ♻️ `:recycle:` - Refactoring

#### Examples:
```
✨ Add student leaderboard feature
🐛 Fix quiz timer not resetting
📚 Update installation documentation
🔒 Add CSRF protection to forms
```

## Pull Request Process

1. **Update documentation** with any new features
2. **Add tests** for new functionality
3. **Ensure all tests pass** before submitting
4. **Update README.md** if you've added new features
5. **Link to any related issues** in the pull request description
6. **Request review** from maintainers
7. **Address feedback** and make requested changes

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_auth.py

# Run with coverage
python -m pytest --cov=app
```

### Writing Tests

Write tests for new features or bug fixes:

```python
import pytest
from app import create_app, mysql

def test_quiz_creation():
    """Test creating a new quiz"""
    app = create_app('testing')
    with app.test_client() as client:
        response = client.post('/teacher/create-quiz', data={
            'title': 'Test Quiz',
            'description': 'Test Description',
            'total_marks': 100,
            'time_limit': 30
        })
        assert response.status_code == 200
```

## Documentation

### Updating Documentation

- Update README.md for major changes
- Add docstrings to all new functions
- Update API routes in DOCUMENTATION.md
- Include examples where helpful

### Documentation Style

```python
def function_name(param1, param2):
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the purpose
    and any important details about the function.
    
    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2
        
    Returns:
        type: Description of return value
        
    Raises:
        ValueError: When certain conditions occur
    """
    pass
```

## Issues and Feature Requests

### Before Submitting

- Check existing issues
- Check pull requests
- Ensure your feature aligns with project goals

### Submitting

1. Use a clear, descriptive title
2. Provide a detailed description
3. Include relevant examples
4. Attach screenshots if applicable

## Questions?

Feel free to open an issue with the `question` label or contact the maintainers.

---

**Thank you for contributing! Together we make this project better! 🎉**
