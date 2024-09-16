import os
import logging
from process_csv import extract_users_from_csv
from send_to_sail_point import send_to_sailpoint
from sailpoint_users import get_sailpoint_users, delete_sailpoint_user

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sync_users(csv_users, sailpoint_users, api_url, auth_header):
    """Synchronizes users between CSV and SailPoint."""
    # Extract userName from SailPoint users
    sailpoint_user_names = {user['userName']: user['id'] for user in sailpoint_users}

    # Track created and deleted users
    created_users = []
    deleted_users = []

    # Compare CSV users with SailPoint users
    for csv_user in csv_users:
        if csv_user['userName'] not in sailpoint_user_names:
            # If the user is not in SailPoint, create the user
            send_to_sailpoint(csv_user['userName'], csv_user['email'], api_url, auth_header)
            created_users.append(csv_user['userName'])
        else:
            # User exists, remove from sailpoint_user_names to avoid deletion
            del sailpoint_user_names[csv_user['userName']]

    # Remaining users in sailpoint_user_names are not present in CSV, delete them
    for user_name, user_id in sailpoint_user_names.items():
        delete_sailpoint_user(user_id, api_url, auth_header)
        deleted_users.append(user_name)

    return created_users, deleted_users

if __name__ == "__main__":
    # Set file paths and retrieve environment variables
    csv_file_path = os.getenv('CSV_FILE_PATH', 'data.csv')
    api_url = os.getenv('SAILPOINT_API_URL', 'localhost') 
    auth_header = os.getenv('SAILPOINT_AUTH_HEADER', '') 

    logging.info("Starting user synchronization process...")

    # Extract users from CSV
    csv_users = extract_users_from_csv(csv_file_path)

    # Retrieve users from SailPoint
    sailpoint_users = get_sailpoint_users(api_url, auth_header)

    # Sync users between CSV and SailPoint
    created, deleted = sync_users(csv_users, sailpoint_users, api_url, auth_header)

    logging.info(f"Created users: {created}")
    logging.info(f"Deleted users: {deleted}")
    logging.info("User synchronization completed.")
