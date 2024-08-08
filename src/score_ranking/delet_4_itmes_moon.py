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
    #Moon google form结果，moon-->D.csv
    ("P12", [14, 4, 9, 8, 11, 15, 3, 1, 6, 12, 13, 2, 7, 10, 5]),
    ("P13", [13, 3, 8, 6, 10, 12, 11, 1, 5, 9, 15, 2, 14, 7, 4]),
    ("P14", [14, 3, 11, 12, 4, 13, 15, 1, 10, 9, 6, 2, 5, 8, 7]),
    ("P15", [15, 12, 4, 10, 11, 14, 13, 1, 6, 3, 2, 7, 8, 9, 5]),
    ("P16", [15, 3, 11, 12, 5, 14, 6, 1, 10, 9, 13, 2, 8, 7, 4]),
    ("P17", [11, 15, 7, 5, 10, 9, 14, 3, 8, 6, 1, 13, 2, 12, 4]),
    ("P18", [13, 3, 9, 10, 11, 14, 4, 1, 5, 12, 6, 2, 8, 5, 7]),
    ("P19", [14, 4, 12, 13, 6, 10, 11, 1, 7, 15, 8, 3, 9, 2, 5]),
    ("P20", [11, 7, 2, 3, 8, 15, 9, 1, 4, 10, 12, 6, 5, 13, 14]),
    ("P21", [8, 3, 13, 14, 6, 15, 2, 5, 7, 11, 4, 1, 9, 10, 12]),
    ("P36", [12, 10, 8, 7, 14, 15, 11, 5, 1, 6, 2, 9, 3, 13, 4]),
    ("P37", [13, 1, 11, 15, 6, 14, 10, 2, 9, 12, 4, 3, 5, 8, 7]),
    # Moon wechat结果 D.csv -->moon
    ("P22", [15, 1, 8, 13, 7, 14, 3, 2, 6, 11, 5, 4, 10, 9, 12]),
    ("P23", [13, 4, 10, 7, 12, 15, 8, 2, 3, 9, 14, 5, 6, 11, 1]),
    ("P24", [5, 3, 8, 6, 7, 14, 15, 1, 10, 13, 9, 2, 11, 4, 12]),
    ("P25", [12, 4, 9, 10, 11, 15, 3, 1, 6, 14, 13, 2, 8, 7, 5]),
    ("P26", [9, 3, 2, 8, 7, 10, 4, 5, 6, 11, 12, 13, 14, 1, 15]),
    ("P27", [13, 6, 9, 10, 7, 14, 11, 1, 12, 8, 15, 2, 5, 3, 4]),
    ("P28", [13, 1, 10, 9, 12, 14, 15, 2, 3, 4, 5, 8, 6, 7, 11]),
    ("P29", [15, 6, 11, 12, 10, 14, 3, 1, 5, 13, 7, 8, 4, 9, 2]),
    ("P30", [12, 1, 13, 2, 10, 3, 4, 5, 6, 15, 9, 14, 11, 7, 8]),
    ("P31", [12, 10, 14, 15, 7, 9, 6, 2, 5, 13, 3, 8, 4, 11, 1]),
    # ("P32", [1, 2, 3, 13, 4, 14, 15, 5, 6, 7, 8, 9, 10, 11, 12]),
    ("P33", [9, 3, 13, 15, 6, 8, 7, 10, 1, 14, 12, 2, 11, 5, 4]),
    ("P34", [14, 12, 6, 5, 9, 15, 11, 1, 3, 10, 4, 2, 13, 7, 8]),
    ("P35", [14, 4, 15, 12, 11, 13, 10, 5, 3, 6, 7, 8, 2, 9, 1])
]
correct_ranks = [15,4,6,8,13,12,3,14,2,10,5]

# 定义要删除的索引（第6、8、10\14个数据，注意索引从0开始）
indices_to_remove = [5, 7, 9, 13]

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