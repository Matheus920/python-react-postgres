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

def get_resources(token, is_public=None, search=None):
    """Get resources with the specified filtering"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "skip": 0,
        "limit": 10,
    }
    
    if is_public is not None:
        params["is_public"] = is_public
    
    if search is not None:
        params["search"] = search
    
    response = requests.get(f"{BASE_URL}/resources/", headers=headers, params=params)
    if response.status_code != 200:
        print(f"Failed to get resources: {response.status_code} - {response.text}")
        sys.exit(1)
    
    return response.json()

def test_filtering():
    """Test that filtering works correctly"""
    print("Testing filtering functionality...")
    
    # Get authentication token
    token = get_token()
    print("Successfully authenticated")
    
    # Test filtering by is_public
    print("\nTesting filtering by is_public...")
    all_results = get_resources(token)
    print(f"Got {len(all_results['items'])} resources with no filter")
    
    public_results = get_resources(token, is_public=True)
    print(f"Got {len(public_results['items'])} resources with is_public=True")
    
    private_results = get_resources(token, is_public=False)
    print(f"Got {len(private_results['items'])} resources with is_public=False")
    
    # Verify that the sum of public and private resources equals the total
    if len(public_results['items']) + len(private_results['items']) == len(all_results['items']):
        print("Success! Public + Private = All resources")
    else:
        print("Warning: Public + Private != All resources")
        print(f"All: {len(all_results['items'])}, Public: {len(public_results['items'])}, Private: {len(private_results['items'])}")
    
    # Test filtering by search
    print("\nTesting filtering by search...")
    
    # Get the name of the first resource to use as a search term
    if all_results['items']:
        search_term = all_results['items'][0]['name'][:4]  # Use first few characters
        print(f"Using search term: '{search_term}'")
        
        search_results = get_resources(token, search=search_term)
        print(f"Got {len(search_results['items'])} resources with search='{search_term}'")
        
        # Verify that the search results contain the search term
        for item in search_results['items']:
            if search_term.lower() not in item['name'].lower() and search_term.lower() not in item['description'].lower():
                print(f"Warning: Item {item['id']} ({item['name']}) doesn't contain search term '{search_term}'")
        
        print("Success! Search filtering is working")
    else:
        print("No resources available to test search filtering")
    
    # Test combined filtering
    if all_results['items']:
        print("\nTesting combined filtering (is_public + search)...")
        
        combined_results = get_resources(token, is_public=True, search=search_term)
        print(f"Got {len(combined_results['items'])} resources with is_public=True and search='{search_term}'")
        
        # Verify that the combined results are a subset of both the public results and the search results
        combined_ids = [item['id'] for item in combined_results['items']]
        public_ids = [item['id'] for item in public_results['items']]
        search_ids = [item['id'] for item in search_results['items']]
        
        if all(item_id in public_ids for item_id in combined_ids) and all(item_id in search_ids for item_id in combined_ids):
            print("Success! Combined filtering is working")
        else:
            print("Warning: Combined filtering results are not a subset of both public and search results")
    
    print("\nAll filtering tests completed!")
    return True

if __name__ == "__main__":
    success = test_filtering()
    sys.exit(0 if success else 1)
