# import numpy as np
# # 定义计算总分的函数
# def calculate_total_difference(correct_ranks, participant_scores):
#     return sum(abs(cr - ps) for cr, ps in zip(correct_ranks, participant_scores))
# def calculate_average_scores(scores_list):
#     num_participants = len(scores_list)
#     num_scores = len(scores_list[0])
#     average_scores = [sum(scores[i] for scores in scores_list) / num_participants for i in range(num_scores)]
#     return average_scores
# # 用户数据
# # 定义每个参与者的得分列表
# participants_scores_withAI = [
#     ('A1', [8, 6, 14, 13, 7, 15, 9, 1, 2, 12, 11, 5, 3, 10, 4]),
#     ('A2', [14, 4, 8, 10, 3, 13, 12, 1, 11, 9, 15, 2, 5, 6, 7]),
#     ('A3', [15, 11, 12, 5, 6, 14, 4, 2, 13, 10, 3, 1, 7, 8, 9]),
#     ('A4', [15, 11, 13, 9, 3, 6, 10, 2, 14, 12, 4, 1, 8, 7, 5]),
#     ('A5', [15, 12, 13, 5, 6, 9, 4, 2, 14, 11, 3, 1, 7, 8, 10]),
#     ('A6', [15, 12, 6, 7, 8, 14, 5, 2, 4, 11, 13, 1, 9, 10, 3]),
#     ('A7', [14, 3, 7, 9, 13, 11, 15, 1, 4, 8, 12, 2, 10, 6, 5]),
#     ('A8', [15, 12, 13, 5, 6, 9, 4, 2, 14, 11, 3, 1, 7, 8, 10]),
#     ('D1', [15, 3, 9, 8, 5, 10, 12, 2, 13, 11, 14, 1, 6, 4, 7]),
#     ('D2', [13, 4, 10, 14, 6, 12, 3, 2, 11, 15, 7, 1, 9, 5, 8]),
#     ('D3', [14, 6, 13, 5, 7, 15, 12, 1, 3, 11, 4, 2, 8, 9, 10]),
#     ('D4', [15, 3, 5, 9, 12, 13, 8, 1, 6, 11, 14, 2, 7, 4, 10]),
#     ('D5', [15, 3, 13, 12, 4, 14, 8, 1, 6, 5, 7, 2, 11, 9, 10]),
#     ('D6', [15, 8, 9, 11, 5, 12, 6, 2, 13, 10, 14, 1, 7, 4, 3])
# ]
#
# participants_scores_alone=[
#     ('B1', [14, 3, 10, 11, 9, 15, 8, 1, 4, 12, 5, 2, 7, 13, 6]),
#     ('B2', [13, 3, 12, 14, 6, 11, 5, 1, 9, 15, 7, 2, 10, 4, 8]),
#     ('B3', [15, 5, 12, 13, 7, 14, 6, 3, 2, 9, 1, 4, 11, 8, 10]),
#     ('C1', [13, 3, 10, 9, 6, 4, 12, 11, 15, 5, 7, 14, 8, 2, 1]),
#     ('C2', [4, 5, 8, 12, 11, 14, 10, 2, 15, 7, 9, 1, 3, 13, 6]),
#     ('C3', [15, 3, 11, 12, 4, 13, 14, 2, 6, 8, 7, 1, 9, 5, 10]),
#     ('C4', [14, 7, 12, 13, 9, 3, 15, 4, 2, 11, 8, 6, 10, 5, 1]),
#     ('C5', [13, 6, 9, 8, 2, 14, 7, 1, 5, 15, 11, 4, 12, 10, 3]),
#     ('C6', [15, 5, 12, 13, 8, 14, 9, 1, 2, 10, 4, 3, 7, 11, 6]),
#     ('C7', [14, 4, 7, 10, 3, 15, 9, 1, 5, 13, 12, 2, 11, 8, 6]),
#
# ]
#
# correct_ranks = [15,4,6,8,13,12,3,14,2,10,7,5]
#
# # 定义要删除的索引（第6、8、10个数据，注意索引从0开始）
# indices_to_remove = [5, 7, 9]
#
# # 创建一个新的列表，去掉指定索引的数据
# remove3_scores_withAI  = [
#     (participant, [score for idx, score in enumerate(scores) if idx not in indices_to_remove])
#     for participant, scores in participants_scores_withAI
# ]
# print(remove3_scores_withAI)
#
# remove3_scores_alone  = [
#     (participant, [score for idx, score in enumerate(scores) if idx not in indices_to_remove])
#     for participant, scores in participants_scores_alone
# ]
# print(remove3_scores_alone)
#
# # # 计算每个参与者的总分并打印结果
# # for participant, scores in remove3_scores_withAI:
# #     total_difference = calculate_total_difference(correct_ranks, scores)
# #     print(f"Score of {remove3_scores_withAI}: {total_difference}")
#
# # 打印所有参与者的总分列表
# score_list_remove3_withAI = []
# for participant, scores in remove3_scores_withAI:
#     # 计算每个参与者的总分
#     total_difference = calculate_total_difference(correct_ranks, scores)
#     # 将总分添加到列表中
#     score_list_remove3_withAI.append(total_difference)
# print(f"task with AI moon", score_list_remove3_withAI)
#
# score_list_remove3_alone =[]
# for participant, scores in remove3_scores_alone:
#     # 计算每个参与者的总分
#     total_difference = calculate_total_difference(correct_ranks, scores)
#     # 将总分添加到列表中
#     score_list_remove3_alone.append(total_difference)
# print(f'task alone moon', score_list_remove3_alone)
#
# # 计算每个参与者的总分并打印结果
# score_dict_remove3_withAI = {}
# for participant, scores in remove3_scores_withAI:
#     total_difference = calculate_total_difference(correct_ranks, scores)
#     score_dict_remove3_withAI[participant] = total_difference
# print(f"task with AI moon: {score_dict_remove3_withAI}")
#
# score_dict_remove3_alone = {}
# for participant, scores in remove3_scores_alone:
#     total_difference = calculate_total_difference(correct_ranks, scores)
#     score_dict_remove3_alone[participant] = total_difference
# print(f'task alone moon: {score_dict_remove3_alone}')
#
# # average scores
# average_score_list_remove3_withAI = np.mean(list(score_dict_remove3_withAI.values()))
# average_score_list_remove3_alone = np.mean(list(score_dict_remove3_alone.values()))
# print(average_score_list_remove3_withAI)
# print(average_score_list_remove3_alone)
import csv
import ast
import numpy as np

