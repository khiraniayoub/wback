import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/users"

# Test 1: Registro
print("\n=== TEST 1: REGISTRO ===")
register_data = {
    "email": "newuser@example.com",
    "password": "TestPassword123!"
}
response = requests.post(f"{BASE_URL}/register/", json=register_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
print(f"JSON: {response.json()}")
