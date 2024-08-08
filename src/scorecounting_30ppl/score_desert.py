# 定义计算总分的函数
def calculate_total_difference(correct_ranks, participant_scores):
    return sum(abs(cr - ps) for cr, ps in zip(correct_ranks, participant_scores))
def calculate_average_scores(scores_list):
    num_participants = len(scores_list)
    num_scores = len(scores_list[0])
    average_scores = [sum(scores[i] for scores in scores_list) / num_participants for i in range(num_scores)]
    return average_scores
# 用户数据
# 定义每个参与者的得分列表
participants_scores = [
    # group A with AI
    ('A1', [7, 8, 1, 6, 2, 10, 4, 15, 12, 3, 11, 9, 14, 5, 13]),
    ('A2', [9, 6, 4, None, 3, 5, 10, 13, 2, 1, 11, 14, 12, 7, 15]),
    ('A3', [5, 6, 8, 14, 9, 10, 15, 4, 3, 1, 12, 13, 11, 2, 7]),
    ('A4', [6, 8, 4, 15, 3, 9, 13, 5, 2, 1, 14, 10, 12, 7, 11]),
    ('A5', [8, 5, 13, 12, 6, 10, 4, None, 11, 1, None, 15, 7, 2, 14]),
    ('A6', [7, 5, 15, 10, 2, 6, 8, 3, 4, 1, 12, 14, 9, 11, 13]),
    ('A7', [12, 6, 3, 15, 2, 4, 10, 11, 5, 1, 7, 8, 14, 13, 9]),
    ('A8', [11, 7, 8, 2, 9, 4, 14, 5, 15, 1, 12, 3, 13, 10, 6]),
    #group D alone
    ('D1', [8, 6, 2, 12, 4, 3, 9, 13, 5, 1, 7, 10, 15, 11, 14]),
    ('D2', [5, 6, 13, 12, 4, 3, 7, 11, 2, 1, 14, 15, 8, 9, 10]),
    ('D3', [14, 2, 4, 13, 3, 11, 15, 10, 7, 1, 5, 8, 12, 9, 6]),
    ('D4', [14, 2, 9, 8, 10, 3, 5, 12, 6, 1, 4, 13, 11, 7, 15]),
    ('D5', [11, 6, 3, 13, 5, 8, 12, 14, 2, 1, 7, 4, 10, 9, 15]),
    ('D6', [6, 4, 9, 13, 7, 3, 2, 10, 15, 1, 8, 5, 12, 14, 11]),
    # group C with AI
    ('C1', [10, 9, 1, 11, 4, 8, 6, 13, 2, 5, 12, 3, 15, 7, 14]),
    ('C2', [7, 14, 3, 8, 6, 9, 12, 10, 2, 1, 13, 4, 15, 5, 11]),
    ('C3', [12, 11, 5, 13, 6, 7, 15, 8, 2, 1, 10, 3, 14, 4, 9]),
    ('C4', [6, 15, 1, 13, 5, 14, 9, 10, 2, 3, 7, 4, 11, 8, 12]),
    ('C5', [15, 14, 1, 13, 5, 7, 9, 11, 2, 3, 10, 4, 12, 6, 8]),
    ('C6', [3, 13, 2, 10, 4, 11, 15, 14, 6, 1, 9, 7, 5, 8, 12]),
    ('C7', [6, 15, 1, 13, 5, 14, 9, 10, 2, 3, 7, 4, 11, 8, 12])
]
correct_ranks = [4,	6,	12,	7,	11,	10,	8,	5,	15,	3,	13,	9,	14,	2,	1]



# 计算每个参与者的总分并打印结果
for participant, scores in participants_scores:
    total_difference = calculate_total_difference(correct_ranks, scores)
    print(f"Score of {participant}: {total_difference}")

# 提取 P12 到 P35 的分数
p12_to_p35_scores = [scores for participant, scores in participants_scores if participant.startswith("P") and int(participant[1:]) >= 12 and int(participant[1:]) <= 44]

# 计算 P12 到 P35 的平均得分
average_scores = calculate_average_scores(p12_to_p35_scores)
print(f"Average scores of P12 to P34: {average_scores}")