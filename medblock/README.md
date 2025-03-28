# MedBlock - Decentralized Healthcare Record System

MedBlock is a decentralized healthcare record system that combines blockchain technology with machine learning to provide secure, transparent, and intelligent healthcare data management. This platform allows patients to control their medical records while providing healthcare providers with the insights they need.

![MedBlock](https://github.com/username/medblock/raw/main/docs/images/medblock-logo.png)

## Features

- **Decentralized Record Storage**: Secure your health data with blockchain technology
- **User-Controlled Access**: Grant and revoke provider access to your records
- **AI-Powered Analytics**: Health predictions and anomaly detection
- **Fraud Prevention**: ML-based fraud detection for claims and transactions
- **Modern UI**: Intuitive, responsive design with dark/light mode

## System Components

### Frontend

- Modern HTML/CSS/JS with responsive design
- Interactive dashboards and data visualizations
- Blockchain transaction explorer
- Theme switching (dark/light mode)
- ICP (Internet Computer Protocol) authentication integration

### Backend (API)

- Flask-based REST API
- ML model integration points
- Mock blockchain verification
- User authentication and record management
- File upload and management

### Machine Learning

- Fraud Detection Model
- Health Prediction Model
- Anomaly Detection Model

## Getting Started

### Prerequisites

- Python 3.8+
- Flask and dependencies
- Modern web browser
- Node.js and npm (for frontend package management)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/medblock.git
   cd medblock
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   cd medblock
   python app.py --port 5001
   ```

4. Access the application:
   - Main site: http://localhost:5001/
   - API Testing: http://localhost:5001/api-test.html

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check API health |
| `/api/auth/login` | POST | User login |
| `/api/users/profile` | GET | Get user profile |
| `/api/records` | GET | Get user's medical records |
| `/api/records` | POST | Create a new medical record |
| `/api/ml/fraud/detect` | POST | Detect fraud in transactions |
| `/api/ml/health/predict` | POST | Get health predictions |
| `/api/ml/anomaly/detect` | POST | Detect anomalies in health data |
| `/api/blockchain/verify` | POST | Verify record integrity |
| `/api/blockchain/access-log` | GET | Get blockchain access logs |

## Project Structure

```
medblock/
├── app.py                     # Main Flask application
├── frontend/                  # Frontend files
│   ├── index.html             # Landing page
│   ├── dashboard.html         # User dashboard
│   ├── blockchain.html        # Blockchain explorer
│   ├── login.html             # Login page
│   ├── api-test.html          # API testing interface
│   ├── css/                   # CSS styles
│   └── js/                    # JavaScript files
├── ml_models/                 # Machine learning models
│   ├── fraud_detection.py
│   ├── health_prediction.py
│   └── anomaly_detection.py
├── data/                      # Mock data storage
├── uploads/                   # File uploads
└── models/                    # Saved ML model states
```

## Demo Mode

For demonstration and testing purposes, MedBlock provides a demo mode that allows you to navigate the system without requiring full authentication:

1. Visit http://localhost:5001/login.html
2. Click "Enter Demo Mode"
3. Explore the system with mock data and functionality

## Screenshots

### Landing Page
![Landing Page](https://github.com/username/medblock/raw/main/docs/screenshots/landing.png)

### User Dashboard
![Dashboard](https://github.com/username/medblock/raw/main/docs/screenshots/dashboard.png)

### Blockchain Explorer
![Blockchain](https://github.com/username/medblock/raw/main/docs/screenshots/blockchain.png)

## Contributors

- Your Name - Lead Developer
- AI Assistant - Development Partner

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was created as a demonstration of integrating machine learning with blockchain for healthcare applications
- Thanks to all open-source libraries and frameworks that made this possible 