# -*- coding: utf-8 -*-
import pandas as pd
import os
import shutil
import re
from chardet import detect


def get_file_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return detect(raw_data)['encoding']


def read_csv_with_encoding(file_path):
    """尝试使用不同的编码读取CSV文件"""
    encodings = ['utf-8', 'gbk', 'gb18030', 'gb2312', 'utf-16']

    # 首先尝试检测编码
    detected_encoding = get_file_encoding(file_path)
    if detected_encoding:
        encodings.insert(0, detected_encoding)

    for encoding in encodings:
        try:
            print(f"尝试使用 {encoding} 编码读取文件...")
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"成功使用 {encoding} 编码读取文件")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"使用 {encoding} 编码时发生错误: {str(e)}")
            continue

    raise Exception("无法使用任何已知编码读取文件")


def process_file(file_path, number_mapping, output_base_path, rel_path):
    """处理单个文件"""
    file_name = os.path.basename(file_path)
    match = re.search(r'序号(\d+)', file_name)

    if match:
        file_number = int(match.group(1))
        if file_number in number_mapping:
            participant_number = number_mapping[file_number]
            _, ext = os.path.splitext(file_name)
            new_filename = f"{participant_number}{ext}"

            # 构建输出路径，保持相对路径结构
            output_dir = os.path.join(output_base_path, rel_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            dst_path = os.path.join(output_dir, new_filename)

            try:
                shutil.copy2(file_path, dst_path)
                return {
                    'original_file': file_path,
                    'new_file': dst_path,
                    'status': 'success'
                }
            except Exception as e:
                return {
                    'original_file': file_path,
                    'error': str(e),
                    'status': 'failed'
                }
        else:
            return {
                'original_file': file_path,
                'error': 'No matching participant number found',
                'status': 'failed'
            }
    return {
        'original_file': file_path,
        'error': 'Could not extract number from filename',
        'status': 'failed'
    }


def rename_files_recursive(csv_path, input_folder, output_folder):
    """递归处理所有子文件夹中的文件"""
    try:
        # 读取CSV文件
        print("开始读取CSV文件...")
        df = read_csv_with_encoding(csv_path)
        print("CSV文件读取成功")

        # 创建编号映射字典
        number_mapping = dict(
            zip(df["序号"], df["2. Your participant's number"]))
        print("\n创建的映射字典：")
        print(number_mapping)

        # 确保输出根文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"\n创建输出根文件夹: {output_folder}")

        results = []
        input_folder_len = len(input_folder)

        # 遍历所有子文件夹
        for root, dirs, files in os.walk(input_folder):
            # 计算相对路径
            rel_path = root[input_folder_len:].lstrip(os.sep)
            print(f"\n处理文件夹: {rel_path or '根目录'}")

            # 处理当前文件夹中的所有文件
            for file in files:
                file_path = os.path.join(root, file)
                print(f"处理文件: {file}")

                result = process_file(
                    file_path=file_path,
                    number_mapping=number_mapping,
                    output_base_path=output_folder,
                    rel_path=rel_path
                )
                results.append(result)

        return results

    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        raise


def main():
    try:
        # 设置路径
        csv_path = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\largescale_result\tripplanning_task\tripplanning_data\tripplanning_new1.csv'
        input_folder = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\largescale_result\tripplanning_task\tripplanning_data\tripplanning_add\tripplanning_add\raw_data'  # 父文件夹路径
        output_folder = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\largescale_result\tripplanning_task\tripplanning_data\downlaod_wjx_2'  # 新的输出父文件夹

        print(f"CSV文件路径: {csv_path}")
        print(f"输入父文件夹: {input_folder}")
        print(f"输出父文件夹: {output_folder}")

        # 检查文件和文件夹是否存在
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"找不到CSV文件: {csv_path}")
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"找不到输入文件夹: {input_folder}")

        # 执行重命名操作
        results = rename_files_recursive(csv_path, input_folder, output_folder)

        # 打印处理结果
        print("\n处理结果汇总:")
        success_count = sum(1 for r in results if r['status'] == 'success')
        fail_count = sum(1 for r in results if r['status'] == 'failed')

        print(f"成功处理文件数: {success_count}")
        print(f"失败处理文件数: {fail_count}")

        # 打印详细信息
        print("\n详细信息:")
        for result in results:
            if result['status'] == 'success':
                print(f"成功: {result['original_file']} -> {result['new_file']}")
            else:
                print(f"失败: {result['original_file']} - 错误: {result['error']}")

    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    main()