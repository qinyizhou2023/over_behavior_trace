import { COMMAND_PRIORITY_EDITOR } from 'lexical';
import { useEffect } from 'react';

import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';

import { SPLIT_SENTENCE_COMMAND } from './commands';
import { LogTextNode } from './node';

export default function LogTextExtension() {
  const [editor] = useLexicalComposerContext();
  useEffect(() => {
    if (!editor.hasNodes([LogTextNode])) {
      throw new Error("LogTextExtension: LogTextNode is not registered");
    }

    return editor.registerCommand(
      SPLIT_SENTENCE_COMMAND,
      () => {
        return true;
      },
      COMMAND_PRIORITY_EDITOR
    );
  }, [editor]);

  return null;
}
