import {
  EditorConfig,
  LexicalNode,
  NodeKey,
  SerializedTextNode,
  Spread,
  TextNode,
} from "lexical";

type SerializedLogTextNode = Spread<
  {
    __typing_speed: number;
    __dwelling_time: number;
    __last_update_timestamp: number;
    __update_count: number;
  },
  SerializedTextNode
>;

export class LogTextNode extends TextNode {
  __typing_speed: number;

  // internal use only
  __dwelling_time: number;
  __last_update_timestamp: number;
  __update_count: number;

  constructor(
    text: string,
    typing_speed?: number,
    dwelling_time?: number,
    last_udate_timestamp?: number,
    update_count?: number,
    key?: NodeKey
  ) {
    super(text, key);
    this.__typing_speed = typing_speed ?? 0;
    this.__last_update_timestamp = last_udate_timestamp ?? Date.now();
    this.__dwelling_time = dwelling_time ?? 0;
    this.__update_count = update_count ?? 0;
  }

  static getType(): string {
    return "log-text";
  }

  static clone(node: LogTextNode): LogTextNode {
    const newNode = new LogTextNode(
      node.__text,
      node.__typing_speed,
      node.__dwelling_time,
      node.__last_update_timestamp,
      node.__update_count,
      node.__key
    );
    return newNode;
  }

  createDOM(config: EditorConfig): HTMLElement {
    const element = super.createDOM(config);
    element.classList.add("log-text");

    element.setAttribute("data-typing-speed", this.__typing_speed.toString());
    return element;
  }

  updateDOM(
    prevNode: LogTextNode,
    dom: HTMLElement,
    config: EditorConfig
  ): boolean {
    const updated = super.updateDOM(prevNode, dom, config);
    if (this.__typing_speed !== prevNode.__typing_speed) {
      dom.setAttribute("data-typing-speed", this.__typing_speed.toString());
    }

    return updated;
  }

  exportJSON(): SerializedLogTextNode {
    return {
      ...super.exportJSON(),
      __typing_speed: this.__typing_speed,
      __dwelling_time: this.__dwelling_time,
      __last_update_timestamp: this.__last_update_timestamp,
      __update_count: this.__update_count,
    };
  }

  static importJSON(json: SerializedLogTextNode): LogTextNode {
    const node = new LogTextNode(
      json.text,
      json.__typing_speed,
      json.__dwelling_time,
      json.__last_update_timestamp,
      json.__update_count
    );
    return node;
  }

  isUnmergeable(): boolean {
    return false;
  }

  override isSimpleText(): boolean {
    return (
      (this.__type === "text" || this.__type === "log-text") &&
      this.__mode === 0
    );
  }

  mergeWithSibling(target: LogTextNode): LogTextNode {
    const merged = super.mergeWithSibling(target);
    return new LogTextNode(
      merged.__text,
      (target.__typing_speed + this.__typing_speed) / 2,
      target.__dwelling_time + this.__dwelling_time,
      Math.max(target.__last_update_timestamp, this.__last_update_timestamp),
      target.__update_count + this.__update_count
    );
  }

  splitText(...splitOffsets: number[]): LogTextNode[] {
    const nodes = super.splitText(...splitOffsets);

    const result: LogTextNode[] = [];

    for (const node of nodes) {
      if (node instanceof LogTextNode) {
        result.push(node);
      } else {
        result.push(
          new LogTextNode(
            node.__text,
            this.__typing_speed,
            this.__dwelling_time,
            this.__last_update_timestamp,
            this.__update_count
          )
        );
      }
    }

    return result;
  }

  // ------------------ Custom methods ------------------
  getTypingSpeed(): number {
    const self = this.getLatest();
    return self.__typing_speed;
  }

  onTyping(): void {
    const writable = this.getWritable();
    // const latest = this.getLatest();

    // freeze latest

    const { __last_update_timestamp, __update_count, __dwelling_time } = this;
    const now = Date.now();

    const delta = now - __last_update_timestamp;

    writable.__last_update_timestamp = now;
    writable.__update_count += 1;

    if (delta > 2000 || delta < 10) {
      return;
    }

    writable.__dwelling_time = __dwelling_time + delta;

    writable.__typing_speed =
      (__update_count + 1) / ((__dwelling_time + delta) / 1000);
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
