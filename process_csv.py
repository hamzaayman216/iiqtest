import csv
import json
import os
import logging
from send_to_sail_point import send_to_sailpoint, get_sailpoint_users, delete_user_in_sailpoint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_last_entry(csv_file_path):
    """Extracts the last entry from the provided CSV file."""
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            last_entry = rows[-1] if rows else None
    except FileNotFoundError:
        logging.error(f"File not found: {csv_file_path}")
        raise
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise
    return last_entry

def compare_and_sync_users(csv_file_path, api_url, auth_header):
    """Compares CSV users with SailPoint users and syncs the data."""
    logging.info("Starting comparison and synchronization process.")
    
    # Extract last entry from the CSV file
    last_entry = extract_last_entry(csv_file_path)
    if not last_entry or len(last_entry) < 2:
        logging.error("Invalid CSV format or insufficient data.")
        raise ValueError("Invalid CSV format or insufficient data.")

    # Retrieve the latest list of users from SailPoint
    sailpoint_users = get_sailpoint_users(api_url, auth_header)
    sailpoint_usernames = {user['userName']: user for user in sailpoint_users}

    # Extract user info from the CSV file
    csv_users = []
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                user_name = row[0].strip()
                email = row[1].strip()
                csv_users.append((user_name, email))

    csv_usernames = {user[0] for user in csv_users}

    # Users to be added
    for user_name, email in csv_users:
        if user_name not in sailpoint_usernames:
            logging.info(f"Creating new user in SailPoint: {user_name}")
            send_to_sailpoint(user_name, email, api_url, auth_header)

    # Users to be deleted
    for sailpoint_user in sailpoint_users:
        if sailpoint_user['userName'] not in csv_usernames:
            logging.info(f"Deleting user from SailPoint: {sailpoint_user['userName']}")
            delete_user_in_sailpoint(sailpoint_user['id'], api_url, auth_header)

def main():
    """Main function to execute the CSV comparison and sync process."""
    csv_file_path = os.getenv('CSV_FILE_PATH', 'data.csv')
    api_url = os.getenv('SAILPOINT_API_URL', 'localhost')
    auth_header = os.getenv('SAILPOINT_AUTH_HEADER', '')

    logging.info(f"Processing CSV file: {csv_file_path}")
    compare_and_sync_users(csv_file_path, api_url, auth_header)

if __name__ == "__main__":
    main()
