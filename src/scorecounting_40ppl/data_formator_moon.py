

import os
import csv

# 修改需要处理的文件源目录
directory_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_40ppl\\answers'


def process_csv(file_path):
    users_answers = []
    current_user_answers = []

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:  # Skip empty rows
                continue
            answer = row[0].strip()
            if answer.startswith("1."):
                if current_user_answers:
                    users_answers.append(current_user_answers)
                current_user_answers = [answer]
            elif answer.startswith("15."):
                current_user_answers.append(answer)
                users_answers.append(current_user_answers)
                current_user_answers = []
            else:
                current_user_answers.append(answer)

        if current_user_answers:  # Append last user answers if any
            users_answers.append(current_user_answers)

    return users_answers


def convert_answers_to_scores(answers, replacements):
    result = []
    unmatched_lines = []
    for answer in answers:
        matched = False
        for key, value in replacements.items():
            if key.lower() in answer.lower():
                result.append(value)
                matched = True
                break
        if not matched:
            unmatched_lines.append(answer)

    reordered_list = [None] * len(replacements)
    for index, value in enumerate(result):
        if value <= len(replacements):
            reordered_list[value - 1] = index + 1

    return reordered_list, unmatched_lines


# 定义关键词和对应的数字
replacements = {
    "matches": 1,
    "food": 2,
    "rope": 3,
    "silk": 4,
    "heating": 5,
    "pistols": 6,
    "milk": 7,
    "oxygen": 8,
    "map": 9,
    "raft": 10,
    "compass": 11,
    "water": 12,
    "flares": 13,
    "kit": 14,
    "FM": 15
}

# 定义用于填充None值的列表
replacement_scores = [11.2, 4.7, 8.8, 9.3, 9, 12, 9.5, 3.1, 7, 9.3, 8, 7.3, 8.4, 7, 9.5]  # Added 9.5 for FM

# 初始化存储所有参与者的总分列表
participants_scores_moon = []

# 遍历目录中的所有文件
for filename in os.listdir(directory_path):
    if filename.endswith("moon.csv"):
        file_path = os.path.join(directory_path, filename)

        print(f"\nProcessing file: {filename}")

        # 处理CSV文件
        users_answers = process_csv(file_path)

        # 将结果存储在 participants_scores 列表中
        participants_scores = []
        for i, user_answers in enumerate(users_answers):
            user_data = "\n".join(user_answers)
            lines = user_data.split('\n')
            result = []
            unmatched_lines = []

            for line in lines:
                matched = False
                for key, value in replacements.items():
                    if key.lower() in line.lower():
                        result.append(value)
                        matched = True
                        break
                if not matched:
                    unmatched_lines.append(line)

            reordered_list = [None] * len(replacements)
            for index, value in enumerate(result):
                if value <= len(replacements):
                    reordered_list[value - 1] = index + 1

            # 填充None值并打印替换信息
            replacements_made = []
            for j, value in enumerate(reordered_list):
                if value is None:
                    reordered_list[j] = replacement_scores[j]
                    replacements_made.append(j + 1)  # 添加1是因为索引从0开始，但我们想显示从1开始的位置

            # 打印替换信息
            if replacements_made:
                print(f"  In {filename}, participant {i+1}: Replaced positions {replacements_made}")

            # 根据文件名确定组名，假设文件名格式为 C_moon.csv
            group_name = filename.split('_')[0]
            participants_scores.append((f"{group_name}{i + 1}", reordered_list))

        # 将当前文件处理的结果添加到总列表中
        participants_scores_moon.extend(participants_scores)

print("\nAll replacements complete. Final scores:")
print(participants_scores_moon)

# 将结果存储到 CSV 文件中
output_file_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_40ppl\\rank_moon.csv'

with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Participant', 'Scores'])  # 写入表头
    for participant, scores in participants_scores_moon:
        writer.writerow([f"({participant}", scores, ")"])

print(f"\nResults have been saved to {output_file_path}")