import { $getSelection } from "lexical";
import { throttle } from "lodash";
import { useCallback, useEffect, useRef } from "react";

import { useLexicalComposerContext } from "@lexical/react/LexicalComposerContext";

import { $isLogTextNode, LogTextNode } from "../log-text/node";

export type MouseActivityType = {
  click: number;
  move_distance: number;
  drag_distance: number;
  scroll_distance: number;
};

export function MouseActivityPlugin() {
  const [editor] = useLexicalComposerContext();
  const currentPosition = useRef<{ x: number; y: number }>();

  const withActiveLogTextNode = useCallback(
    (fn: (logTextNode: LogTextNode) => void) => {
      editor.update(() => {
        const node = $getSelection()?.getNodes()[0];
        if (!$isLogTextNode(node)) return;

        fn(node);
      });
    },
    [editor]
  );

  const handleMouseMovement = throttle((e: MouseEvent) => {
    withActiveLogTextNode((node) => {
      if (!node) return;

      const activity = node.getMouseActivity();

      const currentX = e.clientX;
      const currentY = e.clientY;

      if (currentPosition.current) {
        activity.move_distance += Math.sqrt(
          (currentX - currentPosition.current.x) ** 2 +
            (currentY - currentPosition.current.y) ** 2
        );
      }

      currentPosition.current = { x: currentX, y: currentY };

      node.setMouseActivity(activity);
    });
  }, 100);

  const handleMouseClick = throttle(() => {
    withActiveLogTextNode((node) => {
      if (!node) return;

      const activity = node.getMouseActivity();

      activity.click += 1;

      node.setMouseActivity(activity);
    });
  }, 100);

  const handleScroll = throttle((e: WheelEvent) => {
    withActiveLogTextNode((node) => {
      if (!node) return;

      const activity = node.getMouseActivity();
      activity.scroll_distance += Math.abs(e.deltaY);
      node.setMouseActivity(activity);
    });
  });

  useEffect(() => {
    window.addEventListener("mousemove", handleMouseMovement);
    window.addEventListener("click", handleMouseClick);
    const editor = document.getElementById("editor-container");
    editor?.addEventListener("wheel", handleScroll);
    return () => {
      window.removeEventListener("mousemove", handleMouseMovement);
      window.removeEventListener("click", handleMouseClick);
      editor?.removeEventListener("wheel", handleScroll);
    };
  }, [handleMouseClick, handleMouseMovement, handleScroll]);

  return null;
}
