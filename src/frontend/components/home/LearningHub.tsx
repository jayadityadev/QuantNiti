import React, { useEffect, useState } from "react";
import { BookOpen, CheckCircle, Clock, ChevronRight, Lightbulb, Video, Tag } from "lucide-react";
import { GlassCard, ChipButton, ModalSheet, PrimaryButton } from "../ui";
import { useAppStore } from "../../store/useAppStore";
import { useAbortableRequest } from "../../hooks/useAbortableRequest";

export interface LearningHubProps {
  className?: string;
}

export const LearningHub: React.FC<LearningHubProps> = ({ className = "" }) => {
  const {
    literacyCards,
    setLiteracyCards,
    learnedConcepts,
    toggleLearnedConcept,
    selectedLiteracyCategory,
    setSelectedLiteracyCategory,
  } = useAppStore();

  const [activeConcept, setActiveConcept] = useState<any | null>(null);
  const [activeVideoModal, setActiveVideoModal] = useState<any | null>(null);
  const { request } = useAbortableRequest();

  useEffect(() => {
    if (!literacyCards || literacyCards.length === 0) {
      const fetchCards = async () => {
        try {
          const data = await request<any>("literacy-cards", "/api/v1/literacy/all");
          if (data && Array.isArray(data.cards) && data.cards.length > 0) {
            setLiteracyCards(data.cards);
          }
        } catch {
          // Default initial concept cards
          setLiteracyCards([
            {
              key: "regime-investing",
              title: "Market Regimes 101",
              summary: "How market environments dictate whether momentum or mean-reversion wins.",
              detail: "Market regimes identify shifts in macro volatility, liquidity, and trend persistence. By sizing exposure according to the regime (Bull, Sideways, Bear), you prevent deep drawdowns and capture alpha during expansions.",
              analogy: "Like changing tires on a racecar: soft slicks for dry sunny asphalt, and heavy treads when the monsoon rain drenches the track.",
              category: "strategy",
              read_time_min: 3,
            },
            {
              key: "sharpe-ratio",
              title: "Understanding Sharpe",
              summary: "Learn how excess return per unit of volatility reveals true strategy quality.",
              detail: "The Sharpe Ratio measures the performance of an investment compared to a risk-free asset, after adjusting for its risk. A Sharpe ratio greater than 1.0 is considered good, while over 2.0 is exceptional.",
              analogy: "Like checking fuel efficiency (km/liter) instead of just top speed. A car that travels fast but breaks down every 10 km isn't a winning vehicle.",
              category: "metrics",
              read_time_min: 2,
            },
            {
              key: "esg-scoring",
              title: "ESG Conscience Scoring",
              summary: "Investing aligned with sustainability, corporate governance, and ethics.",
              detail: "Environmental, Social, and Governance (ESG) criteria allow investors to screen for sustainable companies that exhibit resilient long-term governance and minimal regulatory risk.",
              analogy: "Like buying groceries from organic farmers with clean water supplies rather than chemical plants with environmental fines.",
              category: "risk",
              read_time_min: 4,
            },
            {
              key: "drawdown-control",
              title: "Managing Max Drawdown",
              summary: "Why avoiding a -50% loss is far more important than chasing a +50% gain.",
              detail: "If an asset drops 50%, you need a 100% gain just to break even. QuantNiti uses dynamic cash buffers and stop-allocation constraints to protect capital first.",
              analogy: "If you lose half your climbing gear halfway up the mountain, reaching the summit requires twice the remaining effort and energy.",
              category: "risk",
              read_time_min: 3,
            },
          ]);
        }
      };
      fetchCards();
    }
  }, [literacyCards, setLiteracyCards, request]);

  // Derive categories dynamically from available cards
  const dynamicCategories = Array.from(
    new Set((literacyCards || []).map((c: any) => String(c.category || "").toLowerCase()).filter(Boolean))
  );
  const categories = ["all", ...(dynamicCategories.length > 0 ? dynamicCategories : ["basics", "regimes", "risk", "quant"])];

  const filteredCards = (literacyCards || []).filter((card: any) => {
    if (!selectedLiteracyCategory || selectedLiteracyCategory === "all") return true;
    return String(card.category || "").toLowerCase() === selectedLiteracyCategory.toLowerCase();
  });

  const totalCards = literacyCards?.length || 10;
  const completedCount = learnedConcepts?.size || 0;
  const progressPct = Math.min(100, Math.round((completedCount / (totalCards || 1)) * 100));

  return (
    <GlassCard className={`p-5 flex flex-col gap-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-xl bg-accent/10 flex items-center justify-center text-accent">
            <BookOpen className="w-4 h-4 text-accent" />
          </div>
          <div>
            <h3 className="font-extrabold text-sm tracking-tight text-[var(--text-main)]">
              Financial Learning Hub
            </h3>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              Concept Mastery, Real Analogies & Videos
            </span>
          </div>
        </div>

        <div className="text-right">
          <span className="text-xs font-bold font-mono text-accent">
            {completedCount}/{totalCards}
          </span>
          <span className="text-[10px] text-[var(--text-muted)] ml-1">Learned</span>
        </div>
      </div>

      {/* Mastery Progress Bar */}
      <div className="flex flex-col gap-1">
        <div className="h-1.5 w-full rounded-full bg-violet-400/20 dark:bg-violet-500/15 overflow-hidden">
          <div
            style={{ width: `${progressPct}%` }}
            className="h-full rounded-full bg-gradient-to-r from-violet-600 to-indigo-600 transition-all duration-300"
          />
        </div>
        <div className="flex justify-between items-center text-[10px] text-[var(--text-muted)] font-medium">
          <span>{filteredCards.length} modules available</span>
          <span>{progressPct}% Concept Mastery</span>
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
        {categories.map((cat) => (
          <ChipButton
            key={cat}
            selected={(selectedLiteracyCategory || "all").toLowerCase() === cat.toLowerCase()}
            onClick={() => setSelectedLiteracyCategory(cat)}
            className="capitalize whitespace-nowrap text-xs"
          >
            {cat}
          </ChipButton>
        ))}
      </div>

      {/* Carousel */}
      <div className="flex gap-3 overflow-x-auto pb-2 -mx-2 px-2 no-scrollbar snap-x">
        {filteredCards.map((card: any) => {
          const isLearned = learnedConcepts?.has(card.key);
          const hasVideo = Boolean(card.video);
          const excerpt = card.explanation || card.summary || card.detail || "";

          return (
            <div
              key={card.key}
              onClick={() => setActiveConcept(card)}
              className="snap-start shrink-0 w-[240px] p-4 rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] hover:border-violet-500/40 flex flex-col justify-between gap-3 cursor-pointer transition-all duration-150 shadow-sm hover:shadow-md"
            >
              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-accent/10 text-accent">
                    {card.category || "Concept"}
                  </span>
                  <div className="flex items-center gap-1">
                    {hasVideo && (
                      <span className="text-[9px] px-1.5 py-0.5 rounded-md bg-violet-500/10 text-violet-600 dark:text-violet-400 font-semibold flex items-center gap-0.5">
                        <Video className="w-2.5 h-2.5" /> Video
                      </span>
                    )}
                    {isLearned && (
                      <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
                    )}
                  </div>
                </div>

                <h4 className="text-xs font-bold text-[var(--text-main)] line-clamp-1">
                  {card.title}
                </h4>

                <p className="text-[11px] text-[var(--text-muted)] line-clamp-2 leading-relaxed">
                  {excerpt}
                </p>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-[var(--border-subtle)] text-[10px] text-[var(--text-muted)]">
                <div className="flex items-center gap-1 font-mono">
                  <Clock className="w-3 h-3" />
                  <span>{card.read_time_min || 3} min</span>
                </div>
                <div className="flex items-center gap-1 text-accent font-semibold text-[10px]">
                  <span>Explore</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Concept Detail ModalSheet */}
      <ModalSheet
        isOpen={Boolean(activeConcept)}
        onClose={() => setActiveConcept(null)}
        title={activeConcept?.title || "Concept Details"}
      >
        {activeConcept && (
          <div className="flex flex-col gap-4 py-2">
            {/* Badges */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-lg bg-accent/10 text-accent">
                  {activeConcept.category || "Education"}
                </span>
                <span className="text-xs text-[var(--text-muted)] flex items-center gap-1 font-mono">
                  <Clock className="w-3 h-3" />
                  {activeConcept.read_time_min || 3} min read
                </span>
              </div>
              {learnedConcepts.has(activeConcept.key) && (
                <span className="text-xs text-emerald-600 font-semibold flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5" /> Mastered
                </span>
              )}
            </div>

            {/* Core Explanation */}
            <div className="p-3.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)]">
              <span className="text-[10px] font-bold tracking-wider uppercase text-accent mb-1 block">
                Quantitative Concept
              </span>
              <p className="text-sm text-[var(--text-main)] leading-relaxed">
                {activeConcept.explanation || activeConcept.detail || activeConcept.summary}
              </p>
            </div>

            {/* Everyday Analogy */}
            {activeConcept.analogy && (
              <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-900 dark:text-amber-200">
                <div className="flex items-center gap-1.5 font-bold text-xs text-amber-700 dark:text-amber-300 mb-1">
                  <Lightbulb className="w-3.5 h-3.5" />
                  <span>Everyday Relatable Analogy:</span>
                </div>
                <p className="text-xs leading-relaxed italic opacity-95">
                  "{activeConcept.analogy}"
                </p>
              </div>
            )}

            {/* Attached Video Button if present */}
            {activeConcept.video && (
              <div className="p-3 rounded-xl bg-violet-600/10 border border-violet-500/20 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg bg-violet-600 text-white flex items-center justify-center">
                    <Video className="w-4 h-4" />
                  </div>
                  <div>
                    <h5 className="text-xs font-bold text-[var(--text-main)]">
                      {activeConcept.video.video_title || "Watch Explainer"}
                    </h5>
                    <span className="text-[10px] text-[var(--text-muted)] font-mono">
                      {activeConcept.video.video_duration || "2:30"} duration
                    </span>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setActiveVideoModal(activeConcept.video);
                  }}
                  className="px-3 py-1.5 rounded-lg bg-accent text-white text-xs font-semibold hover:bg-accent/90 transition-colors"
                >
                  Play Video
                </button>
              </div>
            )}

            {/* Related concepts */}
            {Array.isArray(activeConcept.related_keys) && activeConcept.related_keys.length > 0 && (
              <div className="flex flex-col gap-1.5">
                <span className="text-[10px] font-bold text-[var(--text-muted)] uppercase tracking-wider flex items-center gap-1">
                  <Tag className="w-3 h-3" /> Related Concepts
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {activeConcept.related_keys.map((k: string) => (
                    <span
                      key={k}
                      className="px-2 py-0.5 rounded-md bg-[var(--bg-card-subtle)] text-[10px] font-mono text-[var(--text-muted)] border border-[var(--border-subtle)]"
                    >
                      #{k}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="pt-2 flex gap-2">
              <PrimaryButton
                fullWidth
                onClick={() => {
                  toggleLearnedConcept(activeConcept.key);
                  setActiveConcept(null);
                }}
              >
                {learnedConcepts.has(activeConcept.key)
                  ? "Mark as Incomplete"
                  : "Mark as Learned ✓"}
              </PrimaryButton>
            </div>
          </div>
        )}
      </ModalSheet>

      {/* Video Modal if clicked from concept card */}
      <ModalSheet
        isOpen={Boolean(activeVideoModal)}
        onClose={() => setActiveVideoModal(null)}
        title={activeVideoModal?.video_title || "Concept Video Explainer"}
      >
        {activeVideoModal && (
          <div className="flex flex-col gap-3 py-2">
            <div className="relative w-full aspect-video rounded-2xl overflow-hidden bg-black shadow-xl">
              <iframe
                title={activeVideoModal.video_title}
                src={`https://www.youtube-nocookie.com/embed/5k3f_eU1j3Q?autoplay=1&rel=0`}
                className="w-full h-full border-0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              Video Explainer covering {activeVideoModal.video_title}. Duration: {activeVideoModal.video_duration}.
            </p>
            <PrimaryButton fullWidth onClick={() => setActiveVideoModal(null)}>
              Close Video
            </PrimaryButton>
          </div>
        )}
      </ModalSheet>
    </GlassCard>
  );
};
