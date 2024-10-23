from __future__ import print_function

import os
import pickle
import time
import requests
import json
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

# OPENQUESTION data
OPENQUESTION_DATA = 'A!S2:S'
FILENAME_DATA = 'A!B2:B'  # 用于文件名的数据范围

# 改2：下载的文件位置
DOWNLOAD_FOLDER = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\largescale_result\summary_task\summary_data\openquestion_rawdata'


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
                r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\credentials\client_secret_65741441027-cium21duh9skfmnnmjd4h2fk4ccb51s4.apps.googleusercontent.com.json',
                SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    max_retries = 5
    retry_delay = 5  # 秒

    for retry in range(max_retries):
        try:
            # 获取答案数据
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=OPENQUESTION_DATA).execute()
            answers = result.get('values', [])

            # 获取文件名数据
            filename_result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                 range=FILENAME_DATA).execute()
            filenames = filename_result.get('values', [])

            if not answers or not filenames:
                print('No data found.')
            else:
                for filename_row, answer_row in zip(filenames, answers):
                    if filename_row and answer_row:  # 确保两行都有值
                        user_name = filename_row[0]
                        answer = answer_row[0]

                        # 创建用户数据字典
                        user_data = {
                            "answer": answer
                        }

                        # 生成安全的文件名
                        safe_filename = "".join(c for c in user_name if c.isalnum() or c in (' ', '.', '_')).rstrip()
                        output_file = os.path.join(DOWNLOAD_FOLDER, f'{safe_filename}.json')

                        # 将用户数据保存到单独的 JSON 文件中
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(user_data, f, ensure_ascii=False, indent=4)

                        print(f'User answer for {user_name} has been saved to {output_file}')

                print("All user answers have been saved to individual files.")
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