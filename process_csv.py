import csv
import json

def extract_last_entry(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        last_entry = rows[-1] if rows else None
    return last_entry

def main():
    csv_file_path = 'data.csv'  # Path to your CSV file
    last_entry = extract_last_entry(csv_file_path)
    
    if not last_entry or len(last_entry) < 2:
        raise ValueError("Invalid CSV format or insufficient data.")
    
    user_name = last_entry[0]  # Assuming userName is in the first column
    email = last_entry[1]      # Assuming email is in the second column
    
    # Save to JSON file
    data = {
        'userName': user_name,
        'email': email
    }
    with open('last_entry.json', 'w') as json_file:
        json.dump(data, json_file)

if __name__ == "__main__":
    main()
