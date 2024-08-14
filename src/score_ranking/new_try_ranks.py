import random
import numpy as np

A_correct_ranks = [15,4,6,8,13,11,12,1,3,9,14,2,10,7,5]
B_correct_ranks = [4, 6, 12, 7, 11, 10, 8, 5, 15, 3, 13, 9, 14, 2, 1]
A_human_ranks = [11.18, 4.7, 8.78, 9.34, 8.94, 11.98, 9.54, 3.16, 6.92, 9.34, 8.1, 5.14, 7.3, 8.38, 7.0]
B_human_ranks = [7.64, 6.42, 5.22, 9.06, 5.1, 5.92, 9.08, 9.52, 7.46, 3.24, 9.5, 8.64, 10.9, 9.4, 12.9]

def calculate_partial_difference(correct_ranks, false_ranks, exclude_indices):
    return sum(abs(cr - ps) for i, (cr, ps) in enumerate(zip(correct_ranks, false_ranks)) if i not in exclude_indices)

def generate_initial_ranks(human_ranks, correct_ranks):
    return [random.uniform(min(human_ranks), max(human_ranks)) for _ in range(len(human_ranks))]

def optimize_ranks(correct_ranks, human_ranks, exclude_indices, target_score):
    false_ranks = generate_initial_ranks(human_ranks, correct_ranks)
    best_score_diff = float('inf')
    best_ranks = false_ranks.copy()

    for _ in range(10000):  # Number of iterations
        i = random.randint(0, len(false_ranks) - 1)
        old_value = false_ranks[i]
        false_ranks[i] = random.uniform(min(human_ranks), max(human_ranks))

        score = calculate_partial_difference(correct_ranks, false_ranks, exclude_indices)
        score_diff = abs(score - target_score)

        if score_diff < best_score_diff:
            best_score_diff = score_diff
            best_ranks = false_ranks.copy()
        else:
            false_ranks[i] = old_value

    return best_ranks

def adjust_ranks(false_ranks, human_ranks, correct_ranks):
    for i in range(len(false_ranks)):
        human_diff = abs(human_ranks[i] - correct_ranks[i])
        if human_diff < 3:
            false_ranks[i] = human_ranks[i] + random.uniform(-0.5, 0.5)
        else:
            false_ranks[i] = false_ranks[i] + random.uniform(-1, 1)
    return false_ranks

# Main optimization loop
best_A_false_ranks = None
best_B_false_ranks = None
best_score_diff = float('inf')

for _ in range(10000):  # Number of attempts
    target_score = random.uniform(65, 70)
    A_false_ranks = optimize_ranks(A_correct_ranks, A_human_ranks, [1, 5, 9], target_score)
    B_false_ranks = optimize_ranks(B_correct_ranks, B_human_ranks, [8, 13, 14], target_score)

    A_score = calculate_partial_difference(A_correct_ranks, A_false_ranks, [1, 5, 9])
    B_score = calculate_partial_difference(B_correct_ranks, B_false_ranks, [8, 13, 14])

    score_diff = abs(A_score - B_score)

    if score_diff < best_score_diff and 65 <= A_score <= 70 and 65 <= B_score <= 70:
        best_score_diff = score_diff
        best_A_false_ranks = A_false_ranks
        best_B_false_ranks = B_false_ranks

    if best_score_diff < 0.1:
        break

# Final adjustment and output
if best_A_false_ranks and best_B_false_ranks:
    best_A_false_ranks = adjust_ranks(best_A_false_ranks, A_human_ranks, A_correct_ranks)
    best_B_false_ranks = adjust_ranks(best_B_false_ranks, B_human_ranks, B_correct_ranks)

    A_score = calculate_partial_difference(A_correct_ranks, best_A_false_ranks, [1, 5, 9])
    B_score = calculate_partial_difference(B_correct_ranks, best_B_false_ranks, [8, 13, 14])

    # 将结果四舍五入到整数
    A_false_ranks_int = [round(x) for x in best_A_false_ranks]
    B_false_ranks_int = [round(x) for x in best_B_false_ranks]

    print("A_false_ranks (整数):", A_false_ranks_int)
    print("B_false_ranks (整数):", B_false_ranks_int)
    print("A_score (excluding indices 2, 6, 10):", round(A_score, 2))
    print("B_score (excluding indices 9, 14, 15):", round(B_score, 2))
    print("Score difference:", round(abs(A_score - B_score), 2))
else:
    print("未能找到满足条件的排名。请尝试放宽条件或增加迭代次数。")