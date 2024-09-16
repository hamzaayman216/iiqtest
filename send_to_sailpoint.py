import http.client
import json
import os

def format_user_details(user_name):
    """Formats user details for the SailPoint API."""
    name_parts = user_name.split(' ')
    if len(name_parts) > 1:
        given_name = name_parts[0]
        family_name = ' '.join(name_parts[1:])
        display_name = user_name
    else:
        given_name = user_name
        family_name = ''
        display_name = user_name

    return family_name, given_name, display_name

def send_to_sailpoint(user_name, email, api_url, auth_header):
    """Sends user creation request to SailPoint."""
    conn = http.client.HTTPConnection(api_url, 8080)

    family_name, given_name, display_name = format_user_details(user_name)

    payload = json.dumps({
        "userName": user_name,
        "name": {
            "formatted": display_name,
            "familyName": family_name,
            "givenName": given_name
        },
        "displayName": display_name,
        "userType": "employee",
        "active": True,
        "password": "string",  # Placeholder for the password
        "emails": [
            {
                "type": "work",
                "value": email,
                "primary": "true"
            }
        ],
    })

    headers = {
        'Content-Type': 'application/scim+json',
        'Accept': 'application/json',
        'Authorization': auth_header
    }

    conn.request("POST", "/identityiq/scim/v2/Users", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return {
        'statusCode': res.status,
        'body': data.decode("utf-8")
    }

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
    
    response_data = json.loads(data.decode("utf-8"))
    
    users = []
    for user in response_data.get("Resources", []):
        user_data = {
            'id': user.get('id'),
            'userName': user.get('userName'),
            'displayName': user.get('name', {}).get('displayName'),
            'emails': [email.get('value') for email in user.get('emails', [])],
            'active': user.get('active')
        }
        users.append(user_data)
    
    return users

def delete_user_in_sailpoint(user_id, api_url, auth_header):
    """Deletes a user from SailPoint by user ID."""
    conn = http.client.HTTPConnection(api_url, 8080)
    
    headers = {
        'Authorization': auth_header
    }

    conn.request("DELETE", f"/identityiq/scim/v2/Users/{user_id}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    return {
        'statusCode': res.status,
        'body': data.decode("utf-8")
    }

if __name__ == "__main__":
    # Load CSV comparison logic here or handle it via another script.
    print("This module handles sending, retrieving, and deleting users in SailPoint.")
