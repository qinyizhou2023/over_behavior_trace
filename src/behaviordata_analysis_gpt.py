# import os
#
# file_path = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\user_behavior_small\\gpt\\P1_behavior_gpt.json'
#
# # 检查文件是否存在
# if os.path.exists(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         data = json.load(file)
# else:
#     print(f"File not found: {file_path}")

import os
import json
from datetime import datetime
import statistics

directory = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\user_behavior_small\\gpt'  # 实际目录路径

# 遍历目录中的每个文件
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)

        # 初始化统计变量
        all_results = []
        windowswitch_count = 0
        focus_time = []
        blur_time = []

        first_timestamp = None
        last_timestamp = None
        click_count = 0
        total_mouse_movement = 0
        scroll_count = 0
        total_scroll_distance = 0
        scroll_distances = []
        total_scroll_speed = 0.0
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
        keyboard_input_count = 0
        total_input_length = 0
        total_input_duration = 0
        input_length = []
        input_duration = []
        idle_count = 0
        total_idle_duration = 0
        idle_duration = []


        # 打开并读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

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

        #计算blur和focus之间的时间
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
                        'focus_start': data[i - 1]['timestamp'],
                        'blur_end': data[i]['timestamp'],
                        'duration': duration
                    })
                    i += 1


        # 遍历 JSON 数据，计算指标
        for event in data:
            if event["type"] == "blur":
                windowswitch_count += 1
            if event["type"] == "click":
                click_count += 1
            elif event["type"] == "mouseMovement":
                total_mouse_movement = event["totalMouseMovement"]
            elif event["type"] == "scroll":
                scroll_count += 1
                scroll_distance = abs(event["deltaY"])
                total_scroll_distance += scroll_distance
                scroll_distances.append(scroll_distance)
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
            elif event["type"] == "keyboardInput":
                keyboard_input_count += 1
                total_input_length += event["userInputLength"]
                total_input_duration += event["duration"]
                input_length.append(event["userInputLength"])
                input_duration.append(event["duration"])

        # 计算平均值和中位数
        total_focus_time = sum(focus_time)
        windowswitch_speed = totaltime / windowswitch_count  if windowswitch_count >0 else 0
        average_scroll_distance = total_scroll_distance / scroll_count if scroll_count > 0 else 0
        average_scroll_speed = total_scroll_distance / scroll_count if scroll_count > 0 else 0
        average_copy_length = total_copy_length / copy_count if copy_count > 0 else 0
        average_paste_length = total_paste_length / paste_count if paste_count > 0 else 0
        average_highlight_length = total_highlight_length / highlight_count if highlight_count > 0 else 0
        average_input_length = total_input_length / keyboard_input_count if keyboard_input_count > 0 else 0
        average_input_duration = total_input_duration / keyboard_input_count if keyboard_input_count > 0 else 0
        med_scroll_distance = statistics.median(scroll_distances) if scroll_distances else 0
        med_copy_length = statistics.median(copy_length) if copy_length else 0
        med_paste_length = statistics.median(paste_length) if paste_length else 0
        med_highlight_length = statistics.median(highlight_length) if highlight_length else 0
        med_idle_duration = statistics.median(idle_duration) if idle_duration else 0
        med_input_length = statistics.median(input_length) if input_length else 0
        med_input_duration = statistics.median(input_duration) if input_duration else 0

        # 构建当前文件的结果字典
        current_result = {
            "total_focus_time": total_focus_time,
            "windowswitch_count":windowswitch_count,
            "windowswitch_speed": windowswitch_speed,

            "filename": filename,
            "totaltime": totaltime,
            "click_count": click_count,
            "total_mouse_movement": total_mouse_movement,
            "scroll_count": scroll_count,
            "total_scroll_distance": total_scroll_distance,
            "average_scroll_distance": average_scroll_distance,
            "med_scroll_distance": med_scroll_distance,

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

            "keyboard_input_count": keyboard_input_count,
            "average_input_length": average_input_length,
            "average_input_duration": average_input_duration,
            "total_input_duration": total_input_duration,
            "med_input_length": med_input_length,
            "med_input_duration": med_input_duration
        }


        # 将当前文件结果添加到所有结果列表中
        all_results.append(current_result)

# 打印所有文件的结果列表
for result in all_results:
    print(result)