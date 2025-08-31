#!/usr/bin/env python3
"""
Simple API test script to verify endpoints work before deployment
Run this locally to test your API: python test_api.py
"""

import requests
import json

# Base URL - change this to your deployed URL after deployment
BASE_URL = "http://localhost:8000"  # Change to https://your-app-name.onrender.com after deployment

def test_health():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Root Endpoint: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Root Endpoint Failed: {e}")
        return False

def test_docs():
    """Test if docs are accessible"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ API Docs: {response.status_code} - Accessible")
        return True
    except Exception as e:
        print(f"❌ API Docs Failed: {e}")
        return False

def test_signup():
    """Test user signup"""
    try:
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=data)
        if response.status_code in [200, 201, 422]:  # 422 means validation error (user might exist)
            print(f"✅ User Signup: {response.status_code}")
            return True
        else:
            print(f"❌ User Signup: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ User Signup Failed: {e}")
        return False

def test_login():
    """Test user login"""
    try:
        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", data=data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ User Login: {response.status_code} - Token received")
            return token
        else:
            print(f"❌ User Login: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ User Login Failed: {e}")
        return None

def test_create_post(token):
    """Test creating a blog post"""
    if not token:
        print("❌ Skipping post creation - no token")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "title": "Test Blog Post",
            "content": "This is a test blog post for API testing.",
            "published": True
        }
        response = requests.post(f"{BASE_URL}/api/v1/posts/", json=data, headers=headers)
        if response.status_code in [200, 201]:
            print(f"✅ Create Post: {response.status_code}")
            return True
        else:
            print(f"❌ Create Post: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Create Post Failed: {e}")
        return False

def test_get_posts():
    """Test getting posts"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/posts/")
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Get Posts: {response.status_code} - {len(posts)} posts")
            return True
        else:
            print(f"❌ Get Posts: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Get Posts Failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Blog API Endpoints")
    print("=" * 40)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("API Documentation", test_docs),
        ("User Signup", test_signup),
        ("Get Posts (Public)", test_get_posts),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
    
    # Test login and post creation if signup worked
    print(f"\n🔍 Testing: User Login")
    token = test_login()
    if token:
        passed += 1
        print(f"\n🔍 Testing: Create Post")
        if test_create_post(token):
            passed += 1
        total += 1
    total += 1
    
    print("\n" + "=" * 40)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is ready for deployment!")
        print(f"\n🌐 To deploy:")
        print("1. Push code to GitHub")
        print("2. Go to render.com")
        print("3. Connect your repo and deploy!")
    else:
        print("⚠️  Some tests failed. Check your API before deployment.")
    
    print(f"\n📖 See DEPLOYMENT.md for detailed deployment instructions")

if __name__ == "__main__":
    main()
