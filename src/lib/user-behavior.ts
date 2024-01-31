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

const $getRootBehavior = (editor: LexicalEditor): UserBehaviorItem => {
  const root = $getRoot();
  const children = root.getChildren();

  const {
    totalSpeed,
    totalChildrenNum,
    totalRevisions,
    totalSentenceCompletion,
  } = children.reduce(
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
        totalSentenceCompletion:
          acc.totalSentenceCompletion + child.getSentenceCompletion(editor),
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
      totalSentenceCompletion: 0,
    }
  );

  const typingSpeed = totalSpeed / totalChildrenNum;
  const sentenceCompletion = totalSentenceCompletion / totalChildrenNum;

  return {
    typing_speed: typingSpeed,
    revisions: totalRevisions,
    sentence_completion: sentenceCompletion,
  };
};

export const getUserBehavior = (editor: LexicalEditor): UserBehaviorType => {
  const userBehavior = defaultUserBehavior;
  const editorState = editor.getEditorState();
  editorState.read(() => {
    const rootBehavior = $getRootBehavior(editor);
    userBehavior.document = rootBehavior;

    const selection = $getSelection();
    if (!selection) return;

    const targetNode = selection.getNodes()[0];

    if ($isLogTextNode(targetNode)) {
      const typingSpeed = targetNode.getTypingSpeed();
      const revisions = targetNode.getRevisions();
      const sentenceCompletion = targetNode.getSentenceCompletion(editor);
      userBehavior.sentence = {
        typing_speed: typingSpeed,
        revisions,
        sentence_completion: sentenceCompletion,
      };

      const parent = $getNearestNodeOfType(targetNode, LogParagraphNode);

      if (parent) {
        const typingSpeed = parent.getTypingSpeed();
        const revisions = parent.getRevisions();
        const sentenceCompletion = parent.getSentenceCompletion(editor);
        userBehavior.paragraph = {
          typing_speed: typingSpeed,
          revisions,
          sentence_completion: sentenceCompletion,
        };
      }
    }
  });
  return userBehavior;
};
