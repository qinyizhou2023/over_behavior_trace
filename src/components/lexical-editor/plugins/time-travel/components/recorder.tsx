import { useAtom, useSetAtom } from "jotai";
import { useEffect, useRef } from "react";
import { toast } from "sonner";
import { v4 as uuidv4 } from "uuid";

import { defaultBlockAnnotation } from "@/atoms/block-atom";
import {
  BlockType,
  LogItem,
  MIN_THRESHOLD_IN_SEC,
  sessionListAtom,
  timeTravelRecorderStateAtom,
} from "@/atoms/time-travel-atom";
import { Button } from "@/components/ui/button";
import { $getDocumentMetrics, getUserBehavior } from "@/lib/user-behavior";
import { useLexicalComposerContext } from "@lexical/react/LexicalComposerContext";
import { PlayIcon, StopIcon } from "@radix-ui/react-icons";

import SessionList from "./session-list";

export default function Recorder() {
  const [editor] = useLexicalComposerContext();
  const [timeTravelRecorderState, setTimeTravelRecorderState] = useAtom(
    timeTravelRecorderStateAtom
  );

  const sessionStartTime = useRef<number>(Date.now());
  const lastUpdateTime = useRef<number>();

  const currentTimeTravelLogs = useRef<{
    logs: LogItem[];
    blocks: BlockType[];
  }>({
    logs: [],
    blocks: [],
  });

  const setSessionList = useSetAtom(sessionListAtom);

  useEffect(() => {
    if (timeTravelRecorderState === "idle") return;
    sessionStartTime.current = Date.now();
    return editor.registerUpdateListener(({ editorState }) => {
      if (!lastUpdateTime.current) {
        lastUpdateTime.current = Date.now();
        currentTimeTravelLogs.current.logs.push({
          id: uuidv4(),
          time: Date.now(),
          editorState,
        });
        return;
      }

      const currentTime = Date.now();

      const timeDiff = currentTime - lastUpdateTime.current;
      const hasBlockBefore = timeDiff > MIN_THRESHOLD_IN_SEC * 1000;

      if (hasBlockBefore) {
        const blockId = uuidv4();
        editorState.read(() => {
          const {
            sentence_completion,
            overall_sentence_cnt,
            overall_word_cnt,
            block_sentence,
          } = $getDocumentMetrics();

          const lastBehavior =
            currentTimeTravelLogs.current.blocks.length > 0
              ? currentTimeTravelLogs.current.blocks[
                  currentTimeTravelLogs.current.blocks.length - 1
                ].user_behavior
              : undefined;
          currentTimeTravelLogs.current.blocks.push({
            id: blockId,
            start_time: currentTime,
            duration_block: timeDiff,
            threshold: MIN_THRESHOLD_IN_SEC * 1000,

            sentence_completion,
            overall_sentence_cnt,
            overall_word_cnt,

            block_sentence,

            relative_start_time: currentTime - sessionStartTime.current,
            num_blocks: currentTimeTravelLogs.current.blocks.length,
            avg_block_duration:
              currentTimeTravelLogs.current.blocks.reduce(
                (acc, curr) => acc + curr.duration_block,
                0
              ) / currentTimeTravelLogs.current.blocks.length,

            user_behavior: getUserBehavior(editor, lastBehavior),
            annotated: false,
            annotation: defaultBlockAnnotation,
          });

          currentTimeTravelLogs.current.logs.push({
            id: uuidv4(),
            time: currentTime,
            editorState,
            blockId: blockId,
          });
        });
      } else {
        currentTimeTravelLogs.current.logs.push({
          id: uuidv4(),
          time: currentTime,
          editorState,
        });
      }

      lastUpdateTime.current = currentTime;
    });
  }, [editor, timeTravelRecorderState]);

  return (
    <div className="flex flex-col space-y-4 w-full">
      {timeTravelRecorderState === "idle" && (
        <Button
          variant={"default"}
          onClick={() => {
            currentTimeTravelLogs.current = {
              logs: [],
              blocks: [],
            };
            setTimeTravelRecorderState("recording");
          }}
        >
          <PlayIcon className="w-4 h-4 mr-2" />
          Start Recording
        </Button>
      )}
      {timeTravelRecorderState === "recording" && (
        <Button
          variant={"outline"}
          onClick={async () => {
            setTimeTravelRecorderState("idle");
            setSessionList((prev) => [
              ...prev,
              {
                id: uuidv4(),
                saveTime: new Date(),
                logs: currentTimeTravelLogs.current.logs,
                blocks: currentTimeTravelLogs.current.blocks,
              },
            ]);

            toast.success("Recording saved.");
          }}
        >
          <StopIcon className="w-4 h-4 mr-2" />
          Stop Recording
        </Button>
      )}
      <SessionList />
    </div>
  );
}
