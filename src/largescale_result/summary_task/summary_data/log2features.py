import os
import json
from datetime import datetime, timedelta
import statistics
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

ignored_keycodes = {13, 16, 17, 18, 20, 27, 91, 93}


def parse_hour_minute(time_string):
    formats = [
        '%Y/%m/%d, %H:%M:%S', '%m/%d/%Y, %I:%M:%S %p', '%Y/%m/%d %H:%M:%S',
        '%m.%d.%Y %I:%M:%S', '%d/%m/%Y %H:%M:%S', '%d.%m.%Y, %H:%M:%S'
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(time_string, fmt)
            return dt.minute * 60 + dt.second
        except ValueError:
            continue
    print(time_string)
    raise ValueError('No valid format found')


def process_prompt_data(data):

    prompts_duration_time = []
    first_message_time = None
    send_count = 0

    for event in data:
        if event["type"] == "firstNotNull":
            first_message_time = parse_hour_minute(event["time"])
            send_count += 1

        if event["type"] == "messageInterval":
            send_count += 1

            message_sent_interval = event["duration"] / 1000
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


def main(directory):

    for filename in os.listdir(directory):

        try:
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            prompt_statistics = process_prompt_data(data)
            tab_switch_statistics = process_tab_switch_data(data)

            # 初始化统计变量
            element_switch_count = 0
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

            prompt_word_count = 0
            prompt_start_time = None
            prompt_durations = []
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

            for event in data:
                if event["type"] == "blur":
                    element_switch_count += 1
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
                    try:
                        high_len = len(event["highlightedText"])
                    except:
                        high_len = len(event['text'])
                    total_highlight_length += high_len
                    highlight_length.append(high_len)
                elif event["type"] == "idle":
                    idle_count += 1
                    total_idle_duration += event["duration"]
                    idle_duration.append(event["duration"])

            total_focus_time = sum(focus_time)
            element_switch_speed = totaltime / element_switch_count if element_switch_count > 0 else 0
            average_mousewheel_distance = total_mousewheel_distance / mousewheel_count if mousewheel_count > 0 else 0
            average_copy_length = total_copy_length / copy_count if copy_count > 0 else 0
            average_paste_length = total_paste_length / paste_count if paste_count > 0 else 0
            average_highlight_length = total_highlight_length / highlight_count if highlight_count > 0 else 0
            average_idle_duration = statistics.mean(
                idle_duration) if idle_duration else 0

            if prompt_start_time is not None:
                start_hm = prompt_start_time.minute * 60 + prompt_start_time.second
                first_prompt_time = prompt_statistics[
                    'first_time_send_message'] - start_hm if prompt_statistics[
                        'first_time_send_message'] else 0
                prompt_durations = prompt_statistics[
                    'prompts_duration_time'] + [
                        first_prompt_time
                    ] if prompt_statistics['prompts_duration_time'] else [
                        first_prompt_time
                    ]
            else:
                prompt_durations = []

            # 构建当前文件的结果字典
            # filename = filename.split('_')[0][2:]
            filename = filename.split('.')[0]
            current_result = {
                "filename":
                int(filename),
                "total_focus_time":
                total_focus_time,
                "element_switch_count":
                element_switch_count,
                "element_switch_speed":
                element_switch_speed,
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
                "copy_count":
                copy_count,
                "average_copy_length":
                average_copy_length,
                "paste_count":
                paste_count,
                "average_paste_length":
                average_paste_length,
                "delete_count":
                delete_count,
                "keypress_count":
                keypress_count,
                "highlight_count":
                highlight_count,
                "average_highlight_length":
                average_highlight_length,
                "idle_count":
                idle_count,
                "average_idle_duration":
                average_idle_duration,
                "total_idle_duration":
                total_idle_duration,
                "prompts_count":
                prompt_statistics['prompts_count'],
                "total_prompts_duration":
                np.sum(prompt_durations),
                "average_prompts_duration":
                np.mean(prompt_durations),
                "tab_switch_count":
                tab_switch_statistics['tab_switch_count'],
                "total_tab_switch_time":
                tab_switch_statistics['total_tab_switch_time'],
                "average_tab_switch_time":
                tab_switch_statistics['average_tab_switch_time']
                if tab_switch_statistics['average_tab_switch_time'] else 0,
            }
            
            if 'tasksheet' in directory:
                delete_features = ['total_focus_time', 'element_switch_count', 'element_switch_speed', 'prompts_count', 'total_prompts_duration', 'average_prompts_duration', 'tab_switch_count', 'total_tab_switch_time', 'average_tab_switch_time']
                for feature in delete_features:
                    del current_result[feature]

            
            df = pd.DataFrame([current_result])
            if not os.path.exists(f'./features/{directory.split("_")[0]}_features.csv'):
                df.to_csv(f'./features/{directory.split("_")[0]}_features.csv',
                          index=False)
            else:
                df.to_csv(f'./features/{directory.split("_")[0]}_features.csv',
                          mode='a',
                          header=False,
                          index=False)
        except Exception as e:
            print(e, filename)


if __name__ == "__main__":
    # dir = './gpt_rawdata'
    # dir = './tasksheet_rawdata'
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, default='gpt_rawdata')
    dir = parser.parse_args().dir
    main(dir)
