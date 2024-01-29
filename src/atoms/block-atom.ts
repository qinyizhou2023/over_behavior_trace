import { atom } from "jotai";
import { focusAtom } from "jotai-optics";

export type BlockStagePossibility = {
  planning: {
    generating: number;
    organizing: number;
    setting: number;
  };
  translating: number;
  reviewing: {
    evaluating: number;
    revising: number;
  };
};

export type BlockAiAssistancePossibility = {
  ideas: number;
  completion: number;
  feedback: number;
  other: string;
};

export type BlockAnnotation = {
  blockPossibility: number;
  blockStage: BlockStagePossibility;
  blockAiAssistance: BlockAiAssistancePossibility;
};

export const defaultBlockAnnotation: BlockAnnotation = {
  blockPossibility: 4,
  blockStage: {
    planning: {
      generating: 4,
      organizing: 4,
      setting: 4,
    },
    translating: 4,
    reviewing: {
      evaluating: 4,
      revising: 4,
    },
  },
  blockAiAssistance: {
    ideas: 4,
    completion: 4,
    feedback: 4,
    other: "",
  },
};

export const isBlockAtom = atom<boolean>(true);

export const blockAnnotationAtom = atom<BlockAnnotation>(
  defaultBlockAnnotation
);

export const blockPossibilityAtom = focusAtom(blockAnnotationAtom, (optic) =>
  optic.prop("blockPossibility")
);

export const blockStageAnnotationAtom = focusAtom(
  blockAnnotationAtom,
  (optic) => optic.prop("blockStage")
);

const blockPlanningStageAnnotationAtom = focusAtom(
  blockStageAnnotationAtom,
  (optic) => optic.prop("planning")
);

export const blockPlanningGeneratingStageAnnotationAtom = focusAtom(
  blockPlanningStageAnnotationAtom,
  (optic) => optic.prop("generating")
);

export const blockPlanningOrganizingStageAnnotationAtom = focusAtom(
  blockPlanningStageAnnotationAtom,
  (optic) => optic.prop("organizing")
);

export const blockPlanningSettingStageAnnotationAtom = focusAtom(
  blockPlanningStageAnnotationAtom,
  (optic) => optic.prop("setting")
);

export const blockTranslatingStageAnnotationAtom = focusAtom(
  blockStageAnnotationAtom,
  (optic) => optic.prop("translating")
);

const blockReviewingStageAnnotationAtom = focusAtom(
  blockStageAnnotationAtom,
  (optic) => optic.prop("reviewing")
);

export const blockReviewingEvaluatingStageAnnotationAtom = focusAtom(
  blockReviewingStageAnnotationAtom,
  (optic) => optic.prop("evaluating")
);

export const blockReviewingRevisingStageAnnotationAtom = focusAtom(
  blockReviewingStageAnnotationAtom,
  (optic) => optic.prop("revising")
);

const blockAiAssistanceAnnotationAtom = focusAtom(
  blockAnnotationAtom,
  (optic) => optic.prop("blockAiAssistance")
);

export const blockAiAssistanceIdeasAnnotationAtom = focusAtom(
  blockAiAssistanceAnnotationAtom,
  (optic) => optic.prop("ideas")
);

export const blockAiAssistanceCompletionAnnotationAtom = focusAtom(
  blockAiAssistanceAnnotationAtom,
  (optic) => optic.prop("completion")
);

export const blockAiAssistanceFeedbackAnnotationAtom = focusAtom(
  blockAiAssistanceAnnotationAtom,
  (optic) => optic.prop("feedback")
);

export const blockAiAssistanceOtherAnnotationAtom = focusAtom(
  blockAiAssistanceAnnotationAtom,
  (optic) => optic.prop("other")
);
