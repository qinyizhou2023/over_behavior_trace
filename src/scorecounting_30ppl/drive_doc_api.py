from __future__ import print_function
import pickle
import os.path
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1_EGcwlFPrtT2xt7WKWKfuRgIllJZ4AQDePzVlnDYjJQ'
#改1： 位置
# A moon + with AI +1
# SAMPLE_RANGE_NAME = 'A!P2:P9'
# # A desert+ alone
# SAMPLE_RANGE_NAME = 'A!AG2:AG9'

# B moon + alone + 2
# SAMPLE_RANGE_NAME = 'B!AG2:AG7'
# # B desert+ with ai+ 2
SAMPLE_RANGE_NAME = 'B!P2:P7'

# C moon + alone + 1
# SAMPLE_RANGE_NAME = 'C!P2:P8'
# # D desert+ alone + 2
# SAMPLE_RANGE_NAME = 'C!T2:T8'

# D moon + with AI +2
# SAMPLE_RANGE_NAME = 'D!T2:T7'
# # D desert+ alone
# SAMPLE_RANGE_NAME = 'D!P2:P7'


#改2： 下载地址
# A moon
# OUTPUT_FILE  = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\answers\\A_moon.csv'

# A desert
# OUTPUT_FILE  = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\answers\\A_desert.csv'

# C desert
# OUTPUT_FILE  = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\answers\\C_desert.csv'
# C moon
# OUTPUT_FILE = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\answers\\C_moon.csv'

# B moon
# OUTPUT_FILE = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\answers\\B_moon.csv'
# B desert
OUTPUT_FILE  = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\answers\\B_desert.csv'


#D moon
# OUTPUT_FILE = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\answers\\D_moon.csv'
# D desert
# OUTPUT_FILE  = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\answers\\D_desert.csv'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
        print('No rawdata found.')
    else:
        # Open the CSV file for writing
        with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the rawdata
            for i, row in enumerate(values, start=1):
                if row:  # Check if the row has any values
                    print(f'{row[0]}')
                    writer.writerow([row[0]])
if __name__ == '__main__':
    main()