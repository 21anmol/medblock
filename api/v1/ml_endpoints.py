"""
Machine Learning API Endpoints for MedBlock

This module defines the API endpoints for interacting with ML models.
"""

import os
import sys
import json
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml_models.fraud_detection import FraudDetectionModel
from ml_models.predictive_healthcare import PredictiveHealthcareModel
from ml_models.anomaly_detection import AnomalyDetectionModel
from utils.database import log_record_access
from config.config import MODELS_DIR

# Set up logger
logger = logging.getLogger(__name__)

# Initialize blueprint
ml_blueprint = Blueprint('ml', __name__, url_prefix='/api/v1/ml')

# Initialize models
def get_models():
    """Get or initialize the ML models"""
    if not hasattr(current_app, 'ml_models'):
        try:
            # Define model paths
            fraud_model_path = os.path.join(MODELS_DIR, 'fraud_detection_model.pkl')
            healthcare_model_path = os.path.join(MODELS_DIR, 'healthcare_prediction_model.h5')
            anomaly_model_path = os.path.join(MODELS_DIR, 'anomaly_detection_model.pkl')
            
            # Initialize models
            current_app.ml_models = {
                'fraud': FraudDetectionModel(model_path=fraud_model_path if os.path.exists(fraud_model_path) else None),
                'healthcare': PredictiveHealthcareModel(model_path=healthcare_model_path if os.path.exists(healthcare_model_path) else None),
                'anomaly': AnomalyDetectionModel(model_path=anomaly_model_path if os.path.exists(anomaly_model_path) else None)
            }
            logger.info("ML models initialized")
        except Exception as e:
            logger.error(f"Error initializing ML models: {str(e)}")
            current_app.ml_models = {}
    
    return current_app.ml_models

# Define API endpoints
@ml_blueprint.route('/fraud/detect', methods=['POST'])
def detect_fraud():
    """Detect fraud in medical claims"""
    try:
        models = get_models()
        if 'fraud' not in models:
            return jsonify({'error': 'Fraud detection model not initialized'}), 500
        
        # Get request data
        data = request.json
        logger.info(f"Received fraud detection request: {json.dumps(data)}")
        
        # Validate input
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid input data'}), 400
        
        # Make prediction
        result = models['fraud'].predict(data)
        
        # Log the result
        logger.info(f"Fraud detection result: {json.dumps(result)}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in fraud detection: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/healthcare/predict', methods=['POST'])
def predict_health():
    """Predict healthcare outcomes"""
    try:
        models = get_models()
        if 'healthcare' not in models:
            return jsonify({'error': 'Healthcare prediction model not initialized'}), 500
        
        # Get request data
        data = request.json
        logger.info(f"Received healthcare prediction request")
        
        # Validate input
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid input data'}), 400
        
        # Make prediction
        result = models['healthcare'].predict(data)
        
        # Log the result
        logger.info(f"Healthcare prediction result: {json.dumps(result)}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in healthcare prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/access/analyze', methods=['POST'])
def analyze_access():
    """Detect anomalies in access patterns"""
    try:
        models = get_models()
        if 'anomaly' not in models:
            return jsonify({'error': 'Anomaly detection model not initialized'}), 500
        
        # Get request data
        data = request.json
        logger.info(f"Received access analysis request")
        
        # Validate input
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid input data'}), 400
        
        # Make prediction
        result = models['anomaly'].predict(data)
        
        # Record the access with anomaly score
        try:
            if 'record_id' in data and 'user_id' in data:
                log_record_access(
                    record_id=data['record_id'],
                    user_id=data['user_id'],
                    action=data.get('action', 'view'),
                    ip_address=data.get('ip_address'),
                    user_agent=data.get('user_agent'),
                    is_authorized=not result['is_anomaly'],
                    anomaly_score=result['anomaly_score']
                )
        except Exception as log_error:
            logger.error(f"Error logging access: {str(log_error)}")
        
        # Log the result if anomaly detected
        if result['is_anomaly']:
            logger.warning(f"Access anomaly detected: {json.dumps(result)}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in anomaly detection: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/fraud/train', methods=['POST'])
def train_fraud_model():
    """Train fraud detection model"""
    try:
        models = get_models()
        if 'fraud' not in models:
            return jsonify({'error': 'Fraud detection model not initialized'}), 500
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_fraud_data.csv')
        file.save(temp_path)
        
        # Train model
        metrics = models['fraud'].train(temp_path)
        
        # Save model
        model_path = os.path.join(MODELS_DIR, 'fraud_detection_model.pkl')
        models['fraud'].save(model_path)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify({
            'message': 'Fraud detection model trained successfully',
            'metrics': metrics
        })
    except Exception as e:
        logger.error(f"Error in training fraud model: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/healthcare/train', methods=['POST'])
def train_healthcare_model():
    """Train healthcare prediction model"""
    try:
        models = get_models()
        if 'healthcare' not in models:
            return jsonify({'error': 'Healthcare prediction model not initialized'}), 500
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get parameters
        epochs = int(request.form.get('epochs', 50))
        batch_size = int(request.form.get('batch_size', 32))
        
        # Save file temporarily
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_healthcare_data.csv')
        file.save(temp_path)
        
        # Train model
        metrics = models['healthcare'].train(temp_path, epochs=epochs, batch_size=batch_size)
        
        # Save model
        model_path = os.path.join(MODELS_DIR, 'healthcare_prediction_model.h5')
        models['healthcare'].save(model_path)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify({
            'message': 'Healthcare prediction model trained successfully',
            'metrics': metrics
        })
    except Exception as e:
        logger.error(f"Error in training healthcare model: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/access/train', methods=['POST'])
def train_anomaly_model():
    """Train anomaly detection model"""
    try:
        models = get_models()
        if 'anomaly' not in models:
            return jsonify({'error': 'Anomaly detection model not initialized'}), 500
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_access_data.csv')
        file.save(temp_path)
        
        # Train model
        metrics = models['anomaly'].train(temp_path)
        
        # Save model
        model_path = os.path.join(MODELS_DIR, 'anomaly_detection_model.pkl')
        models['anomaly'].save(model_path)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify({
            'message': 'Anomaly detection model trained successfully',
            'metrics': metrics
        })
    except Exception as e:
        logger.error(f"Error in training anomaly model: {str(e)}")
        return jsonify({'error': str(e)}), 500 