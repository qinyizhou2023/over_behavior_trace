import {
  EditorConfig,
  LexicalEditor,
  LexicalNode,
  NodeKey,
  SerializedTextNode,
  Spread,
  TextNode,
} from "lexical";

export type Revisions = {
  character_deletings: number[];
  range_deletings: number[];
  insertings: number[];
  pastings: number[];
};

type SerializedLogTextNode = Spread<
  {
    __typing_speed: number;
    __dwelling_time: number;
    __last_update_timestamp: number;
    __update_count: number;
    __revisions: Revisions;
  },
  SerializedTextNode
>;

export class LogTextNode extends TextNode {
  __typing_speed: number;
  __revisions: Revisions;

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
    revisions?: Revisions,
    key?: NodeKey
  ) {
    super(text, key);
    this.__typing_speed = typing_speed ?? 0;
    this.__last_update_timestamp = last_udate_timestamp ?? Date.now();
    this.__dwelling_time = dwelling_time ?? 0;
    this.__update_count = update_count ?? 0;
    this.__revisions = revisions ?? {
      character_deletings: [],
      range_deletings: [],
      insertings: [],
      pastings: [],
    };
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
      node.__revisions,
      node.__key
    );
    return newNode;
  }

  createDOM(config: EditorConfig): HTMLElement {
    const element = super.createDOM(config);
    element.classList.add("log-text");

    element.setAttribute("data-typing-speed", this.__typing_speed.toString());
    element.setAttribute("data-revisions", JSON.stringify(this.__revisions));
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

    if (
      this.__revisions.character_deletings !==
        prevNode.__revisions.character_deletings ||
      this.__revisions.range_deletings !==
        prevNode.__revisions.range_deletings ||
      this.__revisions.insertings !== prevNode.__revisions.insertings ||
      this.__revisions.pastings !== prevNode.__revisions.pastings
    ) {
      dom.setAttribute("data-revisions", JSON.stringify(this.__revisions));
    }

    return updated;
  }

  override exportJSON(): SerializedLogTextNode {
    return {
      ...super.exportJSON(),
      type: LogTextNode.getType(),
      __typing_speed: this.__typing_speed,
      __dwelling_time: this.__dwelling_time,
      __last_update_timestamp: this.__last_update_timestamp,
      __update_count: this.__update_count,
      __revisions: this.__revisions,
    };
  }

  static importJSON(json: SerializedLogTextNode): LogTextNode {
    const node = new LogTextNode(
      json.text,
      json.__typing_speed,
      json.__dwelling_time,
      json.__last_update_timestamp,
      json.__update_count,
      json.__revisions
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
      target.__update_count + this.__update_count,
      {
        character_deletings: [
          ...target.__revisions.character_deletings,
          ...this.__revisions.character_deletings,
        ],
        range_deletings: [
          ...target.__revisions.range_deletings,
          ...this.__revisions.range_deletings,
        ],
        insertings: [
          ...target.__revisions.insertings,
          ...this.__revisions.insertings,
        ],
        pastings: [
          ...target.__revisions.pastings,
          ...this.__revisions.pastings,
        ],
      }
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
            this.__dwelling_time / 2,
            this.__last_update_timestamp,
            this.__update_count / 2,
            {
              character_deletings: this.__revisions.character_deletings.map(
                (x) => x / 2
              ),
              range_deletings: this.__revisions.range_deletings.map(
                (x) => x / 2
              ),
              insertings: this.__revisions.insertings.map((x) => x / 2),
              pastings: this.__revisions.pastings.map((x) => x / 2),
            }
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

  getRevisions(): Revisions {
    const self = this.getLatest();
    return self.__revisions;
  }

  getSentenceCompletion(editor: LexicalEditor): number {
    const self = this.getLatest();
    const sentences =
      editor.getRootElement()?.textContent?.split(/(?<=[.?!])\s+/) ?? [];

    const allWords = editor.getRootElement()?.textContent?.split(/\s+/) ?? [];
    const averageWordPerSentence = allWords.length / sentences.length;

    const words = self.__text.split(/\s+/);
    return self.__text.endsWith(".") ||
      self.__text.endsWith("?") ||
      self.__text.endsWith("!")
      ? 1
      : // scale to 0-1 using sigmoid function
        1 / (1 + Math.exp(-words.length / averageWordPerSentence));
  }

  private getNewRevision(
    metric: keyof Revisions,
    isNew: boolean,
    amount: number = 1
  ): number[] {
    const self = this.getLatest();
    return isNew || self.__revisions[metric].length === 0
      ? [...self.__revisions[metric], amount]
      : [
          ...self.__revisions[metric].slice(0, -1),
          self.__revisions[metric].slice(-1)[0] + amount,
        ];
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

  onDeleting(isRange: boolean, isNew: boolean, amount?: number): void {
    const writable = this.getWritable();

    if (isRange) {
      writable.__revisions = {
        ...writable.__revisions,
        range_deletings: this.getNewRevision("range_deletings", isNew, amount),
      };
    } else {
      writable.__revisions = {
        ...writable.__revisions,
        character_deletings: this.getNewRevision(
          "character_deletings",
          isNew,
          1
        ),
      };
    }
  }

  onInserting(isNew: boolean, amount?: number): void {
    const writable = this.getWritable();
    writable.__revisions = {
      ...writable.__revisions,
      insertings: this.getNewRevision("insertings", isNew, amount),
    };
  }

  onPasting(isNew: boolean, amount?: number): void {
    const writable = this.getWritable();
    writable.__revisions = {
      ...writable.__revisions,
      pastings: this.getNewRevision("pastings", isNew, amount),
    };
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
