import json
from datetime import datetime

# File path to your JSON data
file_path = 'src/user_behavior_small/gpt'

# Load JSON data
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize lists to store focus and blur event details
focus_time = []
blur_time = []

# Iterate through events and calculate stay times
i = 0
while i < len(data):
    if data[i]['type'] == 'focus':
        focus_start = datetime.fromisoformat(data[i]['timestamp'])
        i += 1
        while i < len(data) and data[i]['type'] != 'blur':
            i += 1
        if i < len(data) and data[i]['type'] == 'blur':
            blur_end = datetime.fromisoformat(data[i]['timestamp'])
            duration = (blur_end - focus_start).total_seconds()
            focus_time.append(duration)
            blur_time.append({
                'focus_start': data[i-1]['timestamp'],
                'blur_end': data[i]['timestamp'],
                'duration': duration
            })
            i += 1

# Print or use focus_time and blur_time lists as needed
print("Stay times (seconds) between focus and blur events:")
for duration in focus_time:
    print(duration)

print("\nBlur event details:")
for blur_event in blur_time:
    print(blur_event)
