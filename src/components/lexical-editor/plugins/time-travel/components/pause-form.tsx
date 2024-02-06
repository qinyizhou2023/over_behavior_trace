import { useAtom } from "jotai";
import { useState } from "react";

import {
  blockAiAssistanceCompletionAnnotationAtom,
  blockAiAssistanceFeedbackAnnotationAtom,
  blockAiAssistanceIdeasAnnotationAtom,
  blockAiAssistanceOtherAnnotationAtom,
  blockPlanningGeneratingStageAnnotationAtom,
  blockPlanningOrganizingStageAnnotationAtom,
  blockPlanningSettingStageAnnotationAtom,
  blockPossibilityAtom,
  blockReviewingEvaluatingStageAnnotationAtom,
  blockReviewingRevisingStageAnnotationAtom,
  blockTranslatingStageAnnotationAtom,
} from "@/atoms/block-atom";
import GridSelect from "@/components/grid-select";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sheet, SheetContent, SheetFooter } from "@/components/ui/sheet";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { InfoCircledIcon } from "@radix-ui/react-icons";

interface PauseFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSave: () => void;
}

export default function PauseForm({ open, onSave }: PauseFormProps) {
  const [other, setOther] = useAtom(blockAiAssistanceOtherAnnotationAtom);
  const [currentStep, setCurrentStep] = useState("step-1");
  return (
    <Sheet defaultOpen={false} open={open} modal={false}>
      {/* <SheetTrigger asChild>{trigger}</SheetTrigger> */}
      <SheetContent
        className="flex flex-col space-y-4 pr-1"
        showCloseButton={false}
      >
        <ScrollArea className="flex-1 pr-4">
          <Tabs
            defaultValue="step-1"
            className="w-full flex flex-col"
            value={currentStep}
            onValueChange={(value) => setCurrentStep(value)}
          >
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="step-1">Block Type</TabsTrigger>
              <TabsTrigger value="step-2">AI Assistance</TabsTrigger>
            </TabsList>

            <TabsContent
              value="step-1"
              className="flex-1 flex flex-col space-y-10"
            >
              <div className="flex flex-col space-y-4">
                <Label className="text-xl">Is this a block?</Label>
                <GridSelect atom={blockPossibilityAtom} />
              </div>

              <div className="flex flex-col space-y-4">
                <Label className="text-xl">Planning</Label>
                <ul className="space-y-4">
                  <li>
                    <GridSelect
                      atom={blockPlanningGeneratingStageAnnotationAtom}
                      label="Generating ideas to write about"
                    />
                  </li>
                  <li>
                    <GridSelect
                      atom={blockPlanningOrganizingStageAnnotationAtom}
                      label="Organizing ideas to write about"
                    />
                  </li>
                  <li>
                    <GridSelect
                      atom={blockPlanningSettingStageAnnotationAtom}
                      label="Setting the writing goal"
                    />
                  </li>
                </ul>
              </div>

              <div className="flex flex-col space-y-4">
                <div className="flex flex-row items-center space-x-2">
                  <Label className="text-xl">Translating</Label>
                  <TooltipProvider>
                    <Tooltip delayDuration={100}>
                      <TooltipTrigger asChild>
                        <Button size={"icon"} variant={"link"}>
                          <InfoCircledIcon className="w-4 h-4" />
                        </Button>
                      </TooltipTrigger>

                      <TooltipContent>
                        <span className="italic">Translating</span> ideas and
                        goals into written words and sentences;
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
                <ul className="space-y-4">
                  <GridSelect atom={blockTranslatingStageAnnotationAtom} />
                </ul>
              </div>

              <div className="flex flex-col space-y-4">
                <Label className="text-xl">Reviewing</Label>
                <ul className="space-y-4">
                  <li>
                    <GridSelect
                      label="Evaluating written text"
                      tooltip="Evaluate the quality of the written text, e.g., whether the text is clear, concise, and coherent"
                      atom={blockReviewingEvaluatingStageAnnotationAtom}
                    />
                  </li>
                  <li>
                    <GridSelect
                      label="Revising written text"
                      tooltip="Reading and revising written text, e.g., have the idea of adding, deleting, or reorganizing sentences"
                      atom={blockReviewingRevisingStageAnnotationAtom}
                    />
                  </li>
                </ul>
              </div>
            </TabsContent>
            <TabsContent value="step-2">
              <div className="flex flex-col space-y-4 mt-4 mb-4">
                <Label className="text-xl">
                  What kinds of AI assistance can help with this block?
                </Label>

                <ul className="space-y-4">
                  <li>
                    <GridSelect
                      label="AI suggests ideas to write about"
                      tooltip="e.g., “How about writing about <suggested idea>?"
                      atom={blockAiAssistanceIdeasAnnotationAtom}
                    />
                  </li>
                  <li>
                    <GridSelect
                      label="AI helps complete the sentence you are writing"
                      tooltip="Works like autocomplete / copilot"
                      atom={blockAiAssistanceCompletionAnnotationAtom}
                    />
                  </li>
                  <li>
                    <GridSelect
                      label="AI provides feedback to the sentence you are writing"
                      tooltip="e.g., “This sentence is too long. Consider splitting it into two sentences.”"
                      atom={blockAiAssistanceFeedbackAnnotationAtom}
                    />
                  </li>
                  <li>
                    <div className="flex flex-col space-y-2">
                      <Label htmlFor="custom-ai-support">
                        Others, please specify
                      </Label>
                      <Textarea
                        id="custom-ai-support"
                        value={other}
                        onChange={(e) => {
                          setOther(e.currentTarget.value);
                        }}
                      />
                    </div>
                  </li>
                </ul>
              </div>
            </TabsContent>
          </Tabs>
        </ScrollArea>

        <SheetFooter>
          {currentStep === "step-1" ? (
            <Button onClick={() => setCurrentStep("step-2")}>Next</Button>
          ) : (
            <Button
              onClick={() => {
                setCurrentStep("step-1");
                onSave();
              }}
            >
              Save changes
            </Button>
          )}
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
