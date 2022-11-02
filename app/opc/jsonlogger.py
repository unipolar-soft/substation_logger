import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

file_path = script_dir + "\local\interruption_log.json"

print(file_path)

def write_json(data, filename=file_path):
    with open(filename, 'r+') as log_file:
        log_data = json.load(log_file)
        log_data['logs'].append(data)
        log_file.seek(0)
        json.dump(log_data, log_file, indent=4)

if __name__ == "__main__":
    y = {
        "emp_name":"Aukhilesh",
        "email": "Aukhilesh@geeksforgeeks.org",
        "job_profile": "Full Time"
        }
        
    write_json(y)