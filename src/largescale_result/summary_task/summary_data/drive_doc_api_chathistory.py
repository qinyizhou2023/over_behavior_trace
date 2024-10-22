from __future__ import print_function

import os
import pickle
import time
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# 设置代理（如果需要）
os.environ['HTTP_PROXY'] = 'http://localhost:15236'
os.environ['HTTPS_PROXY'] = 'http://localhost:15236'

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly']

# 改1：修改要查找的位置（注意第一个为下面的form名称）
SAMPLE_SPREADSHEET_ID = '1YdZHoKNUerpQm022fLJs0Fmu13eM1yHuWI3vIsfgcD4'

# chathistory rawdata
CHATHISTORY_DATA = 'A!F2:F'
FILENAME_DATA = 'A!B2:B'  # 用于文件名的数据范围

def download_file_from_google_drive(file_id, destination, creds):
    URL = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    headers = {"Authorization": f"Bearer {creds.token}"}
    response = requests.get(URL, headers=headers, stream=True)
    response.raise_for_status()
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)

#改2：下载的文件位置
DOWNLOAD_FOLDER = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\largescale_result\summary_task\summary_data\chathistory_rawdata'

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
                r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\credentials\client_secret_65741441027-cium21duh9skfmnnmjd4h2fk4ccb51s4.apps.googleusercontent.com.json',SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    max_retries = 5
    retry_delay = 5  # 秒

    for retry in range(max_retries):
        try:
            # 获取tasksheet数据
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=CHATHISTORY_DATA).execute()
            values = result.get('values', [])

            # 获取文件名数据
            filename_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                 range=FILENAME_DATA).execute()
            filenames = filename_result.get('values', [])

            if not values:
                print('No rawdata found.')
            else:
                for (row, filename_row) in zip(values, filenames):
                    if row and filename_row:  # Check if both rows have values
                        file_id = row[0].split('id=')[-1]
                        filename = filename_row[0]  # 使用B列的值作为文件名
                        # 生成文件名
                        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
                        destination = os.path.join(DOWNLOAD_FOLDER, f'{filename}.json')
                        print(f'Downloading file from link {row[0]} to {destination}')
                        download_file_from_google_drive(file_id, destination, creds)
                break  # 如果成功，跳出重试循环


        except (HttpError, TimeoutError, requests.RequestException) as error:
            if retry < max_retries - 1:
                print(f"尝试 {retry + 1}/{max_retries} 失败。等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
            else:
                print("达到最大重试次数，操作失败。")
                raise

if __name__ == '__main__':
    main()