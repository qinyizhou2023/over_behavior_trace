# -*- coding: utf-8 -*-
import csv
import os
import shutil
import re

def read_csv(file_path):
    encodings = ['utf-8', 'gb2312', 'gbk']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                return list(reader)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to read the CSV file with encodings: {encodings}")

def get_number_mapping(csv_data):
    return {row["序号"]: row["2. Your participant's number "].strip() for row in csv_data}

def process_files(dic_user_files, number_mapping):
    chathistory_folder = 'chathistory_rawdata'
    gpt_folder = 'gpt_rawdata'
    tasksheet_folder = 'tasksheet_rawdata'

    for folder in [chathistory_folder, gpt_folder, tasksheet_folder]:
        os.makedirs(folder, exist_ok=True)

    for filename in os.listdir(dic_user_files):
        match = re.search(r'序号(\d+)', filename)
        if match:
            a_number = match.group(1)
            b_number = number_mapping.get(a_number, a_number)

            new_filename = filename.replace(f'序号{a_number}', f'序号{b_number}')

            if 'cha' in filename.lower():
                destination = os.path.join(chathistory_folder, new_filename)
            elif 'gpt' in filename.lower():
                destination = os.path.join(gpt_folder, new_filename)
            elif 'tas' in filename.lower():
                destination = os.path.join(tasksheet_folder, new_filename)
            else:
                continue

            source_path = os.path.join(dic_user_files, filename)
            try:
                shutil.move(source_path, destination)
                print(f"Moved and renamed: {filename} -> {destination}")
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

def main():
    csv_file_path = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\largescale_result\tripplanning_task\tripplanning_data\downlaod_wjx\tripplanning_new1.csv'
    dic_user_files = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\largescale_result\tripplanning_task\tripplanning_data\downlaod_wjx\tripplanning1'

    csv_data = read_csv(csv_file_path)
    number_mapping = get_number_mapping(csv_data)
    process_files(dic_user_files, number_mapping)

if __name__ == "__main__":
    main()