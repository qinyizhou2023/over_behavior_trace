import os
import json
from datetime import datetime, timedelta
import statistics
import numpy as np
import pytz
import pandas as pd

# 改1： gpt/tasksheet
directory = './task1_1_10.16'
all_results = []
timezone_fix = timedelta(hours=7)

ignored_keycodes = {13, 16, 17, 18, 20, 27, 91, 93}


def process_prompt_data(data):

    prompts_duration_time = []
    first_message_time = None
    send_count = 0

    for event in data:
        if event["type"] == "firstNotNull":
            first_message_time = datetime.strptime(event['time'],
                                                   '%m/%d/%Y, %I:%M:%S %p')
            # add 9 hours to match the timezone
            first_message_time = first_message_time.replace(
                tzinfo=pytz.timezone('UTC')) + timezone_fix
            send_count += 1

        if event["type"] == "messageInterval":
            send_count += 1
            start_time = datetime.strptime(event['startTime'],
                                           '%m/%d/%Y, %I:%M:%S %p')
            end_time = datetime.strptime(event['endTime'],
                                         '%m/%d/%Y, %I:%M:%S %p')
            message_sent_interval = end_time - start_time
            message_sent_interval = message_sent_interval.total_seconds()
            prompts_duration_time.append(message_sent_interval)
    return {
        "first_time_send_message": first_message_time,
        "prompts_count": send_count,
        "prompts_duration_time": prompts_duration_time,
    }


def process_tab_switch_data(data):
    tab_switch_count = 0
    tab_switch_time = []

    last_time_visible = None
    for event in data:
        if event["type"] == "visibilityChange":
            tab_switch_count += 1
            # 2024-10-15T06:43:58.770Z
            time_step = datetime.strptime(event['timestamp'],
                                          '%Y-%m-%dT%H:%M:%S.%fZ')
            if event['isHidden'] == True:
                last_time_visible = time_step
            if event['isHidden'] == False and last_time_visible:
                tab_switch_time.append(
                    (time_step - last_time_visible).total_seconds())
                last_time_visible = None
    return {
        "tab_switch_count": tab_switch_count,
        "total_tab_switch_time": np.sum(tab_switch_time),
        "med_tab_switch_time": np.median(tab_switch_time),
        "average_tab_switch_time": np.mean(tab_switch_time)
    }


