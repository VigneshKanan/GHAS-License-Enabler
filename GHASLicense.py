import csv
import requests
from datetime import datetime

# Replace with your GitHub personal access token
auth_token = '<YOUR_GITHUB_TOKEN>' //Scope of pat > Admin : write

# Replace with the path to your CSV file
csv_file_path = 'GHASRepos.csv'

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
log_file_name = f"log_{timestamp}.txt"

# Function to update repository based on CSV data
def update_repository(owner, repo, data):
    url = f'https://api.github.com/repos/{owner}/{repo}'
    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    payload = {
        'security_and_analysis': {
            'advanced_security': {'status': 'enabled'},
            'secret_scanning': {'status': 'enabled'},
            'secret_scanning_push_protection': {'status': 'enabled'},
            'secret_scanning_validity_checks': {'status': 'enabled'},
        }
    }

    try:
        log_to_file(f"Repository '{owner}/{repo}' updated Initiated.\n")
        response = requests.patch(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Repository '{owner}/{repo}' updated successfully.")
        log_to_file(f"Repository '{owner}/{repo}' updated successfully.\n")
    except requests.exceptions.RequestException as err:
        print(f"Error updating repository '{owner}/{repo}': {err}")
        log_to_file(f"Error updating repository '{owner}/{repo}': \n{err}\n")


# Function to read CSV data and update repositories
def update_repositories_from_csv():
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                owner = 'DigitalInnovation'  
                repo = row['GHAS Repos']  
                update_repository(owner, repo, row)
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        log_to_file(f"Error processing CSV file: {e}\n")

# Function to log messages to a file
def log_to_file(message):
    with open(log_file_name, 'a') as log_file:
        log_file.write(f"{message}\n")

# Functional usage
update_repositories_from_csv()
