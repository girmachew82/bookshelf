import requests
import os

def test_api_connection():
   
    try:
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/publishers/',
            proxies={'http': None, 'https': None},
            timeout=10
        )
        
        if response.status_code == 200:
            publishers = response.json()
            print("API Response:", publishers)
            return publishers
        else:
            print(f"HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please ensure:")
        print("1. Django server is running: python manage.py runserver")
        print("2. Server is on http://127.0.0.1:8000/")
        print("3. No firewall is blocking port 8000")
        
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run the test
if __name__ == "__main__":
    test_api_connection()