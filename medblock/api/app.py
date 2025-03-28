"""
MedBlock API Application (Simplified)

This module initializes and configures the Flask application for MedBlock API.
"""

import os
import sys
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add parent directory to path to import ML models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml_models.fraud_detection import FraudDetectionModel
from ml_models.health_prediction import HealthPredictionModel
from ml_models.anomaly_detection import AnomalyDetectionModel
from ml_models.model_utils import load_model

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Initialize models
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

fraud_model_path = os.path.join(MODEL_DIR, 'fraud_detection_model.txt')
healthcare_model_path = os.path.join(MODEL_DIR, 'healthcare_prediction_model.txt')
anomaly_model_path = os.path.join(MODEL_DIR, 'anomaly_detection_model.txt')

# Load models
fraud_model = load_model(FraudDetectionModel, fraud_model_path)
healthcare_model = load_model(HealthPredictionModel, healthcare_model_path)
anomaly_model = load_model(AnomalyDetectionModel, anomaly_model_path)

# Import API blueprints
from api.v1.ml_endpoints import ml_blueprint
from api.v1.users import users_blueprint
from api.v1.records import records_blueprint

# Register blueprints
app.register_blueprint(ml_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(records_blueprint)

# Define health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    return jsonify({
        'status': 'healthy',
        'name': 'MedBlock',
        'version': '0.1.0',
        'timestamp': datetime.now().isoformat(),
        'models': {
            'fraud_detection': os.path.exists(fraud_model_path),
            'healthcare_prediction': os.path.exists(healthcare_model_path),
            'anomaly_detection': os.path.exists(anomaly_model_path)
        }
    })

# Simple frontend route
@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'MedBlock API is running',
        'version': '0.1.0',
        'api_docs': '/api/health'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 