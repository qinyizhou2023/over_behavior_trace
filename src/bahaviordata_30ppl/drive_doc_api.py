from __future__ import print_function
import pickle
import os.path
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly']


# 改1：修改要查找的位置（注意第一个为下面的form名称）
SAMPLE_SPREADSHEET_ID = '1_EGcwlFPrtT2xt7WKWKfuRgIllJZ4AQDePzVlnDYjJQ'
# # A GPT
# SAMPLE_RANGE_NAME = 'A!R2:R9'
# # A tasksheet
# SAMPLE_RANGE_NAME = 'A!S2:S9'

## B GPT
# SAMPLE_RANGE_NAME = 'B!R2:R7'
## B tasksheet
# SAMPLE_RANGE_NAME = 'B!S2:S7'

## C GPT
# SAMPLE_RANGE_NAME = 'C!V2:V8'
## C tasksheet
# SAMPLE_RANGE_NAME = 'C!W2:W8'

# D GPT
# SAMPLE_RANGE_NAME = 'D!V2:V7'
# # D tasksheet
SAMPLE_RANGE_NAME = 'D!W2:W7'


def download_file_from_google_drive(file_id, destination):
    URL = "https://www.googleapis.com/drive/v3/files/{}?alt=media".format(file_id)
    session = requests.Session()

    headers = {"Authorization": "Bearer {}".format(creds.token)}
    response = session.get(URL, headers=headers, stream=True)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)

#改2：下载的文件位置
DOWNLOAD_FOLDER = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_30ppl\\tasksheet'
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
                'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_30ppl\\client_secret_65741441027-cium21duh9skfmnnmjd4h2fk4ccb51s4.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for i, row in enumerate(values, start=1):
            if row:  # Check if the row has any values
                file_id = row[0].split('id=')[-1]
                destination = os.path.join(DOWNLOAD_FOLDER, f'D{i}.json') # Adjust the extension according to the file type
                print(f'Downloading file from link {row[0]} to {destination}')
                download_file_from_google_drive(file_id, destination)
#改3：修改上面就可以改名字

if __name__ == '__main__':
    main()
