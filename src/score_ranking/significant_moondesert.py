import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 8.2 add more
desert_scores =[41, 26, 51, 39, 43, 57, 64, 48, 52, 59, 59, 36, 45, 62, 48, 49, 50, 42, 35, 52, 44, 58, 65, 56, 56, 58, 50, 56, 45, 59, 59, 60, 52, 47, 61]
desert_scores = np.array(desert_scores)

moon_scores = [25, 19, 46, 39, 35, 67, 34, 37, 51, 64, 49, 51, 39, 24, 49, 48, 27, 47, 25, 61, 36, 39, 49, 54, 69, 63, 41, 33, 45, 49, 65, 38, 69, 62, 30]
moon_scores = np.array(moon_scores)


# # remove 3 items
# desert_scores = [41, 26, 51, 39, 43, 57, 64, 48, 52, 59, 59, 36, 49, 50, 42, 35, 52, 44, 58, 65, 56, 56, 58, 50, 56, 45]
# desert_scores = np.array(desert_scores)
#
# moon_scores = [25, 19, 46, 39, 35, 67, 34, 37, 51, 64, 49, 51, 48, 27, 47, 25, 61, 36, 39, 49, 54, 69, 63, 41, 33, 45]
# moon_scores = np.array(moon_scores)

# full items
# desert_scores = [42, 82, 62, 60, 82, 78, 64, 74, 82, 80, 62, 84, 64, 54, 56, 74, 68, 90, 94, 90, 86, 86, 72, 90, 76]
# desert_scores = np.array(desert_scores)
#
# moon_scores = [32, 20, 48, 48, 38, 74, 40, 44, 56, 74, 60, 58, 54, 32, 54, 34, 68, 40, 48, 56, 72, 76, 72, 58, 38, 54]
# moon_scores = np.array(moon_scores)

# # remove P32
# desert_scores =[41, 26, 51, 39, 43, 57, 64, 48, 52, 59, 59, 36, 49, 50, 42, 35, 52, 44, 58, 65, 56, 56, 50, 56, 45]
# desert_scores = np.array(desert_scores)
#
# moon_scores = [25, 19, 46, 39, 35, 67, 34, 37, 51, 64, 49, 51, 48, 27, 47, 25, 61, 36, 39, 49, 54, 69, 41, 33, 45]
# moon_scores = np.array(moon_scores)




# average scores
desert_avg = np.mean(desert_scores)
moon_avg = np.mean(moon_scores)
print(f"Desert average: {desert_avg}")
print(f"Moon average: {moon_avg}")

# standard deviation
desert_std = np.std(desert_scores)
moon_std = np.std(moon_scores)
print(f"Desert std: {desert_std}")
print(f"Moon std: {moon_std}")

# significance test t-test
from scipy.stats import ttest_ind
t_stat, p_val = ttest_ind(desert_scores, moon_scores)
print(f"t-statistic: {t_stat}")
print(f"p-value: {p_val}")