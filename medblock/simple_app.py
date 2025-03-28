#!/usr/bin/env python3
"""
Simple MedBlock API

A simple Flask API without dependencies on ML models or blueprints
"""

import os
import sys
import logging
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)

# Define a simple health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'name': 'MedBlock Simple API',
        'version': '0.1.0'
    })

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'MedBlock Simple API is running',
        'version': '0.1.0',
        'endpoints': ['/api/health']
    })

# Add dummy ML endpoints
@app.route('/api/fraud/detect', methods=['GET'])
def fraud_detect():
    return jsonify({
        'is_fraud': False,
        'fraud_probability': 0.05,
        'risk_level': 'low'
    })

@app.route('/api/health/predict', methods=['GET'])
def health_predict():
    return jsonify({
        'risk_score': 25,
        'recommendations': [
            'Regular check-ups recommended',
            'Maintain healthy diet and exercise'
        ]
    })

@app.route('/api/records', methods=['GET'])
def get_records():
    return jsonify([
        {'id': 1, 'record_id': 'REC123456', 'record_type': 'Lab Test'},
        {'id': 2, 'record_id': 'REC234567', 'record_type': 'Prescription'}
    ])

if __name__ == "__main__":
    port = 8080
    logger.info(f"Starting simple MedBlock API on port {port}")
    print(f"\nMedBlock Simple API is running at: http://localhost:{port}/\n")
    app.run(host='0.0.0.0', port=port, debug=True) 