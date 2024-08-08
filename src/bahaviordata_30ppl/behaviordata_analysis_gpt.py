import os
import json
from datetime import datetime
import statistics
# # 改1： gpt
# directory = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_30ppl\\gpt'  # 实际目录路径

# 改1： tasksheet
directory = 'C:\\Users\\zqy\\Documents\\over regression\\over_behavior_trace\\src\\bahaviordata_30ppl\\tasksheet'  # 实际目录路径

all_results= []


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

        # 初始化统计变量
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
        #
        # #计算blur和focus之间的时间
        # i = 0
        # while i < len(data):
        #     if data[i]['type'] == 'focus':
        #         focus_start = datetime.fromisoformat(data[i]['timestamp'])
        #         i += 1
        #         while i < len(data) and data[i]['type'] != 'blur':
        #             i += 1
        #         if i < len(data) and data[i]['type'] == 'blur':
        #             blur_end = datetime.fromisoformat(data[i]['timestamp'])
        #             duration = (blur_end - focus_start).total_seconds()
        #             focus_time.append(duration)
        #             # blur_time.append({
        #             #     'focus_start': data[i - 1]['timestamp'],
        #             #     'blur_end': data[i]['timestamp'],
        #             #     'duration': duration
        #             # })
        #             i += 1


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
                    prompt_start_time = datetime.fromisoformat(event["timestamp"])
                    in_prompt = True

                prompt_word_count += 1


            elif event["type"] == "highlight":
                highlight_count += 1
                total_highlight_length += event["highlightedTextLength"]
                highlight_length.append(event["highlightedTextLength"])

            elif event["type"] == "idle":
                idle_count += 1
                total_idle_duration += event["duration"]
                idle_duration.append(event["duration"])

            # elif event["type"] == "keyboardInput":
            #     keyboard_input_count += 1
            #     total_input_length += event["userInputLength"]
            #     total_input_duration += event["duration"]
            #     input_length.append(event["userInputLength"])
            #     input_duration.append(event["duration"])

            elif event["type"] == "streaming_start":
                prompt_count += 1
                if in_prompt:
                    prompt_end_time = datetime.fromisoformat(event["timestamp"])
                    prompt_duration = (prompt_end_time - prompt_start_time).total_seconds()
                    prompt_durations.append(prompt_duration)
                    prompt_word_counts.append(prompt_word_count)
                    in_prompt = False
                    prompt_word_count = 0

        # 计算平均值和中位数
        total_focus_time = sum(focus_time)
        windowswitch_speed = totaltime / windowswitch_count  if windowswitch_count >0 else 0
        average_scroll_distance = total_scroll_distance / scroll_count if scroll_count > 0 else 0
        average_mousewheel_distance = total_mousewheel_distance / mousewheel_count if mousewheel_count > 0 else 0
        average_copy_length = total_copy_length / copy_count if copy_count > 0 else 0
        average_paste_length = total_paste_length / paste_count if paste_count > 0 else 0
        average_highlight_length = total_highlight_length / highlight_count if highlight_count > 0 else 0
        average_input_length = total_input_length / keyboard_input_count if keyboard_input_count > 0 else 0
        average_input_duration = total_input_duration / keyboard_input_count if keyboard_input_count > 0 else 0
        med_scroll_distance = statistics.median(scroll_distances) if scroll_distances else 0
        med_mousewheel_distance = statistics.median(mousewheel_distances) if mousewheel_distances else 0
        med_copy_length = statistics.median(copy_length) if copy_length else 0
        med_paste_length = statistics.median(paste_length) if paste_length else 0
        med_highlight_length = statistics.median(highlight_length) if highlight_length else 0
        med_idle_duration = statistics.median(idle_duration) if idle_duration else 0
        # med_input_length = statistics.median(input_length) if input_length else 0
        # med_input_duration = statistics.median(input_duration) if input_duration else 0

        # prompt writing 的平均值和中位数
        average_prompt_duration = statistics.mean(prompt_durations) if prompt_durations else 0
        med_prompt_duration = statistics.median(prompt_durations) if prompt_durations else 0
        average_prompt_word_count = statistics.mean(prompt_word_counts) if prompt_word_counts else 0
        med_prompt_word_count = statistics.median(prompt_word_counts) if prompt_word_counts else 0


        # 构建当前文件的结果字典
        current_result = {
            "filename": filename,

            "total_focus_time": total_focus_time,
            "windowswitch_count":windowswitch_count,
            "windowswitch_speed": windowswitch_speed,


            "totaltime": totaltime,
            "click_count": click_count,
            "total_mouse_movement": total_mouse_movement,

            # "scroll_count": scroll_count,
            # "total_scroll_distance": total_scroll_distance,
            # "average_scroll_distance": average_scroll_distance,
            # "med_scroll_distance": med_scroll_distance,

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

            "prompts_count": prompt_statistics['prompts_count'],
            "total_prompts_duration": prompt_statistics['total_prompts_duration'],
            "total_prompts_length": prompt_statistics['total_prompts_length'],
            "med_prompts_length": prompt_statistics['med_prompts_length']
        }

        # 将当前文件结果添加到所有结果列表中
        all_results.append(current_result)

# 打印所有文件的结果列表
print(json.dumps(all_results, indent=4))

# 改2： 将所有文件的结果写入新的JSON文件中
with open('behavior_result_tasksheet.json', 'w') as f:
    json.dump(all_results, f, indent=4)