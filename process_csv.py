import csv
import json
import sys

def extract_last_entry(csv_file_path):
    last_entry = None
    try:
        with open(csv_file_path, 'r') as file:
            reader = list(csv.reader(file))
            if reader:
                last_entry = reader[-1]
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return last_entry

def save_entry_to_json(entry, json_file_path):
    if entry:
        entry_json = {
            "name": entry[0],
            "email": entry[1]
        }
        with open(json_file_path, 'w') as file:
            json.dump(entry_json, file)
    else:
        with open(json_file_path, 'w') as file:
            json.dump({}, file)

if __name__ == "__main__":
    csv_file_path = 'data.csv'
    json_file_path = 'last_entry.json'

    last_entry = extract_last_entry(csv_file_path)
    save_entry_to_json(last_entry, json_file_path)
