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


# 改1：修改要查找的位置（注意第一个为下面的form名称）
SAMPLE_SPREADSHEET_ID = '1_EGcwlFPrtT2xt7WKWKfuRgIllJZ4AQDePzVlnDYjJQ'
# Define the ranges and their corresponding headers for each group
ALL_RANGES = {
    'A': {
        'A!U2:U': 'TRUST1_deceptive',
        'A!V2:V': 'TRUST2_underhanded',
        'A!W2:W': 'TRUST3_ suspicious',
        'A!X2:X': 'TRUST4_wary',
        'A!Y2:Y': 'TRUST5_harmful',
        'A!Z2:Z': 'TRUST6_confident',
        'A!AA2:AA': 'TRUST7_security'
    },
    'B': {
        'B!U2:U': 'TRUST1_deceptive',
        'B!V2:V': 'TRUST2_underhanded',
        'B!W2:W': 'TRUST3_ suspicious',
        'B!X2:X': 'TRUST4_wary',
        'B!Y2:Y': 'TRUST5_harmful',
        'B!Z2:Z': 'TRUST6_confident',
        'B!AA2:AA': 'TRUST7_security'
    },
    'C': {
        'C!U2:U': 'TRUST1_deceptive',
        'C!V2:V': 'TRUST2_underhanded',
        'C!W2:W': 'TRUST3_ suspicious',
        'C!X2:X': 'TRUST4_wary',
        'C!Y2:Y': 'TRUST5_harmful',
        'C!Z2:Z': 'TRUST6_confident',
        'C!AA2:AA': 'TRUST7_security'
    },
    'D': {
        'D!U2:U': 'TRUST1_deceptive',
        'D!V2:V': 'TRUST2_underhanded',
        'D!W2:W': 'TRUST3_ suspicious',
        'D!X2:X': 'TRUST4_wary',
        'D!Y2:Y': 'TRUST5_harmful',
        'D!Z2:Z': 'TRUST6_confident',
        'D!AA2:AA': 'TRUST7_security'
    }
}

# Output folder
OUTPUT_FOLDER = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\user_trust_30ppl\trust_rough'

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
        json_file = os.path.join(OUTPUT_FOLDER, f'{group}_trust.json')
        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=2)

        print(f'Results for group {group} saved to {json_file}')

        # Note: File download logic removed as it's not needed in this context

if __name__ == '__main__':
    main()

