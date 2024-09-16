import csv
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_last_entry(csv_file_path):
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

def main():
    # Use environment variables or command-line arguments to set file paths
    csv_file_path = os.getenv('CSV_FILE_PATH', 'data.csv')
    
    logging.info(f"Processing CSV file: {csv_file_path}")
    
    last_entry = extract_last_entry(csv_file_path)
    
    if not last_entry or len(last_entry) < 2:
        logging.error("Invalid CSV format or insufficient data.")
        raise ValueError("Invalid CSV format or insufficient data.")
    
    user_name = last_entry[0].strip()  # Remove any leading/trailing whitespace
    email = last_entry[1].strip()      # Remove any leading/trailing whitespace
    
    if not user_name or not email:
        logging.error("User name or email is missing.")
        raise ValueError("User name or email is missing.")
    
    # Save to JSON file
    data = {
        'userName': user_name,
        'email': email
    }
    
    try:
        with open('last_entry.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info("Successfully saved data to last_entry.json")
    except Exception as e:
        logging.error(f"Error writing JSON file: {e}")
        raise

if __name__ == "__main__":
    main()
