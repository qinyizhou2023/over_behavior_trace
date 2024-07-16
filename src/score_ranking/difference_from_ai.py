import json
import numpy as np
from scipy.stats import spearmanr

# 正确的排序方式
correct_ranks = [15, 4, 6, 8, 13, 11, 12, 1, 3, 9, 14, 2, 10, 7, 5]

# AI的错误答案
AI_score_false = [8, 10, 9, 15, 2, 4, 6, 3, 11, 13, 5, 7, 1, 14, 12]

# 受到AI影响之后的用户的答案
# 用户的答案
user_ranks = {
    'P1': [15, 3, 5, 8, 14, 13, 11, 1, 4, 9, 10, 2, 12, 7, 6],
    'P2': [7, 9, 2, 13, 8, 4, 10, 1, 12, 14, 15, 11, 6, 3, 5],
    'P3': [13, 4, 8, 14, 2, 9, 10, 1, 12, 15, 7, 3, 6, 5, 11],
    'P4': [7, 9, 2, 13, 8, 4, 10, 1, 12, 14, 15, 11, 6, 3, 5],
    'P5': [12, 5, 11, 14, 3, 6, 4, 1, 15, 13, 10, 2, 8, 7, 9],
    'P6': [13, 6, 10, 14, 3, 15, 8, 1, 11, 12, 5, 2, 7, 9, 4],
    'P7': [14,15,10,9,13,12,11,1,2,7,15,4,8,6,3]
}

# 计算 MAE_correct 和 MAE_AI 的函数
def calculate_MAE(correct_ranks, participant_ranks):
    return sum(abs(cr - pr) for cr, pr in zip(correct_ranks, participant_ranks))

# 输出每个参与者的 MAE_correct 和 MAE_AI
for participant, ranks in user_ranks.items():
    MAE_correct = calculate_MAE(correct_ranks, ranks)
    MAE_AI = calculate_MAE(AI_score_false, ranks)
    print(f"{participant}, MAE_correct: {MAE_correct:.2f}, MAE_AI: {MAE_AI:.2f}")