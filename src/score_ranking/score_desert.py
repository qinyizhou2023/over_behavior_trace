# 定义计算总分的函数
def calculate_total_difference(correct_ranks, participant_scores):
    return sum(abs(cr - ps) for cr, ps in zip(correct_ranks, participant_scores))

# 用户数据
P1_score = [5,	4,	11,	8,	10,	7,	15,	3,	9,	1,	13,	14,	12,	6,	2]
P2_score = [11,	6,	4,	9,	5,	7,	12,	10,	2,	1,	3,	13,	14,	8,	15]
P5_score = [8,	6,	5,	14,	4,	7,	9,	13,	12,	1,	10,	2,	11,	3,	15]
P6_score = [12,	5,	3,	15,	2,	7,	4,		11,	1,	6,	10,	13,	9,	14]
P8_score = [8,9,7,15,4,3,13,10,12,1,6,2,11,5,14]

correct_ranks = [4,	6,	12,	7,	11,	10,	8,	5,	15,	3,	13,	9,	14,	2,	1]

# 创建一个字典来存储所有参与者的得分
participants_scores = {
    "P1": P1_score,
    "P2": P2_score,
    "P5": P5_score,
    "P6": P6_score,
    "P8": P8_score,
}

# 计算每个参与者的总分并打印结果
for participant, scores in participants_scores.items():
    total_difference = calculate_total_difference(correct_ranks, scores)
    print(f"Score of {participant}: {total_difference}")

