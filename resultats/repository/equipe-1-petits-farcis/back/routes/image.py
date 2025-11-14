"""
Routes for generating revealed images with tile-based reveals.
Endpoint: POST /api/puzzle/reveal
"""
from flask import Blueprint, request, jsonify
import logging
from services.images.storage_service import get_puzzle_data
import base64
import os
from PIL import Image
import io

from services.images.image_service import create_revealed_image_from_puzzle
from . import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('image', __name__, url_prefix='/api/puzzle')

GRID_SIZE = config.GRID_SIZE 

@bp.route('/reveal', methods=['POST'])
def reveal_image():
    """
    Generate a revealed image based on collected clues.
    Unrevealed tiles are covered with black boxes.
    
    Request Body:
        {
            "company_name": str,
            "puzzle_id": str
        }
    
    Returns:
        JSON response with revealed image in base64 format
    """
    try:
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'message': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['company_name', 'puzzle_id']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        company_name = data['company_name']
        puzzle_id = data['puzzle_id']
        
        # Retrieve puzzle data
        puzzle_data = get_puzzle_data(company_name, puzzle_id)
        
        if not puzzle_data:
            return jsonify({
                'message': f'Puzzle not found for company "{company_name}" with ID "{puzzle_id}"'
            }), 404
        
        # Get unrevealed tiles (tiles still covered with black boxes)
        unrevealed_tiles = puzzle_data.get('unrevealed_tiles', [])
        
        # Generate revealed image using the puzzle_id as image filename
        # The image should be stored in app/data/images/ folder
        image_filename = f"{puzzle_id}.jpg"  # Assuming images are named after puzzle_id
        
        result = create_revealed_image_from_puzzle(
            image_source=image_filename,
            unrevealed_tiles=unrevealed_tiles,
            grid_size=GRID_SIZE
        )
        
        logger.info(f"Generated revealed image for {company_name} - {puzzle_id}: "
                   f"{result['revealed_tiles']}/{result['total_tiles']} tiles")
        
        # Decode base64 image
        b64_string = result['revealed_image_b64']
        # Remove data URL prefix if present
        if b64_string.startswith('data:image'):
            b64_string = b64_string.split(',', 1)[1]
        # Add padding if necessary (valid padding only for remainder 2 or 3)
        missing_padding = len(b64_string) % 4
        if missing_padding == 2:
            b64_string += '=='
        elif missing_padding == 3:
            b64_string += '='
        
        image_data = base64.b64decode(b64_string)
        
        # Open image with PIL to crop bottom and right pixels
        img = Image.open(io.BytesIO(image_data))
        width, height = img.size
        
        # Calculate tile dimensions and crop to exact grid dimensions
        tile_width = width // GRID_SIZE
        tile_height = height // GRID_SIZE
        cropped_width = tile_width * GRID_SIZE
        cropped_height = tile_height * GRID_SIZE
        
        # Crop to remove extra pixels at bottom and right
        img_cropped = img.crop((0, 0, cropped_width, cropped_height))
        
        # Convert cropped image back to base64
        buffered = io.BytesIO()
        img_cropped.save(buffered, format="JPEG")
        cropped_image_data = buffered.getvalue()
        cropped_b64 = base64.b64encode(cropped_image_data).decode('utf-8')
        
        # Save the cropped revealed image to storage
        revealed_image_filename = f"{puzzle_id}_revealed.jpg"
        revealed_image_path = f"data/images/{revealed_image_filename}"
        os.makedirs(os.path.dirname(revealed_image_path), exist_ok=True)
        
        with open(revealed_image_path, 'wb') as f:
            f.write(cropped_image_data)

        logger.info(f"Saved revealed image to {revealed_image_path}")
        
        return jsonify({
            'revealed_image_b64': f'data:image/jpeg;base64,{cropped_b64}'
        }), 200
    
    except ValueError as e:
        logger.error(f"Validation error in reveal_image: {e}")
        return jsonify({
            'message': str(e)
        }), 400
    
    except Exception as e:
        logger.error(f"Error in reveal_image: {e}")
        return jsonify({
            'message': f'Internal server error: {str(e)}'
        }), 500