# 读取CSV文件
file_path = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\scorecounting_30ppl\rank_moon.csv'

participants_scores_withAI = []
participants_scores_alone = []

# 定义B组和C组
group_withAI = ['A', 'D']

# 定义A组和D组
group_alone = ['B', 'C']
correct_ranks = [15, 4, 6, 8, 13, 12, 3, 14, 2, 10, 7, 5]

# 从CSV文件中读取数据
with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过表头
    for row in reader:
        participant = row[0].strip('(')  # 去掉前面的左括号
        participant = row[0]
        scores = ast.literal_eval(row[1])
        group = participant[1]  # 获取组信息
        if group in group_withAI:
            participants_scores_withAI.append((participant, scores))
        elif group in group_alone:
            participants_scores_alone.append((participant, scores))

# 打印结果
print("participants_scores_withAI:", participants_scores_withAI)
print("participants_scores_alone:", participants_scores_alone)


# 定义计算总分的函数
def calculate_total_difference(correct_ranks, participant_scores):
    return sum(abs(cr - ps) for cr, ps in zip(correct_ranks, participant_scores))

# 定义要删除的索引（第6,8,10个数据，注意索引从0开始）
indices_to_remove = [5, 7, 9]

# 创建一个新的列表，去掉指定索引的数据
remove3_scores_withAI = [
    (participant, [score for idx, score in enumerate(scores) if idx not in indices_to_remove])
    for participant, scores in participants_scores_withAI
]

remove3_scores_alone = [
    (participant, [score for idx, score in enumerate(scores) if idx not in indices_to_remove])
    for participant, scores in participants_scores_alone
]

# 计算每个参与者的总分并打印结果
score_list_remove3_withAI = []
for participant, scores in remove3_scores_withAI:
    total_difference = calculate_total_difference(correct_ranks, scores)
    score_list_remove3_withAI.append(total_difference)
print(f"task with AI mmon(A&D)", score_list_remove3_withAI)

score_list_remove3_alone = []
for participant, scores in remove3_scores_alone:
    total_difference = calculate_total_difference(correct_ranks, scores)
    score_list_remove3_alone.append(total_difference)
print(f'task alone moon (B&C) ', score_list_remove3_alone)

# 计算每个参与者的总分并打印结果
score_dict_remove3_withAI = {}
for participant, scores in remove3_scores_withAI:
    total_difference = calculate_total_difference(correct_ranks, scores)
    score_dict_remove3_withAI[participant.strip('(')] = total_difference
print(f"task with AI mmon(A&D): {score_dict_remove3_withAI}")

score_dict_remove3_alone = {}
for participant, scores in remove3_scores_alone:
    total_difference = calculate_total_difference(correct_ranks, scores)
    score_dict_remove3_alone[participant.strip('(')] = total_difference
print(f'task alone moon (B&C): {score_dict_remove3_alone}')

# average scores
average_score_list_remove3_withAI = np.mean(list(score_dict_remove3_withAI.values()))
average_score_list_remove3_alone = np.mean(list(score_dict_remove3_alone.values()))
print(f"Average score with AI moon(A&D): {average_score_list_remove3_withAI}")
print(f"Average score alone (B&C): {average_score_list_remove3_alone}")
