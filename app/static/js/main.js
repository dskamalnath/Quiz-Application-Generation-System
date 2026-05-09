// Main JavaScript for Quiz System

console.log('Quiz System Loaded');

// Utility function to show alerts
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
}

// Format time in MM:SS format
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// Confirm before leaving quiz page
window.addEventListener('beforeunload', function(e) {
    const quizForm = document.getElementById('quizForm');
    if (quizForm && !document.body.classList.contains('quiz-submitted')) {
        e.preventDefault();
        e.returnValue = '';
    }
});

// Toggle quiz status
function toggleQuiz(quizId) {
    if (confirm('Are you sure you want to toggle this quiz status?')) {
        fetch(`/teacher/toggle-quiz/${quizId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Quiz status updated successfully!', 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                showAlert('Failed to update quiz status', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred', 'danger');
        });
    }
}

// Add event listener for form submissions
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add any pre-submission validation here
        });
    });
});

// Keyboard shortcut to submit quiz (Ctrl+Enter)
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        const quizForm = document.getElementById('quizForm');
        if (quizForm) {
            if (confirm('Submit quiz?')) {
                quizForm.submit();
            }
        }
    }
});
