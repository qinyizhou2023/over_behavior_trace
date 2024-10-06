import random


def calculate_total_difference(correct_ranks, false_ranks):
    return sum(abs(cr - fr) for cr, fr in zip(correct_ranks, false_ranks))


def calculate_modified_score(correct_ranks, false_ranks, exclude_indices):
    modified_correct = [rank for i, rank in enumerate(correct_ranks) if i + 1 not in exclude_indices]
    modified_false = [rank for i, rank in enumerate(false_ranks) if i + 1 not in exclude_indices]
    return calculate_total_difference(modified_correct, modified_false)


def generate_false_ranks(correct_ranks, exclude_indices, target_score):
    while True:
        false_ranks = list(range(1, len(correct_ranks) + 1))
        random.shuffle(false_ranks)
        score = calculate_modified_score(correct_ranks, false_ranks, exclude_indices)
        if 65 <= score <= 70:
            return false_ranks, score


def find_matching_ranks():
    A_correct = [15, 4, 6, 8, 13, 11, 12, 1, 3, 9, 14, 2, 10, 7, 5]
    B_correct = [4, 6, 12, 7, 11, 10, 8, 5, 15, 3, 13, 9, 14, 2, 1]

    while True:
        A_false, A_score = generate_false_ranks(A_correct, [2, 6, 10], None)
        B_false, B_score = generate_false_ranks(B_correct, [9, 14, 15], A_score)

        if A_score == B_score:
            return A_false, B_false, A_score


A_false, B_false, score = find_matching_ranks()

print(f"A_false: {A_false}")
print(f"B_false: {B_false}")
print(f"Matching score: {score}")
#
# import random
# from typing import List, Tuple, Optional
#
#
# def calculate_total_difference(ranks1: List[float], ranks2: List[float]) -> float:
#     return sum(abs(r1 - r2) for r1, r2 in zip(ranks1, ranks2))
#
#
# def calculate_modified_score(correct_ranks: List[int], false_ranks: List[int], exclude_indices: List[int]) -> float:
#     modified_correct = [rank for i, rank in enumerate(correct_ranks) if i + 1 not in exclude_indices]
#     modified_false = [rank for i, rank in enumerate(false_ranks) if i + 1 not in exclude_indices]
#     return calculate_total_difference(modified_correct, modified_false)
#
#
# def generate_false_ranks(correct_ranks: List[int], human_ranks: List[float], exclude_indices: List[int],
#                          target_score: float) -> Optional[Tuple[List[int], float]]:
#     best_false_ranks = None
#     best_score_diff = float('inf')
#
#     for _ in range(1000):  # 尝试1000次
#         available_ranks = list(range(1, 16))
#         false_ranks = [0] * 15
#
#         # 首先处理不在exclude_indices中的位置
#         for i in range(15):
#             if i + 1 not in exclude_indices:
#                 target = round(human_ranks[i])
#                 closest = min(available_ranks, key=lambda x: abs(x - target))
#                 false_ranks[i] = closest
#                 available_ranks.remove(closest)
#
#         # 然后随机填充剩余的位置
#         for i in range(15):
#             if false_ranks[i] == 0:
#                 rank = random.choice(available_ranks)
#                 false_ranks[i] = rank
#                 available_ranks.remove(rank)
#
#         score = calculate_modified_score(correct_ranks, false_ranks, exclude_indices)
#         score_diff = abs(score - target_score)
#
#         if 64 <= score <= 70 and score_diff < best_score_diff:
#             best_false_ranks = false_ranks
#             best_score_diff = score_diff
#
#             if score_diff <= 2:  # 如果分数差异很小，就直接返回
#                 return best_false_ranks, score
#
#     if best_false_ranks is None:
#         print(f"Warning: Could not find suitable false ranks for target score {target_score}")
#         return None
#
#     return best_false_ranks, calculate_modified_score(correct_ranks, best_false_ranks, exclude_indices)
#
#
# def find_matching_ranks(A_correct: List[int], B_correct: List[int],
#                         A_human: List[float], B_human: List[float],
#                         num_pairs: int = 5) -> List[Tuple[List[int], List[int], float]]:
#     results = []
#     attempts = 0
#     max_attempts = 5000  # 增加最大尝试次数
#
#     while len(results) < num_pairs and attempts < max_attempts:
#         target_score = random.uniform(64, 70)
#         A_result = generate_false_ranks(A_correct, A_human, [2, 6, 10], target_score)
#
#         if A_result is None:
#             attempts += 1
#             continue
#
#         A_false, A_score = A_result
#         B_result = generate_false_ranks(B_correct, B_human, [9, 14, 15], A_score)
#
#         if B_result is None:
#             attempts += 1
#             continue
#
#         B_false, B_score = B_result
#
#         if abs(A_score - B_score) < 1:
#             results.append((A_false, B_false, A_score))
#
#         attempts += 1
#
#     if len(results) < num_pairs:
#         print(
#             f"Warning: Could only generate {len(results)} pairs out of {num_pairs} requested after {attempts} attempts")
#
#     return results
#
#
# # 主程序
# A_correct = [15, 4, 6, 8, 13, 11, 12, 1, 3, 9, 14, 2, 10, 7, 5]
# B_correct = [4, 6, 12, 7, 11, 10, 8, 5, 15, 3, 13, 9, 14, 2, 1]
# A_human = [11.18, 4.7, 8.78, 9.34, 8.94, 11.98, 9.54, 3.16, 6.92, 9.34, 8.1, 5.14, 7.3, 8.38, 7.0]
# B_human = [7.64, 6.42, 5.22, 9.06, 5.1, 5.92, 9.08, 9.52, 7.46, 3.24, 9.5, 8.64, 10.9, 9.4, 12.9]
#
# matching_ranks = find_matching_ranks(A_correct, B_correct, A_human, B_human)
#
# for i, (A_false, B_false, score) in enumerate(matching_ranks, 1):
#     print(f"\nPair {i}:")
#     print(f"A_false: {A_false}")
#     print(f"B_false: {B_false}")
#     print(f"Matching score: {score:.2f}")
#     print(f"A_false unique check: {len(set(A_false)) == 15 and all(1 <= x <= 15 for x in A_false)}")
#     print(f"B_false unique check: {len(set(B_false)) == 15 and all(1 <= x <= 15 for x in B_false)}")