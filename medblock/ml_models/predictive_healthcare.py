import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
import joblib

class PredictiveHealthcareModel:
    def __init__(self, model_path=None):
        """
        Initialize the predictive healthcare model
        
        Args:
            model_path (str, optional): Path to a pre-trained model
        """
        if model_path and os.path.exists(model_path):
            self.model = load_model(model_path)
            scaler_path = model_path.replace('.h5', '_scaler.pkl')
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
            else:
                self.scaler = StandardScaler()
        else:
            self.model = None
            self.scaler = StandardScaler()
            
    def build_model(self, input_dim, num_classes):
        """
        Build the neural network model
        
        Args:
            input_dim (int): Number of input features
            num_classes (int): Number of output classes
            
        Returns:
            tf.keras.Model: Compiled model
        """
        model = Sequential([
            Dense(128, activation='relu', input_shape=(input_dim,)),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.2),
            
            Dense(32, activation='relu'),
            BatchNormalization(),
            
            Dense(num_classes, activation='softmax' if num_classes > 2 else 'sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy' if num_classes > 2 else 'binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def preprocess_data(self, data):
        """
        Preprocess the input data
        
        Args:
            data (pd.DataFrame): Raw input data
            
        Returns:
            pd.DataFrame: Preprocessed data
        """
        # Handle missing values
        numeric_cols = data.select_dtypes(include=np.number).columns
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        
        data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
        data[categorical_cols] = data[categorical_cols].fillna(data[categorical_cols].mode().iloc[0])
        
        # Feature engineering
        if 'age' in data.columns and 'bmi' in data.columns:
            data['age_bmi_ratio'] = data['age'] / data['bmi']
        
        if 'systolic_bp' in data.columns and 'diastolic_bp' in data.columns:
            data['pulse_pressure'] = data['systolic_bp'] - data['diastolic_bp']
        
        # One-hot encode categorical variables
        for col in categorical_cols:
            if col in data.columns and col != 'target':
                dummies = pd.get_dummies(data[col], prefix=col, drop_first=True)
                data = pd.concat([data, dummies], axis=1)
                data.drop(col, axis=1, inplace=True)
        
        return data
    
    def train(self, data_path, target_col='disease_risk', test_size=0.2, epochs=50, batch_size=32):
        """
        Train the healthcare prediction model
        
        Args:
            data_path (str): Path to the training data CSV
            target_col (str): Name of the target column
            test_size (float): Proportion of data to use for testing
            epochs (int): Number of training epochs
            batch_size (int): Batch size for training
            
        Returns:
            dict: Training metrics and history
        """
        # Load data
        data = pd.read_csv(data_path)
        
        # Preprocess
        data = self.preprocess_data(data)
        
        # Split features and target
        X = data.drop(target_col, axis=1)
        y = data[target_col]
        
        # Get number of classes
        num_classes = len(np.unique(y))
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Build model
        self.model = self.build_model(X_train_scaled.shape[1], num_classes)
        
        # Callbacks
        callbacks = [
            EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
            ModelCheckpoint(
                filepath='best_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train model
        history = self.model.fit(
            X_train_scaled, y_train,
            validation_data=(X_test_scaled, y_test),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate
        evaluation = self.model.evaluate(X_test_scaled, y_test)
        
        # Plot training history
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('Model Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper left')
        
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model Loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation'], loc='upper left')
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        
        return {
            'accuracy': evaluation[1],
            'loss': evaluation[0],
            'history': {k: [float(val) for val in v] for k, v in history.history.items()}
        }
    
    def predict(self, features):
        """
        Predict disease risk
        
        Args:
            features (dict or pd.DataFrame): Input features
            
        Returns:
            dict: Prediction results with probability
        """
        if not self.model:
            raise ValueError("Model not trained. Train the model first or load a pre-trained model.")
        
        if isinstance(features, dict):
            features = pd.DataFrame([features])
        
        # Preprocess
        features = self.preprocess_data(features)
        
        # Scale
        features_scaled = self.scaler.transform(features)
        
        # Predict
        probabilities = self.model.predict(features_scaled)
        
        if probabilities.shape[1] > 1:  # Multi-class
            prediction = np.argmax(probabilities[0])
            confidence = float(probabilities[0][prediction])
        else:  # Binary
            prediction = int(probabilities[0][0] > 0.5)
            confidence = float(probabilities[0][0]) if prediction == 1 else 1 - float(probabilities[0][0])
        
        risk_levels = ['Low', 'Medium', 'High']
        risk_level = risk_levels[min(prediction, len(risk_levels)-1)]
        
        return {
            'prediction': int(prediction),
            'confidence': confidence,
            'risk_level': risk_level
        }
    
    def save(self, model_path):
        """
        Save the trained model to disk
        
        Args:
            model_path (str): Path to save the model
        """
        if not self.model:
            raise ValueError("No model to save. Train the model first.")
        
        self.model.save(model_path)
        joblib.dump(self.scaler, model_path.replace('.h5', '_scaler.pkl'))
        print(f"Model saved to {model_path}")


if __name__ == "__main__":
    # Example usage
    model = PredictiveHealthcareModel()
    
    # Create synthetic data for demonstration
    from sklearn.datasets import make_classification
    
    X, y = make_classification(
        n_samples=1000, 
        n_features=15, 
        n_informative=10, 
        n_redundant=3,
        n_classes=3,
        random_state=42
    )
    
    feature_names = [
        'age', 'gender', 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate',
        'glucose', 'cholesterol', 'hdl', 'ldl', 'triglycerides', 
        'smoking_status', 'alcohol_consumption', 'physical_activity', 'family_history'
    ]
    
    # Create DataFrame
    df = pd.DataFrame(X, columns=feature_names)
    df['disease_risk'] = y
    
    # Save synthetic data
    df.to_csv('synthetic_health_data.csv', index=False)
    
    # Train model
    metrics = model.train('synthetic_health_data.csv', epochs=10)  # Lower epochs for demonstration
    print(f"Model accuracy: {metrics['accuracy']:.4f}")
    
    # Save model
    model.save('healthcare_prediction_model.h5')
    
    # Test prediction
    sample = df.drop('disease_risk', axis=1).iloc[0].to_dict()
    prediction = model.predict(sample)
    print(f"Prediction: {prediction}") 