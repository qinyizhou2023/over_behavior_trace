# WATOM Data Console

## Logged block data

### Global data

| Attribute              | Type                                 | Description                                                                                                                                                                                                                                                                                               |
|------------------------| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `totaltime`            | string                               | Unique identifier for the block                                                                                                                                                                                                                                                                           |
| `click`                | number                               | Unix timestamp of the start time of the block                                                                                                                                                                                                                                                             |
| `mouseMovement`        | number                               | Duration of the block in milliseconds                                                                                                                                                                                                                                                                     |
| `111`                  | number                               | User's setting for the minimum duration of a block                                                                                                                                                                                                                                                        |
| `222`                  | number                               | Block's start time relative to the start of the session                                                                                                                                                                                                                                                   |
| `num_blocks`           | number                               | Current count of blocks since the start of the session                                                                                                                                                                                                                                                    |
| `avg_block_duration`   | number                               | Average of current blocks' duration (milliseconds)                                                                                                                                                                                                                                                        |
| `sentence_completion`  | number within 0-1                    | if the user has completed the sentence, the value is 1; otherwise, the value is calculated by the division of the number of words in the sentence that the user was blocked at and the average number of words per sentence the user has written in the article. The value is sigmoided to be within 0-1. |
| `overall_word_cnt`     | number                               | Total word count of the article when the block was logged                                                                                                                                                                                                                                                 |
| `overall_sentence_cnt` | number                               | Total sentence count of the article when the block was logged                                                                                                                                                                                                                                             |
| `block_sentence`       | string                               | Sentence that the user was blocked at                                                                                                                                                                                                                                                                     |
| `user_behavior`        | [UserBehaviorType](#user-behavior)   | User's behavior when the block was logged                                                                                                                                                                                                                                                                 |
| `annotated`            | boolean                              | Whether the block has been annotated                                                                                                                                                                                                                                                                      |
| `annotation`           | [BlockAnnotation](#block-annotation) | Annotation of the block                                                                                                                                                                                                                                                                                   |

### User behavior

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
