
import csv
import ast
import numpy as np

# 读取CSV文件
file_path = r'C:\Users\zqy\Documents\over regression\over_behavior_trace\src\109_pilot_result\rank_count\rank_moon.csv'

participants_scores_withAI = []
participants_scores_alone = []

# 定义B组和C组
group_withAI = ['A', 'D']

# 定义A组和D组
group_alone = ['B', 'C']

#正确的rank（去掉2，6，10）
correct_ranks = [15,6,8,13,12,1,3,14,2,10,7,5]

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

# 定义要删除的索引（第2,6,10个数据，注意索引从0开始）
indices_to_remove = [1, 5, 9]

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
