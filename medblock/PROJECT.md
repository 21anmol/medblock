# MedBlock: Decentralized Healthcare Record System

## Project Overview

MedBlock is an innovative healthcare record system that integrates blockchain technology with machine learning to create a secure, private, and efficient platform for managing electronic health records (EHR). This project addresses key challenges in healthcare data management such as data privacy, unauthorized access, fraud detection, and predictive healthcare analytics.

## Key Components

### 1. Machine Learning Models

- **Fraud Detection Model (`ml_models/fraud_detection.py`)**: Uses Random Forest to identify suspicious insurance claims by analyzing patterns in billing data.
- **Predictive Healthcare Model (`ml_models/predictive_healthcare.py`)**: Deep Learning model that predicts disease risks based on patient health metrics.
- **Anomaly Detection Model (`ml_models/anomaly_detection.py`)**: Isolation Forest algorithm that identifies unusual access patterns to protect patient data.

### 2. Blockchain Integration

- **Smart Contract (`blockchain/smart_contracts.py`)**: Implements role-based access control and encrypted storage of medical records on the blockchain.
- **Contract ABI (`blockchain/abi/MedicalRecords.json`)**: ABI and bytecode for the Ethereum smart contract.

### 3. API Layer

- **Flask API (`api/app.py`)**: RESTful API that connects the frontend with ML models and blockchain infrastructure.

### 4. Frontend

- **React Dashboard (`frontend/src/components/Dashboard.jsx`)**: User interface displaying health predictions, anomaly detection, and fraud risk analytics.

## Technical Architecture

```
┌─────────────────┐      ┌───────────────┐      ┌───────────────┐
│   React Frontend│<────>│   Flask API   │<────>│  ML Models    │
└─────────────────┘      └───────────────┘      └───────────────┘
                               ↑                       ↑
                               │                       │
                               ▼                       ▼
                         ┌───────────────┐      ┌───────────────┐
                         │  Blockchain   │<────>│  Encrypted    │
                         │  Smart Contract│     │  Storage      │
                         └───────────────┘      └───────────────┘
```

## Security Features

1. **Zero-Knowledge Proofs**: Verify identities without revealing sensitive information
2. **Role-Based Access Control**: Fine-grained permissions for different healthcare providers
3. **Blockchain Immutability**: Tamper-proof record of all data access and modifications
4. **ML-Powered Anomaly Detection**: Real-time identification of suspicious access patterns
5. **Encryption**: End-to-end encryption of patient data

## Future Enhancements

1. **Medical Image Processing**: Add CNN-based models for analyzing medical images
2. **NLP for Medical Reports**: Implement text processing for automated report summarization
3. **Cross-Blockchain Compatibility**: Enable interoperability with multiple blockchain platforms
4. **NFT-Based Health Certificates**: Digital health credentials as non-fungible tokens

## Getting Started

1. Install dependencies for the backend:
   ```
   pip install -r requirements.txt
   ```

2. Install dependencies for the frontend:
   ```
   cd frontend
   npm install
   ```

3. Start the API server:
   ```
   python api/app.py
   ```

4. Start the frontend:
   ```
   cd frontend
   npm start
   ```

## Data Requirements

The machine learning models require specific datasets:
- **Fraud Detection**: Claims data with transaction details and fraud labels
- **Healthcare Prediction**: Patient health metrics with associated disease outcomes
- **Anomaly Detection**: System access logs with normal and anomalous patterns 