# 遍历目录中的每个文件
for filename in os.listdir(directory):
    if 'GPT_gpt_data' in filename:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        prompt_statistics = process_prompt_data(data)
        tab_switch_statistics = process_tab_switch_data(data)

        # 初始化统计变量
        windowswitch_count = 0
        focus_time = []
        blur_time = []

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
        keyboard_input_count = 0
        total_input_length = 0
        total_input_duration = 0
        input_length = []
        input_duration = []
        idle_count = 0
        total_idle_duration = 0
        idle_duration = []

        # prompt writing 统计变量
        prompt_count = 0
        prompt_word_count = 0
        prompt_start_time = None
        prompt_durations = []
        prompt_word_counts = []
        in_prompt = False

        if data:
            first_timestamp = data[0]['timestamp']
            last_timestamp = data[-1]['timestamp']

        if first_timestamp and last_timestamp:
            time1 = datetime.fromisoformat(
                first_timestamp.replace('Z', '+00:00'))
            time2 = datetime.fromisoformat(
                last_timestamp.replace('Z', '+00:00'))
            time_difference = time2 - time1
            totaltime = time_difference.total_seconds()
        else:
            totaltime = 0

        type_set = set()
        for event in data:
            type_set.add(event["type"])
            if event["type"] == "blur":
                windowswitch_count += 1
            elif event["type"] == "focus":
                focus_time.append(1)
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
                # 处理 prompt writing 行为
                if not in_prompt:
                    prompt_start_time = datetime.fromisoformat(
                        event["timestamp"].replace('Z', '+00:00'))
                    in_prompt = True
                prompt_word_count += 1
            elif event["type"] == "highlight":
                highlight_count += 1
                total_highlight_length += len(event["text"])
                highlight_length.append(len(event["text"]))
            elif event["type"] == "idle":
                idle_count += 1
                total_idle_duration += event["duration"]
                idle_duration.append(event["duration"])

        print(type_set)
        total_focus_time = sum(focus_time)
        windowswitch_speed = totaltime / windowswitch_count if windowswitch_count > 0 else 0
        average_mousewheel_distance = total_mousewheel_distance / mousewheel_count if mousewheel_count > 0 else 0
        average_copy_length = total_copy_length / copy_count if copy_count > 0 else 0
        average_paste_length = total_paste_length / paste_count if paste_count > 0 else 0
        average_highlight_length = total_highlight_length / highlight_count if highlight_count > 0 else 0
        average_input_length = total_input_length / keyboard_input_count if keyboard_input_count > 0 else 0
        average_input_duration = total_input_duration / keyboard_input_count if keyboard_input_count > 0 else 0
        med_mousewheel_distance = statistics.median(
            mousewheel_distances) if mousewheel_distances else 0
        med_copy_length = statistics.median(copy_length) if copy_length else 0
        med_paste_length = statistics.median(
            paste_length) if paste_length else 0
        med_highlight_length = statistics.median(
            highlight_length) if highlight_length else 0
        med_idle_duration = statistics.median(
            idle_duration) if idle_duration else 0

        # only calculate time difference on minutes and seconds, ignore hours and bigger units
        # print(prompt_statistics['first_time_send_message'])
        # print(prompt_start_time)
        first_prompt_time = prompt_statistics[
            'first_time_send_message'] - prompt_start_time
        first_prompt_time = first_prompt_time.total_seconds()
        prompt_durations = prompt_statistics['prompts_duration_time'] + [
            first_prompt_time
        ] if prompt_statistics['prompts_duration_time'] else [
            first_prompt_time
        ]

        # 构建当前文件的结果字典
        current_result = {
            "filename":
            filename.split('_')[0][2:],
            "total_focus_time":
            total_focus_time,
            "windowswitch_count":
            windowswitch_count,
            "windowswitch_speed":
            windowswitch_speed,
            "totaltime":
            totaltime,
            "click_count":
            click_count,
            "total_mouse_movement":
            total_mouse_movement,
            "mousewheel_count":
            mousewheel_count,
            "total_mousewheel_distance":
            total_mousewheel_distance,
            "average_mousewheel_distance":
            average_mousewheel_distance,
            "med_mousewheel_distance":
            med_mousewheel_distance,
            "copy_count":
            copy_count,
            "average_copy_length":
            average_copy_length,
            "med_copy_length":
            med_copy_length,
            "paste_count":
            paste_count,
            "average_paste_length":
            average_paste_length,
            "med_paste_length":
            med_paste_length,
            "delete_count":
            delete_count,
            "keypress_count":
            keypress_count,
            "highlight_count":
            highlight_count,
            "average_highlight_length":
            average_highlight_length,
            "med_highlight_length":
            med_highlight_length,
            "idle_count":
            idle_count,
            "med_idle_duration":
            med_idle_duration,
            "total_idle_duration":
            total_idle_duration,
            "prompts_count":
            prompt_statistics['prompts_count'],
            "total_prompts_duration":
            np.sum(prompt_durations),
            # "total_prompts_length": prompt_statistics['total_prompts_length'],
            "med_prompts_duration":
            np.median(prompt_durations),
            "average_prompts_duration":
            np.mean(prompt_durations),
            "tab_switch_count":
            tab_switch_statistics['tab_switch_count'],
            "total_tab_switch_time":
            tab_switch_statistics['total_tab_switch_time'],
            "med_tab_switch_time":
            tab_switch_statistics['med_tab_switch_time'],
            "average_tab_switch_time":
            tab_switch_statistics['average_tab_switch_time']
        }

        # 将当前文件结果添加到所有结果列表中
        all_results.append(current_result)

# 打印所有文件的结果列表
print(json.dumps(all_results, indent=4))

data = pd.DataFrame(all_results)
data.to_csv('./behaviors/behavior_result_tasksheet.csv', index=False)
