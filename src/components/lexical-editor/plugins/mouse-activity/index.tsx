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
  const currentDragPosition = useRef<{ x: number; y: number }>();

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

      if (e.buttons === 0) {
        currentDragPosition.current = undefined;

        node.setMouseActivity({
          ...activity,
          move_distance:
            activity.move_distance +
            (currentPosition.current
              ? Math.sqrt(
                  (currentX - currentPosition.current.x) ** 2 +
                    (currentY - currentPosition.current.y) ** 2
                )
              : 0),
        });

        currentPosition.current = { x: currentX, y: currentY };
      } else {
        if (currentDragPosition.current) {
          node.setMouseActivity({
            ...activity,
            drag_distance:
              activity.drag_distance +
              Math.sqrt(
                (currentX - currentDragPosition.current.x) ** 2 +
                  (currentY - currentDragPosition.current.y) ** 2
              ),
          });
        }

        currentDragPosition.current = { x: currentX, y: currentY };
      }
    });
  }, 100);

  const handleMouseClick = throttle(() => {
    withActiveLogTextNode((node) => {
      if (!node) return;

      // console.log("click", node.getMouseActivity(), node.__type, node.getKey());

      const activity = node.getMouseActivity();

      node.setMouseActivity({
        ...activity,
        click: activity.click + 1,
      });
    });
  }, 100);

  const handleScroll = throttle((e: WheelEvent) => {
    withActiveLogTextNode((node) => {
      if (!node) return;

      const activity = node.getMouseActivity();
      node.setMouseActivity({
        ...activity,
        scroll_distance: activity.scroll_distance + Math.abs(e.deltaY),
      });
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
