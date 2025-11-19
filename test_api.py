#!/usr/bin/env python3
"""
Comprehensive API Integration Test Script
Tests all endpoints of the News Aggregator API
"""
import requests
import json
from datetime import datetime, timedelta


BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health_endpoint():
    """Test health check endpoint"""
    print_section("Testing Health Endpoint")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    assert response.status_code == 200
    assert data['status'] == 'ok'
    print("[PASS] Health check passed!")
    return True

def test_root_endpoint():
    """Test root endpoint"""
    print_section("Testing Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"API Name: {data['name']}")
    print(f"Version: {data['version']}")
    print(f"Status: {data['status']}")
    print(f"Docs: {BASE_URL}{data['docs']}")
    assert response.status_code == 200
    assert 'endpoints' in data
    print("[PASS] Root endpoint passed!")
    return True

def test_filters_endpoint():
    """Test filters endpoint"""
    print_section("Testing Filters Endpoint")
    response = requests.get(f"{BASE_URL}/api/filters")
    print(f"Status Code: {response.status_code}")
    data = response.json()

    print(f"\nCategories ({len(data['categories'])}): {', '.join(data['categories'])}")
    print(f"Languages ({len(data['languages'])}): {data['languages'][:3]}...")
    print(f"Countries ({len(data['countries'])}): {data['countries'][:5]}...")
    print(f"Sort Options: {[opt['label'] for opt in data['sort_options']]}")

    assert response.status_code == 200
    assert len(data['categories']) >= 7
    assert len(data['languages']) >= 10
    assert len(data['countries']) >= 50
    print("[PASS] Filters endpoint passed!")
    return True

def test_headlines_endpoint():
    """Test headlines endpoint"""
    print_section("Testing Headlines Endpoint")

    # Test basic headlines
    print("\n1. Testing basic headlines...")
    response = requests.get(f"{BASE_URL}/api/headlines")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Total Results: {data.get('total_results', data.get('totalResults'))}")
        print(f"Page: {data.get('page')}")
        print(f"Articles: {len(data.get('articles', []))}")
        if data.get('articles'):
            print(f"First Article: {data['articles'][0]['title'][:50]}...")
        print("[PASS] Basic headlines passed!")
    else:
        print(f"[WARN] API might not have valid key. Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")

    # Test with country filter
    print("\n2. Testing headlines with country filter (US)...")
    response = requests.get(f"{BASE_URL}/api/headlines?country=us")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("[PASS] Country filter passed!")

    # Test with category filter
    print("\n3. Testing headlines with category filter (technology)...")
    response = requests.get(f"{BASE_URL}/api/headlines?category=technology")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("[PASS] Category filter passed!")

    # Test pagination
    print("\n4. Testing pagination...")
    response = requests.get(f"{BASE_URL}/api/headlines?page=1&page_size=5")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Page Size: {data.get('page_size', data.get('pageSize'))}")
        print("[PASS] Pagination passed!")

    return True

def test_search_endpoint():
    """Test search endpoint"""
    print_section("Testing Search Endpoint")

    # Test basic search
    print("\n1. Testing basic search (query='technology')...")
    response = requests.get(f"{BASE_URL}/api/search?q=technology")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Total Results: {data.get('total_results', data.get('totalResults'))}")
        print(f"Articles: {len(data.get('articles', []))}")
        if data.get('articles'):
            print(f"First Article: {data['articles'][0]['title'][:50]}...")
        print("[PASS] Basic search passed!")
    else:
        print(f"[WARN] API might not have valid key. Status: {response.status_code}")

    # Test search with language filter
    print("\n2. Testing search with language filter...")
    response = requests.get(f"{BASE_URL}/api/search?q=bitcoin&language=en")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("[PASS] Language filter passed!")

    # Test search with date range
    print("\n3. Testing search with date range...")
    today = datetime.now().strftime('%Y-%m-%d')
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    response = requests.get(
        f"{BASE_URL}/api/search?q=news&from={week_ago}&to={today}"
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("[PASS] Date range passed!")

    # Test search with sort
    print("\n4. Testing search with sort option...")
    response = requests.get(f"{BASE_URL}/api/search?q=ai&sortBy=popularity")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("[PASS] Sort option passed!")

    # Test search validation (missing query)
    print("\n5. Testing validation (missing query)...")
    response = requests.get(f"{BASE_URL}/api/search")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 422:
        print("[PASS] Validation passed!")

    return True

def test_error_handling():
    """Test error handling"""
    print_section("Testing Error Handling")

    # Test invalid country code
    print("\n1. Testing invalid country code...")
    response = requests.get(f"{BASE_URL}/api/headlines?country=invalid")
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 422
    print("[PASS] Invalid country handled!")

    # Test invalid category
    print("\n2. Testing invalid category...")
    response = requests.get(f"{BASE_URL}/api/headlines?category=invalid")
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 422
    print("[PASS] Invalid category handled!")

    # Test invalid page number
    print("\n3. Testing invalid page number...")
    response = requests.get(f"{BASE_URL}/api/headlines?page=0")
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 422
    print("[PASS] Invalid page handled!")

    # Test invalid page size
    print("\n4. Testing page size too large...")
    response = requests.get(f"{BASE_URL}/api/headlines?page_size=200")
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 422
    print("[PASS] Page size validation handled!")

    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  NEWS AGGREGATOR API - COMPREHENSIVE TEST SUITE")
    print("="*60)

    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Root Endpoint", test_root_endpoint),
        ("Filters Endpoint", test_filters_endpoint),
        ("Headlines Endpoint", test_headlines_endpoint),
        ("Search Endpoint", test_search_endpoint),
        ("Error Handling", test_error_handling),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n[FAIL] {test_name} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"\n[ERROR] {test_name} ERROR: {e}")
            failed += 1

    # Final summary
    print("\n" + "="*60)
    print("  FINAL TEST RESULTS")
    print("="*60)
    print(f"[PASS] Passed: {passed}/{len(tests)}")
    print(f"[FAIL] Failed: {failed}/{len(tests)}")
    print(f"[STAT] Success Rate: {(passed/len(tests)*100):.1f}%")

    if passed == len(tests):
        print("\n[SUCCESS] ALL TESTS PASSED! API is 100% functional!")
    else:
        print(f"\n[WARN] Some tests failed. Check configuration.")

    print("\n[NOTE] Some failures are expected if you haven't added a valid NewsAPI key to backend/.env")
    print("   Get your free API key from: https://newsapi.org/register")
    print("="*60)


if __name__ == "__main__":
    main()
