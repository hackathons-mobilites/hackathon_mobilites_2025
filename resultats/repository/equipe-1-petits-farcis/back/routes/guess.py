"""
Routes for submitting guesses and checking answers.
Endpoint: POST /api/puzzle/guess
"""
from flask import Blueprint, request, jsonify
import logging
from services.images.storage_service import get_correct_answer, record_user_attempt, reveal_full_image
from . import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('guess', __name__, url_prefix='/api/puzzle')

# Maximum attempts per user per day
MAX_DAILY_ATTEMPTS = 3
# Grid size configuration
GRID_SIZE = config.GRID_SIZE 

@bp.route('/guess', methods=['POST'])
def submit_guess():
    """
    Submit a guess for a puzzle.
    Each user has a maximum of 3 attempts per day.
    
    Request Body:
        {
            "user_id": str,
            "company_name": str,
            "puzzle_id": str,
            "guess": str,
            "attempts_left": int
        }
    
    Returns:
        JSON response indicating if guess is correct and remaining attempts
    """
    try:
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['user_id', 'company_name', 'puzzle_id', 'guess', 'attempts_left']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        user_id = data['user_id']
        company_name = data['company_name']
        puzzle_id = data['puzzle_id']
        guess = data['guess'].strip()
        attempts_left = data['attempts_left']
        
        # Validate attempts_left
        if not isinstance(attempts_left, int) or attempts_left < 0:
            return jsonify({
                'status': 'error',
                'message': 'attempts_left must be a non-negative integer'
            }), 400
        
        # Check if user has attempts remaining
        if attempts_left <= 0:
            logger.warning(f"User {user_id} has no attempts left for {puzzle_id}")
            return jsonify({
                'status': 'error',
                'message': 'No attempts remaining for today. Try again tomorrow!',
                'remaining_attempts': 0
            }), 403
        
        # current_attempts = storage_service.get_user_attempts(user_id, company_name, puzzle_id)

        
        # Get the correct answer from puzzle_answers.csv
        correct_answer = get_correct_answer(company_name, puzzle_id)
        
        if not correct_answer:
            return jsonify({
                'status': 'error',
                'message': 'No correct answer set for this puzzle'
            }), 500
        
        # Record the attempt
        record_user_attempt(user_id, company_name, puzzle_id)
        
        # Check if guess is correct (case-insensitive)
        is_correct = guess.lower() == correct_answer.lower()
        # remaining_attempts = MAX_DAILY_ATTEMPTS - (current_attempts + 1)
        remaining_attempts = attempts_left - 1
        
        if is_correct:
            # Reveal the full image for the company when answer is correct
            reveal_full_image(company_name, puzzle_id, GRID_SIZE)
            
            logger.info(f"User {user_id} guessed correctly for {puzzle_id}")
            return jsonify({
                'status': 'correct',
                'message': 'Congratulations! You guessed correctly!',
                'remaining_attempts': remaining_attempts,
                'correct_answer': correct_answer
            }), 200
        else:
            logger.info(f"User {user_id} guessed incorrectly for {puzzle_id}. "
                       f"Attempts left: {remaining_attempts}")
            return jsonify({
                'status': 'wrong',
                'message': 'Incorrect guess. Try again!',
                'remaining_attempts': remaining_attempts
            }), 200
    
    except Exception as e:
        logger.error(f"Error in submit_guess: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500
