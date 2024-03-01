import { useAtom, useAtomValue, useSetAtom } from "jotai";
import { EditorState } from "lexical";
import { useEffect, useMemo, useRef, useState } from "react";
import { toast } from "sonner";

import { blockAnnotationAtom, currentBlockAtom } from "@/atoms/block-atom";
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
import {
  Table,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Toggle } from "@/components/ui/toggle";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import { useLexicalComposerContext } from "@lexical/react/LexicalComposerContext";
import {
  EnterIcon,
  PlayIcon,
  ReloadIcon,
  StopIcon,
} from "@radix-ui/react-icons";

import PauseForm from "./pause-form";

const PLAYBACK_SPEEDS = [0.5, 0.25, 1, 2, 4];

const LOOPING_WINDOW_SIZE = 15;

export default function Replayer() {
  const [editor] = useLexicalComposerContext();

  const currentSession = useAtomValue(currentSessionAtom);
  const [updatingSession, setUpdatingSession] = useState(currentSession);

  const latestEditorState = useAtomValue(latestEditorStateAtom);

  const [replayState, setReplayState] = useAtom(timeTravelReplayerStateAtom);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [pauseFormOpen, setPauseFormOpen] = useState(false);
  const setTimeTravelState = useSetAtom(timeTravelStateAtom);

  const blockThresholdInSec = useAtomValue(blockThresholdInSecAtom);

  const loopingWindow = useRef<EditorState[]>([]);
  const loopingIndex = useRef(0);

  const [currentBlockAnnotation, setCurrentBlockAnnotation] =
    useAtom(blockAnnotationAtom);

  const setCurrentBlock = useSetAtom(currentBlockAtom);

  const setSessionList = useSetAtom(sessionListAtom);

  const totalSteps = currentSession.logs.length - 1;

  const firstEditorState = useMemo(
    () => currentSession.logs[0]?.editorState,
    [currentSession.logs]
  );

  useEffect(() => {
    let timeoutId: ReturnType<typeof setInterval> | undefined = undefined;
    if (replayState === "looping") {
      editor.setEditable(false);
      timeoutId = setInterval(() => {
        if (loopingIndex.current === loopingWindow.current.length - 1) {
          loopingIndex.current = 0;
        } else {
          loopingIndex.current += 1;
        }

        editor.setEditorState(loopingWindow.current[loopingIndex.current], {});
      }, 200);
    } else {
      editor.setEditable(true);
      if (timeoutId) clearInterval(timeoutId);
    }

    return () => {
      if (timeoutId) clearInterval(timeoutId);
    };
  }, [editor, replayState]);

  useEffect(() => {
    editor.setEditorState(firstEditorState);
    setCurrentStep(0);
  }, [editor, firstEditorState]);

  const [playbackSpeedIndex, setPlaybackSpeedIndex] = useState(2);

  useEffect(() => {
    let timeoutId: ReturnType<typeof setTimeout>;

    const timeDiff =
      updatingSession.logs[currentStep + 1]?.time -
      updatingSession.logs[currentStep]?.time;
    const blocks = updatingSession.blocks.filter(
      (block) => block.duration_block > blockThresholdInSec * 1000
    );

    if (replayState === "playing") {
      // editor.focus();
      const play = () => {
        if (currentStep === totalSteps) {
          setReplayState("finished");
          return;
        }

        if (updatingSession.logs[currentStep].blockId) {
          const block = blocks.find(
            (b) => b.id === updatingSession.logs[currentStep].blockId
          );

          if (block) {
            setCurrentBlockAnnotation(() => block.annotation);
            setCurrentBlock(() => block);
            setPauseFormOpen(true);

            loopingWindow.current = updatingSession.logs
              .slice(
                Math.max(0, currentStep - LOOPING_WINDOW_SIZE),
                currentStep + LOOPING_WINDOW_SIZE
              )
              .map((log) => log.editorState);

            setReplayState("looping");
          }
        }

        timeoutId = setTimeout(() => {
          setCurrentStep((prev) => {
            editor.setEditorState(updatingSession.logs[prev + 1].editorState);
            return prev + 1;
          });

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
    updatingSession.logs,
    updatingSession.blocks,
    currentStep,
    setCurrentBlock,
  ]);

  return (
    <div className="flex flex-col space-y-2 w-full">
      <PauseForm
        open={pauseFormOpen}
        onOpenChange={setPauseFormOpen}
        onSave={async () => {
          setUpdatingSession((prev) => {
            const currentBlock = prev.blocks.find(
              (b) => b.id === prev.logs[currentStep].blockId
            );

            if (!currentBlock) {
              return prev;
            }

            const newBlocks = prev.blocks.map((block) => {
              if (block.id === currentBlock.id) {
                return {
                  ...block,
                  annotated: true,
                  annotation: currentBlockAnnotation,
                  threshold: blockThresholdInSec,
                  num_blocks: prev.blocks.filter(
                    (b) => b.duration_block > blockThresholdInSec * 1000
                  ).length,
                  avg_block_duration:
                    prev.blocks
                      .filter(
                        (b) => b.duration_block > blockThresholdInSec * 1000
                      )
                      .reduce((acc, curr) => acc + curr.duration_block, 0) /
                    prev.blocks.filter(
                      (b) => b.duration_block > blockThresholdInSec * 1000
                    ).length,
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

          setPauseFormOpen(false);
          setCurrentStep((prev) => prev + 1);
          setReplayState("playing");
        }}
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

              if (currentStep === totalSteps) {
                setCurrentStep(0);
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
              looping: <PlayIcon className="w-4 h-4" />,
            }[replayState]
          }
        </Toggle>
        <Label className="justify-self-center">
          Step {currentStep}/{totalSteps}
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
        value={[currentStep]}
        onValueChange={([ind]) => {
          setCurrentStep(ind);
          const editorState = updatingSession.logs[ind].editorState;
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

            setCurrentStep(() => index);

            setReplayState("idle");
            setTimeTravelState("recording");

            setSessionList((prev) => {
              const newSessionList = prev.map((session) => {
                if (session.id === updatingSession.id) {
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
          Save and finish
        </Button>
      </div>
      <Table className="w-full">
        <TableHeader>
          <TableRow>
            <TableHead />
            <TableHead>Step</TableHead>
            <TableHead>Duration</TableHead>
            <TableHead>Blocking Sentence</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        {updatingSession.blocks
          .filter((b) => b.duration_block > blockThresholdInSec * 1000)
          .map((block, index) => {
            const step = updatingSession.logs.findIndex(
              (log) => log.blockId === block.id
            );

            if (!step) {
              return null;
            }

            return (
              <TableRow key={index}>
                <TableCell>
                  <TooltipProvider>
                    <Tooltip delayDuration={0}>
                      <TooltipTrigger asChild>
                        <span
                          className={cn(
                            "flex h-2 w-2 rounded-full",
                            block.annotated
                              ? "bg-green-500"
                              : "bg-yellow-500 animate-pulse",
                            {
                              "bg-blue-500": step === currentStep,
                            }
                          )}
                        />
                      </TooltipTrigger>
                      <TooltipContent side="top">
                        {block.annotated ? "Annotated" : "Not annotated"}
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </TableCell>
                <TableCell>{step}</TableCell>

                <TableCell>
                  {(block.duration_block / 1000).toFixed(2)} s
                </TableCell>
                <TableCell className="max-w-20 break-all">
                  {block.block_sentence}
                </TableCell>

                <TableCell>
                  <TooltipProvider>
                    <Tooltip delayDuration={0}>
                      <TooltipTrigger asChild>
                        <Button
                          variant={"link"}
                          size={"icon"}
                          onClick={() => {
                            setCurrentStep(() => step);
                            setCurrentBlock(() => block);
                            setReplayState("playing");
                            editor.setEditorState(
                              updatingSession.logs[step].editorState
                            );
                          }}
                        >
                          <EnterIcon className="w-4 h-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent side="right">
                        Jump to step {step}
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </TableCell>
              </TableRow>
            );
          })}
      </Table>
    </div>
  );
}
