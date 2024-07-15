import json
from datetime import datetime

# 文件路径
file_path = 'user_behavior_data_gpt/behavior_data_jingchao_gpt.json'

# 打开并读取JSON文件
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 初始化统计变量
click_count = 0
total_mouse_movement = 0
scroll_count = 0
total_scroll_distance = 0
total_scroll_speed = 0.0
copy_count = 0
total_copy_length = 0
paste_count = 0
total_paste_length = 0
delete_count = 0
keypress_count = 0
highlight_count = 0
total_highlight_length = 0
keyboard_input_count = 0
total_input_length = 0
total_input_duration = 0
idle_count = 0
total_idle_duration = 0



# 遍历 JSON 数据，计算指标
for event in data:
    if event["type"] == "click":
        click_count += 1
    elif event["type"] == "mouseMovement":
        total_mouse_movement = event["totalMouseMovement"]
        # # 提取第一个和最后一个时间戳
        # start_time = [0]["timestamp"]
        # end_time = [-1]["timestamp"]
        #
        # # 将时间戳转换为datetime对象
        # start_time_dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        # end_time_dt = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        #
        # # 计算时间差
        # time_difference = end_time_dt - start_time_dt


    elif event["type"] == "scroll":
        scroll_count += 1
        total_scroll_distance += abs(event["deltaY"])

    elif event["type"] == "copy":
        copy_count += 1
        total_copy_length += event["textLength"]
    elif event["type"] == "paste":
        paste_count += 1
        total_paste_length += event["textLength"]
    elif event["type"] == "deleteAction":
        delete_count += 1
    elif event["type"] == "keypress":
        keypress_count += 1
    elif event["type"] == "highlight":
        highlight_count += 1
        total_highlight_length += event["highlightedTextLength"]

    elif event["type"] == "idle":
        idle_count +=1
        total_idle_duration += event["duration"]

    elif event["type"] == "keyboardInput":
        keyboard_input_count += 1
        total_input_length += event["userInputLength"]
        total_input_duration += event["duration"]

# 计算平均值
average_scroll_distance = total_scroll_distance / scroll_count if scroll_count > 0 else 0
average_scroll_speed = total_scroll_distance / scroll_count if scroll_count > 0 else 0
average_copy_length = total_copy_length / copy_count if copy_count > 0 else 0
average_paste_length = total_paste_length / paste_count if paste_count > 0 else 0
average_highlight_length = total_highlight_length / highlight_count if highlight_count > 0 else 0
average_input_length = total_input_length / keyboard_input_count if keyboard_input_count > 0 else 0
average_input_duration = total_input_duration / keyboard_input_count if keyboard_input_count > 0 else 0

# 构建最终输出的字典
result = {
    # "time_difference": time_difference,
    "click_count": click_count,
    "total_mouse_movement": total_mouse_movement,
    "scroll_count": scroll_count,
    "total_scroll_distance":total_scroll_distance,
    "average_scroll_distance": average_scroll_distance,
    "copy_count": copy_count,
    "average_copy_length": average_copy_length,
    "paste_count": paste_count,
    "average_paste_length": average_paste_length,
    "delete_count": delete_count,
    "keypress_count": keypress_count,
    "highlight_count": highlight_count,
    "average_highlight_length": average_highlight_length,
    "idle_count" : idle_count,
    "total_idle_duration" : total_idle_duration,
    "keyboard_input_count" : keyboard_input_count,
    "average_input_length": average_input_length,
    "average_input_duration": average_input_duration,
    "total_input_duration": total_input_duration,
    "keyboard_input_count":keyboard_input_count
}

# 打印结果字典
print(result)
