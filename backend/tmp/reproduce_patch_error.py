import requests
import sys

def test_community_update():
    base_url = "http://localhost:8000/api/v1/communities"
    community_id = 6  # MaiCommunity for example
    
    # Try to update code with a value that should be valid
    payload = {
        "code": "NewCode123!"
    }
    
    print(f"Testing PATCH to {base_url}/{community_id} with {payload}")
    try:
        response = requests.patch(f"{base_url}/{community_id}", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("SUCCESS: Community code updated.")
            # Revert to original if possible or keep track
        else:
            print("FAILED: Server rejected the update.")
            
    except Exception as e:
        print(f"ERROR connecting to server: {e}")

if __name__ == "__main__":
    test_community_update()
