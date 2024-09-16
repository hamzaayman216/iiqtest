import http.client
import json
import os

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

    conn.request("POST", "/identityiq/scim/v2/Users", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return {
        'statusCode': res.status,
        'body': data.decode("utf-8")
    }

if __name__ == "__main__":
    with open('last_entry.json') as json_file:
        data = json.load(json_file)
    
    user_name = data.get('userName', 'defaultUserName')
    email = data.get('email', 'default@example.com')
    
    api_url = os.getenv('SAILPOINT_API_URL', 'localhost') 
    auth_header = os.getenv('SAILPOINT_AUTH_HEADER', '') 

    response = send_to_sailpoint(user_name, email, api_url, auth_header)
    print(f"Status Code: {response['statusCode']}")
