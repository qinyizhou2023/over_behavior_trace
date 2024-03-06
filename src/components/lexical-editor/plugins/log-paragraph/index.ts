import { LexicalNode, ParagraphNode, SerializedParagraphNode } from "lexical";

import { $isLogTextNode, Revisions } from "../log-text/node";

export class LogParagraphNode extends ParagraphNode {
  static getType(): string {
    return "log-paragraph";
  }

  static clone(node: LogParagraphNode): LogParagraphNode {
    return new LogParagraphNode(node.__key);
  }

  static importJSON(): LogParagraphNode {
    return new LogParagraphNode();
  }

  override exportJSON(): SerializedParagraphNode {
    return { ...super.exportJSON(), type: LogParagraphNode.getType() };
  }

  getTypingSpeed(): number {
    const self = this.getLatest();
    const children = self.getChildren();

    const { totalSpeed, totalChildrenNum } = children.reduce(
      (acc, child) => {
        if (!$isLogTextNode(child)) return acc;
        const typingSpeed = child.getTypingSpeed();
        return {
          totalSpeed: acc.totalSpeed + typingSpeed,
          totalChildrenNum: acc.totalChildrenNum + 1,
        };
      },
      { totalSpeed: 0, totalChildrenNum: 0 }
    );

    return totalSpeed / totalChildrenNum;
  }

  getRevisions(): Revisions {
    const self = this.getLatest();
    const children = self.getChildren();

    const revisions = children.reduce(
      (acc, child) => {
        if (!$isLogTextNode(child)) return acc;
        const childRevisions = child.getRevisions();
        return {
          character_deletions: [
            ...acc.character_deletions,
            ...childRevisions.character_deletions,
          ],
          range_deletions: [
            ...acc.range_deletions,
            ...childRevisions.range_deletions,
          ],
          insertions: [...acc.insertions, ...childRevisions.insertions],
          pastings: [...acc.pastings, ...childRevisions.pastings],
        };
      },
      {
        character_deletions: [] as number[],
        range_deletions: [] as number[],
        insertions: [] as number[],
        pastings: [] as number[],
      }
    );

    return revisions;
  }

  getMouseActivity() {
    const self = this.getLatest();
    const children = self.getChildren();

    const { totalActivity } = children.reduce(
      (acc, child) => {
        if (!$isLogTextNode(child)) return acc;
        const activity = child.getMouseActivity();
        return {
          totalActivity: {
            num_clicks: acc.totalActivity.num_clicks + activity.num_clicks,
            move_distance:
              acc.totalActivity.move_distance + activity.move_distance,
            drag_distance:
              acc.totalActivity.drag_distance + activity.drag_distance,
            scroll_distance:
              acc.totalActivity.scroll_distance + activity.scroll_distance,
          },
        };
      },
      {
        totalActivity: {
          num_clicks: 0,
          move_distance: 0,
          drag_distance: 0,
          scroll_distance: 0,
        },
      }
    );

    return totalActivity;
  }
}

export function $createLogParagraphNode(): LogParagraphNode {
  return new LogParagraphNode();
}

export function $isLogParagraphNode(
  node: LexicalNode | null | undefined
): node is LogParagraphNode {
  return node instanceof LogParagraphNode;
}
