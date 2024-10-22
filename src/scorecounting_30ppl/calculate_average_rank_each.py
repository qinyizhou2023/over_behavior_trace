# import csv
# import ast
# import numpy as np
# import pandas as pd
#
# # 读取CSV文件
# rawdata = []
# with open('C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\rank_desert.csv', 'r') as file:
#     reader = csv.reader(file)
#     next(reader)  # Skip the header
#     for row in reader:
#         participant = row[0]
#         scores = ast.literal_eval(row[1])  # Convert string representation of list to actual list
#         rawdata.append((participant, scores))
#
# # 将数据转换为DataFrame
# df = pd.DataFrame(rawdata, columns=['Participant', 'Scores'])
#
# # 将每个用户的Scores列展开成独立的列
# scores_df = pd.DataFrame(df['Scores'].tolist(), index=df['Participant'])
# scores_df.columns = [f'Item_{i+1}' for i in range(scores_df.shape[1])]
#
# # 计算每个物品的平均rank值
# average_ranks = scores_df.mean()
#
# # 打印结果
# print(average_ranks)

import csv
import ast
import pandas as pd

# 文件路径
file_path = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\scorecounting_30ppl\rank_desert.csv'

# 定义组别
group_withAI = ['B', 'C']
group_alone = ['A', 'D']

# 初始化存储数据的列表
participants_scores_withAI = []
participants_scores_alone = []

# 从CSV文件中读取数据并分类
with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过表头
    for row in reader:
        participant = row[0].strip('(').strip()  # 去掉前面的左括号和空格
        scores = ast.literal_eval(row[1])
        group = participant[1]  # 获取组信息
        if group in group_withAI:
            participants_scores_withAI.append((participant, scores))
        elif group in group_alone:
            participants_scores_alone.append((participant, scores))

# 转换为DataFrame
df_withAI = pd.DataFrame([scores for _, scores in participants_scores_withAI])
df_alone = pd.DataFrame([scores for _, scores in participants_scores_alone])

# 设置列名
df_withAI.columns = [f'Item_{i+1}' for i in range(df_withAI.shape[1])]
df_alone.columns = [f'Item_{i+1}' for i in range(df_alone.shape[1])]

# 计算每个物品的平均rank值
average_ranks_withAI = df_withAI.mean()
average_ranks_alone = df_alone.mean()

# 打印结果
print("Average ranks for group C&B:")
print(average_ranks_withAI)
print("\nAverage ranks for group A&D:")
print(average_ranks_alone)

