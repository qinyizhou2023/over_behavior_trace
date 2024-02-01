import { useAtom, useAtomValue, useSetAtom } from "jotai";
import { useEffect, useMemo, useRef, useState } from "react";
import { toast } from "sonner";

import { blockAnnotationAtom } from "@/atoms/block-atom";
import {
  blockThresholdInSecAtom,
  currentSessionAtom,
  latestEditorStateAtom,
  sessionListAtom,
  timeTravelReplayerStateAtom,
  timeTravelStateAtom,
} from "@/atoms/time-travel-atom";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Toggle } from "@/components/ui/toggle";
import { useLexicalComposerContext } from "@lexical/react/LexicalComposerContext";
import { PlayIcon, ReloadIcon, StopIcon } from "@radix-ui/react-icons";

import PauseForm from "./pause-form";

const PLAYBACK_SPEEDS = [0.5, 0.25, 1, 2, 4];

export default function Replayer() {
  const [editor] = useLexicalComposerContext();

  const currentSession = useAtomValue(currentSessionAtom);
  const [updatingSession, setUpdatingSession] = useState(currentSession);

  const latestEditorState = useAtomValue(latestEditorStateAtom);

  const [replayState, setReplayState] = useAtom(timeTravelReplayerStateAtom);
  const [sliderValue, setSliderValue] = useState<number>(0);
  const currentStepRef = useRef<number>(0);
  const [pauseFormOpen, setPauseFormOpen] = useState(false);
  const setTimeTravelState = useSetAtom(timeTravelStateAtom);

  const blockThresholdInSec = useAtomValue(blockThresholdInSecAtom);

  const [currentBlockAnnotation, setCurrentBlockAnnotation] =
    useAtom(blockAnnotationAtom);

  const setSessionList = useSetAtom(sessionListAtom);

  // const [isBlock, setIsBlock] = useAtom(isBlockAtom);

  const totalSteps = currentSession.logs.length - 1;

  const firstEditorState = useMemo(
    () => currentSession.logs[0]?.editorState,
    [currentSession.logs]
  );

  useEffect(() => {
    editor.setEditorState(firstEditorState);
    currentStepRef.current = 0;
    setSliderValue(0);
  }, [editor, firstEditorState]);

  const [playbackSpeedIndex, setPlaybackSpeedIndex] = useState(2);

  useEffect(() => {
    let timeoutId: ReturnType<typeof setTimeout>;

    const timeDiff =
      currentSession.logs[currentStepRef.current + 1]?.time -
      currentSession.logs[currentStepRef.current]?.time;
    const blocks = updatingSession.blocks.filter(
      (block) => block.duration_block > blockThresholdInSec * 1000
    );

    if (replayState === "playing") {
      editor.focus();
      const play = () => {
        const currentStep = currentStepRef.current;

        if (currentStepRef.current === totalSteps) {
          setReplayState("finished");
          return;
        }

        if (currentSession.logs[currentStep].blockId) {
          const block = blocks.find(
            (b) => b.id === currentSession.logs[currentStep].blockId
          );

          if (block) {
            setCurrentBlockAnnotation(() => block.annotation);
            setPauseFormOpen(true);
            setReplayState("idle");
          }
        }

        timeoutId = setTimeout(() => {
          currentStepRef.current++;
          setSliderValue(currentStepRef.current);

          const newStep = currentStepRef.current;

          editor.setEditorState(currentSession.logs[newStep].editorState);

          play();
        }, timeDiff / PLAYBACK_SPEEDS[playbackSpeedIndex]);
      };

      play();
    }

    return () => {
      clearTimeout(timeoutId);
    };
  }, [
    replayState,
    editor,
    playbackSpeedIndex,
    totalSteps,
    blockThresholdInSec,
    setReplayState,
    setCurrentBlockAnnotation,
    currentSession.logs,
    currentSession.blocks,
    updatingSession.blocks,
  ]);

  return (
    <div className="flex flex-col space-y-2 w-full">
      <PauseForm
        open={pauseFormOpen}
        onOpenChange={setPauseFormOpen}
        onSave={async () => {
          setUpdatingSession((prev) => {
            const currentBlock = prev.blocks.find(
              (b) => b.id === prev.logs[currentStepRef.current].blockId
            );

            if (!currentBlock) {
              return prev;
            }

            // newBlocks.splice(newBlocks.indexOf(currentBlock), 1, {
            //   ...currentBlock,
            //   annotated: true,
            //   annotation: currentBlockAnnotation,
            // });

            const newBlocks = prev.blocks.map((block) => {
              if (block.id === currentBlock.id) {
                return {
                  ...block,
                  annotated: true,
                  annotation: currentBlockAnnotation,
                  threshold: blockThresholdInSec,
                };
              }

              return block;
            });

            return {
              ...prev,
              blocks: newBlocks,
            };
          });

          toast.success("Block annotation saved.");

          // timeTravelConfiguration.onUpdateLog(currentTimeTravelLogId, {
          //   id: currentTimeTravelLogId,
          //   saveTime: new Date(),
          //   log: timeTravelLogs,
          // });

          setPauseFormOpen(false);
          currentStepRef.current++;
          setSliderValue(currentStepRef.current);
          setReplayState("playing");
        }}
        // onNotBlocking={() => {
        //   setPauseFormOpen(false);
        //   currentStepRef.current++;
        //   setSliderValue(currentStepRef.current);
        //   setReplayState(TimeTravelReplayerState.Playing);
        // }}
      />

      <div className="grid grid-cols-3 items-center">
        <Toggle
          className="justify-self-start"
          variant="default"
          aria-label="autoplay"
          pressed={replayState === "playing"}
          onPressedChange={(pressed) => {
            if (pressed) {
              setReplayState("playing");

              if (currentStepRef.current === totalSteps) {
                currentStepRef.current = 0;
                setSliderValue(0);
              }
            } else {
              setReplayState("idle");
            }
          }}
        >
          {
            {
              idle: <PlayIcon className="w-4 h-4" />,
              playing: <StopIcon className="w-4 h-4" />,
              finished: <ReloadIcon className="w-4 h-4" />,
            }[replayState]
          }
        </Toggle>
        <Label className="justify-self-center">
          Step {sliderValue}/{totalSteps}
        </Label>
        <Button
          variant={"link"}
          className="justify-self-end"
          onClick={() => {
            setPlaybackSpeedIndex(
              (playbackSpeedIndex + 1) % PLAYBACK_SPEEDS.length
            );
          }}
        >
          {PLAYBACK_SPEEDS[playbackSpeedIndex]}x
        </Button>
      </div>

      <Slider
        min={1}
        max={totalSteps}
        value={[sliderValue]}
        onValueChange={([ind]) => {
          setSliderValue(ind);
          const editorState = currentSession.logs[ind].editorState;
          editor.setEditorState(editorState);
        }}
      />

      <div className="flex justify-between items-center">
        <Button
          variant={"link"}
          onClick={() => {
            const index = totalSteps;

            if (latestEditorState) {
              editor.setEditorState(latestEditorState);
            }

            setSliderValue(index);

            setReplayState("idle");
            setTimeTravelState("recording");

            setSessionList((prev) => {
              const newSessionList = prev.map((session) => {
                if (session.id === currentSession.id) {
                  return {
                    ...session,
                    blocks: updatingSession.blocks,
                  };
                }

                return session;
              });

              return newSessionList;
            });
          }}
        >
          Exit
        </Button>
      </div>
    </div>
  );
}
