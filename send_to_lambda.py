import json
import requests
import sys

def main():
    with open('last_entry.json') as f:
        last_entry = json.load(f)

    if not last_entry:
        print('No valid last entry found.')
        sys.exit(1)

    name = last_entry.get('name', '')
    email = last_entry.get('email', '')

    response = requests.post(
        url=sys.argv[1],
        headers={
            'Content-Type': 'application/json',
            'x-api-key': sys.argv[2]
        },
        json={
            'userName': name,
            'email': email
        }
    )
    print(response.status_code, response.text)

if __name__ == "__main__":
    main()
