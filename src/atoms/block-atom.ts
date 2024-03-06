import { atom } from "jotai";
import { focusAtom } from "jotai-optics";

import { BlockType } from "./time-travel-atom";

export type BlockStateLikelihood = {
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

export type BlockAiAssistanceLikelihood = {
  ideas: number;
  completion: number;
  feedback: number;
  other: string;
};

export type BlockAnnotation = {
  block_likelihood: number;
  block_state: BlockStateLikelihood;
  block_ai_asistance: BlockAiAssistanceLikelihood;
};

const DEFAULT_BLOCK_ANNOTATION_LEVEL = 1;

export const defaultBlockAnnotation: BlockAnnotation = {
  block_likelihood: DEFAULT_BLOCK_ANNOTATION_LEVEL,
  block_state: {
    planning: {
      generating: DEFAULT_BLOCK_ANNOTATION_LEVEL,
      organizing: DEFAULT_BLOCK_ANNOTATION_LEVEL,
      setting: DEFAULT_BLOCK_ANNOTATION_LEVEL,
    },
    translating: DEFAULT_BLOCK_ANNOTATION_LEVEL,
    reviewing: {
      evaluating: DEFAULT_BLOCK_ANNOTATION_LEVEL,
      revising: DEFAULT_BLOCK_ANNOTATION_LEVEL,
    },
  },
  block_ai_asistance: {
    ideas: DEFAULT_BLOCK_ANNOTATION_LEVEL,
    completion: DEFAULT_BLOCK_ANNOTATION_LEVEL,
    feedback: DEFAULT_BLOCK_ANNOTATION_LEVEL,
    other: "",
  },
};

export const isBlockAtom = atom<boolean>(true);

export const blockAnnotationAtom = atom<BlockAnnotation>(
  defaultBlockAnnotation
);

export const currentBlockAtom = atom<BlockType | null>(null);

export const blockLikelihoodAtom = focusAtom(blockAnnotationAtom, (optic) =>
  optic.prop("block_likelihood")
);

export const blockStateAnnotationAtom = focusAtom(
  blockAnnotationAtom,
  (optic) => optic.prop("block_state")
);

const blockPlanningStateAnnotationAtom = focusAtom(
  blockStateAnnotationAtom,
  (optic) => optic.prop("planning")
);

export const blockPlanningGeneratingStateAnnotationAtom = focusAtom(
  blockPlanningStateAnnotationAtom,
  (optic) => optic.prop("generating")
);

export const blockPlanningOrganizingStateAnnotationAtom = focusAtom(
  blockPlanningStateAnnotationAtom,
  (optic) => optic.prop("organizing")
);

export const blockPlanningSettingStateAnnotationAtom = focusAtom(
  blockPlanningStateAnnotationAtom,
  (optic) => optic.prop("setting")
);

export const blockTranslatingStateAnnotationAtom = focusAtom(
  blockStateAnnotationAtom,
  (optic) => optic.prop("translating")
);

const blockReviewingStateAnnotationAtom = focusAtom(
  blockStateAnnotationAtom,
  (optic) => optic.prop("reviewing")
);

export const blockReviewingEvaluatingStateAnnotationAtom = focusAtom(
  blockReviewingStateAnnotationAtom,
  (optic) => optic.prop("evaluating")
);

export const blockReviewingRevisingStateAnnotationAtom = focusAtom(
  blockReviewingStateAnnotationAtom,
  (optic) => optic.prop("revising")
);

const blockAiAssistanceAnnotationAtom = focusAtom(
  blockAnnotationAtom,
  (optic) => optic.prop("block_ai_asistance")
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
