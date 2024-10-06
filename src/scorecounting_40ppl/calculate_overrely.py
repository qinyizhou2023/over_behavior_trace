import csv
import numpy as np

# Provided scores for task alone moon and task with AI desert
task_alone_moon =  {'B1': 42, 'B2': 52, 'B3': 66, 'B4': 36, 'B5': 58, 'B6': 59, 'B7': 43, 'B8': 56, 'B9': 46, 'C1': 23, 'C2': 56, 'C3': 55, 'C4': 27, 'C5': 31, 'C6': 43.8, 'C7': 48, 'C8': 49, 'C9': 42, 'C10': 61.3}
task_with_AI_desert =  {'B1': 76, 'B2': 51, 'B3': 74, 'B4': 72, 'B5': 74, 'B6': 54, 'B7': 51, 'B8': 74, 'B9': 58, 'C1': 74, 'C2': 74, 'C3': 48, 'C4': 70, 'C5': 68, 'C6': 76, 'C7': 74, 'C8': 74, 'C9': 75, 'C10': 63.5}

# Calculate the difference between task_with_AI_desert and task_alone_moon
minus_withAI_alone_BC = {key: task_with_AI_desert[key] - value for key, value in task_alone_moon.items()}

# Print the resulting dictionary
print(minus_withAI_alone_BC)

task_alone_desert = {'A1': 74, 'A2': 49, 'A3': 75, 'A4': 55, 'A5': 55, 'A6': 67, 'A7': 55, 'A8': 49, 'A9': 60, 'A10': 53.6, 'D1': 46, 'D2': 65, 'D3': 69, 'D4': 65, 'D5': 66, 'D6': 60, 'D7': 71, 'D8': 62, 'D9': 64}
task_with_AI_moon = {'A1': 74.5, 'A2': 29, 'A3': 38, 'A4': 75, 'A5': 75, 'A6': 75, 'A7': 75, 'A8': 75, 'A9': 75, 'A10': 75, 'D1': 49, 'D2': 55, 'D3': 35, 'D4': 69, 'D5': 75, 'D6': 80, 'D7': 56, 'D8': 75, 'D9': 75}

# Calculate the difference between task_with_AI_desert and task_alone_moon
minus_withAI_alone_AD = {key: task_with_AI_moon[key] - value for key, value in task_alone_desert.items()}

# Print the resulting dictionary
print(minus_withAI_alone_AD)







