import React, { useState, useEffect } from "react";
import { Star, ShieldCheck, Check, AlertTriangle } from "lucide-react";
import { ModalSheet } from "../ui/ModalSheet";
import { PrimaryButton } from "../ui/PrimaryButton";
import { useAbortableRequest } from "../../hooks/useAbortableRequest";
import { apiUrl } from "../../config";

export interface WriteReviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  targetType?: "stock" | "basket" | "portfolio" | "strategy" | "platform";
  targetId?: string;
  onSuccess?: () => void;
}

export const WriteReviewModal: React.FC<WriteReviewModalProps> = ({
  isOpen,
  onClose,
  targetType = "stock",
  targetId = "RELIANCE",
  onSuccess,
}) => {
  const { request, isLoading } = useAbortableRequest();
  const [rating, setRating] = useState(5);
  const [hoverRating, setHoverRating] = useState(0);
  const [authorName, setAuthorName] = useState("");
  const [title, setTitle] = useState("");
  const [claimedReturn, setClaimedReturn] = useState("+12.4%");
  const [comment, setComment] = useState("");
  const [auditBadge, setAuditBadge] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setAuditBadge(null);
      setErrorMessage(null);
      setIsSuccess(false);
    }
  }, [isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!comment.trim() || !authorName.trim() || !title.trim()) return;

    setErrorMessage(null);
    setAuditBadge(null);

    const cleanNum = claimedReturn.replace(/[^0-9.-]/g, "");
    const parsedClaim = cleanNum ? parseFloat(cleanNum) : null;

    const payload = {
      target_type: targetType,
      target_id: targetId,
      user_name: authorName.trim(),
      rating,
      title: title.trim(),
      review_text: comment.trim(),
      claimed_return_pct: isNaN(parsedClaim as number) ? null : parsedClaim,
      claimed_duration: "6M",
    };

    try {
      const response = await request("submit-review", apiUrl("/api/v1/reviews/submit"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (response) {
        if (response.is_approved) {
          setAuditBadge(response.verification_badge || response.audit_summary || "AI Fact-Checked & Verified");
          setIsSuccess(true);
          setTimeout(() => {
            onSuccess?.();
            onClose();
          }, 1400);
        } else {
          setErrorMessage(
            response.rejection_reason ||
            response.audit_details?.audit_notes ||
            "Review rejected by AI Fact-Checking Agent."
          );
        }
      }
    } catch (err: any) {
      setErrorMessage(err?.message || "Failed to submit review for AI verification.");
    }
  };

  return (
    <ModalSheet
      isOpen={isOpen}
      onClose={onClose}
      title={
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-violet-600/20 border border-violet-500/30 flex items-center justify-center text-violet-400">
            <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
          </div>
          <div>
            <h3 className="font-bold text-[var(--text-main)] text-base">Write a Verified Review</h3>
            <p className="text-[11px] text-[var(--text-muted)]">
              Auditing {targetType.toUpperCase()}: <span className="font-mono text-accent">{targetId}</span>
            </p>
          </div>
        </div>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4 pt-1">
        {/* Rating Stars */}
        <div className="space-y-1.5 text-center p-3 rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)]">
          <span className="text-xs text-[var(--text-muted)] font-medium block">Overall Rating</span>
          <div className="flex items-center justify-center gap-1.5 pt-1">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                aria-label={`Rate ${star} star`}
                onClick={() => setRating(star)}
                onMouseEnter={() => setHoverRating(star)}
                onMouseLeave={() => setHoverRating(0)}
                className="p-1 text-slate-300 dark:text-slate-600 hover:scale-110 transition-transform"
              >
                <Star
                  className={`w-6 h-6 ${
                    (hoverRating || rating) >= star
                      ? "fill-amber-400 text-amber-400"
                      : "text-slate-300 dark:text-slate-600"
                  }`}
                />
              </button>
            ))}
          </div>
        </div>

        {/* Author Name */}
        <div className="space-y-1">
          <label className="text-xs font-semibold text-[var(--text-main)]">Your Name / Handle</label>
          <input
            type="text"
            value={authorName}
            onChange={(e) => setAuthorName(e.target.value)}
            placeholder="e.g. Arun M., Investor"
            required
            className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] text-[var(--text-main)] placeholder:text-[var(--text-muted)] text-xs focus:outline-none focus:border-accent transition-colors shadow-sm"
          />
        </div>

        {/* Review Title & Claimed Return */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="space-y-1">
            <label className="text-xs font-semibold text-[var(--text-main)]">Headline</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Great long-term compounder"
              required
              className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] text-[var(--text-main)] placeholder:text-[var(--text-muted)] text-xs focus:outline-none focus:border-accent transition-colors shadow-sm"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-[var(--text-main)]">Claimed 6M Return %</label>
            <input
              type="text"
              value={claimedReturn}
              onChange={(e) => setClaimedReturn(e.target.value)}
              placeholder="e.g. +12.4%"
              className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] text-[var(--text-main)] placeholder:text-[var(--text-muted)] text-xs focus:outline-none focus:border-accent transition-colors shadow-sm"
            />
          </div>
        </div>

        {/* Comment Text Area */}
        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-[var(--text-main)]">Your Experience</label>
            <span className="text-[10px] text-[var(--text-muted)]">{comment.length} / 500</span>
          </div>
          <textarea
            rows={3}
            value={comment}
            onChange={(e) => setComment(e.target.value.slice(0, 500))}
            placeholder="Describe investment discipline, regime suitability, or price behavior..."
            required
            className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] text-[var(--text-main)] placeholder:text-[var(--text-muted)] text-xs focus:outline-none focus:border-accent transition-colors resize-none shadow-sm"
          />
        </div>

        {/* AI Fact-Checking Badge preview */}
        <div className="p-3 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-start gap-2.5">
          <ShieldCheck className="w-4 h-4 text-teal-600 dark:text-teal-400 shrink-0 mt-0.5" />
          <div className="text-[11px] text-teal-800 dark:text-teal-200/90 leading-relaxed">
            <span className="font-bold text-teal-700 dark:text-teal-300 block">3-Tier AI Fact-Checking Active</span>
            Reviews are audited against historical price data (±3% tolerance) to prevent fraudulent claims and ensure SEBI advertisement compliance.
          </div>
        </div>

        {errorMessage && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-600 dark:text-rose-400 text-xs flex items-start gap-2.5 animate-in fade-in">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold block">AI Verification Rejection</span>
              <p className="mt-0.5 leading-relaxed">{errorMessage}</p>
            </div>
          </div>
        )}

        {auditBadge && isSuccess && (
          <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 text-xs flex items-start gap-2.5 animate-in fade-in">
            <Check className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold block">AI Audit Passed & Published!</span>
              <p className="mt-0.5 font-mono text-[11px]">{auditBadge}</p>
            </div>
          </div>
        )}

        {/* Submit */}
        <div className="pt-2">
          <PrimaryButton
            type="submit"
            fullWidth
            disabled={isLoading || isSuccess || !comment.trim()}
          >
            {isLoading ? "Auditing with AI..." : isSuccess ? "Review Verified & Published!" : "Submit for AI Verification"}
          </PrimaryButton>
        </div>
      </form>
    </ModalSheet>
  );
};
