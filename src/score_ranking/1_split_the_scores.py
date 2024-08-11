# 定义输入数据字符串
data_str = """
10	4	6	12	11	8	3	13	5	1	14	9	7	2	15
10	12	2	14	5	9	8	11	6	1	7	4	13	3	15
5	6	14	7	10	4	11	15	12	1	8	3	2	13	9
1	9	6	12	8	2	10	7	5	3	14	11	4	13	15
3	4	6	5	7	8	10	11	2	1	9	13	14	12	15
2	11	3	10	4	8	12	5	6	1	13	7	9	15	14
10	1	2	5	4	3	9	6	7	8	14	11	12	15	13
5	4	10	11	6	3	13	7	2	1	15	8	9	12	14
4	15	2	3	7	9	5	10	6	11	8	1	12	13	14
3	4	6	14	7	5	9	11	8	1	2	12	13	10	15


"""

# 将字符串按行分割，并去掉首尾的空白字符
data_lines = data_str.strip().split("\n")

# 将每行数据按空格分割，并转换为整数列表
data = [list(map(int, line.split())) for line in data_lines]

# 将数据整理成所需格式
participants_scores = []
for i, scores in enumerate(data):
    participant_id = f"A{i+18}"
    participants_scores.append((participant_id, scores))

# 输出结果
for participant, scores in participants_scores:
    print(f'("{participant}", {scores}),')