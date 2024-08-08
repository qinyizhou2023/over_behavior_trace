# 定义原始输入数据字符串
data_str = """
Score of P12: 41
Score of P13: 26
Score of P14: 51
Score of P15: 39
Score of P16: 43
Score of P17: 57
Score of P18: 64
Score of P19: 48
Score of P20: 52
Score of P21: 59
Score of P36: 59
Score of P37: 36
Score of P42: 45
Score of P43: 62
Score of P44: 48
Score of P22: 49
Score of P23: 50
Score of P24: 42
Score of P25: 35
Score of P26: 52
Score of P27: 44
Score of P28: 58
Score of P29: 65
Score of P30: 56
Score of P31: 56
Score of P32: 58
Score of P33: 50
Score of P34: 56
Score of P35: 45
Score of P36: 59
Score of P37: 59
Score of P38: 60
Score of P39: 52
Score of P40: 47
Score of P41: 61
"""

# 按行分割数据，并去掉首尾的空白字符
data_lines = data_str.strip().split("\n")

# 提取分数部分并转换为整数列表
scores = [int(line.split(":")[1].strip()) for line in data_lines]
print(scores)

# 计算平均值
average_score = sum(scores) / len(scores)

# 打印平均值
print(f"Average score: {average_score}")
