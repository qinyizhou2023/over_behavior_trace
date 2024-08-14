import random

NUM_ITEMS = 15
MAX_ATTEMPTS = 10000


def calculate_total_difference(correct_ranks, false_ranks):
    return sum(abs(cr - ps) for cr, ps in zip(correct_ranks, false_ranks))


def generate_false_ranking(correct_ranks, far_indices, close_indices, semi_close_indices, allowed_distance=2):
    false_ranks = [0] * NUM_ITEMS
    available_numbers = set(range(1, NUM_ITEMS + 1))

    # 处理需要接近正确答案的索引
    for idx in close_indices:
        options = [n for n in range(max(1, correct_ranks[idx] - allowed_distance),
                                    min(NUM_ITEMS + 1, correct_ranks[idx] + allowed_distance + 1))
                   if n in available_numbers]
        if options:
            chosen = random.choice(options)
            false_ranks[idx] = chosen
            available_numbers.remove(chosen)
        else:
            chosen = random.choice(list(available_numbers))
            false_ranks[idx] = chosen
            available_numbers.remove(chosen)

    # 处理semi_close_indices
    for idx, target in semi_close_indices:
        options = [n for n in range(max(1, target - allowed_distance),
                                    min(NUM_ITEMS + 1, target + allowed_distance + 1))
                   if n in available_numbers]
        if options:
            chosen = random.choice(options)
            false_ranks[idx] = chosen
            available_numbers.remove(chosen)
        else:
            chosen = random.choice(list(available_numbers))
            false_ranks[idx] = chosen
            available_numbers.remove(chosen)

    # 处理需要远离正确答案的索引
    for idx in far_indices:
        options = list(available_numbers - set(range(max(1, correct_ranks[idx] - allowed_distance),
                                                     min(NUM_ITEMS + 1, correct_ranks[idx] + allowed_distance + 1))))
        if options:
            chosen = random.choice(options)
            false_ranks[idx] = chosen
            available_numbers.remove(chosen)
        else:
            chosen = random.choice(list(available_numbers))
            false_ranks[idx] = chosen
            available_numbers.remove(chosen)

    # 处理其他索引
    other_indices = [i for i in range(NUM_ITEMS) if
                     i not in far_indices and i not in close_indices and i not in [idx for idx, _ in
                                                                                   semi_close_indices]]
    random.shuffle(other_indices)
    for idx in other_indices:
        if available_numbers:
            chosen = random.choice(list(available_numbers))
            false_ranks[idx] = chosen
            available_numbers.remove(chosen)
        else:
            swap_idx = random.choice([i for i in range(NUM_ITEMS) if
                                      false_ranks[i] != 0 and i not in close_indices and i not in [idx for idx, _ in
                                                                                                   semi_close_indices]])
            false_ranks[idx], false_ranks[swap_idx] = false_ranks[swap_idx], false_ranks[idx]

    return false_ranks


def optimize_rankings(correct_ranks_A, correct_ranks_B):
    for _ in range(MAX_ATTEMPTS):
        A_false = generate_false_ranking(correct_ranks_A,
                                         far_indices=[4, 8, 10],
                                         close_indices=[0, 3, 13, 14],
                                         semi_close_indices=[(1, 5), (5, 12), (9, 9)])

        B_false = generate_false_ranking(correct_ranks_B,
                                         far_indices=[2, 4, 7],
                                         close_indices=[1, 6, 11],
                                         semi_close_indices=[(8, 7), (13, 10), (14, 13)])

        score_A = calculate_total_difference(correct_ranks_A,
                                             [rank for i, rank in enumerate(A_false) if i not in [1, 5, 9]])
        score_B = calculate_total_difference(correct_ranks_B,
                                             [rank for i, rank in enumerate(B_false) if i not in [8, 13, 14]])

        if 65 <= score_A <= 70 and score_A == score_B:
            return A_false, B_false

    raise ValueError("Unable to find suitable rankings after maximum attempts")


# 定义正确排名
correct_ranks_A = [15, 4, 6, 8, 13, 11, 12, 1, 3, 9, 14, 2, 10, 7, 5]
correct_ranks_B = [4, 6, 12, 7, 11, 10, 8, 5, 15, 3, 13, 9, 14, 2, 1]

# 生成满足条件的错误排名
try:
    A_false, B_false = optimize_rankings(correct_ranks_A, correct_ranks_B)

    # 计算并打印结果
    score_A = calculate_total_difference(correct_ranks_A,
                                         [rank for i, rank in enumerate(A_false) if i not in [1, 5, 9]])
    score_B = calculate_total_difference(correct_ranks_B,
                                         [rank for i, rank in enumerate(B_false) if i not in [8, 13, 14]])

    print("A_false =", A_false)
    print("B_false =", B_false)
    print("Score A (without indices 2, 6, 10):", score_A)
    print("Score B (without indices 9, 14, 15):", score_B)
    print("Total difference A:", calculate_total_difference(correct_ranks_A, A_false))
    print("Total difference B:", calculate_total_difference(correct_ranks_B, B_false))
except ValueError as e:
    print(f"Error: {e}")