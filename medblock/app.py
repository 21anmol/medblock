import os
import json
import logging
import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import ML models
try:
    from ml_models.fraud_detection import FraudDetectionModel
    from ml_models.health_prediction import HealthPredictionModel
    from ml_models.anomaly_detection import AnomalyDetectionModel
    ML_IMPORTS_SUCCESS = True
except ImportError:
    ML_IMPORTS_SUCCESS = False
    logging.warning("ML models could not be imported. Using mock implementations.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock user database (would be replaced with a real database)
USERS_DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'users.json')
os.makedirs(os.path.dirname(USERS_DB_FILE), exist_ok=True)

if not os.path.exists(USERS_DB_FILE):
    with open(USERS_DB_FILE, 'w') as f:
        json.dump({
            "users": [
                {
                    "id": "demo-user",
                    "name": "Emily Johnson",
                    "email": "emily.johnson@example.com",
                    "role": "Patient",
                    "avatar": "https://randomuser.me/api/portraits/women/44.jpg"
                }
            ]
        }, f, indent=2)

# Mock medical records database
RECORDS_DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'records.json')
if not os.path.exists(RECORDS_DB_FILE):
    with open(RECORDS_DB_FILE, 'w') as f:
        json.dump({
            "records": [
                {
                    "id": "rec-001",
                    "user_id": "demo-user",
                    "title": "Annual Checkup",
                    "type": "Examination",
                    "date": "2023-05-15",
                    "provider": "Dr. Sarah Williams",
                    "facility": "City Hospital",
                    "notes": "Patient is in good health. Blood pressure normal. Recommended routine blood work.",
                    "attachments": [],
                    "blockchain_hash": "0x7f83b1..."
                },
                {
                    "id": "rec-002",
                    "user_id": "demo-user",
                    "title": "Blood Test Results",
                    "type": "Laboratory",
                    "date": "2023-06-03",
                    "provider": "Dr. Sarah Williams",
                    "facility": "City Hospital Lab",
                    "notes": "All blood work within normal ranges. Slight elevation in cholesterol.",
                    "attachments": [],
                    "blockchain_hash": "0x3a9e8c..."
                },
                {
                    "id": "rec-003",
                    "user_id": "demo-user",
                    "title": "X-Ray Images",
                    "type": "Imaging",
                    "date": "2023-08-15",
                    "provider": "Dr. Michael Wilson",
                    "facility": "MedLab Inc.",
                    "notes": "Chest X-ray shows no abnormalities. Lungs clear.",
                    "attachments": [],
                    "blockchain_hash": "0x8f4d21..."
                }
            ]
        }, f, indent=2)

# Initialize ML models
if ML_IMPORTS_SUCCESS:
    try:
        fraud_model = FraudDetectionModel()
        health_model = HealthPredictionModel()
        anomaly_model = AnomalyDetectionModel()
        logger.info("ML models initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing ML models: {str(e)}")
        ML_IMPORTS_SUCCESS = False

# Mock ML model implementations if imports failed
if not ML_IMPORTS_SUCCESS:
    class MockModel:
        def predict(self, data):
            return {"prediction": "mock_prediction", "confidence": 0.85}
    
    fraud_model = MockModel()
    health_model = MockModel()
    anomaly_model = MockModel()
    logger.info("Using mock ML models")

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_users():
    with open(USERS_DB_FILE, 'r') as f:
        return json.load(f)

def get_user(user_id):
    users_data = get_users()
    for user in users_data["users"]:
        if user["id"] == user_id:
            return user
    return None

def get_records():
    with open(RECORDS_DB_FILE, 'r') as f:
        return json.load(f)

def get_user_records(user_id):
    records_data = get_records()
    return [record for record in records_data["records"] if record["user_id"] == user_id]

def save_record(record):
    records_data = get_records()
    records_data["records"].append(record)
    with open(RECORDS_DB_FILE, 'w') as f:
        json.dump(records_data, f, indent=2)
    return record

