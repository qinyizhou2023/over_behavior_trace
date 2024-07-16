# 用户数据
P1_score = [5,	4,	11,	8,	10,	7,	15,	3,	9,	1,	13,	14,	12,	6,	2]
P2_score = [11,	6,	4,	9,	5,	7,	12,	10,	2,	1,	3,	13,	14,	8,	15]
P5_score = [8,	6,	5,	14,	4,	7,	9,	13,	12,	1,	10,	2,	11,	3,	15]
P6_score = [12,	5,	3,	15,	2,	7,	4,		11,	1,	6,	10,	13,	9,	14]

correct_ranks = [4,	6,	12,	7,	11,	10,	8,	5,	15,	3,	13,	9,	14,	2,	1]

# 计算总分
total_difference = sum(abs(cr - js) for cr, js in zip(correct_ranks, P6_score))

# 打印结果
print("Total Difference:", total_difference)

