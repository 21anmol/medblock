#!/usr/bin/env python3
"""
Minimal MedBlock API 

A minimal Flask API to test if Flask is working correctly
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
        'name': 'MedBlock Minimal API',
        'version': '0.1.0'
    })

# Simple frontend route
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'MedBlock Minimal API is running',
        'version': '0.1.0',
        'endpoints': ['/api/health']
    })

if __name__ == "__main__":
    logger.info("Starting minimal MedBlock API")
    app.run(host='0.0.0.0', port=5000, debug=True) 