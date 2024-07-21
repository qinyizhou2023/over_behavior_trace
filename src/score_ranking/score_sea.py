# 用户数据

correct_ranks = [1,	2,	3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	14,	15]
# 定义计算总分的函数
def calculate_total_difference(correct_ranks, participant_scores):
    return sum(abs(cr - ps) for cr, ps in zip(correct_ranks, participant_scores))

# 定义正确的排名列表
correct_ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# 定义每个参与者的得分列表
P3_score = [7,	3,	1,	6,	2,	9,	8,	11,	10,	5,	13,	14,	4,	12,	15]
P7_score = [6,15,4,14,9,10,12,11,1,3,5,8,7,2,13]
P8_score = [4,3,2,10,8,9,7,14,1,12,5,6,13,15,11]


# 创建一个字典来存储所有参与者的得分
participants_scores = {
    "P3": P3_score,
    "P7": P7_score,
    "P8": P8_score

}

# 计算每个参与者的总分并打印结果
for participant, scores in participants_scores.items():
    total_difference = calculate_total_difference(correct_ranks, scores)
    print(f"Score of {participant}: {total_difference}")