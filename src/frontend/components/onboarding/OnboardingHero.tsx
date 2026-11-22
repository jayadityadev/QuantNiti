import React, { useState } from "react";
import { motion, AnimatePresence, useReducedMotion } from "framer-motion";
import {
  TrendingUp,
  ShieldCheck,
  Target,
  ArrowRight,
  ChevronLeft,
  CheckCircle2,
  Sliders,
  Sparkles,
} from "lucide-react";
import { useAppStore } from "../../store/useAppStore";
import { GlassCard } from "../ui/GlassCard";
import { PrimaryButton } from "../ui/PrimaryButton";
import { GhostButton } from "../ui/GhostButton";
import { ProgressBar } from "../ui/ProgressBar";
import { QUIZ_QUESTIONS, calculatePersonaResult } from "./personaScoring";
import { QuizAnswers, PersonaResult } from "./types";

export interface OnboardingHeroProps {
  onComplete?: (result: PersonaResult) => void;
}

export const OnboardingHero: React.FC<OnboardingHeroProps> = ({ onComplete }) => {
  const shouldReduceMotion = useReducedMotion();
  const { setRiskPersona, setHorizon, setIsOnboarded } = useAppStore();

  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [questionIndex, setQuestionIndex] = useState<number>(0);
  const [answers, setAnswers] = useState<QuizAnswers>({});

  const currentQuestion = QUIZ_QUESTIONS[questionIndex];
  const currentAnswer = currentQuestion ? answers[currentQuestion.id] : undefined;

  const handleSelectOption = (optionId: string) => {
    if (!currentQuestion) return;
    setAnswers((prev) => ({
      ...prev,
      [currentQuestion.id]: optionId,
    }));
  };

  const handleNextQuestion = () => {
    if (questionIndex < QUIZ_QUESTIONS.length - 1) {
      setQuestionIndex((prev) => prev + 1);
    } else {
      setStep(3);
    }
  };

  const handlePrevQuestion = () => {
    if (questionIndex > 0) {
      setQuestionIndex((prev) => prev - 1);
    } else {
      setStep(1);
    }
  };

  const personaResult = calculatePersonaResult(answers);

  const handleFinishOnboarding = () => {
    setRiskPersona(personaResult.riskPersona);
    setHorizon(personaResult.horizon);
    setIsOnboarded(true);
    onComplete?.(personaResult);
  };

  // Motion transitions
  const stepTransition = shouldReduceMotion
    ? { duration: 0.1 }
    : { type: "spring", stiffness: 320, damping: 28 };

  const contentVariants = {
    initial: shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: 24 },
    animate: { opacity: 1, x: 0 },
    exit: shouldReduceMotion ? { opacity: 0 } : { opacity: 0, x: -24 },
  };

  return (
    <div
      data-testid="onboarding-hero"
      className="fixed inset-0 z-50 overflow-y-auto flex flex-col justify-between bg-[var(--bg-primary)] text-[var(--text-main)]"
    >
      {/* Top Header / Progress Bar */}
      <div className="w-full max-w-[520px] mx-auto px-6 pt-6 pb-2">
        <div className="flex items-center justify-between gap-4 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-xl bg-slate-900 dark:bg-teal-700 flex items-center justify-center shadow-sm">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold tracking-tight text-[var(--text-main)] text-base">QuantNiti</span>
          </div>
          <span className="text-xs font-medium text-teal-600 dark:text-teal-400">
            Step {step} of 3
          </span>
        </div>

        <ProgressBar totalSteps={3} currentStep={step} />
      </div>

      {/* Main Step Container */}
      <div className="w-full max-w-[520px] mx-auto px-6 py-4 flex-1 flex flex-col justify-center">
        <AnimatePresence mode="wait">
          {/* STEP 1: Welcome Splash */}
          {step === 1 && (
            <motion.div
              key="step-1"
              variants={contentVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              transition={stepTransition}
              className="flex flex-col items-center text-center space-y-6 my-auto"
            >
              {/* Hero Badge */}
              <motion.div
                initial={shouldReduceMotion ? {} : { scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: "spring", stiffness: 280, damping: 20 }}
                className="w-16 h-16 rounded-2xl bg-slate-900 dark:bg-teal-700 flex items-center justify-center shadow-sm"
              >
                <TrendingUp className="w-8 h-8 text-white" />
              </motion.div>

              {/* Headings */}
              <div className="space-y-3">
                <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-[var(--text-main)]">
                  Intelligent investing, made simple
                </h1>
                <p className="text-sm text-[var(--text-muted)] max-w-md mx-auto leading-relaxed">
                  AI-driven portfolio intelligence for Indian retail investors. Quantitative asset allocation,
                  regime-aware risk guardrails, and automated compounding defense.
                </p>
              </div>

              {/* Value Highlights */}
              <div className="w-full grid grid-cols-1 gap-2.5 pt-2 text-left">
                <GlassCard className="p-3.5 flex items-center gap-3 bg-[var(--bg-card)] border-[var(--border-subtle)]">
                  <ShieldCheck className="w-5 h-5 text-emerald-500 shrink-0" />
                  <div className="text-xs">
                    <p className="font-semibold text-[var(--text-main)]">Regime-adaptive guardrails</p>
                    <p className="text-[var(--text-muted)]">Protects your capital across bull, bear, and sideways regimes.</p>
                  </div>
                </GlassCard>

                <GlassCard className="p-3.5 flex items-center gap-3 bg-[var(--bg-card)] border-[var(--border-subtle)]">
                  <Target className="w-5 h-5 text-teal-600 dark:text-teal-400 shrink-0" />
                  <div className="text-xs">
                    <p className="font-semibold text-[var(--text-main)]">Personalized persona calibrations</p>
                    <p className="text-[var(--text-muted)]">Tailored risk tolerance and compounding horizons.</p>
                  </div>
                </GlassCard>
              </div>

              {/* CTA Button */}
              <div className="w-full pt-4">
                <p className="sr-only">Begin onboarding questionnaire</p>
                <PrimaryButton
                  fullWidth
                  onClick={() => setStep(2)}
                  icon={<ArrowRight className="w-4 h-4" />}
                >
                  Get started
                </PrimaryButton>
              </div>
            </motion.div>
          )}

          {/* STEP 2: Persona Quiz */}
          {step === 2 && currentQuestion && (
            <motion.div
              key={`question-${questionIndex}`}
              variants={contentVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              transition={stepTransition}
              className="flex flex-col space-y-6 my-auto"
            >
              {/* Question Meta & Prompt */}
              <div className="space-y-2">
                <div role="status" aria-live="polite" className="flex items-center justify-between text-xs font-medium text-teal-600 dark:text-teal-400">
                  <span>{currentQuestion.title}</span>
                  <span>
                    Question {questionIndex + 1} of {QUIZ_QUESTIONS.length}
                  </span>
                </div>
                <h2 className="text-lg sm:text-xl font-bold text-[var(--text-main)] tracking-tight leading-snug">
                  {currentQuestion.prompt}
                </h2>
              </div>

              {/* Option Cards */}
              <div className="space-y-3">
                {currentQuestion.options.map((option) => {
                  const isSelected = currentAnswer === option.id;
                  return (
                    <motion.button
                      key={option.id}
                      type="button"
                      whileTap={{ scale: 0.98 }}
                      onClick={() => handleSelectOption(option.id)}
                      className={`w-full text-left p-4 rounded-xl border transition-colors duration-200 flex items-start justify-between gap-3 focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none ${
                        isSelected
                          ? "border-teal-600 dark:border-teal-400 bg-teal-500/10 shadow-sm"
                          : "border-[var(--border-subtle)] bg-[var(--bg-card)] hover:border-slate-300 dark:hover:border-slate-700"
                      }`}
                    >
                      <div className="space-y-1 pr-2">
                        <p className="font-semibold text-sm sm:text-base text-[var(--text-main)]">
                          {option.title}
                        </p>
                        <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                          {option.subtitle}
                        </p>
                      </div>

                      <div
                        className={`w-5 h-5 mt-0.5 rounded-full border flex items-center justify-center shrink-0 transition-colors ${
                          isSelected
                            ? "border-teal-600 bg-teal-600 text-white"
                            : "border-[var(--border-subtle)] bg-[var(--bg-card-subtle)]"
                        }`}
                      >
                        {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-white" />}
                      </div>
                    </motion.button>
                  );
                })}
              </div>

              {/* Action Controls */}
              <div className="flex items-center justify-between gap-3 pt-2">
                <GhostButton
                  onClick={handlePrevQuestion}
                  icon={<ChevronLeft className="w-4 h-4" />}
                >
                  Back
                </GhostButton>

                <PrimaryButton
                  disabled={!currentAnswer}
                  onClick={handleNextQuestion}
                  icon={<ArrowRight className="w-4 h-4" />}
                >
                  {questionIndex === QUIZ_QUESTIONS.length - 1 ? "See My Profile" : "Continue"}
                </PrimaryButton>
              </div>
            </motion.div>
          )}

          {/* STEP 3: Personalized Result */}
          {step === 3 && (
            <motion.div
              key="step-3"
              variants={contentVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              transition={stepTransition}
              className="flex flex-col items-center text-center space-y-6 my-auto"
            >
              {/* Badge Reveal */}
              <motion.div
                initial={shouldReduceMotion ? {} : { scale: 0.6, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: "spring", stiffness: 350, damping: 22 }}
                className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-teal-500/10 border border-teal-500/20 text-teal-700 dark:text-teal-300 text-xs font-medium shadow-sm"
              >
                <Sliders className="w-4 h-4 text-teal-600 dark:text-teal-400" />
                <span>Personalized profile</span>
              </motion.div>

              <div className="space-y-2">
                <h2 className="text-2xl font-bold text-[var(--text-main)]">
                  You're a {personaResult.title}
                </h2>
                <p className="text-sm text-[var(--text-muted)] leading-relaxed max-w-sm mx-auto">
                  {personaResult.description}
                </p>
              </div>

              {/* Suggested Setup Card */}
              <div className="w-full p-4 space-y-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] text-left shadow-sm">
                <div className="flex justify-between items-center text-xs pb-2 border-b border-[var(--border-subtle)]">
                  <span className="text-[var(--text-muted)] font-medium">Recommended horizon:</span>
                  <span className="font-semibold text-teal-700 dark:text-teal-400">{personaResult.horizon}</span>
                </div>
                <div className="space-y-1">
                  <p className="text-xs text-[var(--text-muted)]">Target asset allocation:</p>
                  <p className="text-xs font-semibold text-[var(--text-main)]">{personaResult.suggestedAllocation}</p>
                </div>
                <div className="text-xs text-emerald-600 dark:text-emerald-400 font-medium flex items-center gap-1.5 pt-1">
                  <ShieldCheck className="w-4 h-4 text-emerald-500" />
                  <span>{personaResult.drawdownGuidance}</span>
                </div>
              </div>

              {/* Finish CTA */}
              <div className="w-full pt-2">
                <PrimaryButton
                  fullWidth
                  onClick={handleFinishOnboarding}
                  icon={<ArrowRight className="w-4 h-4" />}
                >
                  Enter QuantNiti
                </PrimaryButton>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer reassurance */}
      <div className="w-full max-w-[520px] mx-auto px-6 pb-6 text-center">
        <p className="text-xs text-[var(--text-muted)]">
          Your risk persona is advisory and can be updated anytime in the Grow tab.
        </p>
      </div>
    </div>
  );
};
