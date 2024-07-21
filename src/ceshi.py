import os
import json
from datetime import datetime
import statistics

directory = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\user_behavior_small\\writingInterface'  # 实际目录路径
all_results = []

ignored_keycodes = {13, 16, 17, 18, 20, 27, 91, 93}
def parse_behavior_data(data):
    prompts = []
    current_prompt = None
    capturing = False
    start_time_recorded = False

    for event in data:
        if event["type"] == "streaming_start":
            if current_prompt and current_prompt["startTime"]:
                current_prompt["endTime"] = event["timestamp"]
                prompts.append(current_prompt)
            capturing = False
            start_time_recorded = False

        if event["type"] == "keypress" and event["keyCode"] not in ignored_keycodes:
            if not capturing:
                capturing = True
                current_prompt = {"startTime": None, "endTime": None, "content": ""}
                if not start_time_recorded:
                    current_prompt["startTime"] = event["timestamp"]
                    start_time_recorded = True
            if capturing:
                current_prompt["content"] += event["key"]

        if event["type"] == "streaming_end":
            capturing = False

    return prompts

def calculate_statistics(prompts):
    prompts_count = len(prompts)
    total_prompts_duration = sum(
        (datetime.fromisoformat(prompt['endTime'].replace('Z', '+00:00')) - datetime.fromisoformat(
            prompt['startTime'].replace('Z', '+00:00'))).total_seconds()
        for prompt in prompts
    )
    total_prompts_length = sum(len(prompt['content']) for prompt in prompts)
    lengths = [len(prompt['content']) for prompt in prompts]
    med_prompts_length = statistics.median(lengths) if lengths else 0

    return {
        "prompts_count": prompts_count,
        "total_prompts_duration": total_prompts_duration,
        "total_prompts_length": total_prompts_length,
        "med_prompts_length": med_prompts_length
    }

# 遍历目录中的每个文件
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Parse prompt-related data
        prompts = parse_behavior_data(data)
        prompt_statistics = calculate_statistics(prompts)

        # 构建当前文件的结果字典
        current_result = {
            "filename": filename,
            "prompts_count": prompt_statistics['prompts_count'],
            "total_prompts_duration": prompt_statistics['total_prompts_duration'],
            "total_prompts_length": prompt_statistics['total_prompts_length'],
            "med_prompts_length": prompt_statistics['med_prompts_length']
        }

        # 将当前文件结果添加到所有结果列表中
        all_results.append(current_result)

# 打印所有文件的结果列表
for result in all_results:
    print(result)
