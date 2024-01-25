import {
  $getSelection,
  $isRangeSelection,
  COMMAND_PRIORITY_EDITOR,
} from "lexical";
import { useEffect } from "react";

import { useLexicalComposerContext } from "@lexical/react/LexicalComposerContext";
import { mergeRegister } from "@lexical/utils";

import { SPLIT_SENTENCE_COMMAND } from "./commands";
import { $createSentenceSeparator } from "./extra/sentence-separator";
import { $isLogTextNode, LogTextNode } from "./node";

export default function LogTextPlugin() {
  const [editor] = useLexicalComposerContext();
  useEffect(() => {
    if (!editor.hasNodes([LogTextNode])) {
      throw new Error("LogTextExtension: LogTextNode is not registered");
    }

    return mergeRegister(
      editor.registerCommand(
        SPLIT_SENTENCE_COMMAND,
        () => {
          const selection = $getSelection();

          if (!$isRangeSelection(selection) || !selection.isCollapsed()) {
            return false;
          }

          selection.deleteCharacter(true);

          const node = selection.getNodes()[0];
          if (!$isLogTextNode(node)) return false;

          const separator = $createSentenceSeparator();
          selection.insertNodes([separator]);
          return true;
        },
        COMMAND_PRIORITY_EDITOR
      ),

      editor.registerTextContentListener(() => {
        editor.update(() => {
          const selection = $getSelection();
          if (!$isRangeSelection(selection) || !selection.isCollapsed()) {
            return;
          }

          const node = selection.getNodes()[0];

          if (!$isLogTextNode(node)) return;

          node.onTyping();
        });
      }),

      editor.registerTextContentListener(() => {
        editor.getEditorState().read(() => {
          const selection = $getSelection();

          if (!$isRangeSelection(selection) || !selection.isCollapsed()) {
            return;
          }

          const text = selection.getNodes()[0].getTextContent();

          const isLast = selection.anchor.offset === text.length;

          const textBeforeSelection = text.slice(0, selection.anchor.offset);

          if (textBeforeSelection.match(/(\.|\?|!)\s$/)) {
            editor.dispatchCommand(SPLIT_SENTENCE_COMMAND, isLast);
          }
        });
      })
    );
  }, [editor]);

  return null;
}
