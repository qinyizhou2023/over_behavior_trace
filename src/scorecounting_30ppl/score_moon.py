import numpy as np
import csv
# 定义计算总分的函数
def calculate_total_difference(correct_ranks, participant_scores):
    return sum(abs(cr - ps) for cr, ps in zip(correct_ranks, participant_scores))

def calculate_average_scores(scores_list):
    num_participants = len(scores_list)
    num_scores = len(scores_list[0])
    average_scores = [sum(scores[i] for scores in scores_list) / num_participants for i in range(num_scores)]
    return average_scores

# 定义正确的排名列表
correct_ranks = [15,4,6,8,13,11,12,1,3,9,14,2,10,7,5]

# 初始化参与者得分列表
participants_scores = []
# 读取rank_moon.csv文件
with open('rank_moon.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        scores = eval(row['Scores'])  # 将字符串转换为列表
        participants_scores.append(scores)



#
# 定义每个参与者的得分列表
participants_scores = [
    ('A1', [8, 6, 14, 13, 7, 15, 9, 1, 2, 12, 11, 5, 3, 10, 4]),
    ('A2', [14, 4, 8, 10, 3, 13, 12, 1, 11, 9, 15, 2, 5, 6, 7]),
    ('A3', [15, 11, 12, 5, 6, 14, 4, 2, 13, 10, 3, 1, 7, 8, 9]),
    ('A4', [15, 11, 13, 9, 3, 6, 10, 2, 14, 12, 4, 1, 8, 7, 5]),
    ('A5', [15, 12, 13, 5, 6, 9, 4, 2, 14, 11, 3, 1, 7, 8, 10]),
    ('A6', [15, 12, 6, 7, 8, 14, 5, 2, 4, 11, 13, 1, 9, 10, 3]),
    ('A7', [14, 3, 7, 9, 13, 11, 15, 1, 4, 8, 12, 2, 10, 6, 5]),
    ('A8', [15, 12, 13, 5, 6, 9, 4, 2, 14, 11, 3, 1, 7, 8, 10]),
    ('B1', [14, 3, 10, 11, 9, 15, 8, 1, 4, 12, 5, 2, 7, 13, 6]),
    ('B2', [13, 3, 12, 14, 6, 11, 5, 1, 9, 15, 7, 2, 10, 4, 8]),
    ('B3', [15, 5, 12, 13, 7, 14, 6, 3, 2, 9, 1, 4, 11, 8, 10]),
    ('C1', [13, 3, 10, 9, 6, 4, 12, 11, 15, 5, 7, 14, 8, 2, 1]),
    ('C2', [4, 5, 8, 12, 11, 14, 10, 2, 15, 7, 9, 1, 3, 13, 6]),
    ('C3', [15, 3, 11, 12, 4, 13, 14, 2, 6, 8, 7, 1, 9, 5, 10]),
    ('C4', [14, 7, 12, 13, 9, 3, 15, 4, 2, 11, 8, 6, 10, 5, 1]),
    ('C5', [13, 6, 9, 8, 2, 14, 7, 1, 5, 15, 11, 4, 12, 10, 3]),
    ('C6', [15, 5, 12, 13, 8, 14, 9, 1, 2, 10, 4, 3, 7, 11, 6]),
    ('C7', [14, 4, 7, 10, 3, 15, 9, 1, 5, 13, 12, 2, 11, 8, 6]),
    ('D1', [15, 3, 9, 8, 5, 10, 12, 2, 13, 11, 14, 1, 6, 4, 7]),
    ('D2', [13, 4, 10, 14, 6, 12, 3, 2, 11, 15, 7, 1, 9, 5, 8]),
    ('D3', [14, 6, 13, 5, 7, 15, 12, 1, 3, 11, 4, 2, 8, 9, 10]),
    ('D4', [15, 3, 5, 9, 12, 13, 8, 1, 6, 11, 14, 2, 7, 4, 10]),
    ('D5', [15, 3, 13, 12, 4, 14, 8, 1, 6, 5, 7, 2, 11, 9, 10]),
    ('D6', [15, 8, 9, 11, 5, 12, 6, 2, 13, 10, 14, 1, 7, 4, 3]),
    #AI false score
    ("AI_FALSE2", [15	,12,	13,	5,	6,	9,	4,	2,	14,	11,	3,	1,	7,	8,	10])
]


for participant, scores in participants_scores:
    total_difference = calculate_total_difference(correct_ranks, scores)
    print(f"Score of {participant}: {total_difference}")

# 提取 分数
scores_withAI = [scores for participant, scores in participants_scores if participant.startswith("A")and("D") ]


# 计算 平均得分
average_scores = calculate_average_scores(scores_withAI)
print(f"Average scores of scores_withAI: {average_scores}")
