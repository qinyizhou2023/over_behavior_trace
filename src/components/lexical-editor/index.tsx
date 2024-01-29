import { ParagraphNode, TextNode } from "lexical";
import React from "react";

import { AutoFocusPlugin } from "@lexical/react/LexicalAutoFocusPlugin";
import {
  InitialConfigType,
  LexicalComposer,
} from "@lexical/react/LexicalComposer";
import { ContentEditable } from "@lexical/react/LexicalContentEditable";
import LexicalErrorBoundary from "@lexical/react/LexicalErrorBoundary";
import { HistoryPlugin } from "@lexical/react/LexicalHistoryPlugin";
import { RichTextPlugin } from "@lexical/react/LexicalRichTextPlugin";

import LogTextPlugin from "./plugins/log-text";
import { SentenceSeparator } from "./plugins/log-text/extra/sentence-separator";
import { LogTextNode } from "./plugins/log-text/node";
import TreeViewPlugin from "./plugins/tree-view";

const DEBUG_MODE = false;

if (DEBUG_MODE) {
  import("./debug.css");
}

export const Editor: React.FC = () => {
  const config: InitialConfigType = {
    namespace: "lexical-editor",
    editable: true,
    theme: {
      root: "prose lg:prose-lg xl:prose-xl focus:outline-none w-full flex-1 mx-auto overflow-auto p-4",
      link: "cursor-pointer",
      placeholder: "text-gray-400",
      text: {
        bold: "font-semibold",
        underline: "underline",
        italic: "italic",
        strikethrough: "line-through",
        underlineStrikethrough: "underlined-line-through",
      },
    },

    nodes: [
      ParagraphNode,
      LogTextNode,
      SentenceSeparator,
      {
        replace: TextNode,
        with: (node: TextNode) => new LogTextNode(node.__text, 0),
      },
    ],

    onError: (error) => {
      console.error(error);
    },
  };
  return (
    <div className="prose dark:prose-invert flex-1 flex m-5 p-4 flex-col relative rounded-lg shadow border lg:prose-lg xl:prose-xl mx-auto">
      {/* <div className="w-full sticky top-0 bg-white z-10">123</div> */}
      <LexicalComposer initialConfig={config}>
        <RichTextPlugin
          contentEditable={<ContentEditable />}
          placeholder={null}
          ErrorBoundary={LexicalErrorBoundary}
        />
        <HistoryPlugin />
        <AutoFocusPlugin />

        <LogTextPlugin />

        {DEBUG_MODE ? (
          <div className="absolute bottom-0 left-0">
            <TreeViewPlugin />
          </div>
        ) : (
          <></>
        )}
      </LexicalComposer>
    </div>
  );
};
