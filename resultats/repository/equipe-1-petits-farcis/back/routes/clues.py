"""
Routes for storing and updating puzzle clues.
Endpoint: POST /api/puzzle/clues
"""
from flask import Blueprint, request, jsonify
import logging
from services.images.storage_service import save_puzzle_clues
from . import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('clues', __name__, url_prefix='/api/puzzle')
GRID_SIZE = config.GRID_SIZE 

@bp.route('/clues', methods=['POST'])
def store_clues():
    """
    Store or update puzzle clues count for a company.
    
    Request Body:
        {
            "company_name": str,
            "puzzle_id": str,
            "nbr_of_unlocked_tiles": int
        }
    
    Returns:
        JSON response with simple message
    """
    try:
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'message': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['company_name', 'puzzle_id', 'nbr_of_unlocked_tiles']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        company_name = data['company_name']
        puzzle_id = data['puzzle_id']
        nbr_of_unlocked_tiles = data['nbr_of_unlocked_tiles']
        
        # Validate data types
        if not isinstance(nbr_of_unlocked_tiles, int) or nbr_of_unlocked_tiles < 0:
            return jsonify({
                'message': 'nbr_of_unlocked_tiles must be a non-negative integer'
            }), 400
        
        # Save puzzle data
        success = save_puzzle_clues(
            company_name=company_name,
            puzzle_id=puzzle_id,
            nbr_of_unlocked_tiles=nbr_of_unlocked_tiles,
            grid_size=GRID_SIZE
        )
        
        if success:
            logger.info(f"Clues saved for {company_name} - {puzzle_id}: {nbr_of_unlocked_tiles} tiles")
            return jsonify({
                'message': 'Clues saved successfully'
            }), 200
        else:
            return jsonify({
                'message': 'Failed to save clues'
            }), 500
    
    except Exception as e:
        logger.error(f"Error in store_clues: {e}")
        return jsonify({
            'message': f'Internal server error: {str(e)}'
        }), 500
