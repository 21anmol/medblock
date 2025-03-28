# MedBlock

![MedBlock](https://via.placeholder.com/800x200.png?text=MedBlock:+Decentralized+Healthcare+Records)

MedBlock is a decentralized healthcare record system that integrates blockchain technology, machine learning, and zero-knowledge proofs to provide secure, private, and efficient management of electronic health records (EHR).

## Features

- 🔐 **Blockchain-Based Security**: Immutable storage of medical records on the blockchain
- 🧠 **Machine Learning Analytics**: Fraud detection, predictive health analytics, and anomaly detection
- 🔒 **Zero-Knowledge Proofs**: Privacy-preserving data sharing
- 👥 **Role-Based Access Control**: Granular access management for patients, providers, and insurers
- 📱 **Modern UI**: React-based frontend for intuitive user experience

## Overview

MedBlock addresses the key challenges in healthcare record management:

1. **Security**: Using blockchain to ensure tamper-proof record storage
2. **Privacy**: Implementing zero-knowledge proofs for private data sharing
3. **Interoperability**: Creating a standardized system for healthcare data exchange
4. **Accessibility**: Providing patients with ownership and control of their data
5. **Analytics**: Leveraging machine learning for improved healthcare outcomes

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL (optional, SQLite works for development)
- Web3 provider (like Ganache for development)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/medblock.git
   cd medblock
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Initialize the database:
   ```
   python -c "from database.models import init_db; init_db()"
   ```

5. Install frontend dependencies:
   ```
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

1. Start the API server:
   ```
   python run.py
   ```

2. In a separate terminal, start the frontend development server:
   ```
   cd frontend
   npm start
   ```

3. Access the application at `http://localhost:3000`

## Architecture

MedBlock follows a modular architecture with the following components:

- **Backend API**: Flask-based REST API
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL
- **Blockchain Integration**: Web3.py for smart contract interaction
- **Machine Learning Models**: Scikit-learn and TensorFlow-based models
- **Frontend**: React with Material-UI

## Machine Learning Models

MedBlock includes three key ML models:

1. **Fraud Detection**: Identifies potentially fraudulent insurance claims
2. **Predictive Healthcare**: Predicts health risks based on patient data
3. **Anomaly Detection**: Detects unusual access patterns for security

## Documentation

For more detailed documentation, see the [docs](docs) directory:

- [System Architecture](docs/architecture.md)
- [API Reference](docs/api_reference.md)
- [Machine Learning Models](docs/ml_models.md)
- [Blockchain Integration](docs/blockchain.md)
- [Frontend Guide](docs/frontend.md)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The blockchain and healthcare communities for inspiration
- All open-source libraries and frameworks used in this project

---

Made with ❤️ by the MedBlock Team 