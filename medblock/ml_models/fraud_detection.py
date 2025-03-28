"""
Fraud Detection Model for MedBlock

This is a placeholder implementation that simulates fraud detection functionality
without requiring actual ML dependencies. In a production environment, this would
be replaced with a real implementation using frameworks like TensorFlow, PyTorch,
or specialized fraud detection libraries.
"""

import os
import logging
import json
import random
import hashlib
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FraudDetectionModel:
    """
    Placeholder implementation of a fraud detection model.
    
    This class simulates the behavior of a machine learning model for detecting
    fraudulent activities in medical records and transactions without requiring
    actual ML dependencies.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the fraud detection model.
        
        Args:
            model_path (str, optional): Path to a saved model file. Defaults to None.
        """
        logger.info("Initialized placeholder fraud detection model")
        self.model_path = model_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models",
            "fraud_detection_model.txt"
        )
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Placeholder model metadata
        self.metadata = {
            "model_type": "fraud_detection",
            "version": "0.1.0",
            "created_at": datetime.now().isoformat(),
            "features": [
                "transaction_amount", "transaction_time", "user_history", 
                "ip_address", "device_info", "location", "access_pattern",
                "record_modification_frequency", "unusual_record_access"
            ],
            "detection_categories": [
                "identity_theft", "unauthorized_access", "record_tampering",
                "billing_fraud", "insurance_fraud", "prescription_fraud"
            ]
        }
        
        # Suspicious patterns (would be learned from data in a real model)
        self.suspicious_patterns = {
            "time_patterns": [
                {"hour_start": 1, "hour_end": 4, "risk_factor": 2.5},  # Late night activity
                {"hour_start": 23, "hour_end": 24, "risk_factor": 1.8}  # Late night activity
            ],
            "frequency_thresholds": {
                "high_access": 15,  # More than 15 accesses in a day is suspicious
                "rapid_modifications": 8  # More than 8 modifications in an hour is suspicious
            },
            "amount_thresholds": {
                "suspicious_min": 8000,  # Amounts above this are somewhat suspicious
                "highly_suspicious": 15000  # Amounts above this are highly suspicious
            }
        }
        
        # Save placeholder model
        self.save()
    
    def detect(self, transaction_data):
        """
        Detect potential fraud in a transaction or activity.
        
        In a real implementation, this would process the input through a trained
        machine learning model. This placeholder returns realistic but deterministic
        fraud detection results based on simple rules.
        
        Args:
            transaction_data (dict): Input data containing transaction or activity details.
            
        Returns:
            dict: Fraud detection results with risk scores and flags.
        """
        logger.info(f"Analyzing transaction for potential fraud: {transaction_data}")
        
        # Validate input data (simplified)
        if not isinstance(transaction_data, dict):
            transaction_data = {}
        
        # Extract relevant features (with defaults)
        amount = transaction_data.get('amount', 0)
        timestamp = transaction_data.get('timestamp', datetime.now().isoformat())
        ip_address = transaction_data.get('ip_address', '')
        user_id = transaction_data.get('user_id', '')
        action_type = transaction_data.get('action_type', 'view')
        record_id = transaction_data.get('record_id', '')
        
        # Generate a transaction hash for tracking
        transaction_hash = self._generate_transaction_hash(transaction_data)
        
        # Base risk score (0-100, higher means more risky)
        base_risk = 5.0  # Start with a low baseline risk
        
        # Apply simple rule-based fraud detection logic
        risk_factors = []
        
        # 1. Check for suspicious amounts
        if amount > self.suspicious_patterns['amount_thresholds']['highly_suspicious']:
            base_risk += 30
            risk_factors.append({
                "factor": "high_transaction_amount",
                "severity": "high",
                "details": f"Transaction amount (${amount}) exceeds highly suspicious threshold"
            })
        elif amount > self.suspicious_patterns['amount_thresholds']['suspicious_min']:
            base_risk += 15
            risk_factors.append({
                "factor": "elevated_transaction_amount",
                "severity": "medium",
                "details": f"Transaction amount (${amount}) exceeds suspicious threshold"
            })
        
        # 2. Check for suspicious timing
        try:
            if isinstance(timestamp, str):
                txn_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                txn_time = timestamp
                
            txn_hour = txn_time.hour
            
            # Check against suspicious time patterns
            for pattern in self.suspicious_patterns['time_patterns']:
                if pattern['hour_start'] <= txn_hour < pattern['hour_end']:
                    base_risk += pattern['risk_factor'] * 5
                    risk_factors.append({
                        "factor": "suspicious_timing",
                        "severity": "medium",
                        "details": f"Activity occurred during suspicious hours ({txn_hour}:00)"
                    })
        except (ValueError, TypeError):
            # If timestamp parsing fails, add a small risk factor
            base_risk += 5
            risk_factors.append({
                "factor": "invalid_timestamp",
                "severity": "low",
                "details": "Transaction contains invalid timestamp format"
            })
        
        # 3. Simulate analysis of access patterns (using hash to make it deterministic)
        hash_value = int(transaction_hash[-6:], 16)  # Take last 6 chars of hash as hex
        
        # If hash value is divisible by 7, simulate detecting a suspicious pattern
        if hash_value % 7 == 0:
            pattern_risk = 25 + (hash_value % 15)
            base_risk += pattern_risk
            risk_factors.append({
                "factor": "unusual_access_pattern",
                "severity": "high",
                "details": "Unusual access pattern detected for this user"
            })
        
        # 4. Check action type (more risk for modifications than views)
        if action_type.lower() in ['modify', 'update', 'delete']:
            base_risk += 10
            risk_factors.append({
                "factor": "sensitive_action",
                "severity": "medium",
                "details": f"Sensitive action performed: {action_type}"
            })
        
        # 5. Simulate IP address reputation check
        if ip_address:
            # Use the IP to generate a deterministic reputation score
            ip_hash = sum(ord(c) for c in ip_address)
            if ip_hash % 10 == 0:  # 10% chance of suspicious IP
                base_risk += 35
                risk_factors.append({
                    "factor": "suspicious_ip",
                    "severity": "high",
                    "details": "IP address associated with suspicious activity"
                })
        
        # Ensure risk score is within bounds
        risk_score = min(max(base_risk, 0), 100)
        
        # Determine risk level category
        risk_level = "low"
        if risk_score >= 75:
            risk_level = "critical"
        elif risk_score >= 50:
            risk_level = "high"
        elif risk_score >= 25:
            risk_level = "medium"
        
        # Generate fraud detection response
        detection_result = {
            "transaction_id": transaction_hash,
            "timestamp": datetime.now().isoformat(),
            "risk_score": round(risk_score, 1),
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "confidence": 0.7 + (len(risk_factors) * 0.05),  # Higher confidence with more risk factors
            "recommendation": self._generate_recommendation(risk_level, risk_factors)
        }
        
        return detection_result
    
    def _generate_recommendation(self, risk_level, risk_factors):
        """
        Generate recommendation based on the risk assessment.
        
        Args:
            risk_level (str): The overall risk level of the transaction.
            risk_factors (list): List of identified risk factors.
            
        Returns:
            dict: A recommendation for handling the transaction.
        """
        recommendations = {
            "low": {
                "action": "allow",
                "message": "Transaction appears normal. No additional verification needed."
            },
            "medium": {
                "action": "verify",
                "message": "Some risk factors detected. Consider additional verification."
            },
            "high": {
                "action": "review",
                "message": "Multiple risk factors detected. Recommend manual review before proceeding."
            },
            "critical": {
                "action": "block",
                "message": "Critical risk level. Block transaction and investigate immediately."
            }
        }
        
        recommendation = recommendations.get(risk_level, recommendations["low"])
        
        # Add specific advice based on risk factors
        if len(risk_factors) > 0:
            factor_types = [f["factor"] for f in risk_factors]
            
            if "suspicious_ip" in factor_types:
                recommendation["additional_steps"] = recommendation.get("additional_steps", [])
                recommendation["additional_steps"].append(
                    "Verify user identity through secondary authentication channel"
                )
            
            if "unusual_access_pattern" in factor_types:
                recommendation["additional_steps"] = recommendation.get("additional_steps", [])
                recommendation["additional_steps"].append(
                    "Review recent access history for this record"
                )
            
            if "high_transaction_amount" in factor_types:
                recommendation["additional_steps"] = recommendation.get("additional_steps", [])
                recommendation["additional_steps"].append(
                    "Confirm transaction details with authorizing party"
                )
        
        return recommendation
    
    def _generate_transaction_hash(self, transaction_data):
        """
        Generate a unique hash for a transaction.
        
        Args:
            transaction_data (dict): Transaction data to hash.
            
        Returns:
            str: A unique hash string for the transaction.
        """
        # Convert transaction data to string
        serialized = json.dumps(transaction_data, sort_keys=True)
        
        # Generate a unique hash
        hash_obj = hashlib.sha256(serialized.encode())
        
        # Return a transaction ID format with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"txn-{timestamp}-{hash_obj.hexdigest()[:12]}"
    
    def analyze_user_behavior(self, user_id, activity_history):
        """
        Analyze user behavior for potential anomalies.
        
        Args:
            user_id (str): The ID of the user to analyze.
            activity_history (list): List of past activities by this user.
            
        Returns:
            dict: User behavior analysis results.
        """
        logger.info(f"Analyzing behavior for user: {user_id}")
        
        # Validate input
        if not activity_history or not isinstance(activity_history, list):
            activity_history = []
        
        # Count activities per type
        activity_counts = {}
        for activity in activity_history:
            activity_type = activity.get('action_type', 'unknown')
            activity_counts[activity_type] = activity_counts.get(activity_type, 0) + 1
        
        # Generate a deterministic anomaly score based on user_id
        user_hash = sum(ord(c) for c in str(user_id))
        anomaly_base = (user_hash % 10) / 10.0
        
        # Adjust based on activity patterns
        anomaly_score = anomaly_base
        
        if len(activity_history) > 0:
            # More varied activity types is generally less suspicious
            unique_actions = len(activity_counts)
            if unique_actions <= 1:
                anomaly_score += 0.2  # Single action type is somewhat suspicious
            
            # Check for high frequency of certain actions
            for action_type, count in activity_counts.items():
                if action_type.lower() in ['delete', 'modify', 'update'] and count > 5:
                    anomaly_score += 0.15  # High frequency of modifications is suspicious
        
        # Normalize to 0-1 range
        anomaly_score = min(max(anomaly_score, 0), 1)
        
        # Generate recommendations based on anomaly score
        if anomaly_score < 0.3:
            recommendation = "Normal user behavior detected. No action required."
        elif anomaly_score < 0.6:
            recommendation = "Some unusual patterns detected. Monitor this user's activity."
        else:
            recommendation = "Significant behavioral anomalies detected. Review account activity."
        
        # Create behavior analysis response
        return {
            "user_id": user_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "anomaly_score": round(anomaly_score, 2),
            "activity_summary": activity_counts,
            "recommendation": recommendation
        }
    
    def save(self, filepath=None):
        """
        Save the model to a file.
        
        In a real implementation, this would serialize the trained model.
        This placeholder creates a text file with model metadata.
        
        Args:
            filepath (str, optional): Path to save the model. Defaults to self.model_path.
            
        Returns:
            str: Path to the saved model file.
        """
        filepath = filepath or self.model_path
        
        # Create a simple text file as a placeholder for the model
        with open(filepath, 'w') as f:
            f.write(f"MedBlock Fraud Detection Model (Placeholder)\n")
            f.write(f"Created: {self.metadata['created_at']}\n")
            f.write(f"Version: {self.metadata['version']}\n\n")
            f.write(f"Features: {', '.join(self.metadata['features'])}\n")
            f.write(f"Detection Categories: {', '.join(self.metadata['detection_categories'])}\n\n")
            f.write("Note: This is a placeholder model file for demonstration purposes.\n")
            f.write("In a production environment, this would be a trained ML model.")
        
        logger.info(f"Saved placeholder model to {filepath}")
        return filepath
    
    def load(self, filepath=None):
        """
        Load a saved model from a file.
        
        In a real implementation, this would deserialize a trained model.
        This placeholder simply checks if the file exists and logs the action.
        
        Args:
            filepath (str, optional): Path to the saved model. Defaults to self.model_path.
            
        Returns:
            bool: True if the model was loaded, False otherwise.
        """
        filepath = filepath or self.model_path
        
        if os.path.exists(filepath):
            logger.info(f"Loaded placeholder model from {filepath}")
            return True
        else:
            logger.warning(f"Model file not found at {filepath}")
            return False


if __name__ == "__main__":
    # Example usage
    model = FraudDetectionModel()
    
    # Example transaction data
    sample_transaction = {
        "user_id": "user-12345",
        "action_type": "modify",
        "record_id": "record-6789",
        "timestamp": datetime.now().isoformat(),
        "ip_address": "192.168.1.1",
        "amount": 12500,
        "details": {
            "modified_fields": ["diagnosis", "prescription"],
            "device_info": "Windows 10, Chrome 96.0.4664.110"
        }
    }
    
    # Detect potential fraud
    result = model.detect(sample_transaction)
    print(json.dumps(result, indent=2))
    
    # Example activity history for user behavior analysis
    activity_history = [
        {"action_type": "view", "timestamp": (datetime.now() - timedelta(days=3)).isoformat()},
        {"action_type": "view", "timestamp": (datetime.now() - timedelta(days=2)).isoformat()},
        {"action_type": "modify", "timestamp": (datetime.now() - timedelta(days=1)).isoformat()},
        {"action_type": "view", "timestamp": datetime.now().isoformat()},
    ]
    
    # Analyze user behavior
    behavior_analysis = model.analyze_user_behavior("user-12345", activity_history)
    print(json.dumps(behavior_analysis, indent=2)) 