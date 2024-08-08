import csv

# Provided scores for task alone moon and task with AI desert
task_alone_moon = {'B1': 37, 'B2': 48, 'B3': 47, 'B4': 41, 'B5': 47, 'B6': 49, 'C1': 57, 'C2': 54, 'C3': 40, 'C4': 39, 'C5': 37, 'C6': 40, 'C7': 24}
task_with_AI_desert = {'B1': 37, 'B2': 37, 'B3': 54, 'B4': 63, 'B5': 38, 'B6': 55, 'C1': 59, 'C2': 52, 'C3': 63, 'C4': 65, 'C5': 69, 'C6': 64, 'C7': 65}

# Calculate the difference between task_with_AI_desert and task_alone_moon
minus_withAI_alone_BC = {key: task_with_AI_desert[key] - value for key, value in task_alone_moon.items()}

# Print the resulting dictionary
print(minus_withAI_alone_BC)

task_alone_desert = {'A1': 36, 'A2': 61, 'A3': 42, 'A4': 45, 'A5': 55, 'A6': 40, 'A7': 58, 'A8': 39, 'D1': 55, 'D2': 49, 'D3': 62, 'D4': 62, 'D5': 67, 'D6': 44}
task_with_AI_moon = {'A1': 49, 'A2': 32, 'A3': 61, 'A4': 51, 'A5': 65, 'A6': 30, 'A7': 11, 'A8': 65, 'D1': 32, 'D2': 50, 'D3': 38, 'D4': 22, 'D5': 43, 'D6': 43}

# Calculate the difference between task_with_AI_desert and task_alone_moon
minus_withAI_alone_AD = {key: task_with_AI_moon[key] - value for key, value in task_alone_desert.items()}

# Print the resulting dictionary
print(minus_withAI_alone_AD)



