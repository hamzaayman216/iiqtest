import csv
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_users_from_csv(csv_file_path):
    """Extracts all users from the CSV file."""
    users = []
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:  # Ensure row has enough columns (userName and email)
                    user_name = row[0].strip()
                    email = row[1].strip()
                    users.append({'userName': user_name, 'email': email})
    except FileNotFoundError:
        logging.error(f"File not found: {csv_file_path}")
        raise
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise
    return users

if __name__ == "__main__":
    csv_file_path = os.getenv('CSV_FILE_PATH', 'data.csv')
    logging.info(f"Extracting users from CSV file: {csv_file_path}")
    
    csv_users = extract_users_from_csv(csv_file_path)
    logging.info(f"CSV Users: {csv_users}")
