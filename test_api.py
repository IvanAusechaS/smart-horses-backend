#!/usr/bin/env python3
"""
Test script to verify all API endpoints are working.
Run this with the server running on localhost:5000
"""

import requests
import json
import sys

API_URL = "http://localhost:5000"

def test_endpoint(name, method, url, data=None):
    """Test a single endpoint."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code in [200, 201]:
            print("✅ PASSED")
            return True
        else:
            print("❌ FAILED")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("  SMART HORSES BACKEND - API TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Health Check
    results.append(test_endpoint(
        "Health Check",
        "GET",
        f"{API_URL}/health"
    ))
    
    # Test 2: Root endpoint
    results.append(test_endpoint(
        "Root Endpoint",
        "GET",
        f"{API_URL}/"
    ))
    
    # Test 3: New Game - Beginner
    results.append(test_endpoint(
        "New Game - Beginner",
        "POST",
        f"{API_URL}/api/game/new",
        {"difficulty": "beginner"}
    ))
    
    # Test 4: New Game - Amateur
    results.append(test_endpoint(
        "New Game - Amateur",
        "POST",
        f"{API_URL}/api/game/new",
        {"difficulty": "amateur"}
    ))
    
    # Test 5: New Game - Expert
    results.append(test_endpoint(
        "New Game - Expert",
        "POST",
        f"{API_URL}/api/game/new",
        {"difficulty": "expert"}
    ))
    
    # Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"Total Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print("="*60 + "\n")
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
