#!/usr/bin/env python3
"""
MedBlock System Runner (Simplified)

This script initializes and runs the basic MedBlock API with placeholder ML models.
No blockchain or heavy ML dependencies required.
"""

import os
import sys
import logging
import argparse
import time
from threading import Thread

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_api_server(port=5000, debug=False):
    """Run the Flask API server"""
    try:
        from flask import Flask, jsonify
        from flask_cors import CORS
        
        # Import API blueprints
        from api.v1.ml_endpoints import ml_blueprint
        from api.v1.users import users_blueprint
        from api.v1.records import records_blueprint
        
        # Create app
        app = Flask(__name__)
        
        # Set up CORS
        CORS(app, resources={r"/api/*": {"origins": "*"}})
        
        # Register blueprints
        app.register_blueprint(ml_blueprint)
        app.register_blueprint(users_blueprint)
        app.register_blueprint(records_blueprint)
        
        # Add a health check endpoint
        @app.route('/api/health', methods=['GET'])
        def health_check():
            return jsonify({
                'status': 'ok',
                'name': 'MedBlock',
                'version': '0.1.0'
            })
        
        # Serve frontend if available
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve_frontend(path):
            frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'build')
            if os.path.exists(frontend_dir):
                from flask import send_from_directory
                if path and os.path.exists(os.path.join(frontend_dir, path)):
                    return send_from_directory(frontend_dir, path)
                else:
                    return send_from_directory(frontend_dir, 'index.html')
            else:
                return jsonify({
                    'message': 'MedBlock API is running. Frontend is not built yet.'
                })
                
        logger.info(f"Starting API server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=debug)
    except ImportError as e:
        logger.error(f"Error importing Flask dependencies: {str(e)}")
        logger.error("Please install required packages: pip install flask flask-cors")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting API server: {str(e)}")


def initialize_ml_models():
    """Initialize machine learning models (simplified placeholder versions)"""
    from ml_models.fraud_detection import FraudDetectionModel
    from ml_models.health_prediction import HealthPredictionModel
    from ml_models.anomaly_detection import AnomalyDetectionModel
    
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    logger.info("Initializing machine learning models (placeholder versions)")
    
    models = {
        'fraud': None,
        'healthcare': None,
        'anomaly': None
    }
    
    # Initialize fraud detection model
    try:
        fraud_model_path = os.path.join(model_dir, 'fraud_detection_model.txt')
        models['fraud'] = FraudDetectionModel(model_path=fraud_model_path)
        models['fraud'].save(fraud_model_path)
        logger.info("Initialized fraud detection model (placeholder)")
    except Exception as e:
        logger.error(f"Error initializing fraud detection model: {str(e)}")
    
    # Initialize healthcare prediction model
    try:
        healthcare_model_path = os.path.join(model_dir, 'healthcare_prediction_model.txt')
        models['healthcare'] = HealthPredictionModel(model_path=healthcare_model_path)
        models['healthcare'].save(healthcare_model_path)
        logger.info("Initialized healthcare prediction model (placeholder)")
    except Exception as e:
        logger.error(f"Error initializing healthcare prediction model: {str(e)}")
    
    # Initialize anomaly detection model
    try:
        anomaly_model_path = os.path.join(model_dir, 'anomaly_detection_model.txt')
        models['anomaly'] = AnomalyDetectionModel(model_path=anomaly_model_path)
        models['anomaly'].save(anomaly_model_path)
        logger.info("Initialized anomaly detection model (placeholder)")
    except Exception as e:
        logger.error(f"Error initializing anomaly detection model: {str(e)}")
    
    return models


def print_banner():
    """Print application banner"""
    banner = """
    __  ___         __ ____  __         __  
   /  |/  /__ ___ _/ // __ )/ /___  ___/ /__
  / /|_/ / -_) _ `/ // __  / // _ \\/ _  / -_)
 /_/  /_/\\__/\\_,_/_//____/_/ \\___/\\_,_/\\__/ 
 
 Decentralized Healthcare Record System (Simplified)
 
 Version: 0.1.0
 Mode: Development with placeholder models
    """
    print(banner)


def main():
    """Main function to run the API system with placeholder ML models"""
    parser = argparse.ArgumentParser(description='Run the MedBlock system (simplified)')
    parser.add_argument('--port', type=int, default=5000, help='Port for the API server')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    print_banner()
    
    logger.info("Starting MedBlock system (simplified version)")
    
    # Initialize ML models
    models = initialize_ml_models()
    
    # Start API server
    run_api_server(port=args.port, debug=args.debug)
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 