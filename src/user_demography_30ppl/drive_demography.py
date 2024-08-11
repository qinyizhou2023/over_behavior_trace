from __future__ import print_function
import pickle
import os.path
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
from googleapiclient.http import build_http

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly']

# Spreadsheet ID
SAMPLE_SPREADSHEET_ID = '1_EGcwlFPrtT2xt7WKWKfuRgIllJZ4AQDePzVlnDYjJQ'

# Define the ranges and their corresponding headers for each group
ALL_RANGES = {
    'A': {
        'A!G2:G': 'familiarity with AI',
        'A!H2:H': 'usage frequency with AI',
        'A!I2:I': 'personality_Extroversion',
        'A!J2:J': 'personality_Emotional Stability',
        'A!K2:K': 'personality_Agreeableness',
        'A!L2:L': 'personality_Conscientiousness',
        'A!M2:M': 'personality_Intellect/Imagination'
    },
    'B': {
        'B!G2:G': 'familiarity with AI',
        'B!H2:H': 'usage frequency with AI',
        'B!I2:I': 'personality_Extroversion',
        'B!J2:J': 'personality_Emotional Stability',
        'B!K2:K': 'personality_Agreeableness',
        'B!L2:L': 'personality_Conscientiousness',
        'B!M2:M': 'personality_Intellect/Imagination'
    },
    'C': {
        'C!G2:G': 'familiarity with AI',
        'C!H2:H': 'usage frequency with AI',
        'C!I2:I': 'personality_Extroversion',
        'C!J2:J': 'personality_Emotional Stability',
        'C!K2:K': 'personality_Agreeableness',
        'C!L2:L': 'personality_Conscientiousness',
        'C!M2:M': 'personality_Intellect/Imagination'
    },
    'D': {
        'D!G2:G': 'familiarity with AI',
        'D!H2:H': 'usage frequency with AI',
        'D!I2:I': 'personality_Extroversion',
        'D!J2:J': 'personality_Emotional Stability',
        'D!K2:K': 'personality_Agreeableness',
        'D!L2:L': 'personality_Conscientiousness',
        'D!M2:M': 'personality_Intellect/Imagination'
    }
}

# Output folder
OUTPUT_FOLDER = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\user_demography_30ppl\demogrphy_rough'

def download_file_from_google_drive(file_id, destination):
    URL = "https://www.googleapis.com/drive/v3/files/{}?alt=media".format(file_id)
    session = requests.Session()

    headers = {"Authorization": "Bearer {}".format(creds.token)}
    response = session.get(URL, headers=headers, stream=True)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)

def process_group(service, group, ranges):
    results = {}
    for range_name, header in ranges.items():
        result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                     range=range_name).execute()
        values = result.get('values', [])
        results[header] = values

    json_data = []
    for i in range(max(len(values) for values in results.values())):
        row = {'filename': f'{group}{i+1}.json'}
        for header, values in results.items():
            if i < len(values):
                try:
                    row[header] = int(values[i][0])  # Convert to integer if possible
                except ValueError:
                    row[header] = values[i][0]  # Keep as string if not convertible to int
            else:
                row[header] = None  # Use None for missing values
        json_data.append(row)

    return json_data

def main():
    global creds
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\bahaviordata_30ppl\client_secret_65741441027-cium21duh9skfmnnmjd4h2fk4ccb51s4.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Ensure the output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for group, ranges in ALL_RANGES.items():
        json_data = process_group(service, group, ranges)

        # Write to JSON file
        json_file = os.path.join(OUTPUT_FOLDER, f'{group}_demography.json')
        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=2)

        print(f'Results for group {group} saved to {json_file}')

        # Note: File download logic removed as it's not needed in this context

if __name__ == '__main__':
    main()