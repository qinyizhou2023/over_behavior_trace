import json

# 只改： 定义文件路径
# #tasksheet:
# input_file_path =  'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_40ppl\\behavior_result_tasksheet.json'
# output_file_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_40ppl\\merge_data_tasksheet.json'
# # # gpt:
input_file_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_40ppl\\behavior_result_gpt.json'
output_file_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_40ppl\\merge_data_gpt.json'

# 定义分数列表 (calculate_minus手动传数据)
scores_list = [
    {'B1': 34, 'B2': -1, 'B3': 8, 'B4': 36, 'B5': 16, 'B6': -5, 'B7': 8, 'B8': 18, 'B9': 12, 'C1': 51, 'C2': 18, 'C3': -7, 'C4': 43, 'C5': 37, 'C6': 32.2, 'C7': 26, 'C8': 25, 'C9': 33, 'C10': 2.2},
    {'A1': 0.5, 'A2': -20, 'A3': -37, 'A4': 20, 'A5': 20, 'A6': 8, 'A7': 20, 'A8': 26, 'A9': 15, 'A10': 21.4, 'D1': 3, 'D2': -10, 'D3': -34, 'D4': 4, 'D5': 9, 'D6': 20, 'D7': -15, 'D8': 13, 'D9': 11}
]

# 将分数列表转化为字典
scores_dict = {key: value for score_dict in scores_list for key, value in score_dict.items()}

# 读取json文件并处理数据
merged_data = []

with open(input_file_path, 'r', encoding='utf-8') as file:
    data_list = json.load(file)
    for data in data_list:
        filename = data.get('filename', '')
        # 提取文件名的前两位作为键值
        user_key = filename[:2]
        if user_key in scores_dict:
            data['overreliance_score'] = scores_dict[user_key]
        merged_data.append(data)

# 写入新的json文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(merged_data, file, ensure_ascii=False, indent=4)

print(f"Data has been merged and saved to {output_file_path}")
