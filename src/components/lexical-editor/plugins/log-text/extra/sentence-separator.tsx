import { DecoratorNode, NodeKey } from "lexical";
import { ReactNode } from "react";

import type { LexicalNode, SerializedLexicalNode } from "lexical";

export class SentenceSeparator extends DecoratorNode<ReactNode> {
  static getType() {
    return "sentence-separator";
  }

  static clone(node: SentenceSeparator): SentenceSeparator {
    return new SentenceSeparator(node.__key);
  }

  constructor(key?: NodeKey) {
    super(key);
  }

  createDOM(): HTMLElement {
    return document.createElement("span");
  }

  updateDOM(): false {
    return false;
  }

  decorate(): ReactNode {
    return <span className="border border-blue-400">&nbsp;</span>;
  }

  isInline(): boolean {
    return true;
  }

  isIsolated(): boolean {
    return true;
  }

  isKeyboardSelectable(): boolean {
    return false;
  }

  static importJSON(): SentenceSeparator {
    return new SentenceSeparator();
  }

  exportJSON(): SerializedLexicalNode {
    return {
      type: SentenceSeparator.getType(),
      version: 1,
    };
  }
}

export function $createSentenceSeparator(): SentenceSeparator {
  return new SentenceSeparator();
}

export function $isSentenceSeparator(
  node: LexicalNode | null | undefined
): node is SentenceSeparator {
  return node instanceof SentenceSeparator;
}
