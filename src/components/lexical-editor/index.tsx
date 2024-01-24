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
// import { PlainTextPlugin } from '@lexical/react/LexicalPlainTextPlugin';
import { RichTextPlugin } from "@lexical/react/LexicalRichTextPlugin";

import LogTextPlugin from "./plugins/log-text";
import { SentenceSeparator } from "./plugins/log-text/extra/sentence-separator";
import { LogTextNode } from "./plugins/log-text/node";
import TreeViewPlugin from "./plugins/tree-view";

export const Editor: React.FC = () => {
  const config: InitialConfigType = {
    namespace: "lexical-editor",
    editable: true,
    theme: {
      root: "prose dark:prose-invert lg:prose-lg focus:outline-none flex-1 mx-auto shadow overflow-auto p-4 border m-4 rounded-md",
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
        with: (node: TextNode) => new LogTextNode(node.__text),
      },
    ],

    onError: (error) => {
      console.error(error);
    },
  };
  return (
    <div className="container flex w-full h-full">
      <LexicalComposer initialConfig={config}>
        <RichTextPlugin
          contentEditable={<ContentEditable />}
          placeholder={null}
          // placeholder={"Type something..."}
          ErrorBoundary={LexicalErrorBoundary}
        />
        <HistoryPlugin />
        <AutoFocusPlugin />

        <LogTextPlugin />
        {/* <MarkdownShortcutPlugin transformers={TRANSFORMERS} /> */}

        <div className="absolute bottom-0 left-0 border border-red-500 overflow-auto max-w-full h-1/2">
          <TreeViewPlugin />
        </div>
      </LexicalComposer>
    </div>
  );
};