def generate_blockchain_hash():
    """Mock function to generate a blockchain hash"""
    import random
    import string
    prefix = "0x"
    hash_string = ''.join(random.choices(string.hexdigits, k=6))
    return f"{prefix}{hash_string}..."

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is working"""
    return jsonify({
        "status": "ok",
        "message": "MedBlock API is operational",
        "ml_models": "active" if ML_IMPORTS_SUCCESS else "mock",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Mock login endpoint - in real implementation this would verify credentials"""
    data = request.json
    if not data or 'principalId' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    # In a real app, we would validate credentials
    # For demo, we'll return the demo user
    user = get_user("demo-user")
    if user:
        return jsonify({
            "success": True,
            "user": user
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/users/profile', methods=['GET'])
def get_user_profile():
    """Get user profile information"""
    # In a real app, we would get the user ID from the auth token
    # For demo, we'll return the demo user
    user = get_user("demo-user")
    if user:
        # Add some stats
        records = get_user_records(user["id"])
        user_data = user.copy()
        user_data["stats"] = {
            "total_records": len(records),
            "providers": len(set(record["provider"] for record in records)),
            "recent_activity": "2023-09-01"
        }
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/records', methods=['GET'])
def get_all_records():
    """Get all records for the authenticated user"""
    # In a real app, we would get the user ID from the auth token
    user_id = request.args.get('user_id', 'demo-user')
    records = get_user_records(user_id)
    return jsonify({"records": records})

@app.route('/api/records/<record_id>', methods=['GET'])
def get_record(record_id):
    """Get a specific record by ID"""
    records_data = get_records()
    for record in records_data["records"]:
        if record["id"] == record_id:
            return jsonify(record)
    return jsonify({"error": "Record not found"}), 404

@app.route('/api/records', methods=['POST'])
def create_record():
    """Create a new medical record"""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    # Create a new record
    record_id = f"rec-{len(get_records()['records']) + 1:03d}"
    new_record = {
        "id": record_id,
        "user_id": data.get("user_id", "demo-user"),
        "title": data.get("title", "New Record"),
        "type": data.get("type", "Other"),
        "date": data.get("date", datetime.datetime.now().strftime("%Y-%m-%d")),
        "provider": data.get("provider", ""),
        "facility": data.get("facility", ""),
        "notes": data.get("notes", ""),
        "attachments": [],
        "blockchain_hash": generate_blockchain_hash()
    }
    
    saved_record = save_record(new_record)
    return jsonify({"success": True, "record": saved_record}), 201

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload a file attachment for a medical record"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    record_id = request.form.get('record_id')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # In a real app, we would update the record with the file attachment
        # and potentially store the file on a secure storage service
        
        return jsonify({
            "success": True,
            "filename": filename,
            "path": file_path,
            "record_id": record_id
        })
    
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/api/ml/fraud/detect', methods=['POST'])
def detect_fraud():
    """Endpoint for fraud detection using ML model"""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    try:
        # Process data through fraud detection model
        result = fraud_model.predict(data)
        
        # In a real app, we would log this activity and potentially alert
        # if fraud is detected
        
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in fraud detection: {str(e)}")
        return jsonify({"error": "Error processing fraud detection"}), 500

@app.route('/api/ml/health/predict', methods=['POST'])
def predict_health():
    """Endpoint for health prediction using ML model"""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    try:
        # Process data through health prediction model
        result = health_model.predict(data)
        
        # Add some demo health insights
        insights = [
            {
                "type": "risk_factor",
                "name": "Cardiovascular Risk",
                "value": 15,
                "description": "Based on your recent records, your cardiovascular risk is below average."
            },
            {
                "type": "recommendation",
                "name": "Exercise",
                "value": "Moderate",
                "description": "Recommended 150 minutes of moderate exercise weekly."
            },
            {
                "type": "trend",
                "name": "Cholesterol",
                "value": "Stable",
                "description": "Your cholesterol levels have remained stable over the past year."
            }
        ]
        
        return jsonify({
            "success": True,
            "result": result,
            "insights": insights,
            "timestamp": datetime.datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in health prediction: {str(e)}")
        return jsonify({"error": "Error processing health prediction"}), 500

@app.route('/api/ml/anomaly/detect', methods=['POST'])
def detect_anomaly():
    """Endpoint for anomaly detection in medical records using ML model"""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    try:
        # Process data through anomaly detection model
        result = anomaly_model.predict(data)
        
        # Add some demo anomalies
        if float(result.get('confidence', 0)) > 0.7:
            anomalies = [
                {
                    "type": "data_gap",
                    "severity": "low",
                    "description": "Missing vaccination records from 2020-2021."
                }
            ]
        else:
            anomalies = []
        
        return jsonify({
            "success": True,
            "result": result,
            "anomalies": anomalies,
            "timestamp": datetime.datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in anomaly detection: {str(e)}")
        return jsonify({"error": "Error processing anomaly detection"}), 500

@app.route('/api/blockchain/verify', methods=['POST'])
def verify_blockchain():
    """Endpoint to verify a record's blockchain hash"""
    data = request.json
    if not data or 'hash' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    # In a real app, we would verify the hash against the blockchain
    # For demo, we'll always return success
    
    return jsonify({
        "success": True,
        "verified": True,
        "hash": data['hash'],
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/blockchain/access-log', methods=['GET'])
def get_access_log():
    """Get blockchain access log for a user"""
    # In a real app, we would query the blockchain for access logs
    # For demo, we'll return mock data
    
    mock_logs = [
        {
            "timestamp": "2023-09-01 10:23:45",
            "entity": "Dr. Sarah Chen",
            "action": "View",
            "record": "Blood Test Results",
            "ip_address": "192.168.1.45",
            "status": "Authorized"
        },
        {
            "timestamp": "2023-08-28 14:15:22",
            "entity": "MedLab Inc.",
            "action": "Upload",
            "record": "X-Ray Images",
            "ip_address": "203.45.67.89",
            "status": "Completed"
        },
        {
            "timestamp": "2023-08-25 09:12:33",
            "entity": "Unknown",
            "action": "Access",
            "record": "Patient History",
            "ip_address": "78.90.123.45",
            "status": "Denied"
        }
    ]
    
    return jsonify({"logs": mock_logs})

# Serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path == "" or path == "/":
        return send_from_directory(app.static_folder, 'index.html')
    elif os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='MedBlock API Server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    # Print banner
    print(r"""
    __  ___         __ ____  __         __  
   /  |/  /__ ___ _/ // __ )/ /___  ___/ /__
  / /|_/ / -_) _ `/ // __  / // _ \/ _  / -_)
 /_/  /_/\__/\_,_/_//____/_/ \___/\_,_/\__/ 
 
 Decentralized Healthcare Record System (with ML Integration)
 
 Version: 0.2.0
 Mode: Development
    """)
    
    logger.info(f"Starting MedBlock API server on port {args.port}")
    app.run(host='0.0.0.0', port=args.port, debug=args.debug) 