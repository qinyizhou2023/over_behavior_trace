import os
import csv

# 修改需要处理的文件源目录
directory_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\answers'


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
    "battery": 1,
    "knife": 2,
    "map": 3,
    "raincoat": 4,
    "compass": 5,
    "kit": 6,
    "pistol": 7,
    "parachute": 8,
    "salt": 9,
    "water": 10,
    "book": 11,
    "sunglasses": 12,
    "liquor": 13,
    "overcoat": 14,
    "mirror": 15
}
# 初始化存储所有参与者的总分列表
participants_scores_desert = []

# 遍历目录中的所有文件
for filename in os.listdir(directory_path):
    if filename.endswith("desert.csv"):
        file_path = os.path.join(directory_path, filename)

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

            # 根据文件名确定组名，假设文件名格式为 C_desert.csv
            group_name = filename.split('_')[0]
            participants_scores.append((f"{group_name}{i + 1}", reordered_list))

        # 将当前文件处理的结果添加到总列表中
        participants_scores_desert.extend(participants_scores)
print(participants_scores_desert)

# 将结果存储到 CSV 文件中
output_file_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\scorecounting_30ppl\\rank_desert.csv'

with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Participant', 'Scores'])  # 写入表头
    for participant, scores in participants_scores_desert:
        writer.writerow([f"({participant}", scores, ")"])