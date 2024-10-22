from __future__ import print_function
import pickle
import os.path
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


# 修改要查找的位置
SAMPLE_SPREADSHEET_ID = '1HbzMp12uIqBqLIZsRn59sB0pvdn__A8RXVzp5ltEp1M'
SAMPLE_RANGE_NAME = 'D!F2:G'  # 修改为包含F和G列

# 下载文件夹路径
DOWNLOAD_FOLDER_GPT = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\109_pilot_result\\drive_GPT_data'
DOWNLOAD_FOLDER_TASKSHEET = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\109_pilot_result\\drive_Tasksheet_data'



def download_file_from_google_drive(file_id, destination):
    URL = "https://www.googleapis.com/drive/v3/files/{}?alt=media".format(file_id)
    session = requests.Session()

    headers = {"Authorization": "Bearer {}".format(creds.token)}
    response = session.get(URL, headers=headers, stream=True)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)


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
                'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_30ppl\\client_secret_65741441027-cium21duh9skfmnnmjd4h2fk4ccb51s4.apps.googleusercontent.com.json',
                SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    # 获取U列的用户序号
    user_numbers = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                      range='D!U2:U').execute().get('values', [])

    if not values:
        print('No rawdata found.')
    else:
        for i, (row, user_number) in enumerate(zip(values, user_numbers), start=1):
            if len(row) >= 2:  # 确保行至少有两列
                # 下载F列文件
                if row[0]:  # 检查F列是否有值
                    file_id = row[0].split('id=')[-1]
                    destination = os.path.join(DOWNLOAD_FOLDER_GPT, f'user_{user_number[0]}_GPT.json')
                    print(f'Downloading GPT file for user {user_number[0]} to {destination}')
                    download_file_from_google_drive(file_id, destination)

                # 下载G列文件
                if len(row) > 1 and row[1]:  # 检查G列是否有值
                    file_id = row[1].split('id=')[-1]
                    destination = os.path.join(DOWNLOAD_FOLDER_TASKSHEET, f'user_{user_number[0]}_Tasksheet.json')
                    print(f'Downloading Tasksheet file for user {user_number[0]} to {destination}')
                    download_file_from_google_drive(file_id, destination)


if __name__ == '__main__':
    main()