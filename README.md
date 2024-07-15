## Score Counting 

## Logged Data
### BehaviorTracker_extension_gpt
We logged many users' behaviors, including mousemovement, copy-paste, and 

| Behavior      | Attribute                 | Type                           | Description                                                                                                     |
|---------------|---------------------------| ------------------------------ |-----------------------------------------------------------------------------------------------------------------|
|               |                           |                                |                                                                                                                 |
| click         | `click_count`             |                                | The number of of click actions                                                                                  |
| Mousemovement | `mouseMovenment`          | string                         | The distance of each mouse movement                                                                             |
|               | `total_mouse_Movenment`   |                                | The total distance the mouse moves                                                                              |
| scroll        | `scroll_count`            | number                         | The number of of scroll actions                                                                                 |
|               | `Total_Scroll_Distance `  |                                | The total distance scroll                                                                                       |
|               | `mouseMovement`           | number                         | Duration of the block in milliseconds                                                                           |
|               | `med_scroll_distance`     |                                | The median diatance of scroll actions.                                                                          |
| copy          | `copy_count`              |                                | The total times of copy                                                                                         |
|               | `med_copy_length`         |                                | The median length of copy actions.                                                                              |
|               | `average_scroll_distance` |                                | The average of all rolling distances                                                                            |
| paste         | `paste_count`             | number                         | The number of paste actions.                                                                                    |
|               | `med_paste_length`        | number                         | The median length of paste actions.                                                                             |
|               | `average_paste_length`    | number                         | The average length of each paste action.                                                                        |
|deleteAction     | `delet_count`             | number                         | The number of delet actions. (delet, backspace, ctrl+z included.)                                               |
|keypress         | `keypress_count`          | number within 0-1              | The number of keypress actions.                                                                                 |
|highlight            | `highlight_count`        | number                         | The number of highlight actions.                                                                                |
|               | `total_highlight_length`    | number                         | The total length of all highlights.                                                                             |
|               | `med_highlight_length`          | string                         | The median length of highlights.                                                                                |
|               | `average_highlight_length`           | [UserBehaviorType](#user-behavior) | The average length of each highlight.                                                                           |
| idle              | `annotated`               | boolean                        | The number of pauses detected.(Idle records a pause time when there is no activity for over 2000 milliseconds.) |
|               | `annotation`              | [BlockAnnotation](#block-annotation) | Annotation of the block                                                                                         |

### BehaviorTracker_extension_notion

Each block is logged within 4 different time-windows:

- `sentence`: Within the sentence that the user was blocked at
- `paragraph`: Within the paragraph that the user was blocked at
- `document`: Since the start of the session
- `since_last_block`: Since the last block

For each time-window, the following attributes are logged:

| Attribute        | Type                                      | Description                                   |
| ---------------- | ----------------------------------------- | --------------------------------------------- |
| `typing_speed`   | number                                    | Typing speed in word per minute               |
| `revisions`      | [RevisionsType](#revision-type)           | User's revisions count within the time-window |
| `mouse_activity` | [MouseActivityType](#mouse-activity-type) | User's mouse activity within the time-window  |

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
