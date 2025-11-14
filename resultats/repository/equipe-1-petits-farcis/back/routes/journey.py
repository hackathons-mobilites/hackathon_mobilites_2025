"""
Routes for calculating journeys with gifts.
Endpoints: 
    - POST /api/journeys
    - GET /api/health
"""
from flask import Blueprint, request, jsonify
import logging
from services.tripplanner.trip_planner import calculate_journeys_with_gifts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('journey', __name__, url_prefix='/api')

@bp.route('/journeys', methods=['POST'])
def get_journeys():
    """
    Calculate journeys with gifts based on the provided parameters.
    
    Request Body:
        {
            "from": {"lon": "2.33792", "lat": "48.85827"},
            "to": {"lon": "2.3588523", "lat": "48.9271087"},
            "datetime": "20251121T073000"
        }
    
    Returns:
        JSON response with journey information including gifts
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400
        
        from_location = data.get('from')
        to_location = data.get('to')
        datetime = data.get('datetime')
        
        if not from_location or not to_location or not datetime:
            return jsonify({
                "error": "Missing required fields: 'from', 'to', and 'datetime' are required"
            }), 400
        
        # Validate from_location format
        if not isinstance(from_location, dict) or 'lon' not in from_location or 'lat' not in from_location:
            return jsonify({
                "error": "'from' must be an object with 'lon' and 'lat' properties"
            }), 400
        
        # Validate to_location format
        if not isinstance(to_location, dict) or 'lon' not in to_location or 'lat' not in to_location:
            return jsonify({
                "error": "'to' must be an object with 'lon' and 'lat' properties"
            }), 400
        
        # Calculate journeys
        logger.info(f"Calculating journeys from {from_location} to {to_location} at {datetime}")
        journeys = calculate_journeys_with_gifts(from_location, to_location, datetime)
        
        if journeys is None:
            return jsonify({
                "error": "Failed to calculate journeys. Please check your parameters."
            }), 500
        
        logger.info(f"Successfully calculated {len(journeys)} journeys")
        return jsonify({
            "success": True,
            "journeys": journeys
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_journeys: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500


@bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the server is running.
    
    Returns:
        JSON response with server status
    """
    return jsonify({
        "status": "healthy",
        "service": "Company Puzzle Competition Game Server"
    }), 200
