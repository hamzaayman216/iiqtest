import http.client
import json
import os

def get_sailpoint_users(api_url, auth_header):
    """Retrieves all users from SailPoint."""
    conn = http.client.HTTPConnection(api_url, 8080)
    
    headers = {
        'Accept': 'application/json',
        'Authorization': auth_header
    }

    conn.request("GET", "/identityiq/scim/v2/Users", headers=headers)
    res = conn.getresponse()
    data = res.read()
    
    if res.status != 200:
        raise Exception(f"Failed to retrieve users from SailPoint: {res.status}")
    
    sailpoint_users = json.loads(data.decode("utf-8")).get("Resources", [])
    return sailpoint_users

def delete_sailpoint_user(user_id, api_url, auth_header):
    """Deletes a user from SailPoint."""
    conn = http.client.HTTPConnection(api_url, 8080)
    
    headers = {
        'Authorization': auth_header
    }

    conn.request("DELETE", f"/identityiq/scim/v2/Users/{user_id}", headers=headers)
    res = conn.getresponse()
    
    if res.status != 204:
        raise Exception(f"Failed to delete user from SailPoint: {res.status}")
    
    return True

if __name__ == "__main__":
    # Test SailPoint user retrieval
    api_url = os.getenv('SAILPOINT_API_URL', 'localhost') 
    auth_header = os.getenv('SAILPOINT_AUTH_HEADER', '') 

    users = get_sailpoint_users(api_url, auth_header)
    print(f"Retrieved users from SailPoint: {users}")
