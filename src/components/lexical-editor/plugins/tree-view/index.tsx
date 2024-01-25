/**
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 *
 */

import { buttonVariants } from "@/components/ui/button";
import { useLexicalComposerContext } from "@lexical/react/LexicalComposerContext";
import { TreeView } from "@lexical/react/LexicalTreeView";

export default function TreeViewPlugin(): JSX.Element {
  const [editor] = useLexicalComposerContext();
  return (
    <TreeView
      // viewClassName="tree-view-output"
      timeTravelPanelClassName="debug-timetravel-panel"
      treeTypeButtonClassName={buttonVariants({
        variant: "default",
      })}
      viewClassName="rounded border bg-card text-card-foreground shadow p-6 m-4"
      timeTravelButtonClassName={buttonVariants({
        variant: "default",
      })}
      timeTravelPanelSliderClassName="debug-timetravel-panel-slider"
      timeTravelPanelButtonClassName={buttonVariants({
        variant: "default",
      })}
      editor={editor}
    />
  );
}
