# Score Counting 
## Measure Overreliance
  - We retrieve the gpt logs to check if they have truly mentioned this item
  - Pick the items that have truly been mentioned by GPT.

### Whether users are overreliance?


[1]

To quantify the degree of user overreliance, you can use the Mean Absolute Error (MAE) method combined with a comparison approach to gauge how closely the user's influenced ranking aligns with the AI's incorrect ranking compared to the correct ranking. Here is a step-by-step approach:

1. **Calculate the Mean Absolute Error (MAE) for Different Rankings**:
    - **MAE between User's Influenced Ranking and Correct Ranking (MAE\_correct)**:
      \[
      \text{MAE\_correct} = \frac{1}{n} \sum_{i=1}^{n} | \text{User\_influenced\_rank}[i] - \text{Correct\_rank}[i] |
      \]
    - **MAE between User's Influenced Ranking and AI's Incorrect Ranking (MAE\_AI)**:
      \[
      \text{MAE\_AI} = \frac{1}{n} \sum_{i=1}^{n} | \text{User\_influenced\_rank}[i] - \text{AI\_incorrect\_rank}[i] |
      \]

2. **Calculate Overreliance Index**:
    - Define an overreliance index as the ratio of the MAE between the user's influenced ranking and the AI's incorrect ranking to the MAE between the user's influenced ranking and the correct ranking:
      \[
      \text{Overreliance\_Index} = \frac{\text{MAE\_AI}}{\text{MAE\_correct}}
      \]
    - If the Overreliance Index is greater than 1, it indicates that the user’s ranking is closer to the AI's incorrect ranking than to the correct ranking, suggesting overreliance. The higher the index, the greater the degree of overreliance.

3. **Interpret the Overreliance Index**:
    - **Overreliance Index < 1**: User's influenced ranking is closer to the correct ranking, indicating less overreliance.
    - **Overreliance Index = 1**: User's influenced ranking is equally distant from both the correct and AI's incorrect rankings.
    - **Overreliance Index > 1**: User's influenced ranking is closer to the AI's incorrect ranking, indicating overreliance.


  - For items mentioned by GPT:
  - If index＜1, it indicates that the user is more influenced by GPT.
  - If the MAE between the user ranking and the AI ranking is less than the MAE between the user ranking and the correct ranking, it can be considered that the user has a certain degree of overreliance.
----
[2]
Compare MAE between:

    - MAE_human_alone = user alone & correct answer

    - MAE_ai = Al alone & correct answer

    - MAE_human_with_ai = human + AI & correct answer

  - For items mentioned by GPT, If MAE_human_with_ai ＜ MAEu:
  - it indicates that the human+AI team is performing worse than either the human or AI alone, suggesting overreliance.

### How much does the user overreliance?

(MAE_AI - MAE_correct)²

the higher, the more reliant on AI


# Logged Data
### Behaviors Within GPT Interface
In [`behaviorTracker_extension_gpt`](src/behaviorTracker_extension_gpt), We logged many users' behaviors, including mousemovement, copy-paste, click...   

