# MedBlock Documentation

Welcome to the MedBlock documentation! This directory contains detailed documentation on how to use and extend the MedBlock system.

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Getting Started](#getting-started)
4. [API Reference](#api-reference)
5. [Machine Learning Models](#machine-learning-models)
6. [Blockchain Integration](#blockchain-integration)
7. [Frontend](#frontend)
8. [Contributing](#contributing)

## Introduction

MedBlock is a decentralized healthcare record system that integrates blockchain technology, machine learning, and zero-knowledge proofs to provide secure, private, and efficient management of electronic health records (EHR).

Key features include:
- Blockchain-based EHR storage
- Role-Based Access Control (RBAC)
- Zero-Knowledge Proofs for privacy
- ML-Driven Analytics

## System Architecture

MedBlock follows a modular architecture with the following components:

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

For more detailed architecture information, see the [System Architecture](architecture.md) document.

## Getting Started

To get started with MedBlock:

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your environment:
   ```
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Initialize the database:
   ```python
   from database.models import init_db
   init_db()
   ```

4. Start the API server:
   ```
   python run.py
   ```

For more detailed setup instructions, see the [Getting Started](tutorials/getting_started.md) guide.

## API Reference

The MedBlock API provides the following endpoints:

- `/api/v1/ml/fraud/detect` - Fraud detection in medical claims
- `/api/v1/ml/healthcare/predict` - Predictive healthcare analytics
- `/api/v1/ml/access/analyze` - Access pattern anomaly detection
- `/api/v1/users` - User management
- `/api/v1/records` - Medical record management

For complete API documentation, see the [API Reference](api_reference.md) document.

## Machine Learning Models

MedBlock includes three main machine learning models:

1. **Fraud Detection Model**: Random Forest classifier for detecting fraudulent insurance claims
2. **Predictive Healthcare Model**: Deep Learning model for disease risk prediction
3. **Anomaly Detection Model**: Isolation Forest for detecting unusual access patterns

For more details on the ML models, see the [Machine Learning Models](ml_models.md) document.

## Blockchain Integration

MedBlock uses blockchain technology for:

- Immutable record storage
- Access control
- Audit trail
- Zero-knowledge proofs

For details on blockchain integration, see the [Blockchain Integration](blockchain.md) document.

## Frontend

The frontend is built with React and provides:

- User-friendly interface
- Real-time analytics
- Responsive design
- Secure authentication

For frontend documentation, see the [Frontend Guide](frontend.md).

## Contributing

We welcome contributions to MedBlock! Please see the [Contributing Guide](contributing.md) for details on how to contribute. 