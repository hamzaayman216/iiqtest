import csv
import json
import os
import logging
from send_to_sailpoint import send_to_sailpoint, get_sailpoint_usernames, delete_user_from_sailpoint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_csv_file(csv_file_path):
    csv_users = {}
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip the header row
            for row in reader:
                if len(row) >= 2:
                    user_name = row[0].strip()
                    email = row[1].strip()
                    if user_name and email:
                        csv_users[user_name] = email
    except FileNotFoundError:
        logging.error(f"File not found: {csv_file_path}")
        raise
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise
    return csv_users

def main():
    csv_file_path = os.getenv('CSV_FILE_PATH', 'data.csv')
    api_url = os.getenv('SAILPOINT_API_URL', 'localhost')
    auth_header = os.getenv('SAILPOINT_AUTH_HEADER', '')

    logging.info(f"Processing CSV file: {csv_file_path}")

    csv_users = process_csv_file(csv_file_path)
    csv_usernames = set(csv_users.keys())

    sailpoint_usernames = set(get_sailpoint_usernames(api_url, auth_header))

    users_to_delete = sailpoint_usernames - csv_usernames
    users_to_create = csv_usernames - sailpoint_usernames

    for user_name in users_to_delete:
        if user_name != 'spadmin':  # Exclude 'spadmin' from deletion
            response = delete_user_from_sailpoint(user_name, api_url, auth_header)
            logging.info(f"Deleted user {user_name}: {response}")

    for user_name in users_to_create:
        email = csv_users[user_name]
        response = send_to_sailpoint(user_name, email, api_url, auth_header)
        logging.info(f"Created user {user_name}: Status Code {response['statusCode']}")

if __name__ == "__main__":
    main()
