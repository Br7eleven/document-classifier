#!/usr/bin/env python3
"""
Simple test script for Docker deployment
"""

import requests
import json
import time
from io import BytesIO

API_BASE_URL = 'http://localhost:5000'
AUTH_TOKEN = 'Bearer stub_token_12345'

def test_api():
    """Test the API endpoints"""
    print("🐳 Testing Document Classifier API in Docker")
    print("=" * 50)
    
    # Wait for API to be ready
    print("⏳ Waiting for API to be ready...")
    for i in range(30):
        try:
            response = requests.get(f'{API_BASE_URL}/status', timeout=5)
            if response.status_code == 200:
                print("✅ API is ready!")
                break
        except:
            print(f"⏳ Waiting... ({i+1}/30)")
            time.sleep(2)
    else:
        print("❌ API not responding after 60 seconds")
        return False
    
    # Test health check
    print("\n🔍 Testing health check...")
    try:
        response = requests.get(f'{API_BASE_URL}/status')
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Model loaded: {data['model_loaded']}")
        print(f"Categories: {data['categories']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test categories
    print("\n📋 Testing categories endpoint...")
    try:
        response = requests.get(f'{API_BASE_URL}/categories')
        data = response.json()
        print(f"Available categories: {data['categories']}")
    except Exception as e:
        print(f"❌ Categories test failed: {e}")
    
    # Test authentication
    print("\n🔐 Testing authentication...")
    try:
        response = requests.post(f'{API_BASE_URL}/classify')
        print(f"Without token: {response.status_code} - {response.json()['error']}")
        
        headers = {'Authorization': 'Bearer invalid_token'}
        response = requests.post(f'{API_BASE_URL}/classify', headers=headers)
        print(f"Invalid token: {response.status_code} - {response.json()['error']}")
    except Exception as e:
        print(f"❌ Auth test failed: {e}")
    
    print("\n🎉 Docker API test completed!")
    print("\n📋 Next steps:")
    print("1. Open chatbot.html in your browser")
    print("2. Upload a PDF or DOCX file")
    print("3. See the classification results!")
    print("\n💡 API Endpoints:")
    print(f"   Health: {API_BASE_URL}/status")
    print(f"   Classify: POST {API_BASE_URL}/classify")
    print(f"   Categories: {API_BASE_URL}/categories")
    print(f"\n🔑 Auth Token: {AUTH_TOKEN}")
    
    return True

if __name__ == '__main__':
    test_api()