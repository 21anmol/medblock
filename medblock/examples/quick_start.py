#!/usr/bin/env python3
"""
MedBlock Quick Start Example

This script demonstrates the key features of MedBlock by running through a simple workflow.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_models.fraud_detection import FraudDetectionModel
from ml_models.predictive_healthcare import PredictiveHealthcareModel
from ml_models.anomaly_detection import AnomalyDetectionModel
from blockchain.smart_contracts import BlockchainIntegration
from utils.zero_knowledge import ZeroKnowledgeProof

def create_synthetic_data():
    """Create synthetic data for demonstration"""
    print("\n=== Creating Synthetic Data ===")
    
    # Create directory for data
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    print(f"Storing data in {data_dir}")
    
    # 1. Healthcare data
    np.random.seed(42)
    n_samples = 1000
    
    # Generate health metrics
    health_data = pd.DataFrame({
        'age': np.random.randint(18, 85, size=n_samples),
        'gender': np.random.choice(['M', 'F'], size=n_samples),
        'bmi': np.random.normal(26, 5, size=n_samples),
        'systolic_bp': np.random.normal(125, 15, size=n_samples),
        'diastolic_bp': np.random.normal(80, 10, size=n_samples),
        'heart_rate': np.random.normal(75, 10, size=n_samples),
        'glucose': np.random.normal(100, 20, size=n_samples),
        'cholesterol': np.random.normal(190, 35, size=n_samples),
        'hdl': np.random.normal(55, 15, size=n_samples),
        'ldl': np.random.normal(115, 30, size=n_samples),
        'triglycerides': np.random.normal(150, 50, size=n_samples),
        'smoking_status': np.random.choice(['never', 'former', 'current'], size=n_samples),
        'alcohol_consumption': np.random.choice(['none', 'light', 'moderate', 'heavy'], size=n_samples),
        'physical_activity': np.random.choice(['low', 'moderate', 'high'], size=n_samples),
        'family_history': np.random.choice([0, 1], size=n_samples)
    })
    
    # Generate disease risk based on age, bmi, blood pressure, etc.
    health_data['risk_score'] = (
        (health_data['age'] - 18) / 67 +  # Age factor
        (health_data['bmi'] - 18.5) / 17 +  # BMI factor
        (health_data['systolic_bp'] - 90) / 60 +  # Systolic BP factor
        (health_data['glucose'] - 70) / 80 +  # Glucose factor
        (health_data['smoking_status'] == 'current') * 0.5 +  # Smoking factor
        (health_data['physical_activity'] == 'low') * 0.3 +  # Lack of exercise
        (health_data['family_history']) * 0.4  # Family history
    ) / 5.0  # Normalize
    
    # Convert to disease risk category (0: Low, 1: Medium, 2: High)
    health_data['disease_risk'] = pd.cut(
        health_data['risk_score'], 
        bins=[-float('inf'), 0.3, 0.6, float('inf')], 
        labels=[0, 1, 2]
    ).astype(int)
    
    health_data.drop('risk_score', axis=1, inplace=True)
    
    # Save to CSV
    health_data_path = os.path.join(data_dir, 'health_data.csv')
    health_data.to_csv(health_data_path, index=False)
    print(f"Created healthcare dataset with {n_samples} samples")
    
    # 2. Insurance claims data for fraud detection
    n_claims = 1000
    
    # Generate providers
    n_providers = 20
    provider_ids = [f"PROV{i:03d}" for i in range(1, n_providers+1)]
    
    # Generate patients
    n_patients = 100
    patient_ids = [f"PAT{i:03d}" for i in range(1, n_patients+1)]
    
    # Generate procedure codes
    procedure_codes = [f"PROC{i:03d}" for i in range(1, 51)]
    
    # Generate diagnosis codes
    diagnosis_codes = [f"DIAG{i:03d}" for i in range(1, 31)]
    
    # Generate normal claims
    claims_data = pd.DataFrame({
        'provider_id': np.random.choice(provider_ids, size=n_claims),
        'patient_id': np.random.choice(patient_ids, size=n_claims),
        'claim_id': [f"CLM{i:05d}" for i in range(1, n_claims+1)],
        'claim_amount': np.random.normal(500, 200, size=n_claims),
        'procedure_code': np.random.choice(procedure_codes, size=n_claims),
        'diagnosis_code': np.random.choice(diagnosis_codes, size=n_claims),
        'service_date': pd.date_range(start='2023-01-01', periods=n_claims),
        'billing_date': None,
        'is_fraud': 0
    })
    
    # Add billing date (typically a few days after service)
    claims_data['billing_date'] = claims_data['service_date'] + pd.to_timedelta(np.random.randint(1, 14, size=n_claims), unit='d')
    
    # Insert fraudulent patterns (5% of claims)
    fraud_count = int(n_claims * 0.05)
    fraud_indices = np.random.choice(n_claims, fraud_count, replace=False)
    
    # Fraud pattern 1: Unusually high claim amounts
    amount_fraud = fraud_indices[:fraud_count//3]
    claims_data.loc[amount_fraud, 'claim_amount'] = np.random.normal(1500, 300, size=len(amount_fraud))
    
    # Fraud pattern 2: Billing date much later than service date
    date_fraud = fraud_indices[fraud_count//3:2*fraud_count//3]
    claims_data.loc[date_fraud, 'billing_date'] = claims_data.loc[date_fraud, 'service_date'] + pd.to_timedelta(np.random.randint(60, 120, size=len(date_fraud)), unit='d')
    
    # Fraud pattern 3: Unusual procedure/diagnosis combinations
    combo_fraud = fraud_indices[2*fraud_count//3:]
    claims_data.loc[combo_fraud, 'procedure_code'] = "PROC999"
    claims_data.loc[combo_fraud, 'diagnosis_code'] = "DIAG999"
    
    # Mark fraudulent claims
    claims_data.loc[fraud_indices, 'is_fraud'] = 1
    
    # Save to CSV
    claims_data_path = os.path.join(data_dir, 'claims_data.csv')
    claims_data.to_csv(claims_data_path, index=False)
    print(f"Created insurance claims dataset with {n_claims} claims ({fraud_count} fraudulent)")
    
    # 3. Access logs for anomaly detection
    n_logs = 1000
    
    # Generate users
    n_users = 50
    user_ids = [f"USER{i:03d}" for i in range(1, n_users+1)]
    
    # Generate resources
    n_resources = 200
    resource_ids = [f"RES{i:04d}" for i in range(1, n_resources+1)]
    
    # Generate normal access patterns
    access_logs = pd.DataFrame({
        'user_id': np.random.choice(user_ids, size=n_logs),
        'resource_id': np.random.choice(resource_ids, size=n_logs),
        'action_type': np.random.choice(['view', 'edit', 'download'], size=n_logs, p=[0.7, 0.2, 0.1]),
        'device_type': np.random.choice(['desktop', 'mobile', 'tablet'], size=n_logs, p=[0.6, 0.3, 0.1]),
        'ip_address': np.random.randint(1, 255, size=n_logs).astype(str) + "." + 
                      np.random.randint(1, 255, size=n_logs).astype(str) + "." + 
                      np.random.randint(1, 255, size=n_logs).astype(str) + "." + 
                      np.random.randint(1, 255, size=n_logs).astype(str),
        'session_duration': np.random.normal(300, 100, size=n_logs),  # seconds
        'bytes_transferred': np.random.normal(5000, 1000, size=n_logs),
        'success': np.random.choice([0, 1], p=[0.05, 0.95], size=n_logs),
        'is_anomaly': 0
    })
    
    # Generate timestamps (mostly during business hours)
    base_time = datetime(2023, 1, 1)
    
    # Generate random hour offsets centered around 2 PM (14:00)
    hour_offsets = np.random.normal(14, 4, size=n_logs)
    # Clip to mostly business hours
    hour_offsets = np.clip(hour_offsets, 8, 18)
    
    # Generate random day offsets within a month
    day_offsets = np.random.randint(0, 30, size=n_logs)
    
    # Create timestamps
    timestamps = [
        base_time + timedelta(days=int(d), hours=int(h)) 
        for d, h in zip(day_offsets, hour_offsets)
    ]
    access_logs['timestamp'] = timestamps
    
    # Insert anomalous patterns (5% of logs)
    anomaly_count = int(n_logs * 0.05)
    anomaly_indices = np.random.choice(n_logs, anomaly_count, replace=False)
    
    # Anomaly type 1: Unusual access hours
    time_anomalies = anomaly_indices[:anomaly_count//3]
    for idx in time_anomalies:
        # Set to early morning hours (midnight to 5 AM)
        access_logs.loc[idx, 'timestamp'] = access_logs.loc[idx, 'timestamp'].replace(hour=np.random.randint(0, 5))
    
    # Anomaly type 2: Unusual resource access patterns
    resource_anomalies = anomaly_indices[anomaly_count//3:2*anomaly_count//3]
    access_logs.loc[resource_anomalies, 'resource_id'] = [f"RES{i:04d}" for i in range(9000, 9000 + len(resource_anomalies))]
    
    # Anomaly type 3: Unusual session behavior
    session_anomalies = anomaly_indices[2*anomaly_count//3:]
    access_logs.loc[session_anomalies, 'session_duration'] = np.random.normal(3000, 500, size=len(session_anomalies))
    access_logs.loc[session_anomalies, 'bytes_transferred'] = np.random.normal(50000, 10000, size=len(session_anomalies))
    
    # Mark anomalous access
    access_logs.loc[anomaly_indices, 'is_anomaly'] = 1
    
    # Save to CSV
    access_logs_path = os.path.join(data_dir, 'access_logs.csv')
    access_logs.to_csv(access_logs_path, index=False)
    print(f"Created access logs dataset with {n_logs} entries ({anomaly_count} anomalous)")
    
    return {
        'health_data': health_data_path,
        'claims_data': claims_data_path,
        'access_logs': access_logs_path
    }

def train_and_test_ml_models(data_paths):
    """Train and test machine learning models"""
    print("\n=== Training and Testing ML Models ===")
    
    # Create directory for models
    models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Train and test fraud detection model
    print("\n1. Fraud Detection Model")
    fraud_model = FraudDetectionModel()
    fraud_metrics = fraud_model.train(data_paths['claims_data'])
    print(f"Model accuracy: {fraud_metrics['accuracy']:.4f}")
    
    # Save model
    fraud_model_path = os.path.join(models_dir, 'fraud_detection_model.pkl')
    fraud_model.save(fraud_model_path)
    
    # Test prediction on a sample
    claims_data = pd.read_csv(data_paths['claims_data'])
    # Get one fraudulent and one legitimate claim
    fraud_sample = claims_data[claims_data['is_fraud'] == 1].iloc[0].drop('is_fraud').to_dict()
    legit_sample = claims_data[claims_data['is_fraud'] == 0].iloc[0].drop('is_fraud').to_dict()
    
    fraud_prediction = fraud_model.predict(fraud_sample)
    legit_prediction = fraud_model.predict(legit_sample)
    
    print(f"Fraudulent claim prediction: {fraud_prediction}")
    print(f"Legitimate claim prediction: {legit_prediction}")
    
    # 2. Train and test healthcare prediction model
    print("\n2. Healthcare Prediction Model")
    healthcare_model = PredictiveHealthcareModel()
    # Use fewer epochs for demonstration
    healthcare_metrics = healthcare_model.train(data_paths['health_data'], epochs=5, batch_size=32)
    print(f"Model accuracy: {healthcare_metrics['accuracy']:.4f}")
    
    # Save model
    healthcare_model_path = os.path.join(models_dir, 'healthcare_prediction_model.h5')
    healthcare_model.save(healthcare_model_path)
    
    # Test prediction on a sample
    health_data = pd.read_csv(data_paths['health_data'])
    # Get samples for each risk level
    low_risk_sample = health_data[health_data['disease_risk'] == 0].iloc[0].drop('disease_risk').to_dict()
    high_risk_sample = health_data[health_data['disease_risk'] == 2].iloc[0].drop('disease_risk').to_dict()
    
    low_risk_prediction = healthcare_model.predict(low_risk_sample)
    high_risk_prediction = healthcare_model.predict(high_risk_sample)
    
    print(f"Low risk patient prediction: {low_risk_prediction}")
    print(f"High risk patient prediction: {high_risk_prediction}")
    
    # 3. Train and test anomaly detection model
    print("\n3. Anomaly Detection Model")
    anomaly_model = AnomalyDetectionModel()
    anomaly_metrics = anomaly_model.train(data_paths['access_logs'])
    print(f"Anomaly detection results: {anomaly_metrics}")
    
    # Save model
    anomaly_model_path = os.path.join(models_dir, 'anomaly_detection_model.pkl')
    anomaly_model.save(anomaly_model_path)
    
    # Test prediction on a sample
    access_logs = pd.read_csv(data_paths['access_logs'])
    # Get one anomalous and one normal access
    anomaly_sample = access_logs[access_logs['is_anomaly'] == 1].iloc[0].to_dict()
    normal_sample = access_logs[access_logs['is_anomaly'] == 0].iloc[0].to_dict()
    
    anomaly_prediction = anomaly_model.predict(anomaly_sample)
    normal_prediction = anomaly_model.predict(normal_sample)
    
    print(f"Anomalous access prediction: {anomaly_prediction}")
    print(f"Normal access prediction: {normal_prediction}")
    
    return {
        'fraud_model': fraud_model_path,
        'healthcare_model': healthcare_model_path,
        'anomaly_model': anomaly_model_path
    }

def demo_blockchain_integration():
    """Demonstrate blockchain integration for storing medical records"""
    print("\n=== Blockchain Integration Demo ===")
    print("Note: This demo simulates blockchain operations without a real blockchain network")
    
    # Initialize blockchain integration
    blockchain = BlockchainIntegration(
        provider_url=None,  # Simulated mode
        keyfile="demo_encryption_key.key"
    )
    
    # Create sample medical record
    patient_id = "PAT001"
    record_id = "REC001"
    
    medical_record = {
        "patient_name": "John Smith",
        "date_of_birth": "1980-05-15",
        "blood_type": "A+",
        "allergies": ["Penicillin", "Peanuts"],
        "diagnoses": [
            {"condition": "Hypertension", "date": "2022-10-12"},
            {"condition": "Type 2 Diabetes", "date": "2022-10-12"}
        ],
        "medications": [
            {"name": "Lisinopril", "dosage": "10mg", "frequency": "Once daily"},
            {"name": "Metformin", "dosage": "500mg", "frequency": "Twice daily"}
        ],
        "vital_signs": {
            "blood_pressure": "130/85",
            "heart_rate": 78,
            "temperature": 98.6,
            "respiratory_rate": 16
        }
    }
    
    # Encrypt the medical record
    print("\nEncrypting medical record...")
    encrypted_data = blockchain.encrypt(json.dumps(medical_record))
    print(f"Original record: {json.dumps(medical_record, indent=2)}")
    print(f"Encrypted record (excerpt): {encrypted_data[:50]}...")
    
    # Decrypt the medical record
    print("\nDecrypting medical record...")
    decrypted_data = blockchain.decrypt(encrypted_data)
    decrypted_record = json.loads(decrypted_data)
    print(f"Decrypted record matches original: {decrypted_record == medical_record}")
    
    # Demonstrate zero-knowledge proof for access control
    print("\nDemonstrating Zero-Knowledge Proof for access control...")
    
    # Create a ZKP instance
    zkp = ZeroKnowledgeProof(key_directory="demo_keys")
    
    # Generate keys for demonstration
    patient_private, patient_public = zkp.generate_key_pair("patient001")
    doctor_private, doctor_public = zkp.generate_key_pair("doctor001")
    hospital_private, hospital_public = zkp.generate_key_pair("hospital001")
    
    # List of authorized doctors
    authorized_doctors = ["doctor001", "doctor002"]
    
    # Hospital creates a proof that doctor001 is authorized to access patient001's records
    auth_proof = zkp.create_zkp_for_medical_authorization(
        "patient001", "doctor001", "record001", authorized_doctors, hospital_private
    )
    
    # Doctor verifies the authorization
    is_authorized = zkp.verify_zkp_for_medical_authorization(auth_proof, hospital_public)
    print(f"Doctor is authorized to access patient's record: {is_authorized}")
    
    # Try with unauthorized doctor
    unauthorized_proof = zkp.create_zkp_for_medical_authorization(
        "patient001", "doctor003", "record001", authorized_doctors, hospital_private
    )
    
    if unauthorized_proof is None:
        print("Proof creation failed for unauthorized doctor (as expected)")
    
    return True

def main():
    """Main function for the quick start example"""
    print("\nMedBlock Quick Start Example")
    print("============================\n")
    
    print("This script demonstrates the key features of MedBlock by:")
    print("1. Creating synthetic data for healthcare predictions, fraud detection, and anomaly detection")
    print("2. Training and testing machine learning models on this data")
    print("3. Demonstrating blockchain integration for secure medical record storage")
    print("4. Demonstrating zero-knowledge proofs for privacy-preserving access control\n")
    
    # Create synthetic data
    data_paths = create_synthetic_data()
    
    # Train and test ML models
    model_paths = train_and_test_ml_models(data_paths)
    
    # Demo blockchain integration
    demo_blockchain_integration()
    
    print("\n=== Quick Start Complete ===")
    print("You have successfully demonstrated the core features of MedBlock!")
    print("\nNext steps:")
    print("1. Start the API server: python medblock/api/app.py")
    print("2. Start the frontend: cd medblock/frontend && npm start")
    print("3. Explore the codebase to understand how all components work together")

if __name__ == "__main__":
    main() 