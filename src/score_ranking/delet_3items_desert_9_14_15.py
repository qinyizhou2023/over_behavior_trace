import math
# 定义计算总分的函数
def calculate_total_difference(correct_ranks_new, participant_scores):
    return sum(abs(cr - ps) for cr, ps in zip(correct_ranks_new, participant_scores))
def calculate_average_scores(scores_list):
    num_participants = len(scores_list)
    num_scores = len(scores_list[0])
    average_scores = [sum(scores[i] for scores in scores_list) / num_participants for i in range(num_scores)]
    return average_scores
# 用户数据
# 定义每个参与者的得分列表
participants_scores = [
    ("A1", [7, 12, 3, 11, 2, 10, 9, 8, 5, 1, 13, 6, 14, 4, 15]),
    ("A2", [6, 4, 8, 3, 7, 10, 15, 5, 14, 1, 11, 9, 12, 2, 13]),
    ("A3", [6, 7, 8, 12, 5, 4, 11, 9, 2, 1, 3, 10, 14, 13, 15]),
    ("A4", [2, 3, 9, 7, 4, 8, 13, 15, 10, 1, 12, 6, 11, 5, 14]),
    ("A5", [7, 5, 4, 3, 12, 9, 10, 11, 14, 1, 15, 8, 2, 6, 13]),
    ("A6", [11, 1, 3, 10, 2, 9, 12, 15, 5, 4, 8, 7, 14, 6, 13]),
    ("A7", [12, 11, 1, 15, 6, 7, 5, 14, 13, 2, 10, 9, 3, 4, 8]),
    ("A8", [7, 11, 3, 14, 2, 5, 10, 12, 13, 1, 9, 8, 15, 4, 6]),
    ("A9", [9, 8, 5, 10, 4, 7, 12, 13, 2, 1, 11, 6, 14, 3, 15]),
    ("A10", [8, 9, 7, 15, 4, 3, 13, 10, 12, 1, 6, 2, 11, 5, 14]),
    ("A11", [9, 13, 1, 4, 6, 8, 11, 10, 7, 2, 3, 12, 15, 5, 14]),
    ("A12", [3, 2, 10, 5, 4, 6, 9, 13, 15, 1, 7, 12, 11, 8, 14]),
    ("A13", [6, 9, 5, 10, 3, 8, 15, 13, 2, 1, 4, 12, 11, 7, 14]),
    ("A14", [12, 5, 4, 13, 3, 7, 6, 11, 8, 1, 9, 14, 2, 10, 15]),
    ("A15", [3, 11, 4, 5, 6, 7, 8, 9, 10, 12, 13, 1, 14, 2, 15]),
    ("A16", [9, 7, 8, 14, 6, 3, 4, 13, 2, 1, 5, 10, 12, 15, 11]),
    ("A17", [6, 8, 3, 14, 4, 5, 7, 9, 12, 1, 10, 2, 11, 13, 15]),
    ("A18", [10, 4, 6, 12, 11, 8, 3, 13, 5, 1, 14, 9, 7, 2, 15]),
    ("A19", [10, 12, 2, 14, 5, 9, 8, 11, 6, 1, 7, 4, 13, 3, 15]),
    ("A20", [5, 6, 14, 7, 10, 4, 11, 15, 12, 1, 8, 3, 2, 13, 9]),
    # ("A21", [1, 9, 6, 12, 8, 2, 10, 7, 5, 3, 14, 11, 4, 13, 15]),
    ("A22", [3, 4, 6, 5, 7, 8, 10, 11, 2, 1, 9, 13, 14, 12, 15]),
    ("A23", [2, 11, 3, 10, 4, 8, 12, 5, 6, 1, 13, 7, 9, 15, 14]),
    ("A24", [10, 1, 2, 5, 4, 3, 9, 6, 7, 8, 14, 11, 12, 15, 13]),
    ("A25", [5, 4, 10, 11, 6, 3, 13, 7, 2, 1, 15, 8, 9, 12, 14]),
    ("A26", [4, 15, 2, 3, 7, 9, 5, 10, 6, 11, 8, 1, 12, 13, 14]),
    # ("A27", [3, 4, 6, 14, 7, 5, 9, 11, 8, 1, 2, 12, 13, 10, 15]),
    # B desert -- moon
    ("B1", [8, 4, 7, 6, 1, 3, 9, 12, 5, 2, 11, 14, 10, 13, 15]),
    ("B2", [12, 4, 9, 13, 6, 5, 15, 3, 7, 2, 14, 10, 8, 11, 1]),
    ("B3", [10, 4, 11, 6, 12, 3, 13, 7, 2, 1, 14, 8, 15, 5, 9]),
    ("B4", [7, 6, 1, 8, 2, 9, 10, 11, 13, 5, 14, 4, 15, 3, 12]),
    ("B5", [10, 9, 1, 11, 6, 7, 12, 8, 13, 2, 3, 4, 14, 5, 15]),
    ("B6", [15, 4, 13, 1, 5, 6, 8, 9, 10, 2, 12, 3, 11, 14, 7]),
    ("B7", [9, 1, 2, 13, 3, 4, 8, 11, 5, 6, 7, 10, 14, 12, 15]),
    ("B8", [13, 6, 7, 5, 2, 3, 14, 8, 4, 9, 15, 10, 1, 11, 12]),
    ("B9", [8, 7, 6, 10, 3, 5, 1, 13, 4, 2, 11, 12, 9, 15, 14]),
    ("B10", [10, 7, 5, 12, 6, 9, 8, 1, 3, 4, 2, 14, 11, 15, 13]),
    ("B11", [1, 2, 3, 10, 4, 5, 11, 12, 6, 7, 13, 14, 8, 9, 15]),
    ("B12", [8, 5, 10, 9, 6, 3, 4, 12, 2, 1, 11, 15, 14, 13, 7]),
    ("B13", [10, 9, 1, 14, 2, 5, 6, 3, 7, 4, 11, 12, 8, 13, 15]),
    ("B14", [9, 6, 1, 12, 5, 8, 11, 2, 10, 3, 7, 4, 14, 13, 15]),
    ("B15", [9, 13, 1, 4, 6, 8, 11, 10, 7, 2, 3, 12, 15, 5, 14]),
    ("B16", [6, 9, 7, 4, 3, 1, 5, 12, 2, 8, 14, 13, 10, 11, 15]),
    # ("B17", [6, 7, 3, 14, 10, 9, 5, 11, 2, 1, 4, 15, 13, 8, 12]),
    ("B18", [13, 6, 2, 11, 3, 7, 4, 5, 12, 8, 14, 1, 9, 10, 15]),
    # ("B19", [12, 5, 1, 9, 2, 3, 6, 4, 13, 7, 11, 10, 8, 14, 15]),
    ("B20", [6, 3, 5, 12, 8, 2, 9, 15, 7, 1, 4, 11, 10, 13, 14]),
    ("B21", [6, 8, 4, 13, 5, 9, 12, 1, 3, 2, 7, 10, 11, 14, 15]),
    ("B22", [5, 8, 3, 6, 2, 4, 7, 1, 9, 10, 11, 13, 14, 12, 15]),
    ("B23", [14, 1, 11, 2, 8, 5, 4, 10, 3, 12, 7, 9, 13, 15, 6]),
    # ("B24", [6, 2, 7, 11, 3, 4, 5, 10, 9, 1, 8, 12, 13, 14, 15]),
    ("B25", [5, 4, 6, 9, 8, 2, 10, 7, 11, 1, 3, 12, 13, 14, 15]),
    ("B26", [4, 3, 9, 5, 10, 8, 2, 13, 14, 1, 15, 7, 12, 6, 11]),
    ("B27", [1, 5, 4, 10, 3, 2, 13, 8, 12, 6, 7, 11, 9, 14, 15]),
    ("B28", [11,	4,	1,	15,	2,	5,	6,	14,	10,	3,	8,	9,	13,	7,	12]),
     ("AI",    [11,	7,	6,	14,	3,	2,	12,	15,	8,	5,	4,	9,	1,	10,	13])
]

