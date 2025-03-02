import requests
import json
import sys

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def get_token():
    """Get an authentication token"""
    # Use form data instead of JSON for OAuth2 compatibility
    login_data = {
        "username": "regularuser",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code != 200:
        print(f"Failed to login: {response.status_code} - {response.text}")
        sys.exit(1)
    
    return response.json()["access_token"]

def get_resources(token, sort_by="name", sort_order="asc"):
    """Get resources with the specified sorting"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "skip": 0,
        "limit": 10,
        "sort_by": sort_by,
        "sort_order": sort_order
    }
    
    response = requests.get(f"{BASE_URL}/resources/", headers=headers, params=params)
    if response.status_code != 200:
        print(f"Failed to get resources: {response.status_code} - {response.text}")
        sys.exit(1)
    
    return response.json()

def compare_results(asc_results, desc_results):
    """Compare ascending and descending results to ensure they're different"""
    if not asc_results["items"] or not desc_results["items"]:
        print("No items returned in one or both responses")
        return False
    
    # Check if the order is different
    asc_ids = [item["id"] for item in asc_results["items"]]
    desc_ids = [item["id"] for item in desc_results["items"]]
    
    if asc_ids == desc_ids:
        print("WARNING: Same order of IDs for both ascending and descending sorts!")
        print(f"Ascending IDs: {asc_ids}")
        print(f"Descending IDs: {desc_ids}")
        return False
    
    # Check if the first items are different
    if asc_results["items"][0]["id"] == desc_results["items"][0]["id"]:
        print("WARNING: First item is the same for both ascending and descending sorts!")
        print(f"Ascending first item: {asc_results['items'][0]}")
        print(f"Descending first item: {desc_results['items'][0]}")
        return False
    
    print("Success! Ascending and descending sorts return different results.")
    print(f"Ascending first item: {asc_results['items'][0]['name']} (ID: {asc_results['items'][0]['id']})")
    print(f"Descending first item: {desc_results['items'][0]['name']} (ID: {desc_results['items'][0]['id']})")
    
    return True

def test_sorting():
    """Test that sorting works correctly"""
    print("Testing sorting functionality...")
    
    # Get authentication token
    token = get_token()
    print("Successfully authenticated")
    
    # Test sorting by name
    print("\nTesting sorting by name...")
    asc_results = get_resources(token, sort_by="name", sort_order="asc")
    print(f"Got {len(asc_results['items'])} resources with ascending sort")
    
    desc_results = get_resources(token, sort_by="name", sort_order="desc")
    print(f"Got {len(desc_results['items'])} resources with descending sort")
    
    name_sort_works = compare_results(asc_results, desc_results)
    
    # Test sorting by id
    print("\nTesting sorting by id...")
    asc_results = get_resources(token, sort_by="id", sort_order="asc")
    print(f"Got {len(asc_results['items'])} resources with ascending sort")
    
    desc_results = get_resources(token, sort_by="id", sort_order="desc")
    print(f"Got {len(desc_results['items'])} resources with descending sort")
    
    id_sort_works = compare_results(asc_results, desc_results)
    
    # Print overall result
    if name_sort_works and id_sort_works:
        print("\nAll sorting tests passed!")
        return True
    else:
        print("\nSome sorting tests failed!")
        return False

if __name__ == "__main__":
    success = test_sorting()
    sys.exit(0 if success else 1)
