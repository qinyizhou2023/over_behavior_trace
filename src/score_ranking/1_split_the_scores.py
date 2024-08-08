# 定义输入数据字符串
data_str = """
3	11	4	5	6	7	8	9	10	12	13	1	14	2	15
9	7	8	14	6	3	4	13	2	1	5	10	12	15	11
6	8	3	14	4	5	7	9	12	1	10	2	11	13	15



"""

# 将字符串按行分割，并去掉首尾的空白字符
data_lines = data_str.strip().split("\n")

# 将每行数据按空格分割，并转换为整数列表
data = [list(map(int, line.split())) for line in data_lines]

# 将数据整理成所需格式
participants_scores = []
for i, scores in enumerate(data):
    participant_id = f"P{i+22}"
    participants_scores.append((participant_id, scores))

# 输出结果
for participant, scores in participants_scores:
    print(f'("{participant}", {scores}),')