import os
import json
import http.client
from urllib.parse import urlparse

def format_user_details(user_name):
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
        "password": "string",
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

    # Parse the URL
    parsed_url = urlparse(api_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid API URL. It must include http:// or https://")

    conn = http.client.HTTPConnection(parsed_url.netloc) if parsed_url.scheme == 'http' else http.client.HTTPSConnection(parsed_url.netloc)
    conn.request("POST", f'{parsed_url.path}/identityiq/scim/v2/Users', payload, headers)

    res = conn.getresponse()
    data = res.read()

    return {
        'statusCode': res.status,
        'body': data.decode('utf-8')
    }

if __name__ == "__main__":
    # Read data from last_entry.json
    with open('last_entry.json') as json_file:
        data = json.load(json_file)
    
    user_name = data.get('userName', 'defaultUserName')
    email = data.get('email', 'default@example.com')
    
    # Retrieve secrets from environment variables
    api_url = os.getenv('SAILPOINT_API_URL')
    auth_header = os.getenv('SAILPOINT_AUTH_HEADER')

    if not api_url or not auth_header:
        print("API URL or Authorization Header is missing.")
        exit(1)

    response = send_to_sailpoint(user_name, email, api_url, auth_header)
    print(f"Status Code: {response['statusCode']}")
    print(f"Response Body: {response['body']}")