| Behavior     | Attribute                  | Type   | Description                                                                                                                             |
|--------------|----------------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------|
| windowswitch | `windowswitch_count`       | number | The number of of window switch actions.                                                                                                 |
|              | `windowswitch_speed`       |        | totaltime / windowswitch_count.                                                                                                         |
|              | `total_focus_time`         |        | Total time spent on GPT window (seconds).                                                                                               |
| click        | `click_count`              | number | The number of of click actions.                                                                                                         |
| Mousemovement | `mouseMovenment`           | number | The distance of each mouse movement.                                                                                                    |
|              | `total_mouse_Movenment`    | number | The total distance the mouse moves.                                                                                                     |
| scroll       | `scroll_count`             | number | The number of of scroll actions.                                                                                                        |
|              | `total_scroll_distance `   | number | The total distance scroll.                                                                                                              |
|              | `average_scroll_distance`  | number | The average diatance of scroll actions.                                                                                                 |
|              | `med_scroll_distance`      | number | The median diatance of scroll actions.                                                                                                  |
| copy         | `copy_count`               | number | The total times of copy.                                                                                                                |
|              | `med_copy_length`          | number | The median length of copy actions.                                                                                                      |
|              | `average_scroll_distance`  | number | The average of all rolling distances                                                                                                    |
| paste        | `paste_count`              | number | The number of paste actions.                                                                                                            |
|              | `med_paste_length`         | number | The median length of paste actions.                                                                                                     |
|              | `average_paste_length`     | number | The average length of each paste action.                                                                                                |
| deleteAction | `delet_count`              | number | The number of delet actions. (delet, backspace, ctrl+z included.)                                                                       |
| keypress     | `keypress_count`           | number | The number of keypress actions.                                                                                                         |
| highlight    | `highlight_count`          | number | The number of highlight actions.                                                                                                        |
|              | `total_highlight_length`   | number | The total length of all highlights.                                                                                                     |
|              | `med_highlight_length`     | number | The median length of highlights.                                                                                                        |
|              | `average_highlight_length` | number | The average length of each highlight.                                                                                                   |
| idle         | `idle_count`               | number | The number of pauses detected.(Idle records a pause time when there is no activity for over 2000 milliseconds.)                         |
|              | `total_idle_duration`      | number | The total duration of all pauses.                                                                                                       |
|              | `med_idle_duration`        | number | The median duration of pauses.                                                                                                          |
|              | `average_idle_duration`    | number | The average duration of each pause.                                                                                                     |
| windowSwitch | `windowswitch_count`       | number | The total times of window switches.                                                                                                     |
| keyboardInput |                            |        | The time between the user starting to type in the textarea and clicking the send button.                                                |
|              | `time_before_input`        | number | The time elapsed between two input prompt actions.                                                                                      |
|              | `keyboard_input_count`     | number | The total number of input prompts.                                                                                                      |
|              | `med_input_length`         | number | The median length of the input prompts.                                                                                                 |
|              | `average_input_length`     | number | The average length of each input prompt.                                                                                                |
|              | `med_input_duration`       | number | The median time taken to write an input prompt.                                                                                         |
|              | `average_input_duration`   | number | The average time taken to write each input prompt.                                                                                      |
|              | `total_input_duration`     | number | The total time spent by the user writing input prompts.                                                                                 |
|              | `input_proportion`         | number | The proportion of time the user spends writing prompts compared to the total task completion time: `total_input_duration / total_time`. |
### Time Sequence Logs
Each block is logged within different time-windows:
- `totaltime`: Total time spent in finishing the task.
- `answerGenerate`: While GPT is generating the answer. The time between the user click the send button to the send button become actived.
- `keyboardInput`: While user is writing the prompt. The time between the user starting to type in the textarea and clicking the send button.

- `WithinGPTWindow`: Time spent in GPT window
- `WithinWritingWindow`:Time spent in writing window


| TimeSlot       | Attribute             | Type   | Description                              |
|----------------|-----------------------|--------|------------------------------------------|
| answerGenerate | `ag_startTime`        |        | Timestamp when user send a query to GPT. |
|                | `ag_duration`         | number | Time spent on generating an answer.      |

### Behavior Within Writing Interface
 In [`behaviorTracker_extension_notion`](src/behaviorTracker_extension_notion), we collected users' behavior when they editting in writing interface.


| Behavior      | Attribute                  | Type            | Description                                                                                                     |
|---------------|----------------------------|-----------------|-----------------------------------------------------------------------------------------------------------------|
| click         | `click_count`              | number          | The number of of click actions                                                                                  |
| Mousemovement | `mouseMovenment`           | number          | The distance of each mouse movement                                                                             |
|               | `total_mouse_Movenment`    | number                | The total distance the mouse moves                                                                              |
| scroll        | `scroll_count`             | number          | The number of of scroll actions                                                                                 |
|               | `Total_Scroll_Distance `   | number                | The total distance scroll                                                                                       |
|               | `average_scroll_distance`  | number          | The average diatance of scroll actions.                                                                         |
|               | `med_scroll_distance`      | number                | The median diatance of scroll actions.                                                                          |
| copy          | `copy_count`               | number                | The total times of copy                                                                                         |
|               | `med_copy_length`          | number                | The median length of copy actions.                                                                              |
|               | `average_scroll_distance`  | number                | The average of all rolling distances                                                                            |
| paste         | `paste_count`              | number          | The number of paste actions.                                                                                    |
|               | `med_paste_length`         | number          | The median length of paste actions.                                                                             |
|               | `average_paste_length`     | number          | The average length of each paste action.                                                                        |
| deleteAction  | `delet_count`              | number          | The number of delet actions. (delet, backspace, ctrl+z included.)                                               |
| keypress      | `keypress_count`           | number          | The number of keypress actions.                                                                                 |
| highlight     | `highlight_count`          | number          | The number of highlight actions.                                                                                |
|               | `total_highlight_length`   | number          | The total length of all highlights.                                                                             |
|               | `med_highlight_length`     | number          | The median length of highlights.                                                                                |
|               | `average_highlight_length` | number          | The average length of each highlight.                                                                           |
| idle          | `idle_count`               | number          | The number of pauses detected.(Idle records a pause time when there is no activity for over 2000 milliseconds.) |
|               | `total_idle_duration`      | number          | The total duration of all pauses.                                                                               |
|               | `med_idle_duration`        | number                | The median duration of pauses.                                                                                  |
|               | `average_idle_duration`    | number                | The average duration of each pause.                                                                             |

#Data Analysis
We used Pearson_correlation_coefficient to  [`measure the correlation between behavior data and overreliance`](src/regression_modeling/preason.py).


