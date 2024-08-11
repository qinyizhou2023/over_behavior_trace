import math
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
    ("A1", [14, 4, 9, 8, 11, 15, 3, 1, 6, 12, 13, 2, 7, 10, 5]),
    ("A2", [13, 3, 8, 6, 10, 12, 11, 1, 5, 9, 15, 2, 14, 7, 4]),
    ("A3", [14, 3, 11, 12, 4, 13, 15, 1, 10, 9, 6, 2, 5, 8, 7]),
    ("A4", [15, 12, 4, 10, 11, 14, 13, 1, 6, 3, 2, 7, 8, 9, 5]),
    ("A5", [15, 3, 11, 12, 5, 14, 6, 1, 10, 9, 13, 2, 8, 7, 4]),
    ("A6", [11, 15, 7, 5, 10, 9, 14, 3, 8, 6, 1, 13, 2, 12, 4]),
    ("A7", [13, 3, 9, 10, 11, 14, 4, 1, 5, 12, 6, 2, 8, 5, 7]),
    ("A8", [14, 4, 12, 13, 6, 10, 11, 1, 7, 15, 8, 3, 9, 2, 5]),
    ("A9", [11, 7, 2, 3, 8, 15, 9, 1, 4, 10, 12, 6, 5, 13, 14]),
    ("A10", [8, 3, 13, 14, 6, 15, 2, 5, 7, 11, 4, 1, 9, 10, 12]),
    ("A11", [12, 10, 8, 7, 14, 15, 11, 5, 1, 6, 2, 9, 3, 13, 4]),
    ("A12", [13, 1, 11, 15, 6, 14, 10, 2, 9, 12, 4, 3, 5, 8, 7]),
    ("A13", [10, 1, 9, 11, 8, 15, 14, 5, 7, 12, 4, 2, 13, 6, 3]),
    ("A14", [15, 4, 12, 11, 5, 13, 14, 1, 8, 10, 7, 2, 6, 9, 3]),
    ("A15", [12, 1, 5, 6, 7, 8, 15, 2, 9, 10, 11, 3, 13, 14, 4]),
    ("A16", [12, 3, 8, 9, 5, 11, 13, 1, 4, 15, 14, 2, 7, 10, 6]),
    ("A17", [12, 2, 8, 13, 6, 11, 15, 3, 10, 14, 4, 1, 7, 5, 9]),
    ("A18", [11, 4, 12, 13, 6, 3, 2, 1, 8, 14, 9, 7, 5, 15, 10]),
    ("A19", [14, 6, 9, 13, 8, 15, 10, 1, 4, 5, 3, 2, 12, 7, 11]),
    ("A20", [15, 6, 7, 12, 11, 14, 8, 1, 10, 2, 9, 3, 4, 13, 5]),
    ("A21", [1, 4, 2, 10, 7, 13, 3, 6, 8, 9, 14, 15, 11, 12, 5]),
    ("A22", [12, 4, 10, 5, 11, 14, 15, 9, 13, 3, 7, 6, 1, 8, 2]),
    ("A23", [12, 1, 14, 8, 9, 13, 15, 2, 10, 11, 5, 7, 6, 3, 4]),
    ("A24", [14, 1, 8, 4, 13, 15, 7, 2, 9, 10, 11, 3, 5, 6, 12]),
    ("A25", [10, 6, 5, 7, 15, 13, 14, 8, 11, 2, 12, 1, 3, 9, 4]),
    ("A26", [3, 8, 9, 1, 12, 4, 2, 5, 10, 6, 7, 14, 11, 13, 15]),
    ("A27", [15, 3, 5, 8, 11, 13, 14, 1, 7, 12, 6, 2, 9, 4, 10]),
    # B desert --moon
    ("B1", [15, 1, 8, 13, 7, 14, 3, 2, 6, 11, 5, 4, 10, 9, 12]),
    ("B2", [13, 4, 10, 7, 12, 15, 8, 2, 3, 9, 14, 5, 6, 11, 1]),
    ("B3", [5, 3, 8, 6, 7, 14, 15, 1, 10, 13, 9, 2, 11, 4, 12]),
    ("B4", [12, 4, 9, 10, 11, 15, 3, 1, 6, 14, 13, 2, 8, 7, 5]),
    ("B5", [9, 3, 2, 8, 7, 10, 4, 5, 6, 11, 12, 13, 14, 1, 15]),
    ("B6", [13, 6, 9, 10, 7, 14, 11, 1, 12, 8, 15, 2, 5, 3, 4]),
    ("B7", [13, 1, 10, 9, 12, 14, 15, 2, 3, 4, 5, 8, 6, 7, 11]),
    ("B8", [15, 6, 11, 12, 10, 14, 3, 1, 5, 13, 7, 8, 4, 9, 2]),
    ("B9", [12, 1, 13, 2, 10, 3, 4, 5, 6, 15, 9, 14, 11, 7, 8]),
    ("B10", [12, 10, 14, 15, 7, 9, 6, 2, 5, 13, 3, 8, 4, 11, 1]),
    ("B11", [1, 2, 3, 13, 4, 14, 15, 5, 6, 7, 8, 9, 10, 11, 12]),
    ("B12", [9, 3, 13, 15, 6, 8, 7, 10, 1, 14, 12, 2, 11, 5, 4]),
    ("B13", [14, 12, 6, 5, 9, 15, 11, 1, 3, 10, 4, 2, 13, 7, 8]),
    ("B14", [14, 4, 15, 12, 11, 13, 10, 5, 3, 6, 7, 8, 2, 9, 1]),
    ("B15", [12, 10, 8, 7, 14, 15, 11, 5, 1, 6, 2, 9, 3, 13, 4]),
    ("B16", [1, 2, 5, 13, 12, 4, 3, 6, 15, 10, 11, 7, 8, 9, 14]),
    ("B17", [13, 5, 2, 12, 9, 14, 15, 1, 3, 10, 6, 4, 7, 11, 8]),
    ("B18", [2, 8, 13, 12, 14, 3, 15, 4, 9, 5, 6, 10, 1, 11, 7]),
    ("B19", [7, 8, 13, 9, 14, 10, 15, 1, 11, 2, 3, 12, 4, 5, 6]),
    ("B20", [14, 3, 11, 15, 12, 13, 10, 1, 4, 9, 8, 2, 7, 5, 6]),
    ("B21", [15, 5, 4, 2, 14, 12, 13, 3, 1, 10, 7, 11, 6, 9, 8]),
    ("B22", [9, 5, 11, 12, 13, 14, 10, 4, 15, 3, 6, 8, 1, 7, 2]),
    ("B23", [6, 3, 4, 5, 7, 15, 8, 1, 10, 12, 14, 2, 13, 9, 11]),
    ("B24", [13, 8, 14, 2, 9, 6, 15, 5, 7, 3, 10, 1, 11, 12, 4]),
    ("B25", [6, 3, 7, 8, 4, 9, 2, 10, 11, 12, 13, 1, 14, 5, 15]),
    ("B26", [2, 7, 10, 9, 8, 6, 13, 11, 3, 14, 4, 1, 5, 12, 15]),
    ("B27", [15, 11, 4, 7, 3, 14, 13, 5, 6, 1, 8, 12, 9, 10, 2]),
     # ("AI", [15, 12, 13, 5, 6, 9, 4, 2, 14, 11, 3, 1, 7, 8, 10])
]
correct_ranks = [15,4,6,8,13,12,3,14,2,10,7,5]

# 定义要删除的索引（第6、8、10个数据，注意索引从0开始）
indices_to_remove = [5, 7, 9]

# 创建一个新的列表，去掉指定索引的数据
new_participants_scores = [
    (participant, [score for idx, score in enumerate(scores) if idx not in indices_to_remove])
    for participant, scores in participants_scores
]


def calculate_group_stats(group_scores, group_name):
    total_differences = []
    for participant, scores in group_scores:
        total_difference = calculate_total_difference(correct_ranks, scores)
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
#
# # 排序合并的列表（可选，如果你想按照用户ID排序）
# merged_total_differences.sort(key=lambda x: x[0])

print("\n合并的总分差异列表：")
print("new_participants_score_moon =", merged_total_differences)
