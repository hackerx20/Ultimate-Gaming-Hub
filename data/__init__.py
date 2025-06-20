__version__ = "1.0.0"
__author__ = "Ultimate Gaming Platform"

# Initialize data variables
questions = []
options = []
correct_answers = []

# Import data components
try:
    from .Questions import questions
    from .Options import options  
    from .CorrectAnswer import correct_answers
    DATA_LOADED = True
except ImportError as e:
    print(f"Warning: Could not load data files: {e}")
    DATA_LOADED = False

# Data file paths
DATA_FILES = {
    'questions': 'Questions.py',
    'options': 'Options.py', 
    'answers': 'CorrectAnswer.py',
    'scores': 'scores.json',
    'statistics': 'statistics.json',
    'achievements': 'achievements.json'
}

def get_data_status():
    """Get the status of data loading"""
    return {
        'loaded': DATA_LOADED,
        'files': DATA_FILES
    }

def validate_quiz_data():
    """Validate that quiz data is properly loaded"""
    if not DATA_LOADED:
        return False, "Data files not loaded"
    
    try:
        # Check if data exists and has length
        if not hasattr(Questions, '__len__') or not hasattr(Options, '__len__') or not hasattr(CorrectAnswer, '__len__'):
            return False, "Data objects don't support length operations"
        
        questions_len = len(Questions)
        options_len = len(Options)
        answers_len = len(CorrectAnswer)
        
        if questions_len != options_len or questions_len != answers_len:
            return False, f"Mismatched data lengths: Questions({questions_len}), Options({options_len}), Answers({answers_len})"
        
        if questions_len == 0:
            return False, "No data loaded"
        
        return True, f"Data validated: {questions_len} questions loaded"
    except Exception as e:
        return False, f"Validation error: {e}"