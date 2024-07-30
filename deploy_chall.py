import os
import requests
import yaml

CTFD_URL = os.environ['CTFD_URL']
API_TOKEN = os.environ['CTFD_ADMIN_TOKEN']
HEADERS = {
    'Authorization': f'Token {API_TOKEN}',
    'Content-Type': 'application/json'
}

def deploy_challenge(challenge_path):
    with open(os.path.join(challenge_path, 'challenge.yml'), 'r') as f:
        challenge_data = yaml.safe_load(f)

    # Create the challenge
    response = requests.post(f'{CTFD_URL}/api/v1/challenges', headers=HEADERS, json=challenge_data)
    if response.status_code != 200:
        print(f"Failed to create challenge {challenge_data['name']}: {response.text}")
        return

    challenge_id = response.json()['data']['id']

    # Upload the challenge files
    files_path = os.path.join(challenge_path, 'files')
    for file_name in os.listdir(files_path):
        with open(os.path.join(files_path, file_name), 'rb') as f:
            files = {'file': (file_name, f)}
            response = requests.post(f'{CTFD_URL}/api/v1/files?challenge_id={challenge_id}', headers=HEADERS, files=files)
            if response.status_code != 200:
                print(f"Failed to upload file {file_name} for challenge {challenge_data['name']}: {response.text}")
                return

    print(f"Challenge {challenge_data['name']} deployed successfully")

if __name__ == "__main__":
    challenges_dir = 'challenges'
    for challenge_name in os.listdir(challenges_dir):
        challenge_path = os.path.join(challenges_dir, challenge_name)
        if os.path.isdir(challenge_path):
            deploy_challenge(challenge_path)
