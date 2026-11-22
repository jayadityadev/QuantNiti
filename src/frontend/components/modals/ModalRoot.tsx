import React, { useEffect } from "react";
import { Bot } from "lucide-react";
import { useAppStore } from "../../store/useAppStore";
import { NitiBotModal } from "./NitiBotModal";
import { NotificationDrawer } from "./NotificationDrawer";
import { WriteReviewModal } from "./WriteReviewModal";
import { ConceptDetailModal } from "./ConceptDetailModal";
import { CompetitorBenchmarkModal } from "./CompetitorBenchmarkModal";
import { OrderSheetModal } from "./OrderSheetModal";
import { getDemoPortfolio } from "../portfolio/demoPortfolioData";

const PortfolioReportCard = React.lazy(() =>
  import("./PortfolioReportCard").then((mod) => ({
    default: mod.PortfolioReportCard,
  }))
);

export const ModalRoot: React.FC = () => {
  const {
    activeModal,
    modalPayload,
    closeModal,
    openModal,
    activePortfolio,
    portfolios,
    setActiveTab,
  } = useAppStore();

  // Android back gesture (popstate) closes topmost open modal
  useEffect(() => {
    const handlePopState = () => {
      if (activeModal) {
        closeModal();
      }
    };

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, [activeModal, closeModal]);

  const currentPortfolio =
    activePortfolio || (portfolios.length > 0 ? portfolios[0] : getDemoPortfolio());

  return (
    <>
      {/* 1. NitiBot AI Assistant Modal */}
      <NitiBotModal
        isOpen={activeModal === "nitibot"}
        onClose={closeModal}
      />

      {/* 2. Smart Notification Drawer */}
      <NotificationDrawer
        isOpen={activeModal === "notifications"}
        onClose={closeModal}
      />

      {/* 3. Write Verified Review Modal */}
      <WriteReviewModal
        isOpen={activeModal === "review"}
        onClose={closeModal}
        targetType={modalPayload?.targetType}
        targetId={modalPayload?.targetId}
        onSuccess={modalPayload?.onSuccess}
      />

      {/* 4. Financial Literacy Concept Detail Modal */}
      <ConceptDetailModal
        isOpen={activeModal === "concept"}
        onClose={closeModal}
        concept={modalPayload?.concept}
      />

      {/* 5. Competitor Benchmark Modal */}
      <CompetitorBenchmarkModal
        isOpen={activeModal === "competitors"}
        onClose={closeModal}
        onNavigateToGrow={() => setActiveTab("grow")}
      />

      {/* 6. 1-Click Broker Order Sheet Modal */}
      <OrderSheetModal
        isOpen={activeModal === "orderSheet"}
        onClose={closeModal}
        portfolio={modalPayload?.portfolio || currentPortfolio}
      />

      {/* 7. Portfolio Audit Report Card */}
      <React.Suspense fallback={null}>
        <PortfolioReportCard
          isOpen={activeModal === "reportCard"}
          onClose={closeModal}
          portfolio={modalPayload?.portfolio || currentPortfolio}
        />
      </React.Suspense>

      {/* 8. Floating NitiBot FAB button (Persistent on desktop & mobile above bottom nav) */}
      <div className="fixed bottom-24 right-4 sm:right-6 z-40">
        <button
          type="button"
          onClick={() => openModal("nitibot")}
          aria-label="Ask NitiBot AI"
          title="Ask NitiBot AI"
          className="group relative flex items-center justify-center w-12 h-12 rounded-xl bg-slate-900 text-white dark:bg-teal-600 shadow-md hover:scale-105 active:scale-95 transition-transform duration-150 border border-slate-700 dark:border-teal-500 focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none"
        >
          <Bot className="w-5 h-5 transition-transform group-hover:rotate-6" />
          <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-emerald-500 border-2 border-[var(--bg-primary)]" />
        </button>
      </div>
    </>
  );
};
