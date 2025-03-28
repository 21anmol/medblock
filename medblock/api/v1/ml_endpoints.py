"""
Machine Learning API Endpoints for MedBlock

This module defines the API endpoints for ML model predictions.
"""

import os
import sys
import json
import logging
from flask import Blueprint, request, jsonify, current_app

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

from ml_models.fraud_detection import FraudDetectionModel
from ml_models.health_prediction import HealthPredictionModel
from ml_models.anomaly_detection import AnomalyDetectionModel
from ml_models.model_utils import load_model, save_predictions

# Set up logger
logger = logging.getLogger(__name__)

# Initialize blueprint
ml_blueprint = Blueprint('ml', __name__, url_prefix='/api/v1/ml')

# Initialize models
MODEL_DIR = os.path.join(parent_dir, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

fraud_model_path = os.path.join(MODEL_DIR, 'fraud_detection_model.txt')
healthcare_model_path = os.path.join(MODEL_DIR, 'healthcare_prediction_model.txt')
anomaly_model_path = os.path.join(MODEL_DIR, 'anomaly_detection_model.txt')

# Load models
fraud_model = load_model(FraudDetectionModel, fraud_model_path)
healthcare_model = load_model(HealthPredictionModel, healthcare_model_path)
anomaly_model = load_model(AnomalyDetectionModel, anomaly_model_path)

# Define API endpoints
@ml_blueprint.route('/fraud/detect', methods=['POST'])
def detect_fraud():
    """Endpoint to detect fraud in medical claims"""
    try:
        data = request.json
        logger.info(f"Received fraud detection request")
        
        # Validate input
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid input data'}), 400
        
        # Make prediction
        result = fraud_model.predict(data)
        
        # Log the result
        if result.get('is_fraud', False):
            logger.warning(f"Fraud detected: {json.dumps(result)}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in fraud detection: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/health/predict', methods=['POST'])
def predict_health():
    """Endpoint to predict health conditions and risks"""
    try:
        data = request.json
        logger.info(f"Received health prediction request")
        
        # Validate input
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid input data'}), 400
        
        # Make prediction
        result = healthcare_model.predict(data)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in health prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/anomaly/detect', methods=['POST'])
def detect_anomaly():
    """Endpoint to detect anomalies in access or usage patterns"""
    try:
        data = request.json
        logger.info(f"Received anomaly detection request")
        
        # Validate input
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid input data'}), 400
        
        # Make prediction
        result = anomaly_model.predict(data)
        
        # Log if anomaly detected
        if result.get('is_anomaly', False):
            logger.warning(f"Anomaly detected: {json.dumps(result)}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in anomaly detection: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/fraud/train', methods=['POST'])
def train_fraud_model():
    """Endpoint to train fraud detection model"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        temp_path = os.path.join(os.getcwd(), 'temp_fraud_data.csv')
        file.save(temp_path)
        
        # Train model
        metrics = fraud_model.train(temp_path)
        
        # Save model
        fraud_model.save(fraud_model_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            'message': 'Fraud detection model trained successfully',
            'metrics': metrics
        })
    except Exception as e:
        logger.error(f"Error in training fraud model: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/health/train', methods=['POST'])
def train_health_model():
    """Endpoint to train health prediction model"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        temp_path = os.path.join(os.getcwd(), 'temp_health_data.csv')
        file.save(temp_path)
        
        # Train model
        metrics = healthcare_model.train(temp_path)
        
        # Save model
        healthcare_model.save(healthcare_model_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            'message': 'Health prediction model trained successfully',
            'metrics': metrics
        })
    except Exception as e:
        logger.error(f"Error in training health model: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_blueprint.route('/anomaly/train', methods=['POST'])
def train_anomaly_model():
    """Endpoint to train anomaly detection model"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        temp_path = os.path.join(os.getcwd(), 'temp_anomaly_data.csv')
        file.save(temp_path)
        
        # Train model
        metrics = anomaly_model.train(temp_path)
        
        # Save model
        anomaly_model.save(anomaly_model_path)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            'message': 'Anomaly detection model trained successfully',
            'metrics': metrics
        })
    except Exception as e:
        logger.error(f"Error in training anomaly model: {str(e)}")
        return jsonify({'error': str(e)}), 500 