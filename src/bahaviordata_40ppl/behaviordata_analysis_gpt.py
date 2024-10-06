
import os
import json
from datetime import datetime
import statistics

# 改1： tasksheet
directory = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_40ppl\\gpt'  # 实际目录路径

all_results = []

ignored_keycodes = {13, 16, 17, 18, 20, 27, 91, 93}


def count_prompts(data):
    prompt_count = 0
    for event in data:
        if event["type"] == "streaming_start":
            prompt_count += 1
    return prompt_count

def calculate_prompt_durations(data):
    prompt_durations = []
    prompt_start = None
    for event in data:
        if event["type"] in ["keypress", "copy", "paste"] and prompt_start is None:
            prompt_start = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        elif event["type"] == "streaming_start" and prompt_start is not None:
            prompt_end = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
            duration = (prompt_end - prompt_start).total_seconds()
            prompt_durations.append(duration)
            prompt_start = None
    return prompt_durations

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        prompt_durations = calculate_prompt_durations(data)

        if prompt_durations:
            average_prompt_duration = statistics.mean(prompt_durations)
            med_prompt_duration = statistics.median(prompt_durations)
        else:
            average_prompt_duration = 0
            med_prompt_duration = 0
        # 初始化统计变量
        windowswitch_count = 0
        focus_time = []
        first_timestamp = None
        last_timestamp = None
        click_count = 0
        total_mouse_movement = 0
        mousewheel_count = 0
        total_mousewheel_distance = 0
        mousewheel_distances = []
        copy_count = 0
        total_copy_length = 0
        copy_length = []
        paste_count = 0
        total_paste_length = 0
        paste_length = []
        delete_count = 0
        keypress_count = 0
        highlight_count = 0
        total_highlight_length = 0
        highlight_length = []
        idle_count = 0
        total_idle_duration = 0
        idle_duration = []

        # 计算totaltime
        if data:
            first_timestamp = data[0]['timestamp']
            last_timestamp = data[-1]['timestamp']

        if first_timestamp and last_timestamp:
            time1 = datetime.fromisoformat(first_timestamp)
            time2 = datetime.fromisoformat(last_timestamp)
            time_difference = time2 - time1
            totaltime = time_difference.total_seconds()
        else:
            totaltime = 0

        # 遍历 JSON 数据，计算指标
        for event in data:
            if event["type"] == "blur":
                windowswitch_count += 1
            elif event["type"] == "click":
                click_count += 1
            elif event["type"] == "mouseMovement":
                total_mouse_movement = event["totalMouseMovement"]
            elif event["type"] == "mousewheel":
                mousewheel_count += 1
                mousewheel_distance = abs(event["deltaY"])
                total_mousewheel_distance += mousewheel_distance
                mousewheel_distances.append(mousewheel_distance)
            elif event["type"] == "copy":
                copy_count += 1
                total_copy_length += event["textLength"]
                copy_length.append(event["textLength"])
            elif event["type"] == "paste":
                paste_count += 1
                total_paste_length += event["textLength"]
                paste_length.append(event["textLength"])
            elif event["type"] == "deleteAction":
                delete_count += 1
            elif event["type"] == "keypress":
                keypress_count += 1
            elif event["type"] == "highlight":
                highlight_count += 1
                total_highlight_length += event["highlightedTextLength"]
                highlight_length.append(event["highlightedTextLength"])
            elif event["type"] == "idle":
                idle_count += 1
                total_idle_duration += event["duration"]
                idle_duration.append(event["duration"])

        # 计算平均值和中位数
        total_focus_time = sum(focus_time)
        windowswitch_speed = totaltime / windowswitch_count if windowswitch_count > 0 else 0
        average_mousewheel_distance = total_mousewheel_distance / mousewheel_count if mousewheel_count > 0 else 0
        average_copy_length = total_copy_length / copy_count if copy_count > 0 else 0
        average_paste_length = total_paste_length / paste_count if paste_count > 0 else 0
        average_highlight_length = total_highlight_length / highlight_count if highlight_count > 0 else 0
        med_mousewheel_distance = statistics.median(mousewheel_distances) if mousewheel_distances else 0
        med_copy_length = statistics.median(copy_length) if copy_length else 0
        med_paste_length = statistics.median(paste_length) if paste_length else 0
        med_highlight_length = statistics.median(highlight_length) if highlight_length else 0
        med_idle_duration = statistics.median(idle_duration) if idle_duration else 0

        # 构建当前文件的结果字典
        current_result = {
            "filename": filename,
            "total_working_time": totaltime,
            "average_prompt_duration": average_prompt_duration,
            "med_prompt_duration": med_prompt_duration,
            "total_focus_time": total_focus_time,
            "windowswitch_count": windowswitch_count,
            "windowswitch_speed": windowswitch_speed,
            "totaltime": totaltime,
            "click_count": click_count,
            "total_mouse_movement": total_mouse_movement,
            "mousewheel_count": mousewheel_count,
            "total_mousewheel_distance": total_mousewheel_distance,
            "average_mousewheel_distance": average_mousewheel_distance,
            "med_mousewheel_distance": med_mousewheel_distance,
            "copy_count": copy_count,
            "average_copy_length": average_copy_length,
            "med_copy_length": med_copy_length,
            "paste_count": paste_count,
            "average_paste_length": average_paste_length,
            "med_paste_length": med_paste_length,
            "delete_count": delete_count,
            "keypress_count": keypress_count,
            "highlight_count": highlight_count,
            "average_highlight_length": average_highlight_length,
            "med_highlight_length": med_highlight_length,
            "idle_count": idle_count,
            "med_idle_duration": med_idle_duration,
            "total_idle_duration": total_idle_duration,
        }

        # 将当前文件结果添加到所有结果列表中
        all_results.append(current_result)

# 打印所有文件的结果列表
print(json.dumps(all_results, indent=4))

# 改2： 将所有文件的结果写入新的JSON文件中
with open('behavior_result_gpt_4.json', 'w') as f:
    json.dump(all_results, f, indent=4)