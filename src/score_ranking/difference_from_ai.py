import json
import numpy as np
from scipy.stats import spearmanr

# 正确的排序方式
correct_ranks = [15, 4, 6, 8, 13, 11, 12, 1, 3, 9, 14, 2, 10, 7, 5]

# AI的错误答案
AI_score_false = [8, 10, 9, 15, 2, 4, 6, 3, 11, 13, 5, 7, 1, 14, 12]

# 受到AI影响之后的用户的答案
P6_Ranks = [13,	6,	10,	14,	3,	15,	8,	1,	11,	12,	5,	2,	7, 9,	4]
P4_ranks = [7,	9,	2,	13,	8,	4,	10,	1,	12,	14,	15,	11,	6,	3,	5]
P1_ranks = [15,	3,	5,	8,	14,	13,	11,	1,	4,	9,	10,	2,	12,	7,	6]
P3_ranks = [13,	4,	8,	14,	2,	9,	10,	1,	12,	15,	7,	3,	6,	5,	11]
P2_Ranks = [15,	6,	13,	10,	7,	12,	11,	1,	4,	14,	5,	2,	3,	8,	9]
P_Ranks = [6,	3,	12,	13,	5,	8,	15,	1,	14,	4,	10,	2,	7,	9,	11]

# 计算用户排序与正确排序之间的Spearman相关系数
corr_user_correct, _ = spearmanr(correct_ranks, P6_Ranks)

# 计算用户排序与AI排序之间的Spearman相关系数
corr_user_AI, _ = spearmanr(AI_score_false, P6_Ranks)

print(f"Correlation between user's ranks and correct ranks: {corr_user_correct}")
print(f"Correlation between user's ranks and AI's ranks: {corr_user_AI}")

# 计算每个选项的影响程度
impact_correct = np.abs(np.array(correct_ranks) - np.array(P6_Ranks))
impact_AI = np.abs(np.array(AI_score_false) - np.array(P6_Ranks))

print("\nImpact from correct ranks:")
for i, impact in enumerate(impact_correct):
    print(f"Item {i+1}: {impact}")

print("\nImpact from AI ranks:")
for i, impact in enumerate(impact_AI):
    print(f"Item {i+1}: {impact}")

# 选出每个用户受到AI影响最大的选项
user_impact = {}

for i in range(len(P6_Ranks)):
    if impact_AI[i] > impact_correct[i]:
        user_impact[f'Item {i+1}'] = impact_AI[i]

print("\nUser impact from AI (greater than correct impact):")
print(impact_AI-impact_correct)