// MedBlock API testing utility
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to the test buttons
    document.querySelectorAll('.api-test-btn').forEach(button => {
        button.addEventListener('click', function() {
            const endpoint = this.getAttribute('data-endpoint');
            const method = this.getAttribute('data-method') || 'GET';
            const resultContainer = document.getElementById('api-result');
            
            // Show loading state
            resultContainer.innerHTML = '<div class="loading">Testing API...</div>';
            
            // Prepare sample data based on endpoint
            let data = null;
            if (endpoint === '/api/ml/fraud/detect') {
                data = {
                    "transaction_id": "tx-12345",
                    "user_id": "demo-user",
                    "timestamp": new Date().toISOString(),
                    "amount": 250.00,
                    "provider": "Remote Health Services",
                    "service_code": "VTC-001",
                    "location": "Remote",
                    "ip_address": "192.168.1.100"
                };
            } else if (endpoint === '/api/ml/health/predict') {
                data = {
                    "user_id": "demo-user",
                    "age": 42,
                    "gender": "female",
                    "height": 165,
                    "weight": 65,
                    "blood_pressure": "120/80",
                    "cholesterol": 190,
                    "glucose": 85,
                    "smoking": false,
                    "alcohol": "moderate",
                    "exercise": "regular",
                    "family_history": {
                        "diabetes": true,
                        "heart_disease": false,
                        "cancer": true
                    }
                };
            } else if (endpoint === '/api/ml/anomaly/detect') {
                data = {
                    "user_id": "demo-user",
                    "metrics": [
                        {"name": "blood_pressure", "values": [120, 122, 118, 130, 125]},
                        {"name": "heart_rate", "values": [72, 75, 70, 71, 85]},
                        {"name": "glucose", "values": [85, 90, 88, 86, 100]}
                    ],
                    "timeframe": "last_month"
                };
            } else if (endpoint === '/api/blockchain/verify') {
                data = {
                    "record_id": "rec-001",
                    "hash": "0x7f83b1..."
                };
            } else if (endpoint === '/api/auth/login') {
                data = {
                    "principalId": "demo-user",
                    "email": "demo@example.com"
                };
            } else if (endpoint === '/api/records') {
                if (method === 'POST') {
                    data = {
                        "user_id": "demo-user",
                        "title": "New Test Record",
                        "type": "Examination",
                        "date": new Date().toISOString().split('T')[0],
                        "provider": "Test Provider",
                        "facility": "Test Facility",
                        "notes": "This is a test record created via API"
                    };
                }
            }
            
            // Make API call
            makeApiCall(endpoint, method, data)
                .then(response => {
                    // Format and display result
                    resultContainer.innerHTML = `
                        <div class="api-result-header">
                            <h3>API Response</h3>
                            <span class="status-code">Status: ${response.status}</span>
                        </div>
                        <pre class="api-response-data">${formatJson(response.data)}</pre>
                    `;
                })
                .catch(error => {
                    resultContainer.innerHTML = `
                        <div class="api-result-header error">
                            <h3>API Error</h3>
                            <span class="status-code">Status: ${error.status || 'Error'}</span>
                        </div>
                        <pre class="api-response-error">${error.message || JSON.stringify(error, null, 2)}</pre>
                    `;
                });
        });
    });
    
    // Function to make API calls
    async function makeApiCall(endpoint, method, data) {
        const baseUrl = window.location.protocol + '//' + window.location.hostname + ':5001';
        const url = baseUrl + endpoint;
        
        try {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            
            if (data && (method === 'POST' || method === 'PUT')) {
                options.body = JSON.stringify(data);
            }
            
            const response = await fetch(url, options);
            
            // Check if the response is ok (status code 200-299)
            if (!response.ok) {
                throw {
                    status: response.status,
                    message: `API returned ${response.status} ${response.statusText}`
                };
            }
            
            const responseData = await response.json();
            
            return {
                status: response.status,
                data: responseData
            };
        } catch (error) {
            console.error('API call error:', error);
            
            // Handle network errors
            if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                throw {
                    status: 'Network Error',
                    message: 'Could not connect to the server. Make sure the API is running on port 5001.'
                };
            }
            
            throw {
                status: error.status || 'Error',
                message: error.message || 'Error making API call'
            };
        }
    }
    
    // Helper function to format JSON for display
    function formatJson(json) {
        return JSON.stringify(json, null, 2);
    }
}); 