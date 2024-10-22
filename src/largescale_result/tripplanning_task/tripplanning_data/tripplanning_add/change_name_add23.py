# -*- coding: utf-8 -*-
import os
import re
import shutil
import sys


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))


def safe_rename(old_path, new_path):
    try:
        os.rename(old_path, new_path)
        return True
    except OSError as e:
        safe_print(f"Error renaming file: {e}")
        return False


def organize_and_rename_files(source_folder):
    # 创建目标文件夹
    target_folders = {
        "chathistory_rawdata": "Upload your cha",
        "gpt_rawdata": "Upload your GPT",
        "tasksheet_rawdata": "Upload your tas"
    }

    for folder in target_folders.keys():
        os.makedirs(os.path.join(source_folder, folder), exist_ok=True)

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        if os.path.isfile(os.path.join(source_folder, filename)):
            try:
                # 使用正则表达式匹配序号
                match = re.match(r'序号(\d+)_(.*)', filename)
                if match:
                    old_number = int(match.group(1))
                    new_number = old_number + 23
                    new_filename = f'序号{new_number}_{match.group(2)}'

                    # 确定目标文件夹
                    target_folder = None
                    for folder, keyword in target_folders.items():
                        if keyword in filename:
                            target_folder = folder
                            break

                    old_path = os.path.join(source_folder, filename)
                    if target_folder:
                        # 移动并重命名文件
                        new_path = os.path.join(source_folder, target_folder, new_filename)
                        if safe_rename(old_path, new_path):
                            safe_print(f"Moved and renamed: {filename} -> {new_filename}")
                    else:
                        # 如果文件不属于任何目标文件夹,只重命名
                        new_path = os.path.join(source_folder, new_filename)
                        if safe_rename(old_path, new_path):
                            safe_print(f"Renamed: {filename} -> {new_filename}")
                else:
                    safe_print(f"Skipped: {filename} (doesn't match the expected format)")
            except Exception as e:
                safe_print(f"Error processing file {filename}: {e}")


# 使用脚本
source_folder = r"C:\Users\zqy\Documents\over regression\over_behavior_trace\src\largescale_result\tripplanning_task\tripplanning_data\tripplanning_add\tripplanning_add\raw_data"
organize_and_rename_files(source_folder)