#!/usr/bin/env python
"""Test script for the doador search feature"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_search_doadores():
    """Test the search endpoint"""
    print("Testing doador search API...")
    
    # Test 1: Search by name
    print("\n1. Testing search by name (Ricardo):")
    response = requests.get(
        f"{BASE_URL}/api/colaborador/buscar-doadores?query=ricardo",
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 401:
        print("Got 401 Unauthorized - Need to authenticate")
        print("Response:", response.text)
    else:
        print("Response:", json.dumps(response.json(), indent=2))
    
    # Test 2: Search by CPF
    print("\n2. Testing search by CPF (partial):")
    response = requests.get(
        f"{BASE_URL}/api/colaborador/buscar-doadores?query=123",
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 401:
        print("Got 401 Unauthorized - Need to authenticate")
    else:
        print("Response:", json.dumps(response.json(), indent=2))
    
    # Test 3: Short query
    print("\n3. Testing with short query (< 2 chars):")
    response = requests.get(
        f"{BASE_URL}/api/colaborador/buscar-doadores?query=r",
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 401:
        print("Got 401 Unauthorized - Need to authenticate")
    else:
        print("Response:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_search_doadores()
