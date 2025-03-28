"""
Anomaly Detection Model for MedBlock

This is a placeholder implementation that simulates anomaly detection functionality
without requiring actual ML dependencies. In a production environment, this would
be replaced with a real implementation using frameworks like TensorFlow, PyTorch,
or specialized anomaly detection libraries.
"""

import os
import logging
import json
import random
import math
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnomalyDetectionModel:
    """
    Placeholder implementation of an anomaly detection model.
    
    This class simulates the behavior of a machine learning model for detecting
    anomalies in medical data without requiring actual ML dependencies.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the anomaly detection model.
        
        Args:
            model_path (str, optional): Path to a saved model file. Defaults to None.
        """
        logger.info("Initialized placeholder anomaly detection model")
        self.model_path = model_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models",
            "anomaly_detection_model.txt"
        )
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Placeholder model metadata
        self.metadata = {
            "model_type": "anomaly_detection",
            "version": "0.1.0",
            "created_at": datetime.now().isoformat(),
            "features": [
                "heart_rate", "blood_pressure", "temperature", "respiratory_rate",
                "oxygen_saturation", "glucose_level", "white_blood_cell_count",
                "red_blood_cell_count", "hemoglobin", "platelets"
            ],
            "detection_categories": [
                "vital_sign_anomaly", "lab_result_anomaly", "medication_response_anomaly",
                "treatment_outcome_anomaly", "diagnostic_inconsistency"
            ]
        }
        
        # Reference ranges for common medical metrics
        self.reference_ranges = {
            "heart_rate": {"min": 60, "max": 100, "unit": "bpm"},
            "systolic_bp": {"min": 90, "max": 120, "unit": "mmHg"},
            "diastolic_bp": {"min": 60, "max": 80, "unit": "mmHg"},
            "temperature": {"min": 36.1, "max": 37.2, "unit": "°C"},
            "respiratory_rate": {"min": 12, "max": 20, "unit": "breaths/min"},
            "oxygen_saturation": {"min": 95, "max": 100, "unit": "%"},
            "glucose_level": {"min": 70, "max": 100, "unit": "mg/dL"},
            "white_blood_cell_count": {"min": 4.5, "max": 11.0, "unit": "×10^9/L"},
            "red_blood_cell_count": {"min": 4.5, "max": 5.9, "unit": "×10^12/L"},
            "hemoglobin": {"min": 13.5, "max": 17.5, "unit": "g/dL"},
            "platelets": {"min": 150, "max": 450, "unit": "×10^9/L"}
        }
        
        # Save placeholder model
        self.save()
    
    def detect_anomalies(self, medical_data):
        """
        Detect anomalies in medical data.
        
        In a real implementation, this would process the input through a trained
        machine learning model. This placeholder returns realistic but rule-based
        anomaly detection results.
        
        Args:
            medical_data (dict): Input data containing medical metrics.
            
        Returns:
            dict: Anomaly detection results with anomaly scores and details.
        """
        logger.info(f"Detecting anomalies in medical data: {medical_data}")
        
        # Validate input data (simplified)
        if not isinstance(medical_data, dict):
            medical_data = {}
        
        # Track all detected anomalies
        anomalies = []
        
        # Get patient context (if available)
        patient_age = medical_data.get('patient_age', random.randint(30, 70))
        patient_gender = medical_data.get('patient_gender', random.choice(['male', 'female']))
        patient_history = medical_data.get('patient_history', [])
        
        # Analyze each metric against reference ranges
        for metric, value in medical_data.items():
            # Skip non-medical metrics or non-numeric values
            if (metric not in self.reference_ranges or 
                not isinstance(value, (int, float))):
                continue
                
            ref_range = self.reference_ranges[metric]
            min_val, max_val = ref_range["min"], ref_range["max"]
            
            # Check if the value is outside the reference range
            if value < min_val or value > max_val:
                deviation_percent = (
                    (value - min_val) / min_val * 100 if value < min_val else
                    (value - max_val) / max_val * 100
                )
                
                severity = "low"
                if abs(deviation_percent) > 30:
                    severity = "high"
                elif abs(deviation_percent) > 15:
                    severity = "medium"
                
                anomalies.append({
                    "metric": metric,
                    "value": value,
                    "reference_range": f"{min_val}-{max_val} {ref_range['unit']}",
                    "deviation_percent": round(deviation_percent, 1),
                    "severity": severity,
                    "description": self._generate_anomaly_description(
                        metric, value, min_val, max_val, severity
                    )
                })
        
        # Look for correlation anomalies (simplified)
        if ('heart_rate' in medical_data and 
            'respiratory_rate' in medical_data and 
            medical_data['heart_rate'] > 100 and 
            medical_data['respiratory_rate'] < 12):
            
            anomalies.append({
                "type": "correlation_anomaly",
                "metrics": ["heart_rate", "respiratory_rate"],
                "values": [medical_data['heart_rate'], medical_data['respiratory_rate']],
                "severity": "medium",
                "description": "Elevated heart rate with low respiratory rate is an unusual combination"
            })
        
        # Check for temporal anomalies if historical data is available
        if 'historical_readings' in medical_data and isinstance(medical_data['historical_readings'], list):
            for metric in self.reference_ranges.keys():
                if metric in medical_data and len(medical_data['historical_readings']) >= 3:
                    temporal_anomaly = self._check_temporal_anomaly(
                        metric, medical_data[metric], medical_data['historical_readings']
                    )
                    if temporal_anomaly:
                        anomalies.append(temporal_anomaly)
        
        # Calculate an overall anomaly score (0-100)
        anomaly_score = min(len(anomalies) * 15, 100)
        if len(anomalies) > 0:
            # Increase score based on severity
            severity_factor = sum(
                3 if a.get('severity') == 'high' else
                2 if a.get('severity') == 'medium' else 1
                for a in anomalies
            ) / len(anomalies)
            anomaly_score = min(anomaly_score * severity_factor, 100)
        
        # Generate health recommendations based on anomalies
        recommendations = self._generate_recommendations(anomalies, patient_age, patient_gender)
        
        # Create anomaly detection response
        result = {
            "analysis_id": f"anom-{random.randint(1000, 9999)}",
            "timestamp": datetime.now().isoformat(),
            "anomaly_score": round(anomaly_score, 1),
            "anomaly_level": (
                "critical" if anomaly_score >= 70 else
                "significant" if anomaly_score >= 40 else
                "moderate" if anomaly_score >= 20 else
                "minor" if anomaly_score > 0 else "normal"
            ),
            "detected_anomalies": anomalies,
            "recommendations": recommendations,
            "confidence": 0.7 + (random.random() * 0.25)  # Simulated confidence score
        }
        
        return result
    
    def _check_temporal_anomaly(self, metric, current_value, historical_readings):
        """
        Check for sudden changes in a metric compared to historical values.
        
        Args:
            metric (str): The name of the metric.
            current_value (float): The current value of the metric.
            historical_readings (list): List of historical readings.
            
        Returns:
            dict or None: Temporal anomaly information if detected, None otherwise.
        """
        # Extract historical values for this metric
        historical_values = []
        for reading in historical_readings:
            if isinstance(reading, dict) and metric in reading:
                historical_values.append(reading[metric])
        
        if len(historical_values) < 2:
            return None
            
        # Calculate average and standard deviation
        avg_value = sum(historical_values) / len(historical_values)
        std_dev = math.sqrt(sum((x - avg_value) ** 2 for x in historical_values) / len(historical_values))
        
        # Calculate z-score (how many standard deviations from the mean)
        z_score = (current_value - avg_value) / (std_dev if std_dev > 0 else 1)
        
        # If z-score magnitude is greater than 2.5, consider it an anomaly
        if abs(z_score) > 2.5:
            direction = "increase" if z_score > 0 else "decrease"
            percent_change = abs((current_value - avg_value) / avg_value * 100)
            
            return {
                "type": "temporal_anomaly",
                "metric": metric,
                "current_value": current_value,
                "average_value": round(avg_value, 2),
                "percent_change": round(percent_change, 1),
                "z_score": round(z_score, 2),
                "direction": direction,
                "severity": "high" if abs(z_score) > 4 else "medium",
                "description": f"Abnormal {direction} in {metric} compared to patient's history"
            }
            
        return None
    
    def _generate_anomaly_description(self, metric, value, min_val, max_val, severity):
        """
        Generate a human-readable description of an anomaly.
        
        Args:
            metric (str): The name of the metric.
            value (float): The observed value.
            min_val (float): The minimum reference value.
            max_val (float): The maximum reference value.
            severity (str): The anomaly severity.
            
        Returns:
            str: A description of the anomaly.
        """
        formatted_metric = metric.replace('_', ' ')
        
        if value < min_val:
            if severity == "high":
                return f"Critically low {formatted_metric}"
            else:
                return f"{formatted_metric.capitalize()} below normal range"
        else:
            if severity == "high":
                return f"Critically elevated {formatted_metric}"
            else:
                return f"{formatted_metric.capitalize()} above normal range"
    
    def _generate_recommendations(self, anomalies, patient_age, patient_gender):
        """
        Generate recommendations based on detected anomalies.
        
        Args:
            anomalies (list): Detected anomalies.
            patient_age (int): Patient's age.
            patient_gender (str): Patient's gender.
            
        Returns:
            list: Recommendations for addressing the anomalies.
        """
        if not anomalies:
            return [
                {
                    "type": "general",
                    "priority": "low",
                    "description": "No anomalies detected. Continue regular health monitoring."
                }
            ]
        
        recommendations = []
        
        # Check for high severity anomalies
        high_severity = any(a.get('severity') == 'high' for a in anomalies)
        if high_severity:
            recommendations.append({
                "type": "medical",
                "priority": "high",
                "description": "Seek immediate medical attention to address critical readings."
            })
        
        # Check for specific metrics and provide relevant recommendations
        metrics = [a.get('metric') for a in anomalies]
        
        if 'heart_rate' in metrics or 'systolic_bp' in metrics or 'diastolic_bp' in metrics:
            recommendations.append({
                "type": "cardiovascular",
                "priority": "medium",
                "description": "Monitor cardiovascular health closely and consult with cardiologist."
            })
            
        if 'glucose_level' in metrics:
            recommendations.append({
                "type": "metabolic",
                "priority": "medium",
                "description": "Schedule follow-up tests to monitor glucose levels. Consider endocrinology consultation."
            })
            
        if 'white_blood_cell_count' in metrics or 'red_blood_cell_count' in metrics or 'hemoglobin' in metrics:
            recommendations.append({
                "type": "hematology",
                "priority": "medium",
                "description": "Follow up with hematologist to address abnormal blood cell counts."
            })
        
        # Always include a general recommendation
        if len(recommendations) == 0 or not high_severity:
            recommendations.append({
                "type": "general",
                "priority": "medium",
                "description": "Schedule follow-up appointment to monitor these abnormal readings."
            })
        
        # Add age-specific recommendations for older patients
        if patient_age > 65 and ('heart_rate' in metrics or 'systolic_bp' in metrics):
            recommendations.append({
                "type": "geriatric",
                "priority": "medium",
                "description": "Consider geriatric cardiology evaluation for age-appropriate treatment options."
            })
        
        return recommendations
    
    def analyze_historical_trends(self, patient_id, metric_history):
        """
        Analyze historical trends in patient metrics.
        
        Args:
            patient_id (str): The ID of the patient.
            metric_history (dict): Dictionary of metrics with historical values.
            
        Returns:
            dict: Analysis of historical trends.
        """
        logger.info(f"Analyzing historical trends for patient: {patient_id}")
        
        if not isinstance(metric_history, dict):
            return {
                "patient_id": patient_id,
                "analysis_timestamp": datetime.now().isoformat(),
                "error": "Invalid metric history format"
            }
        
        trends = []
        
        # Analyze each metric's history
        for metric, history in metric_history.items():
            if not isinstance(history, list) or len(history) < 3:
                continue
                
            # Ensure history is in chronological order
            try:
                sorted_history = sorted(history, key=lambda x: x.get("timestamp", ""))
                values = [h.get("value") for h in sorted_history if "value" in h]
                
                if len(values) < 3:
                    continue
                    
                # Calculate simple linear regression
                n = len(values)
                x = list(range(n))
                mean_x = sum(x) / n
                mean_y = sum(values) / n
                
                # Calculate slope (m) and y-intercept (b)
                numerator = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
                denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
                
                slope = numerator / denominator if denominator != 0 else 0
                intercept = mean_y - slope * mean_x
                
                # Calculate rate of change (% change over the entire period)
                first_value = values[0]
                last_value = values[-1]
                percent_change = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0
                
                # Determine trend direction and significance
                trend_direction = "stable"
                if percent_change > 10:
                    trend_direction = "increasing"
                elif percent_change < -10:
                    trend_direction = "decreasing"
                
                significance = "minor"
                if abs(percent_change) > 30:
                    significance = "significant"
                elif abs(percent_change) > 15:
                    significance = "moderate"
                
                # Check if the trend crosses reference range boundaries
                crosses_boundary = False
                if metric in self.reference_ranges:
                    min_val = self.reference_ranges[metric]["min"]
                    max_val = self.reference_ranges[metric]["max"]
                    
                    was_within_range = min_val <= first_value <= max_val
                    is_within_range = min_val <= last_value <= max_val
                    
                    if was_within_range != is_within_range:
                        crosses_boundary = True
                
                trends.append({
                    "metric": metric,
                    "direction": trend_direction,
                    "significance": significance,
                    "percent_change": round(percent_change, 1),
                    "slope": round(slope, 4),
                    "first_value": first_value,
                    "last_value": last_value,
                    "crosses_reference_boundary": crosses_boundary,
                    "analysis": self._generate_trend_analysis(metric, trend_direction, significance, crosses_boundary)
                })
                
            except (TypeError, ValueError, KeyError) as e:
                logger.warning(f"Error analyzing trend for {metric}: {str(e)}")
                continue
        
        # Generate overall assessment
        concerning_trends = [t for t in trends if t["significance"] != "minor" or t["crosses_reference_boundary"]]
        
        overall_assessment = "No concerning trends identified."
        if len(concerning_trends) > 0:
            if any(t["significance"] == "significant" for t in concerning_trends):
                overall_assessment = "Significant concerning trends identified that require medical attention."
            else:
                overall_assessment = "Some concerning trends identified that should be monitored."
        
        return {
            "patient_id": patient_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "trends": trends,
            "overall_assessment": overall_assessment
        }
    
    def _generate_trend_analysis(self, metric, direction, significance, crosses_boundary):
        """
        Generate a human-readable analysis of a trend.
        
        Args:
            metric (str): The metric name.
            direction (str): The trend direction.
            significance (str): The trend significance.
            crosses_boundary (bool): Whether the trend crosses a reference boundary.
            
        Returns:
            str: A human-readable analysis of the trend.
        """
        formatted_metric = metric.replace('_', ' ')
        
        if direction == "stable":
            return f"{formatted_metric.capitalize()} has remained stable."
            
        concern_level = ""
        if crosses_boundary:
            concern_level = "concerning"
        elif significance == "significant":
            concern_level = "significant"
        elif significance == "moderate":
            concern_level = "notable"
            
        if concern_level:
            return f"{formatted_metric.capitalize()} shows a {concern_level} {direction} trend."
        else:
            return f"{formatted_metric.capitalize()} is slightly {direction}."
    
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
            f.write(f"MedBlock Anomaly Detection Model (Placeholder)\n")
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
    model = AnomalyDetectionModel()
    
    # Example input data with anomalies
    sample_data = {
        "patient_age": 45,
        "patient_gender": "female",
        "heart_rate": 115,  # Higher than normal
        "systolic_bp": 145,  # Higher than normal
        "diastolic_bp": 95,  # Higher than normal
        "temperature": 37.1,  # Normal
        "respiratory_rate": 10,  # Lower than normal
        "oxygen_saturation": 93,  # Lower than normal
        "glucose_level": 130,  # Higher than normal
        "white_blood_cell_count": 12.3,  # Higher than normal
        "historical_readings": [
            {
                "timestamp": (datetime.now() - timedelta(days=30)).isoformat(),
                "heart_rate": 72,
                "systolic_bp": 118,
                "glucose_level": 85
            },
            {
                "timestamp": (datetime.now() - timedelta(days=20)).isoformat(),
                "heart_rate": 75,
                "systolic_bp": 120,
                "glucose_level": 88
            },
            {
                "timestamp": (datetime.now() - timedelta(days=10)).isoformat(),
                "heart_rate": 80,
                "systolic_bp": 125,
                "glucose_level": 95
            }
        ]
    }
    
    # Detect anomalies
    result = model.detect_anomalies(sample_data)
    print(json.dumps(result, indent=2))
    
    # Example metric history for trend analysis
    metric_history = {
        "systolic_bp": [
            {"timestamp": (datetime.now() - timedelta(days=180)).isoformat(), "value": 120},
            {"timestamp": (datetime.now() - timedelta(days=150)).isoformat(), "value": 122},
            {"timestamp": (datetime.now() - timedelta(days=120)).isoformat(), "value": 126},
            {"timestamp": (datetime.now() - timedelta(days=90)).isoformat(), "value": 130},
            {"timestamp": (datetime.now() - timedelta(days=60)).isoformat(), "value": 135},
            {"timestamp": (datetime.now() - timedelta(days=30)).isoformat(), "value": 140},
            {"timestamp": datetime.now().isoformat(), "value": 145}
        ],
        "glucose_level": [
            {"timestamp": (datetime.now() - timedelta(days=180)).isoformat(), "value": 85},
            {"timestamp": (datetime.now() - timedelta(days=150)).isoformat(), "value": 88},
            {"timestamp": (datetime.now() - timedelta(days=120)).isoformat(), "value": 90},
            {"timestamp": (datetime.now() - timedelta(days=90)).isoformat(), "value": 95},
            {"timestamp": (datetime.now() - timedelta(days=60)).isoformat(), "value": 100},
            {"timestamp": (datetime.now() - timedelta(days=30)).isoformat(), "value": 115},
            {"timestamp": datetime.now().isoformat(), "value": 130}
        ]
    }
    
    # Analyze trends
    trend_analysis = model.analyze_historical_trends("patient-12345", metric_history)
    print(json.dumps(trend_analysis, indent=2)) 