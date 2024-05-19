# caller_number_processor.py
import os
import requests

def process_caller_number(caller_number):
    url = os.getenv('API_URL')

    data = {
        "caller_number": caller_number
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        print(f"Error: API request failed with status code {response.status_code}")
        return None

    audio_file_path = response.json().get('audio_file_path')

    return audio_file_path