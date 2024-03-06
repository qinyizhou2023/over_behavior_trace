import { $getRoot, $getSelection, LexicalEditor } from "lexical";

import {
  defaultUserBehavior,
  UserBehaviorItem,
  UserBehaviorType,
} from "@/atoms/time-travel-atom";
import {
  $isLogParagraphNode,
  LogParagraphNode,
} from "@/components/lexical-editor/plugins/log-paragraph";
import { $isLogTextNode } from "@/components/lexical-editor/plugins/log-text/node";
import { MouseActivityType } from "@/components/lexical-editor/plugins/mouse-activity";
import { $getNearestNodeOfType } from "@lexical/utils";

import { DEFAULT_MOUSE_ACTIVITY } from "./constants";

const $getRootBehavior = (): UserBehaviorItem => {
  const root = $getRoot();
  const children = root.getChildren();

  const { totalSpeed, totalChildrenNum, totalRevisions, totalMouseActivity } =
    children.reduce(
      (acc, child) => {
        if (!$isLogParagraphNode(child)) return acc;
        const typingSpeed = child.getTypingSpeed();
        const revisions = child.getRevisions();
        const mouseActivity = child.getMouseActivity();
        return {
          totalSpeed: acc.totalSpeed + typingSpeed,
          totalChildrenNum: acc.totalChildrenNum + 1,
          totalRevisions: {
            character_deletions: [
              ...acc.totalRevisions.character_deletions,
              ...revisions.character_deletions,
            ],
            range_deletions: [
              ...acc.totalRevisions.range_deletions,
              ...revisions.range_deletions,
            ],

            insertions: [
              ...acc.totalRevisions.insertions,
              ...revisions.insertions,
            ],
            pastings: [...acc.totalRevisions.pastings, ...revisions.pastings],
          },

          totalMouseActivity: {
            num_clicks:
              acc.totalMouseActivity.num_clicks + mouseActivity.num_clicks,
            move_distance:
              acc.totalMouseActivity.move_distance +
              mouseActivity.move_distance,
            drag_distance:
              acc.totalMouseActivity.drag_distance +
              mouseActivity.drag_distance,
            scroll_distance:
              acc.totalMouseActivity.scroll_distance +
              mouseActivity.scroll_distance,
          },
        };
      },
      {
        totalSpeed: 0,
        totalChildrenNum: 0,
        totalRevisions: {
          character_deletions: [] as number[],
          range_deletions: [] as number[],
          insertions: [] as number[],
          pastings: [] as number[],
        },
        totalMouseActivity: DEFAULT_MOUSE_ACTIVITY,
      }
    );

  const typingSpeed = totalSpeed / totalChildrenNum;

  return {
    typing_speed: typingSpeed,
    revisions: totalRevisions,
    mouse_activity: totalMouseActivity,
  };
};

export const $getDocumentMetrics = () => {
  const selection = $getSelection();
  const rootNode = $getRoot();
  const allSentence = rootNode.getTextContent().split(/(?<=[.?!])\s+/) ?? [];

  const allWords = rootNode.getTextContent().split(/\s+/) ?? [];

  if (!selection)
    return {
      sentence_completion: 0,
      overall_word_cnt: allWords.length,
      overall_sentence_cnt: allSentence.length,
      block_sentence: "",
    };
  const targetNode = selection.getNodes()[0];
  if (!$isLogTextNode(targetNode))
    return {
      sentence_completion: 0,
      overall_word_cnt: allWords.length,
      overall_sentence_cnt: allSentence.length,
      block_sentence: "",
    };
  const currentSentence = targetNode.getTextContent();

  const currentWords = currentSentence.split(/\s+/) ?? [];

  const averageWords = allWords.length / allSentence.length;
  const currentWordsLength = currentWords.length;

  const completion =
    currentSentence.trim().endsWith(".") ||
    currentSentence.trim().endsWith("?") ||
    currentSentence.trim().endsWith("!")
      ? 1
      : 1 / (1 + Math.exp(-currentWordsLength / averageWords));

  return {
    sentence_completion: completion,
    overall_word_cnt: allWords.length,
    overall_sentence_cnt: allSentence.length,
    block_sentence: currentSentence,
  };
};

const getUserBehaviorDiff = (
  current: UserBehaviorItem,
  last: UserBehaviorItem
): UserBehaviorItem => {
  const typingSpeed = (current.typing_speed + last.typing_speed) / 2;
  const revisions = {
    character_deletions: current.revisions.character_deletions.slice(
      last.revisions.character_deletions.length
    ),

    range_deletions: current.revisions.range_deletions.slice(
      last.revisions.range_deletions.length
    ),
    insertions: current.revisions.insertions.slice(
      last.revisions.insertions.length
    ),
    pastings: current.revisions.pastings.slice(last.revisions.pastings.length),
  };

  const mouseActivity: MouseActivityType = {
    num_clicks:
      current.mouse_activity.num_clicks - last.mouse_activity.num_clicks,
    move_distance:
      current.mouse_activity.move_distance - last.mouse_activity.move_distance,
    drag_distance:
      current.mouse_activity.drag_distance - last.mouse_activity.drag_distance,
    scroll_distance:
      current.mouse_activity.scroll_distance -
      last.mouse_activity.scroll_distance,
  };

  return {
    typing_speed: typingSpeed,
    revisions,
    mouse_activity: mouseActivity,
  };
};

export const getUserBehavior = (
  editor: LexicalEditor,
  lastBlockUserBehavior?: UserBehaviorType
): UserBehaviorType => {
  let userBehavior = defaultUserBehavior;
  const editorState = editor.getEditorState();
  editorState.read(() => {
    const rootBehavior = $getRootBehavior();
    userBehavior = {
      ...userBehavior,
      document: rootBehavior,
    };

    userBehavior = {
      ...userBehavior,
      since_last_block: lastBlockUserBehavior
        ? getUserBehaviorDiff(rootBehavior, lastBlockUserBehavior.document)
        : rootBehavior,
    };

    const selection = $getSelection();
    if (!selection) return;

    const targetNode = selection.getNodes()[0];

    if ($isLogTextNode(targetNode)) {
      const typingSpeed = targetNode.getTypingSpeed();
      const revisions = targetNode.getRevisions();
      const mouseActivity = targetNode.getMouseActivity();
      // userBehavior.sentence = {
      //   typing_speed: typingSpeed,
      //   revisions,
      //   mouse_activity: mouseActivity,
      // };

      userBehavior = {
        ...userBehavior,
        sentence: {
          typing_speed: typingSpeed,
          revisions,
          mouse_activity: mouseActivity,
        },
      };

      const parent = $getNearestNodeOfType(targetNode, LogParagraphNode);

      if (parent) {
        const typingSpeed = parent.getTypingSpeed();
        const revisions = parent.getRevisions();
        const mouseActivity = parent.getMouseActivity();
        // userBehavior.paragraph = {
        //   typing_speed: typingSpeed,
        //   revisions,
        //   mouse_activity: mouseActivity,
        // };
        userBehavior = {
          ...userBehavior,
          paragraph: {
            typing_speed: typingSpeed,
            revisions,
            mouse_activity: mouseActivity,
          },
        };
      }
    }
  });
  return userBehavior;
};
