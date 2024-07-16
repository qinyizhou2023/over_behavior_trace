# 定义计算总分的函数
def calculate_total_difference(correct_ranks, participant_scores):
    return sum(abs(cr - ps) for cr, ps in zip(correct_ranks, participant_scores))

# 定义正确的排名列表
correct_ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# 定义每个参与者的得分列表
P1_score = [15, 3, 5, 8, 14, 13, 11, 1, 4, 9, 10, 2, 12, 7, 6]
P2_score = [15, 6, 13, 10, 7, 12, 11, 1, 4, 14, 5, 2, 3, 8, 9]
P3_score = [13, 4, 8, 14, 2, 9, 10, 1, 12, 15, 7, 3, 6, 5, 11]
P4_score = [7, 9, 2, 13, 8, 4, 10, 1, 12, 14, 15, 11, 6, 3, 5]
P5_score = [12, 5, 11, 14, 3, 6, 4, 1, 15, 13, 10, 2, 8, 7, 9]
P6_score = [13, 6, 10, 14, 3, 15, 8, 1, 11, 12, 5, 2, 7, 9, 4]
P7_score = [14,15,10,9,13,12,11,1,2,7,15,4,8,6,3]
AI_score = [8,	10,	9,	15,	2,	4,6,	3,	11,	13,	5,	7,1,	14,	12]


# 创建一个字典来存储所有参与者的得分
participants_scores = {
    "P1": P1_score,
    "P2": P2_score,
    "P3": P3_score,
    "P4": P4_score,
    "P5": P5_score,
    "P6": P6_score,
    "P7": P7_score,
    "AI": AI_score
}

# 计算每个参与者的总分并打印结果
for participant, scores in participants_scores.items():
    total_difference = calculate_total_difference(correct_ranks, scores)
    print(f"Score of {participant}: {total_difference}")
