import { ParagraphNode, TextNode } from 'lexical';
import React from 'react';

import { AutoFocusPlugin } from '@lexical/react/LexicalAutoFocusPlugin';
import { InitialConfigType, LexicalComposer } from '@lexical/react/LexicalComposer';
import { ContentEditable } from '@lexical/react/LexicalContentEditable';
import LexicalErrorBoundary from '@lexical/react/LexicalErrorBoundary';
import { HistoryPlugin } from '@lexical/react/LexicalHistoryPlugin';
// import { PlainTextPlugin } from '@lexical/react/LexicalPlainTextPlugin';
import { RichTextPlugin } from '@lexical/react/LexicalRichTextPlugin';

import { LogTextNode } from './extensions/log-text/node';

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
        {/* <MarkdownShortcutPlugin transformers={TRANSFORMERS} /> */}
      </LexicalComposer>
    </div>
  );
};
