from flask import Flask
from flask_cors import CORS
from services.tripplanner.intermodal_trip_planner import load_bike_parking_data, load_car_parking_data

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    from routes import clues, image, guess, journey
    
    app.register_blueprint(clues.bp)
    app.register_blueprint(image.bp)
    app.register_blueprint(guess.bp)
    app.register_blueprint(journey.bp)
    
    return app

app = create_app()

if __name__ == '__main__':
   
    print("� Loading parking data...")
    load_bike_parking_data()
    load_car_parking_data()
    
    print("�🚀 Starting Company Puzzle Competition Game Server...")
    print("📍 Server running at: http://localhost:5000")
    print("📚 API Endpoints:")
    print("   - POST /api/puzzle/clues")
    print("   - POST /api/puzzle/reveal")
    print("   - POST /api/puzzle/guess")
    print("   - POST /api/journeys")
    print("   - GET /api/health")
    print("\n✨ Server is ready! Press CTRL+C to stop.\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
