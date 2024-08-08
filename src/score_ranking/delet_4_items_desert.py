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
    #google sheet答案 moon-->D.csv
    ("P12", [7, 12, 3, 11, 2, 10, 9, 8, 5, 1, 13, 6, 14, 4, 15]),
    ("P13", [6, 4, 8, 3, 7, 10, 15, 5, 14, 1, 11, 9, 12, 2, 13]),
    ("P14", [6, 7, 8, 12, 5, 4, 11, 9, 2, 1, 3, 10, 14, 13, 15]),
    ("P15", [2, 3, 9, 7, 4, 8, 13, 15, 10, 1, 12, 6, 11, 5, 14]),
    ("P16", [7, 5, 4, 3, 12, 9, 10, 11, 14, 1, 15, 8, 2, 6, 13]),
    ("P17", [11, 1, 3, 10, 2, 9, 12, 15, 5, 4, 8, 7, 14, 6, 13]),
    ("P18", [12, 11, 1, 15, 6, 7, 5, 14, 13, 2, 10, 9, 3, 4, 8]),
    ("P19", [7, 11, 3, 14, 2, 5, 10, 12, 13, 1, 9, 8, 15, 4, 6]),
    ("P20", [9, 8, 5, 10, 4, 7, 12, 13, 2, 1, 11, 6, 14, 3, 15]),
    ("P21", [8, 9, 7, 15, 4, 3, 13, 10, 12, 1, 6, 2, 11, 5, 14]),
    ("P36", [9, 13, 1, 4, 6, 8, 11, 10, 7, 2, 3, 12, 15, 5, 14]),
    ("P37", [3,2,10,5,4,6,9,13,15,1,7,12,11,8,14]),
    #wechat答案 D.csv -->moon
    ("P22", [8, 4, 7, 6, 1, 3, 9, 12, 5, 2, 11, 14, 10, 13, 15]),
    ("P23", [12, 4, 9, 13, 6, 5, 15, 3, 7, 2, 14, 10, 8, 11, 1]),
    ("P24", [10, 4, 11, 6, 12, 3, 13, 7, 2, 1, 14, 8, 15, 5, 9]),
    ("P25", [7, 6, 1, 8, 2, 9, 10, 11, 13, 5, 14, 4, 15, 3, 12]),
    ("P26", [10, 9, 1, 11, 6, 7, 12, 8, 13, 2, 3, 4, 14, 5, 15]),
    ("P27", [15, 4, 13, 1, 5, 6, 8, 9, 10, 2, 12, 3, 11, 14, 7]),
    ("P28", [9, 1, 2, 13, 3, 4, 8, 11, 5, 6, 7, 10, 14, 12, 15]),
    ("P29", [13, 6, 7, 5, 2, 3, 14, 8, 4, 9, 15, 10, 1, 11, 12]),
    ("P30", [8, 7, 6, 10, 3, 5, 1, 13, 4, 2, 11, 12, 9, 15, 14]),
    ("P31", [10, 7, 5, 12, 6, 9, 8, 1, 3, 4, 2, 14, 11, 15, 13]),
    ("P32", [1, 2, 3, 10, 4, 5, 11, 12, 6, 7, 13, 14, 8, 9, 15]),
    ("P33", [8, 5, 10, 9, 6, 3, 4, 12, 2, 1, 11, 15, 14, 13, 7]),
    ("P34", [10, 9, 1, 14, 2, 5, 6, 3, 7, 4, 11, 12, 8, 13, 15]),
    ("P35", [9, 6, 1, 12, 5, 8, 11, 2, 10, 3, 7, 4, 14, 13, 15]),
    ("P36", [9, 13, 1, 4, 6, 8, 11, 10, 7, 2, 3, 12, 15, 5, 14]),
    ("P37", [6, 9, 7, 4, 3, 1, 5, 12, 2, 8, 14, 13, 10, 11, 15]),
    ("P38", [6, 7, 3, 14, 10, 9, 5, 11, 2, 1, 4, 15, 13, 8, 12]),
    ("P39", [13, 6, 2, 11, 3, 7, 4, 5, 12, 8, 14, 1, 9, 10, 15]),
    ("P40", [12, 5, 1, 9, 2, 3, 6, 4, 13, 7, 11, 10, 8, 14, 15]),
    ("P41", [6, 3, 5, 12, 8, 2, 9, 15, 7, 1, 4, 11, 10, 13, 14]),
    ("AI", [13, 10, 6, 8, 4, 7, 2, 15, 14, 1, 3, 9, 5, 11, 12])
]

correct_ranks = [4,	6,	12,	7,	10,	8,	5,	3,	13,	9,	14]

# 定义要删除的索引（第5、\9、14、15个数据，注意索引从0开始）
indices_to_remove = [4, 8, 13, 14]

# 创建一个新的列表，去掉指定索引的数据
new_participants_scores = [
    (participant, [score for idx, score in enumerate(scores) if idx not in indices_to_remove])
    for participant, scores in participants_scores
]

print(new_participants_scores)

# 计算每个参与者的总分并打印结果
for participant, scores in new_participants_scores:
    total_difference = calculate_total_difference(correct_ranks, scores)
    print(f"Score of {participant}: {total_difference}")

# 提取 P12 到 P35 的分数
p12_to_p35_scores = [scores for participant, scores in participants_scores if participant.startswith("P") and int(participant[1:]) >= 12 and int(participant[1:]) <= 35]

# 计算 P12 到 P35 的平均得分
average_scores = calculate_average_scores(p12_to_p35_scores)
print(f"Average scores of P12 to P34: {average_scores}")