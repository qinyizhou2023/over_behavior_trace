import {
  LexicalEditor,
  LexicalNode,
  ParagraphNode,
  SerializedParagraphNode,
} from "lexical";

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
          character_deletings: [
            ...acc.character_deletings,
            ...childRevisions.character_deletings,
          ],
          range_deletings: [
            ...acc.range_deletings,
            ...childRevisions.range_deletings,
          ],
          insertings: [...acc.insertings, ...childRevisions.insertings],
          pastings: [...acc.pastings, ...childRevisions.pastings],
        };
      },
      {
        character_deletings: [] as number[],
        range_deletings: [] as number[],
        insertings: [] as number[],
        pastings: [] as number[],
      }
    );

    return revisions;
  }

  getSentenceCompletion(editor: LexicalEditor): number {
    const self = this.getLatest();
    const children = self.getChildren();

    const { totalCompletion, totalChildrenNum } = children.reduce(
      (acc, child) => {
        if (!$isLogTextNode(child)) return acc;
        const completion = child.getSentenceCompletion(editor);
        return {
          totalCompletion: acc.totalCompletion + completion,
          totalChildrenNum: acc.totalChildrenNum + 1,
        };
      },
      { totalCompletion: 0, totalChildrenNum: 0 }
    );

    return totalCompletion / totalChildrenNum;
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
