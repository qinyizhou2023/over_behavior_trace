import { EditorConfig, LexicalNode, NodeKey, TextNode } from 'lexical';

export class LogTextNode extends TextNode {
  constructor(text: string, key?: NodeKey) {
    super(text, key);
  }

  static getType(): string {
    return "log-text";
  }

  static clone(node: LogTextNode): LogTextNode {
    return new LogTextNode(node.__text, node.__key);
  }

  createDOM(config: EditorConfig): HTMLElement {
    const element = super.createDOM(config);
    element.classList.add("log-text");
    return element;
  }

  updateDOM(
    prevNode: LogTextNode,
    dom: HTMLElement,
    config: EditorConfig
  ): boolean {
    const updated = super.updateDOM(prevNode, dom, config);
    // if (updated) {
    //     dom.classList.add("log-text");
    // }
    return updated;
  }
}

export function $createLogTextNode(text: string): LogTextNode {
  return new LogTextNode(text);
}

export function $isLogTextNode(
  node: LexicalNode | null | undefined
): node is LogTextNode {
  return node instanceof LogTextNode;
}
