import {
  EditorConfig,
  LexicalNode,
  NodeKey,
  SerializedTextNode,
  Spread,
  TextNode,
} from "lexical";

import { DEFAULT_MOUSE_ACTIVITY } from "@/lib/constants";

import { MouseActivityType } from "../mouse-activity";

export type Revisions = {
  character_deletions: number[];
  range_deletions: number[];
  insertions: number[];
  pastings: number[];
};

type SerializedLogTextNode = Spread<
  {
    __typing_speed: number;
    __dwelling_time: number;
    __last_update_timestamp: number;
    __update_count: number;
    __revisions: Revisions;
    __mouse_activity: MouseActivityType;
  },
  SerializedTextNode
>;

export class LogTextNode extends TextNode {
  __typing_speed: number;
  __revisions: Revisions;
  __mouse_activity: MouseActivityType;

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
    mouse_activity?: MouseActivityType,
    key?: NodeKey
  ) {
    super(text, key);
    this.__typing_speed = typing_speed ?? 0;
    this.__last_update_timestamp = last_udate_timestamp ?? Date.now();
    this.__dwelling_time = dwelling_time ?? 0;
    this.__update_count = update_count ?? 0;
    this.__revisions = revisions ?? {
      character_deletions: [],
      range_deletions: [],
      insertions: [],
      pastings: [],
    };

    this.__mouse_activity = mouse_activity ?? DEFAULT_MOUSE_ACTIVITY;
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
      node.__mouse_activity,
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
      this.__revisions.character_deletions !==
        prevNode.__revisions.character_deletions ||
      this.__revisions.range_deletions !==
        prevNode.__revisions.range_deletions ||
      this.__revisions.insertions !== prevNode.__revisions.insertions ||
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
      __mouse_activity: this.__mouse_activity,
    };
  }

  static importJSON(json: SerializedLogTextNode): LogTextNode {
    const node = new LogTextNode(
      json.text,
      json.__typing_speed,
      json.__dwelling_time,
      json.__last_update_timestamp,
      json.__update_count,
      json.__revisions,
      json.__mouse_activity
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
        character_deletions: [
          ...target.__revisions.character_deletions,
          ...this.__revisions.character_deletions,
        ],
        range_deletions: [
          ...target.__revisions.range_deletions,
          ...this.__revisions.range_deletions,
        ],
        insertions: [
          ...target.__revisions.insertions,
          ...this.__revisions.insertions,
        ],
        pastings: [
          ...target.__revisions.pastings,
          ...this.__revisions.pastings,
        ],
      },
      {
        num_clicks:
          target.__mouse_activity.num_clicks + this.__mouse_activity.num_clicks,
        move_distance:
          target.__mouse_activity.move_distance +
          this.__mouse_activity.move_distance,
        drag_distance:
          target.__mouse_activity.drag_distance +
          this.__mouse_activity.drag_distance,
        scroll_distance:
          target.__mouse_activity.scroll_distance +
          this.__mouse_activity.scroll_distance,
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
            this.__dwelling_time / nodes.length,
            this.__last_update_timestamp,
            this.__update_count / nodes.length,
            {
              character_deletions: this.__revisions.character_deletions.map(
                (x) => x / nodes.length
              ),
              range_deletions: this.__revisions.range_deletions.map(
                (x) => x / nodes.length
              ),
              insertions: this.__revisions.insertions.map(
                (x) => x / nodes.length
              ),
              pastings: this.__revisions.pastings.map((x) => x / nodes.length),
            },
            {
              num_clicks: this.__mouse_activity.num_clicks / nodes.length,
              move_distance: this.__mouse_activity.move_distance / nodes.length,
              drag_distance: this.__mouse_activity.drag_distance / nodes.length,
              scroll_distance:
                this.__mouse_activity.scroll_distance / nodes.length,
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

  getMouseActivity(): MouseActivityType {
    const self = this.getLatest();
    return self.__mouse_activity;
  }

  setMouseActivity(activity: MouseActivityType): void {
    const writable = this.getWritable();
    writable.__mouse_activity = activity;
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
      (((__update_count + 1) / ((__dwelling_time + delta) / 1000)) * 60) /
      this.__text.split(" ").length;
  }

  onDeleting(isRange: boolean, isNew: boolean, amount?: number): void {
    const writable = this.getWritable();

    if (isRange) {
      writable.__revisions = {
        ...writable.__revisions,
        range_deletions: this.getNewRevision("range_deletions", isNew, amount),
      };
    } else {
      writable.__revisions = {
        ...writable.__revisions,
        character_deletions: this.getNewRevision(
          "character_deletions",
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
      insertions: this.getNewRevision("insertions", isNew, amount),
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