correct_ranks = [4,	6,	12,	7,	11,	10,	8,	5,	15,	3,	13,	9,	14,	2,	1]

#
# 定义要删除的索引（第9、14、15个数据，注意索引从0开始）
indices_to_remove = [8, 13, 14]

#
# # 定义要删除的索引（第5、14、15个数据，注意索引从0开始）
# indices_to_remove = [4, 13, 14]

# 创建一个新的列表，去掉指定索引的数据
new_participants_scores = [
    (participant, [score for idx, score in enumerate(scores) if idx not in indices_to_remove])
    for participant, scores in participants_scores
]

correct_ranks_new = [rank for idx, rank in enumerate(correct_ranks) if idx not in indices_to_remove]

def calculate_group_stats(group_scores, group_name):
    total_differences = []
    for participant, scores in group_scores:
        total_difference = calculate_total_difference(correct_ranks_new, scores)
        total_differences.append((participant, total_difference))

    average = sum(diff for _, diff in total_differences) / len(total_differences)
    variance = sum((diff - average) ** 2 for _, diff in total_differences) / len(total_differences)
    std_dev = math.sqrt(variance)

    print(f"\n{group_name} 组统计：")
    for participant, total_difference in total_differences:
        print(f"Score of {participant}: {total_difference}")
    print(f"{group_name} 组平均总分差异: {average}")
    print(f"{group_name} 组标准差: {std_dev}")

    return total_differences, average, std_dev


# 分组并计算
group_a_scores = [(p, s) for p, s in new_participants_scores if p.startswith('A')]
group_b_scores = [(p, s) for p, s in new_participants_scores if p.startswith('B')]
all_scores = new_participants_scores

# 计算 A 组统计
group_a_stats, group_a_avg, group_a_sd = calculate_group_stats(group_a_scores, "A")

# 计算 B 组统计
group_b_stats, group_b_avg, group_b_sd = calculate_group_stats(group_b_scores, "B")

# 计算所有用户统计
all_stats, all_avg, all_sd = calculate_group_stats(all_scores, "所有")

# 打印总结
print("\n总结：")
print(f"A 组平均总分: {group_a_avg}, 标准差: {group_a_sd}")
print(f"B 组平均总分 {group_b_avg}, 标准差: {group_b_sd}")
print(f"所有用户平均总分: {all_avg}, 标准差: {all_sd}")



# 创建合并的总分差异列表
merged_total_differences = [(participant, total_difference) for participant, total_difference in all_stats]

# # 排序合并的列表（可选，如果你想按照用户ID排序）
# merged_total_differences.sort(key=lambda x: x[0])

print("\n合并的总分差异列表：")
print("new_participants_score_desert =", merged_total_differences)