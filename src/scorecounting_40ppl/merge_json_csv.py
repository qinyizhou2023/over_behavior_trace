import json
import csv

# 读取 JSON 文件
input_file = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_40ppl\\merge_data_gpt.json'  # 替换为您的输入文件名
output_file = 'merge_gpt.csv'  # 替换为您想要的输出文件名

with open(input_file, 'r') as f:
    data = json.load(f)

# 确保数据是列表格式
if not isinstance(data, list):
    data = [data]

# 获取所有可能的列名
fieldnames = set()
for item in data:
    fieldnames.update(item.keys())

# 将 set 转换为有序列表
fieldnames = sorted(list(fieldnames))

# 写入 CSV 文件
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 写入表头
    writer.writeheader()

    # 写入数据行
    for item in data:
        writer.writerow(item)

print(f"转换完成。CSV 文件已保存为 {output_file}")