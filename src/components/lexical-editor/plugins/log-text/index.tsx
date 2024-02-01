import {
  $getSelection,
  $isRangeSelection,
  COMMAND_PRIORITY_EDITOR,
  COMMAND_PRIORITY_LOW,
  DELETE_CHARACTER_COMMAND,
  PASTE_COMMAND,
} from "lexical";
import { useEffect, useRef } from "react";

import { useLexicalComposerContext } from "@lexical/react/LexicalComposerContext";
import { mergeRegister } from "@lexical/utils";

import { SPLIT_SENTENCE_COMMAND } from "./commands";
import { $createSentenceSeparator } from "./extra/sentence-separator";
import { $isLogTextNode, LogTextNode } from "./node";

export default function LogTextPlugin() {
  const [editor] = useLexicalComposerContext();

  const deleteTimeout = useRef<NodeJS.Timeout | null>(null);
  const insertTimeout = useRef<NodeJS.Timeout | null>(null);

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
      }),

      editor.registerTextContentListener(() => {
        editor.update(() => {
          const selection = $getSelection();
          if (!$isRangeSelection(selection) || !selection.isCollapsed()) {
            return;
          }

          const node = selection.getNodes()[0];

          if (!$isLogTextNode(node)) return;

          // if typing is in the middle of the text
          if (selection.anchor.offset !== node.getTextContent().length) {
            if (insertTimeout.current === null) {
              node.onInserting(true, 1);
            } else {
              node.onInserting(false, 1);
              clearTimeout(insertTimeout.current);
            }

            insertTimeout.current = setTimeout(() => {
              insertTimeout.current = null;
            }, 1000);
          }

          node.onTyping();
        });
      }),

      editor.registerCommand(
        DELETE_CHARACTER_COMMAND,
        () => {
          const selection = $getSelection();

          if (!$isRangeSelection(selection)) {
            return false;
          }

          const nodes = selection.getNodes();

          nodes.forEach((node) => {
            if ($isLogTextNode(node)) {
              if (deleteTimeout.current === null) {
                node.onDeleting(
                  !selection.isCollapsed(),
                  true,
                  selection.isCollapsed()
                    ? 1
                    : selection.getTextContent().length
                );
              } else {
                node.onDeleting(
                  !selection.isCollapsed(),
                  false,
                  selection.isCollapsed()
                    ? 1
                    : selection.getTextContent().length
                );
                clearTimeout(deleteTimeout.current);
              }

              deleteTimeout.current = setTimeout(() => {
                deleteTimeout.current = null;
              }, 1000);
            }
          });

          return false;
        },
        COMMAND_PRIORITY_LOW
      ),

      editor.registerCommand(
        PASTE_COMMAND,
        () => {
          const selection = $getSelection();

          if (!$isRangeSelection(selection)) {
            return false;
          }

          const nodes = selection.getNodes();

          nodes.forEach((node) => {
            if ($isLogTextNode(node)) {
              node.onPasting(true);
            }
          });

          return false;
        },
        COMMAND_PRIORITY_LOW
      )
    );
  }, [editor]);

  return null;
}
