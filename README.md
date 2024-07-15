## Score Counting 

## Logged Data
### Behaviors Within GPT Interface
In [`behaviorTracker_extension_gpt`](src/behaviorTracker_extension_gpt), We logged many users' behaviors, including mousemovement, copy-paste, click...   

| Behavior     | Attribute                  | Type   | Description                                                                                                                             |
|--------------|----------------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------|
| windowswitch | `windowswitch_count`       | number | The number of of window switch actions.                                                                                                 |
|              | `windowswitch_speed`       |        | windowswitch_count / total time                                                                                                         |
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
Each block is logged within 2 different time-windows:
- `totaltime`: Total time spent in finishing the task.
- `answerGenerate`: While GPT is generating the answer. The time between the user click the send button to the send button become actived.
- `keyboardInput`: While user is writing the prompt. The time between the user starting to type in the textarea and clicking the send button.


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


<!-- Revision type -->

#### Revision type

| Attribute             | Type     | Description                                                       |
| --------------------- | -------- | ----------------------------------------------------------------- |
| `character_deletions` | number[] | Array of character deletions (`Backspace` and `Delete` key press) |
| `range_deletions`     | number[] | Array of range deletions (select and delete)                      |
| `insertions`          | number[] | Array of insertions in the previous written text                  |
| `pastings`            | number[] | Array of pastings                                                 |

For each attribute, the array contains the number of **sequential operations** that the user has performed. For example, if the user has deleted 3 characters in a row, and then does some other operations, and then deletes 2 characters in a row, the array would be `[3, 2]`.

<!-- Mouse activity type -->

#### Mouse activity type

| Attribute         | Type   | Description                     |
| ----------------- | ------ | ------------------------------- |
| `num_clicks`      | number | Number of clicks                |
| `move_distance`   | number | Total pixels of mouse movement  |
| `drag_distance`   | number | Total pixels of mouse dragging  |
| `scroll_distance` | number | Total pixels of mouse scrolling |

### Block annotation

| Attribute            | Type                                                           | Description                                                      |
| -------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------- |
| `block_likelihood`   | number                                                         | The likelihood that this stalk is a block in the writing process |
| `block_state`        | [BlockStateLikelihood](#block-state-likelihood)                | The likelihood of the block state                                |
| `block_ai_asistance` | [BlockAiAssistanceLikelihood](#block-ai-assistance-likelihood) | The requirement of AI assistance during the block                |

#### Block state likelihood

| Attribute     | Type                                                    | Description                                                              |
| ------------- | ------------------------------------------------------- | ------------------------------------------------------------------------ |
| `planning`    | [PlanningStateLikelihood](#planning-state-likelihood)   | The likelihood of the block happening in planning state                  |
| `translating` | number                                                  | The likelihood of translating the ideas into written words and sentences |
| `reviewing`   | [ReviewingStateLikelihood](#reviewing-state-likelihood) | The likelihood of the block happening in reviewing state                 |

##### Planning state likelihood

| Attribute    | Type   | Description                                       |
| ------------ | ------ | ------------------------------------------------- |
| `generating` | number | The likelihood of generating ideas to write about |
| `organizing` | number | The likelihood of organizing the ideas            |
| `setting`    | number | The likelihood of setting the writing goals       |

##### Reviewing state likelihood

| Attribute    | Type   | Description                                                                                                              |
| ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------ |
| `evaluating` | number | The likelihood of evaluating the quality of the written text, e.g., whether the text is clear, concise, and coherent     |
| `revising`   | number | The likelihood of reading and revising written text, e.g., have the idea of adding, deleting, or reorganizing sentences" |

#### Block AI assistance likelihood

| Attribute    | Type   | Description                                                                                                                            |
| ------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `ideas`      | number | AI suggests ideas to write about. e.g., “How about writing about <suggested idea>?                                                     |
| `completion` | number | AI helps complete the sentence you are writing. e.g., Working like autocomplete / copilot"                                             |
| `feedback`   | number | AI provides feedback to the sentence the user is writing. e.g., “This sentence is too long. Consider splitting it into two sentences.” |
| `other`      | string | Custom AI assistance that is not covered by the above categories                                                                       |
