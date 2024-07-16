# 定义计算总分的函数
def calculate_total_difference(correct_ranks, participant_scores):
    return sum(abs(cr - ps) for cr, ps in zip(correct_ranks, participant_scores))

# 定义正确的排名列表
correct_ranks = [4,	1,	11.5,	2.5,	6.5,	5.5,	5.5,	13,	10.5,	14,	7,	8.5,	10,	14.5]

# 用户数据
P4_score = [1,	6,	3,	8,	9,	14,	10,	13,	2,	5,	4,	11,	7,	12]


# 创建一个字典来存储所有参与者的得分
participants_scores = {
    "P4": P4_score
}

# 计算每个参与者的总分并打印结果
for participant, scores in participants_scores.items():
    total_difference = calculate_total_difference(correct_ranks, scores)
    print(f"Score of {participant}: {total_difference}")


