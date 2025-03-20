import requests
import time

# Replace with your GitHub organization name and personal access token
ORG_NAME = 'your_org_name'
TOKEN = 'your_personal_access_token'

# GitHub API URL
API_URL = f'https://api.github.com/orgs/{ORG_NAME}/repos'

# Function to check the current rate limit
def check_rate_limit():
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    if response.status_code == 200:
        return response.json()['rate']['remaining'], response.json()['rate']['reset']
    else:
        print(f'Failed to check rate limit: {response.status_code} - {response.text}')
        return 0, 0

# Function to create a repository
def create_repo(repo_name):
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': repo_name,
        'private': False  # Change to True if you want a private repo
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f'Repository "{repo_name}" created successfully.')
    elif response.status_code == 422:
        print(f'Repository "{repo_name}" already exists.')
    elif response.status_code == 403:
        print('Rate limit exceeded. Waiting for reset...')
        reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
        wait_time = reset_time - int(time.time())
        time.sleep(wait_time + 5)  # Wait for the rate limit to reset
        create_repo(repo_name)  # Retry creating the repo
    else:
        print(f'Failed to create repository "{repo_name}": {response.status_code} - {response.text}')

# Function to create multiple repositories with rate limit handling
def create_multiple_repos(repo_names):
    for repo_name in repo_names:
        remaining_requests, reset_time = check_rate_limit()
        
        if remaining_requests < 1:
            wait_time = reset_time - int(time.time())
            print(f'Rate limit reached. Waiting for {wait_time + 5} seconds...')
            time.sleep(wait_time + 5)  # Wait for the rate limit to reset
        
        create_repo(repo_name)
        time.sleep(1)  # Optional: Sleep to space out requests

# List of repository names to create
repo_names = [f'repo-{i}' for i in range(1, 101)]  # Change the range as needed

# Create repositories
create_multiple_repos(repo_names)
