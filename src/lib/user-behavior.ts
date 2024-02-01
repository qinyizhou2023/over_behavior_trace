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
import { $getNearestNodeOfType } from "@lexical/utils";

const $getRootBehavior = (): UserBehaviorItem => {
  const root = $getRoot();
  const children = root.getChildren();

  const { totalSpeed, totalChildrenNum, totalRevisions } = children.reduce(
    (acc, child) => {
      if (!$isLogParagraphNode(child)) return acc;
      const typingSpeed = child.getTypingSpeed();
      const revisions = child.getRevisions();
      return {
        totalSpeed: acc.totalSpeed + typingSpeed,
        totalChildrenNum: acc.totalChildrenNum + 1,
        totalRevisions: {
          character_deletings:
            acc.totalRevisions.character_deletings +
            revisions.character_deletings,
          range_deletings:
            acc.totalRevisions.range_deletings + revisions.range_deletings,
          insertings: acc.totalRevisions.insertings + revisions.insertings,
          pastings: acc.totalRevisions.pastings + revisions.pastings,
        },
      };
    },
    {
      totalSpeed: 0,
      totalChildrenNum: 0,
      totalRevisions: {
        character_deletings: 0,
        range_deletings: 0,
        insertings: 0,
        pastings: 0,
      },
    }
  );

  const typingSpeed = totalSpeed / totalChildrenNum;

  return {
    typing_speed: typingSpeed,
    revisions: totalRevisions,
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
    };
  const targetNode = selection.getNodes()[0];
  if (!$isLogTextNode(targetNode))
    return {
      sentence_completion: 0,
      overall_word_cnt: allWords.length,
      overall_sentence_cnt: allSentence.length,
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
  };
};

export const getUserBehavior = (editor: LexicalEditor): UserBehaviorType => {
  const userBehavior = defaultUserBehavior;
  const editorState = editor.getEditorState();
  editorState.read(() => {
    const rootBehavior = $getRootBehavior();
    userBehavior.document = rootBehavior;

    const selection = $getSelection();
    if (!selection) return;

    const targetNode = selection.getNodes()[0];

    if ($isLogTextNode(targetNode)) {
      const typingSpeed = targetNode.getTypingSpeed();
      const revisions = targetNode.getRevisions();
      userBehavior.sentence = {
        typing_speed: typingSpeed,
        revisions,
      };

      const parent = $getNearestNodeOfType(targetNode, LogParagraphNode);

      if (parent) {
        const typingSpeed = parent.getTypingSpeed();
        const revisions = parent.getRevisions();
        userBehavior.paragraph = {
          typing_speed: typingSpeed,
          revisions,
        };
      }
    }
  });
  return userBehavior;
};
