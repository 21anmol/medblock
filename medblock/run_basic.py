"""
Basic MedBlock API Server

This is a minimal Flask application for testing purposes.
"""

from flask import Flask, jsonify

# Create the Flask app
app = Flask(__name__)

# Define a simple health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'name': 'MedBlock Basic API',
        'version': '0.1.0'
    })

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'MedBlock Basic API is running',
        'version': '0.1.0',
        'endpoints': ['/api/health']
    })

if __name__ == "__main__":
    port = 7000
    print(f"\nMedBlock Basic API is running at: http://localhost:{port}/\n")
    app.run(host='0.0.0.0', port=port, debug=True) 