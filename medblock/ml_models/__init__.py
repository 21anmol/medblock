"""
MedBlock ML Models Package

This package contains the machine learning models used by the MedBlock application
for health prediction, fraud detection, and anomaly detection.

These are placeholder implementations that simulate ML functionality without
requiring actual ML dependencies. In a production environment, these would
be replaced with real implementations using frameworks like TensorFlow or PyTorch.
"""

import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create models directory if it doesn't exist
models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
os.makedirs(models_dir, exist_ok=True)

# Import models
try:
    from .health_prediction import HealthPredictionModel
    from .fraud_detection import FraudDetectionModel
    from .anomaly_detection import AnomalyDetectionModel
    
    __all__ = [
        'HealthPredictionModel',
        'FraudDetectionModel',
        'AnomalyDetectionModel'
    ]
    
    logger.info("Successfully loaded ML models")
except ImportError as e:
    logger.warning(f"Error importing ML models: {e}")
    
    # Define placeholder classes to avoid crashes
    class PlaceholderModel:
        def __init__(self, *args, **kwargs):
            self.name = self.__class__.__name__
            logger.warning(f"Using placeholder {self.name}")
        
        def predict(self, *args, **kwargs):
            return {"error": f"{self.name} is not available", "result": "placeholder_result"}
    
    class HealthPredictionModel(PlaceholderModel):
        pass
    
    class FraudDetectionModel(PlaceholderModel):
        pass
    
    class AnomalyDetectionModel(PlaceholderModel):
        pass
    
    __all__ = [
        'HealthPredictionModel',
        'FraudDetectionModel',
        'AnomalyDetectionModel'
    ]