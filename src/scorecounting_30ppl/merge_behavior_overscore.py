import json

# 只改： 定义文件路径
#tasksheet:
input_file_path =  'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_30ppl\\behavior_result_tasksheet.json'
output_file_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\merge_data_tasksheet.json'
# # gpt:
# input_file_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_30ppl\\behavior_result_gpt.json'
# output_file_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\merge_data_gpt.json'

# 定义分数列表 (calculate_minus手动传数据)
scores_list = [
    {'B1': 0, 'B2': -11, 'B3': 7, 'B4': 22, 'B5': -9, 'B6': 6, 'C1': 2, 'C2': -2, 'C3': 23, 'C4': 26, 'C5': 32, 'C6': 24, 'C7': 41},
    {'A1': 13, 'A2': -29, 'A3': 19, 'A4': 6, 'A5': 10, 'A6': -10, 'A7': -47, 'A8': 26, 'D1': -23, 'D2': 1, 'D3': -24, 'D4': -40, 'D5': -24, 'D6': -1}
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
