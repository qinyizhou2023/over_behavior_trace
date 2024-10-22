# -*- coding: utf-8 -*-
import pandas as pd
import os
import shutil
import re
from chardet import detect


def get_file_encoding(folder_path):
    """检测文件编码"""
    with open(folder_path, 'rb') as file:
        raw_data = file.read()
    return detect(raw_data)['encoding']


def read_csv_with_encoding(folder_path):
    """尝试使用不同的编码读取CSV文件"""
    encodings = ['utf-8', 'gbk', 'gb18030', 'gb2312', 'utf-16']

    # 首先尝试检测编码
    detected_encoding = get_file_encoding(folder_path)
    if detected_encoding:
        encodings.insert(0, detected_encoding)

    for encoding in encodings:
        try:
            print(f"尝试使用 {encoding} 编码读取文件...")
            df = pd.read_csv(folder_path, encoding=encoding)
            print(f"成功使用 {encoding} 编码读取文件")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"使用 {encoding} 编码时发生错误: {str(e)}")
            continue

    raise Exception("无法使用任何已知编码读取文件")


def rename_files(folder_path):
    """批量重命名文件"""
    try:
        # 确保文件夹存在
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"找不到文件夹: {folder_path}")

        print(f"开始处理文件夹: {folder_path}")

        # 用于记录处理结果
        success_count = 0
        fail_count = 0
        results = []

        # 获取文件夹中的所有文件
        files = os.listdir(folder_path)

        for file_name in files:
            try:
                # 使用正则表达式匹配"序号"后的四位数
                match = re.search(r'序号(\d{4})', file_name)

                if match:
                    number = match.group(1)  # 提取的四位数
                    # 保持原始扩展名
                    _, ext = os.path.splitext(file_name)
                    new_name = f"{number}{ext}"

                    # 构建完整的文件路径
                    old_path = os.path.join(folder_path, file_name)
                    new_path = os.path.join(folder_path, new_name)

                    # 检查新文件名是否已存在
                    if os.path.exists(new_path):
                        print(f"警告: 文件 {new_name} 已存在，跳过重命名 {file_name}")
                        results.append({
                            'original': file_name,
                            'new': new_name,
                            'status': 'skipped',
                            'reason': 'file already exists'
                        })
                        fail_count += 1
                        continue

                    # 重命名文件
                    os.rename(old_path, new_path)
                    success_count += 1
                    results.append({
                        'original': file_name,
                        'new': new_name,
                        'status': 'success'
                    })
                    print(f"成功: {file_name} -> {new_name}")

                else:
                    print(f"跳过: {file_name} (未找到匹配的序号)")
                    results.append({
                        'original': file_name,
                        'status': 'skipped',
                        'reason': 'no match found'
                    })
                    fail_count += 1

            except Exception as e:
                print(f"处理文件 {file_name} 时发生错误: {str(e)}")
                results.append({
                    'original': file_name,
                    'status': 'error',
                    'reason': str(e)
                })
                fail_count += 1

        # 打印总结
        print("\n处理完成!")
        print(f"成功处理: {success_count} 个文件")
        print(f"失败/跳过: {fail_count} 个文件")

        return results

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None


def main():
    # 指定要处理的文件夹路径
    folder_path = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\largescale_result\tripplanning_task\tripplanning_data\downlaod_wjx\tasksheet_rawdata'  # 请替换为你的文件夹路径

    print("文件重命名工具")
    print("-" * 50)

    # 确认操作
    print(f"\n将要处理文件夹: {folder_path}")
    confirm = input("确定要继续吗? (y/n): ").lower()

    if confirm == 'y':
        results = rename_files(folder_path)

        if results:
            # 打印详细结果
            print("\n详细处理结果:")
            for result in results:
                if result['status'] == 'success':
                    print(f"成功: {result['original']} -> {result['new']}")
                elif result['status'] == 'skipped':
                    print(f"跳过: {result['original']} ({result['reason']})")
                else:
                    print(f"错误: {result['original']} ({result['reason']})")
    else:
        print("操作已取消")


if __name__ == "__main__":
    main()