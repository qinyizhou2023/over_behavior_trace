# WATOM Data Console

## Logged block data

### Global data

| Attribute              | Type                                 | Description                                                   |
| ---------------------- | ------------------------------------ | ------------------------------------------------------------- |
| `id`                   | string                               | Unique identifier for the block                               |
| `start_time`           | number                               | Unix timestamp of the start time of the block                 |
| `duration_block`       | number                               | Duration of the block in milliseconds                         |
| `threshold`            | number                               | User's setting for the minimum duration of a block            |
| `relative_start_time`  | number                               | Block's start time relative to the start of the session       |
| `num_blocks`           | number                               | Current count of blocks since the start of the session        |
| `avg_block_duration`   | number                               | Average of current blocks' duration (milliseconds)            |
| `sentence_completion`  | number within 0-1                    | Percentage of sentence completion                             |
| `overall_word_cnt`     | number                               | Total word count of the article when the block was logged     |
| `overall_sentence_cnt` | number                               | Total sentence count of the article when the block was logged |
| `block_sentence`       | string                               | Sentence that the user was blocking at                        |
| `user_behavior`        | [UserBehaviorType](#user-behavior)   | User's behavior when the block was logged                     |
| `annotated`            | boolean                              | Whether the block has been annotated                          |
| `annotation`           | [BlockAnnotation](#block-annotation) | Annotation of the block                                       |

### User behavior

Each block is logged within 4 different time-windows:

- `sentence`: Within the sentence that the user was blocking at
- `paragraph`: Within the paragraph that the user was blocking at
- `document`: Since the start of the session
- `since_block`: Since the last block

For each time-window, the following attributes are logged:

| Attribute        | Type                                      | Description                                   |
| ---------------- | ----------------------------------------- | --------------------------------------------- |
| `typing_speed`   | number                                    | Typing speed in characters per second         |
| `revisions`      | [RevisionsType](#revision-type)           | User's revisions count within the time-window |
| `mouse_activity` | [MouseActivityType](#mouse-activity-type) | User's mouse activity within the time-window  |

<!-- Revision type -->

#### Revision type

| Attribute             | Type     | Description                                      |
| --------------------- | -------- | ------------------------------------------------ |
| `character_deletings` | number[] | Array of character deletings                     |
| `range_deletings`     | number[] | Array of range deletings (select and delete)     |
| `insertings`          | number[] | Array of insertings in the previous written text |
| `pastings`            | number[] | Array of pastings                                |

For each attribute, the array contains the number of **sequential operations** that the user has performed. For example, if the user has deleted 3 characters in a row, and then does some other operations, and then deletes 2 characters in a row, the array would be `[3, 2]`.

<!-- Mouse activity type -->

#### Mouse activity type

| Attribute         | Type   | Description                     |
| ----------------- | ------ | ------------------------------- |
| `click`           | number | Number of clicks                |
| `move_distance`   | number | Total pixels of mouse movement  |
| `drag_distance`   | number | Total pixels of mouse dragging  |
| `scroll_distance` | number | Total pixels of mouse scrolling |

### Block annotation

| Attribute           | Type                                                             | Description                                                          |
| ------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------- |
| `blockPossibility`  | number                                                           | The possibility that this stalk is a blocking in the writing process |
| `blockStage`        | [BlockStagePossibility](#block-stage-possibility)                | The possibility of the block stage                                   |
| `blockAiAssistance` | [BlockAiAssistancePossibility](#block-ai-assistance-possibility) | The requirement of AI assistance during the block                    |

#### Block stage possibility

| Attribute     | Type                                                      | Description                                                               |
| ------------- | --------------------------------------------------------- | ------------------------------------------------------------------------- |
| `planning`    | [PlanningStagePossibility](#planning-stage-possibility)   | The possibility of the block happening in planning stage                  |
| `translating` | number                                                    | The possibility of translating the ideas into written words and sentences |
| `reviewing`   | [ReviewingStagePossibility](#reviewing-stage-possibility) | The possibility of the block happening in reviewing stage                 |

##### Planning stage possibility

| Attribute    | Type   | Description                                        |
| ------------ | ------ | -------------------------------------------------- |
| `generating` | number | The possibility of generating ideas to write about |
| `organizing` | number | The possibility of organizing the ideas            |
| `setting`    | number | The possibility of setting the writing goals       |

##### Reviewing stage possibility

| Attribute    | Type   | Description                                                                                                               |
| ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------- |
| `evaluating` | number | The possibility of evaluating the quality of the written text, e.g., whether the text is clear, concise, and coherent     |
| `revising`   | number | The possibility of reading and revising written text, e.g., have the idea of adding, deleting, or reorganizing sentences" |

#### Block AI assistance possibility

| Attribute    | Type   | Description                                                                                                                            |
| ------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `ideas`      | number | AI suggests ideas to write about. e.g., “How about writing about <suggested idea>?                                                     |
| `completion` | number | AI helps complete the sentence you are writing. e.g., Working like autocomplete / copilot"                                             |
| `feedback`   | number | AI provides feedback to the sentence the user is writing. e.g., “This sentence is too long. Consider splitting it into two sentences.” |
| `other`      | string | Custom AI assistance that is not covered by the above categories                                                                       |
