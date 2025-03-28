"""
Test script for MedBlock API

This script makes HTTP requests to test if the MedBlock API is working.
"""

import requests
import json
import sys

def test_api(base_url):
    """
    Test the MedBlock API by making requests to various endpoints
    
    Args:
        base_url (str): Base URL of the API, e.g., 'http://localhost:8080'
    """
    print(f"Testing MedBlock API at {base_url}...")
    
    # Test endpoints
    endpoints = [
        '/',
        '/api/health',
        '/api/fraud/detect',
        '/api/health/predict',
        '/api/records'
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            print(f"\nTesting endpoint: {endpoint}")
            response = requests.get(url)
            
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                print("Response content:")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"Error: {response.reason}")
        except Exception as e:
            print(f"Error connecting to {url}: {str(e)}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    # Default base URL
    base_url = "http://localhost:8080"
    
    # Use command line argument if provided
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    test_api(base_url) 