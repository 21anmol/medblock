"""
Predictive Healthcare Model for MedBlock

This module implements the predictive healthcare model for predicting health conditions and risks.
"""

import os
import sys
import logging
import numpy as np
import pandas as pd
import json
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Set up logger
logger = logging.getLogger(__name__)

class PredictiveHealthcareModel:
    """Predictive healthcare model for disease risk prediction"""
    
    def __init__(self, model_path=None):
        """
        Initialize the predictive healthcare model
        
        Args:
            model_path (str, optional): Path to a saved model
        """
        self.model = None
        self.scaler = StandardScaler()
        
        # Try to load the model if provided
        if model_path and os.path.exists(model_path):
            try:
                # Load Keras model
                self.model = keras.models.load_model(model_path)
                
                # Load metadata (feature names, etc.)
                metadata_path = os.path.join(os.path.dirname(model_path), 'healthcare_model_metadata.json')
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        self.features = metadata['features']
                        self.conditions = metadata['conditions']
                        
                        # Load scaler
                        scaler_path = os.path.join(os.path.dirname(model_path), 'healthcare_scaler.pkl')
                        if os.path.exists(scaler_path):
                            import pickle
                            with open(scaler_path, 'rb') as f:
                                self.scaler = pickle.load(f)
                
                logger.info(f"Loaded healthcare prediction model from {model_path}")
            except Exception as e:
                logger.error(f"Error loading model from {model_path}: {str(e)}")
                self._initialize_default_model()
        else:
            logger.info("No model path provided or model file not found, initializing default model")
            self._initialize_default_model()
    
    def _initialize_default_model(self):
        """Initialize a default model with basic settings"""
        # Define features and conditions
        self.features = [
            'age', 'gender', 'weight', 'height', 'smoker', 'family_history',
            'cholesterol', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'blood_sugar', 'physical_activity', 'sleep_hours'
        ]
        
        self.conditions = [
            'heart_disease', 'diabetes', 'hypertension', 'obesity', 'respiratory_disease'
        ]
        
        # Create a simple neural network
        input_layer = layers.Input(shape=(len(self.features),))
        x = layers.Dense(64, activation='relu')(input_layer)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(32, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        output_layer = layers.Dense(len(self.conditions), activation='sigmoid')(x)
        
        self.model = keras.Model(inputs=input_layer, outputs=output_layer)
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        logger.info("Initialized default healthcare prediction model")
    
    def preprocess_data(self, data, for_training=False):
        """
        Preprocess input data for the model
        
        Args:
            data (dict or DataFrame): Input data
            for_training (bool): Whether preprocessing is for training
            
        Returns:
            numpy.ndarray: Preprocessed features
        """
        if isinstance(data, dict):
            # Convert single record to DataFrame
            df = pd.DataFrame([data])
        else:
            df = data.copy()
        
        # Handle missing features
        for feature in self.features:
            if feature not in df.columns:
                df[feature] = 0
        
        # Handle categorical features
        # Example: convert gender to binary
        if 'gender' in df.columns:
            df['gender'] = df['gender'].map({'male': 0, 'female': 1}).fillna(0)
        
        # Extract features
        X = df[self.features].copy()
        
        # Fill missing values
        X.fillna(0, inplace=True)
        
        # Scale features
        if for_training:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def train(self, data_path, epochs=50, batch_size=32, validation_split=0.2, random_state=42):
        """
        Train the healthcare prediction model
        
        Args:
            data_path (str): Path to the training data file
            epochs (int): Number of training epochs
            batch_size (int): Batch size for training
            validation_split (float): Proportion of data to use for validation
            random_state (int): Random seed for reproducibility
            
        Returns:
            dict: Training metrics
        """
        try:
            # Load data
            df = pd.read_csv(data_path)
            logger.info(f"Loaded training data with {df.shape[0]} records and {df.shape[1]} features")
            
            # Check if target variables exist
            for condition in self.conditions:
                if condition not in df.columns:
                    raise ValueError(f"Training data must include '{condition}' column")
            
            # Preprocess data
            X = self.preprocess_data(df, for_training=True)
            y = df[self.conditions].values
            
            # Split into train and validation sets
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=validation_split, random_state=random_state
            )
            
            # Train model
            logger.info("Training healthcare prediction model...")
            history = self.model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_val, y_val),
                verbose=1
            )
            
            # Get final metrics
            train_metrics = self.model.evaluate(X_train, y_train, verbose=0)
            val_metrics = self.model.evaluate(X_val, y_val, verbose=0)
            
            metrics = {
                'train_loss': float(train_metrics[0]),
                'train_accuracy': float(train_metrics[1]),
                'val_loss': float(val_metrics[0]),
                'val_accuracy': float(val_metrics[1])
            }
            
            logger.info(f"Model training completed with metrics: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise
    
    def predict(self, data):
        """
        Make health predictions on input data
        
        Args:
            data (dict): Input data for prediction
            
        Returns:
            dict: Prediction results
        """
        try:
            # Check if model is trained
            if self.model is None:
                raise ValueError("Model is not trained yet")
            
            # Preprocess data
            X = self.preprocess_data(data)
            
            # Make prediction
            predictions = self.model.predict(X)[0]
            
            # Format results
            result = {
                'predictions': {},
                'overall_risk': 0
            }
            
            # Add individual condition predictions
            for i, condition in enumerate(self.conditions):
                prob = float(predictions[i])
                result['predictions'][condition] = {
                    'probability': prob,
                    'risk_level': 'high' if prob > 0.7 else 'medium' if prob > 0.3 else 'low'
                }
            
            # Calculate overall risk (average of all probabilities)
            result['overall_risk'] = float(np.mean(predictions))
            result['overall_risk_level'] = 'high' if result['overall_risk'] > 0.7 else 'medium' if result['overall_risk'] > 0.3 else 'low'
            
            # Add important feature values used in prediction
            result['key_factors'] = {}
            for feature in self.features:
                if feature in data:
                    result['key_factors'][feature] = data[feature]
            
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise
    
    def save(self, model_path):
        """
        Save the model to files
        
        Args:
            model_path (str): Path to save the model
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            model_dir = os.path.dirname(model_path)
            os.makedirs(model_dir, exist_ok=True)
            
            # Save the keras model
            self.model.save(model_path)
            
            # Save metadata
            metadata = {
                'features': self.features,
                'conditions': self.conditions
            }
            metadata_path = os.path.join(model_dir, 'healthcare_model_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Save scaler
            import pickle
            scaler_path = os.path.join(model_dir, 'healthcare_scaler.pkl')
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            logger.info(f"Model and metadata saved to {model_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False 