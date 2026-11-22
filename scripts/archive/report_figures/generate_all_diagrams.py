"""
Generate publication-quality diagrams for the QuantNiti Academic Project Report.
Outputs 300 DPI PNGs and vector PDFs for:
- Fig 2.1: Literature Survey Methodology Pipeline
- Fig 4.2: UML Use Case Diagram
- Fig 4.3: UML Sequence Diagram - Portfolio Generation Workflow
- Fig 4.4: UML Sequence Diagram - Smart Alert & Rebalance Loop
- Fig 4.5: UML Sequence Diagram - 3-Tier Review Fact-Checking
- Fig 4.6: UML Activity Diagram - End-to-End User Experience
- Fig 4.7: UML Class & Module Hierarchy Diagram
- Fig 4.8a: DFD Level 0 Context Diagram
- Fig 4.8b: DFD Level 1 System Decomposition Diagram
- Fig 4.9: Database Entity-Relationship (ER) Schema
- Fig 4.10: Cloud & Native Android Deployment Topology Diagram
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIRS = [
    "docs/academic_docs/figures",
    "docs/academic_docs/report_latex/figures"
]

for d in OUTPUT_DIRS:
    os.makedirs(d, exist_ok=True)

# Color Palette (IEEE Modern Crisp)
NAVY_DARK = "#0F172A"
BLUE_BG, BLUE_BORDER = "#EFF6FF", "#2563EB"
EMERALD_BG, EMERALD_BORDER = "#ECFDF5", "#059669"
AMBER_BG, AMBER_BORDER = "#FFFBEB", "#D97706"
ROSE_BG, ROSE_BORDER = "#FFF1F2", "#E11D48"
PURPLE_BG, PURPLE_BORDER = "#FAF5FF", "#7C3AED"
SLATE_BG, SLATE_BORDER = "#F8FAFC", "#475569"


def save_fig(fig, base_name):
    for d in OUTPUT_DIRS:
        png_path = os.path.join(d, f"{base_name}.png")
        pdf_path = os.path.join(d, f"{base_name}.pdf")
        fig.savefig(png_path, dpi=300, bbox_inches='tight')
        fig.savefig(pdf_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {base_name}.png and .pdf")


# -------------------------------------------------------------
# 1. Fig 2.1: Literature Survey Methodology Pipeline
# -------------------------------------------------------------
def make_fig_2_1():
    fig, ax = plt.subplots(figsize=(11, 4.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.5)

    stages = [
        ("Phase 1: Identification", "Problem Formulation",
         ["• Retail demat boom & losses", "• Markowitz error maximization", "• Continuous vs integer shares"],
         BLUE_BG, BLUE_BORDER),
        ("Phase 2: Database Ingestion", "Multi-Source Extraction",
         ["• IEEE Xplore, ACM Digital Lib", "• ScienceDirect, SSRN, arXiv", "• SEBI & NCFE official studies"],
         EMERALD_BG, EMERALD_BORDER),
        ("Phase 3: PRISMA Screening", "Inclusion & Exclusion",
         ["• Filtered 65+ down to 12", "• Retained Indian equity relevance", "• Audited lookahead & backtests"],
         AMBER_BG, AMBER_BORDER),
        ("Phase 4: Synthesis", "Thematic Taxonomies",
         ["• Regime-switching models (GMM/HMM)", "• Inversion-free HRP optimization", "• 4-pillar XAI Trust Architecture"],
         PURPLE_BG, PURPLE_BORDER)
    ]

    card_w, card_h = 2.4, 3.8
    y_card = 0.35

    for i, (title_h, sub_h, bullets, bg, border) in enumerate(stages):
        x = 0.3 + i * 2.65
        card = patches.FancyBboxPatch((x, y_card), card_w, card_h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                      facecolor=bg, edgecolor=border, linewidth=1.5, zorder=2)
        ax.add_patch(card)

        # Header bar
        header = patches.FancyBboxPatch((x, y_card + card_h - 0.7), card_w, 0.7,
                                        boxstyle="round,pad=0.02,rounding_size=0.08",
                                        facecolor=border, edgecolor=border, zorder=3)
        ax.add_patch(header)
        sq = patches.Rectangle((x, y_card + card_h - 0.7), card_w, 0.2, facecolor=border, edgecolor=border, zorder=3)
        ax.add_patch(sq)

        ax.text(x + card_w/2, y_card + card_h - 0.25, title_h, ha='center', va='center',
                fontsize=8, fontweight='bold', color="#FFFFFF")
        ax.text(x + card_w/2, y_card + card_h - 0.52, sub_h, ha='center', va='center',
                fontsize=7.5, color="#FFFFFF")

        # Bullets
        y_text = y_card + card_h - 1.05
        for b in bullets:
            ax.text(x + 0.12, y_text, b, ha='left', va='top', fontsize=7, color=NAVY_DARK, wrap=True)
            y_text -= 0.75

        # Arrow to next
        if i < len(stages) - 1:
            ax.annotate('', xy=(x + card_w + 0.22, y_card + card_h/2),
                        xytext=(x + card_w + 0.03, y_card + card_h/2),
                        arrowprops=dict(facecolor=SLATE_BORDER, edgecolor=SLATE_BORDER, width=2, headwidth=6),
                        zorder=5)

    save_fig(fig, "fig2_1_literature_pipeline")


# -------------------------------------------------------------
# 2. Fig 4.2: UML Use Case Diagram
# -------------------------------------------------------------
def make_fig_4_2():
    fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.2)

    # System boundary box
    sys_box = patches.FancyBboxPatch((2.2, 0.4), 6.6, 6.4, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor="#FFFFFF", edgecolor=SLATE_BORDER, linewidth=1.8, linestyle="--", zorder=1)
    ax.add_patch(sys_box)
    ax.text(5.5, 6.55, "QuantNiti System Boundary", ha='center', va='center',
            fontsize=12, fontweight='bold', color=NAVY_DARK)

    # Actors
    def draw_actor(x, y, label):
        # Head
        ax.add_patch(patches.Circle((x, y), 0.16, facecolor="#FFFFFF", edgecolor=BLUE_BORDER, linewidth=1.5, zorder=4))
        # Body
        ax.plot([x, x], [y - 0.16, y - 0.52], color=BLUE_BORDER, linewidth=1.5, zorder=4)
        # Arms
        ax.plot([x - 0.22, x + 0.22], [y - 0.3, y - 0.3], color=BLUE_BORDER, linewidth=1.5, zorder=4)
        # Legs
        ax.plot([x, x - 0.18], [y - 0.52, y - 0.85], color=BLUE_BORDER, linewidth=1.5, zorder=4)
        ax.plot([x, x + 0.18], [y - 0.52, y - 0.85], color=BLUE_BORDER, linewidth=1.5, zorder=4)
        ax.text(x, y - 1.05, label, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY_DARK)

    draw_actor(1.1, 5.2, "Retail Investor")
    draw_actor(1.1, 2.3, "Novice Learner")
    draw_actor(9.9, 5.2, "NitiBot Assistant")
    draw_actor(9.9, 2.3, "Daemon Evaluator")

    # Use cases
    use_cases = [
        (5.5, 5.9, "UC1: Behavioral Risk Assessment & Persona Deduction"),
        (5.5, 5.1, "UC2: Live Market Regime Radar & Feature Telemetry"),
        (5.5, 4.3, "UC3: Generate Regime-Adaptive HRP Basket & Shares"),
        (5.5, 3.5, "UC4: Review 4-Pillar Explainable Trust Card"),
        (5.5, 2.7, "UC5: Track Real-Time MTM Virtual Paper Portfolio"),
        (5.5, 1.9, "UC6: Conversational Grounded RAG Inquiries"),
        (5.5, 1.1, "UC7: Submit & Verify SEBI-Compliant Review"),
    ]

    for (cx, cy, label) in use_cases:
        ellipse = patches.FancyBboxPatch((cx - 2.8, cy - 0.3), 5.6, 0.6,
                                         boxstyle="round,pad=0.02,rounding_size=0.3",
                                         facecolor=BLUE_BG, edgecolor=BLUE_BORDER, linewidth=1.2, zorder=3)
        ax.add_patch(ellipse)
        ax.text(cx, cy, label, ha='center', va='center', fontsize=7.8, fontweight='bold', color=NAVY_DARK, zorder=4)

    # Actor association lines
    connections = [
        # Investor
        ((1.3, 5.0), (2.7, 5.9)),
        ((1.3, 5.0), (2.7, 5.1)),
        ((1.3, 5.0), (2.7, 4.3)),
        ((1.3, 5.0), (2.7, 3.5)),
        ((1.3, 5.0), (2.7, 2.7)),
        ((1.3, 5.0), (2.7, 1.1)),
        # Learner
        ((1.3, 2.2), (2.7, 5.9)),
        ((1.3, 2.2), (2.7, 3.5)),
        ((1.3, 2.2), (2.7, 1.9)),
        # NitiBot
        ((9.7, 5.0), (8.3, 1.9)),
        ((9.7, 5.0), (8.3, 3.5)),
        # Daemon
        ((9.7, 2.2), (8.3, 5.1)),
        ((9.7, 2.2), (8.3, 2.7)),
        ((9.7, 2.2), (8.3, 1.1)),
    ]

    for (p1, p2) in connections:
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#94A3B8", linewidth=1.0, linestyle="-", zorder=2)

    save_fig(fig, "fig4_2_use_case_diagram")


# -------------------------------------------------------------
# 3. Fig 4.3: UML Sequence Diagram - Portfolio Generation Workflow
# -------------------------------------------------------------
def make_fig_4_3():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)

    lifelines = [
        ("User / PWA", 1.2),
        ("FastAPI Gateway", 3.2),
        ("Regime Classifier", 5.2),
        ("HRP Optimizer", 7.2),
        ("Discrete Allocator", 9.2),
    ]

    # Draw lifelines
    for label, x in lifelines:
        box = patches.FancyBboxPatch((x - 0.9, 6.7), 1.8, 0.55, boxstyle="round,pad=0.02,rounding_size=0.08",
                                     facecolor=BLUE_BG, edgecolor=BLUE_BORDER, linewidth=1.5, zorder=3)
        ax.add_patch(box)
        ax.text(x, 6.97, label, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY_DARK)
        ax.plot([x, x], [0.6, 6.7], color="#94A3B8", linewidth=1.0, linestyle="--", zorder=1)

    # Sequence messages
    msgs = [
        (1.2, 3.2, 6.2, "1: POST /api/v1/grow/recommend (Capital, Horizon, Persona)", False),
        (3.2, 5.2, 5.5, "2: get_active_regime(historical_window)", False),
        (5.2, 3.2, 4.8, "3: Return π_t = [π_Bull, π_Bear, π_Flat]", True),
        (3.2, 7.2, 4.1, "4: solve_hrp(returns_df, π_t, persona_bounds)", False),
        (7.2, 7.2, 3.4, "5: compute_shrunk_covariance() & bisection", "self"),
        (7.2, 9.2, 2.7, "6: Target continuous weights w* ∈ [0, 1]^N", False),
        (9.2, 9.2, 2.0, "7: greedy_knapsack(C, P_i, w*) -> n_i ∈ Z+", "self"),
        (9.2, 3.2, 1.4, "8: Return discrete shares n_i & 4-Pillar Trust Card", True),
        (3.2, 1.2, 0.8, "9: Render Order Sheet modal & uncertainty cone", True),
    ]

    for (x1, x2, y, text, is_return) in msgs:
        if is_return == "self":
            # Self call loop
            ax.annotate('', xy=(x1 + 0.05, y - 0.25), xytext=(x1 + 0.05, y),
                        arrowprops=dict(facecolor=AMBER_BORDER, edgecolor=AMBER_BORDER, width=1.2, headwidth=4.5), zorder=4)
            ax.plot([x1 + 0.05, x1 + 0.6, x1 + 0.6, x1 + 0.05], [y, y, y - 0.25, y - 0.25],
                    color=AMBER_BORDER, linewidth=1.2, zorder=3)
            ax.text(x1 + 0.7, y - 0.12, text, ha='left', va='center', fontsize=7.2, color=NAVY_DARK)
        else:
            style = "--" if is_return else "-"
            col = EMERALD_BORDER if is_return else BLUE_BORDER
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(facecolor=col, edgecolor=col, width=1.2, headwidth=4.5, linestyle=style), zorder=4)
            mid_x = (x1 + x2) / 2
            ax.text(mid_x, y + 0.15, text, ha='center', va='bottom', fontsize=7.2, color=NAVY_DARK,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=0.5))

    save_fig(fig, "fig4_3_sequence_portfolio_generation")


# -------------------------------------------------------------
# 4. Fig 4.4: UML Sequence Diagram - Smart Alert & Rebalance Loop
# -------------------------------------------------------------
def make_fig_4_4():
    fig, ax = plt.subplots(figsize=(11, 7.0), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.0)

    lifelines = [
        ("Market Tick Stream", 1.2),
        ("Alert Evaluator", 3.7),
        ("Portfolio Storage", 6.2),
        ("Notification Dispatcher", 8.7),
        ("User Client (PWA)", 10.2)
    ]

    for label, x in lifelines:
        box = patches.FancyBboxPatch((x - 0.8, 6.2), 1.6, 0.55, boxstyle="round,pad=0.02,rounding_size=0.08",
                                     facecolor=AMBER_BG, edgecolor=AMBER_BORDER, linewidth=1.5, zorder=3)
        ax.add_patch(box)
        ax.text(x, 6.47, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color=NAVY_DARK)
        ax.plot([x, x], [0.6, 6.2], color="#94A3B8", linewidth=1.0, linestyle="--", zorder=1)

    msgs = [
        (1.2, 3.7, 5.6, "1: Ingest tick P_{t} & update rolling indicators", False),
        (3.7, 6.2, 4.9, "2: Query active virtual portfolios & positions", False),
        (6.2, 3.7, 4.3, "3: Return portfolio baseline & target weights", True),
        (3.7, 3.7, 3.6, "4: Evaluate 6 Triggers (Regime, SL, TP, Drift, Vol, ESG)", "self"),
        (3.7, 8.7, 2.8, "5: Trigger fired: Regime Shift / Drift > 5%", False),
        (8.7, 10.2, 2.0, "6: Dispatch in-app notification & browser Web Push", False),
        (10.2, 3.7, 1.2, "7: User requests regime-shift rebalance preview", False),
        (3.7, 10.2, 0.7, "8: Return before/after share delta diff", True),
    ]

    for (x1, x2, y, text, is_return) in msgs:
        if is_return == "self":
            ax.annotate('', xy=(x1 + 0.05, y - 0.25), xytext=(x1 + 0.05, y),
                        arrowprops=dict(facecolor=ROSE_BORDER, edgecolor=ROSE_BORDER, width=1.2, headwidth=4.5), zorder=4)
            ax.plot([x1 + 0.05, x1 + 0.6, x1 + 0.6, x1 + 0.05], [y, y, y - 0.25, y - 0.25],
                    color=ROSE_BORDER, linewidth=1.2, zorder=3)
            ax.text(x1 + 0.7, y - 0.12, text, ha='left', va='center', fontsize=7.2, color=NAVY_DARK)
        else:
            style = "--" if is_return else "-"
            col = EMERALD_BORDER if is_return else BLUE_BORDER
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(facecolor=col, edgecolor=col, width=1.2, headwidth=4.5, linestyle=style), zorder=4)
            mid_x = (x1 + x2) / 2
            ax.text(mid_x, y + 0.15, text, ha='center', va='bottom', fontsize=7.2, color=NAVY_DARK,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=0.5))

    save_fig(fig, "fig4_4_sequence_smart_alert")


# -------------------------------------------------------------
# 5. Fig 4.5: UML Sequence Diagram - 3-Tier Fact-Checking Review
# -------------------------------------------------------------
def make_fig_4_5():
    fig, ax = plt.subplots(figsize=(11, 7.0), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.0)

    lifelines = [
        ("Review Author", 1.2),
        ("Review Service", 3.4),
        ("Tier 1 Regex Filter", 5.6),
        ("Tier 2 Math FactChecker", 7.8),
        ("Tier 3 Gemini LLM", 9.8),
    ]

    for label, x in lifelines:
        box = patches.FancyBboxPatch((x - 0.85, 6.2), 1.7, 0.55, boxstyle="round,pad=0.02,rounding_size=0.08",
                                     facecolor=PURPLE_BG, edgecolor=PURPLE_BORDER, linewidth=1.5, zorder=3)
        ax.add_patch(box)
        ax.text(x, 6.47, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color=NAVY_DARK)
        ax.plot([x, x], [0.6, 6.2], color="#94A3B8", linewidth=1.0, linestyle="--", zorder=1)

    msgs = [
        (1.2, 3.4, 5.6, "1: POST /api/v1/reviews (Text, Symbol, ClaimedReturn)", False),
        (3.4, 5.6, 4.9, "2: check_heuristics(spam, phone, telegram, guarantees)", False),
        (5.6, 3.4, 4.3, "3: Tier 1 Passed (No deceptive spam)", True),
        (3.4, 7.8, 3.6, "4: verify_return(Symbol, Period, ClaimedReturn)", False),
        (7.8, 3.4, 2.9, "5: |Claim - Actual| = 1.4% <= 3% (Verified)", True),
        (3.4, 9.8, 2.2, "6: audit_solicitation_and_sentiment(ReviewText)", False),
        (9.8, 3.4, 1.5, "7: Regulatory Compliance Approved (No solicitation)", True),
        (3.4, 1.2, 0.8, "8: Publish review with SEBI Verified Badge", True),
    ]

    for (x1, x2, y, text, is_return) in msgs:
        style = "--" if is_return else "-"
        col = EMERALD_BORDER if is_return else BLUE_BORDER
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(facecolor=col, edgecolor=col, width=1.2, headwidth=4.5, linestyle=style), zorder=4)
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 0.15, text, ha='center', va='bottom', fontsize=7.2, color=NAVY_DARK,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=0.5))

    save_fig(fig, "fig4_5_sequence_review_factchecking")


# -------------------------------------------------------------
# 6. Fig 4.6: UML Activity Diagram - End-to-End User Experience
# -------------------------------------------------------------
def make_fig_4_6():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)

    # 3 Swimlanes
    lanes = [
        ("Investor (Client Layer)", 0.2, 3.6, BLUE_BG),
        ("Application Gateway (FastAPI)", 3.8, 7.2, EMERALD_BG),
        ("Quantitative ML Engines", 7.4, 10.8, PURPLE_BG)
    ]

    for title, x1, x2, bg in lanes:
        w = x2 - x1
        rect = patches.Rectangle((x1, 0.4), w, 6.7, facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2, zorder=1)
        ax.add_patch(rect)
        hdr = patches.Rectangle((x1, 6.6), w, 0.5, facecolor=bg, edgecolor="#CBD5E1", linewidth=1.2, zorder=2)
        ax.add_patch(hdr)
        ax.text((x1 + x2)/2, 6.85, title, ha='center', va='center', fontsize=9, fontweight='bold', color=NAVY_DARK)

    # Nodes
    # Start
    ax.add_patch(patches.Circle((1.9, 6.1), 0.18, facecolor=NAVY_DARK, edgecolor=NAVY_DARK, zorder=3))
    ax.text(1.9, 6.4, "Start", ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY_DARK)

    def draw_action(x, y, text, w=2.8, h=0.6, bg=BLUE_BG, border=BLUE_BORDER):
        patch = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02,rounding_size=0.15",
                                      facecolor=bg, edgecolor=border, linewidth=1.2, zorder=3)
        ax.add_patch(patch)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.2, fontweight='bold', color=NAVY_DARK, zorder=4)

    draw_action(1.9, 5.2, "Complete 3-Q Scenario Quiz")
    draw_action(1.9, 4.2, "Input Capital (e.g. ₹50,000)")
    draw_action(5.5, 4.2, "Request Regime-Aware Allocation", bg=EMERALD_BG, border=EMERALD_BORDER)
    draw_action(9.1, 4.2, "Classify Macro Regime (GMM)", bg=PURPLE_BG, border=PURPLE_BORDER)
    draw_action(9.1, 3.2, "HRP Covariance Shrinkage & Bisection", bg=PURPLE_BG, border=PURPLE_BORDER)
    draw_action(9.1, 2.2, "Quantile Forecast & Discrete Sizing", bg=PURPLE_BG, border=PURPLE_BORDER)
    draw_action(5.5, 2.2, "Synthesize 4-Pillar Trust Card", bg=EMERALD_BG, border=EMERALD_BORDER)
    draw_action(1.9, 2.2, "Inspect Allocation & Trust Card")
    draw_action(1.9, 1.2, "Execute Virtual Paper Portfolio")

    # Final node
    ax.add_patch(patches.Circle((1.9, 0.6), 0.18, facecolor="#FFFFFF", edgecolor=NAVY_DARK, linewidth=1.5, zorder=3))
    ax.add_patch(patches.Circle((1.9, 0.6), 0.12, facecolor=NAVY_DARK, edgecolor=NAVY_DARK, zorder=4))

    # Activity flow arrows
    flows = [
        ((1.9, 5.92), (1.9, 5.5)),
        ((1.9, 4.9), (1.9, 4.5)),
        ((3.3, 4.2), (4.1, 4.2)),
        ((6.9, 4.2), (7.7, 4.2)),
        ((9.1, 3.9), (9.1, 3.5)),
        ((9.1, 2.9), (9.1, 2.5)),
        ((7.7, 2.2), (6.9, 2.2)),
        ((4.1, 2.2), (3.3, 2.2)),
        ((1.9, 1.9), (1.9, 1.5)),
        ((1.9, 0.9), (1.9, 0.78)),
    ]

    for (p1, p2) in flows:
        ax.annotate('', xy=p2, xytext=p1,
                    arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1.2, headwidth=4), zorder=5)

    save_fig(fig, "fig4_6_activity_user_workflow")


# -------------------------------------------------------------
# 7. Fig 4.7: UML Class & Module Hierarchy Diagram
# -------------------------------------------------------------
def make_fig_4_7():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)

    classes = [
        ("MarketRegimeClassifier", 2.2, 5.8,
         ["- n_components: int = 3", "- gmm: GaussianMixture", "- scaler: StandardScaler"],
         ["+ fit_predict(df) -> Tuple", "+ get_active_regime() -> Dict", "+ predict_proba(X) -> np.ndarray"],
         BLUE_BG, BLUE_BORDER),
        ("HierarchicalRiskParityOptimizer", 5.5, 5.8,
         ["- returns_df: DataFrame", "- use_shrinkage: bool = True"],
         ["+ compute_shrunk_cov() -> Tuple", "+ tree_clustering() -> Linkage", "+ recursive_bisection() -> Series"],
         EMERALD_BG, EMERALD_BORDER),
        ("QuantileForecaster", 8.8, 5.8,
         ["- horizons: List[int]", "- factor_model: FactorRanker"],
         ["+ pinball_loss(y, y_hat, tau)", "+ forecast_quantiles(series)", "+ enforce_monotonicity()"],
         AMBER_BG, AMBER_BORDER),
        ("DiscreteAllocator", 2.2, 2.2,
         ["- cash_buffer_pct: float = 0.02", "- max_concentration: float"],
         ["+ allocate_shares(weights, prices, C)", "+ compute_residual_cash() -> float"],
         PURPLE_BG, PURPLE_BORDER),
        ("SmartAlertEvaluator", 5.5, 2.2,
         ["- evaluators: List[RuleEvaluator]", "- notification_repo: Repo"],
         ["+ evaluate_all(context) -> List[Alert]", "+ check_regime_shift() -> Optional", "+ check_drawdown_limit()"],
         ROSE_BG, ROSE_BORDER),
        ("ReviewVerificationAgent", 8.8, 2.2,
         ["- tier1_filter: RegexFilter", "- tier2_math: MarketReturnVerifier", "- tier3_llm: GeminiAuditor"],
         ["+ verify_review(text, claimed_return)", "+ audit_sebi_compliance() -> Result"],
         SLATE_BG, SLATE_BORDER),
    ]

    card_w, card_h = 2.8, 2.6

    for name, cx, cy, attrs, methods, bg, border in classes:
        x = cx - card_w/2
        y = cy - card_h/2
        card = patches.FancyBboxPatch((x, y), card_w, card_h, boxstyle="round,pad=0.02,rounding_size=0.05",
                                      facecolor="#FFFFFF", edgecolor=border, linewidth=1.5, zorder=2)
        ax.add_patch(card)

        # Title bar
        hdr = patches.Rectangle((x, y + card_h - 0.45), card_w, 0.45, facecolor=bg, edgecolor=border, linewidth=1.0, zorder=3)
        ax.add_patch(hdr)
        ax.text(cx, y + card_h - 0.22, name, ha='center', va='center', fontsize=7.8, fontweight='bold', color=NAVY_DARK)

        # Divider lines
        ax.plot([x, x + card_w], [y + card_h - 1.25, y + card_h - 1.25], color="#CBD5E1", linewidth=0.8, zorder=3)

        # Attributes
        ya = y + card_h - 0.65
        for a in attrs:
            ax.text(x + 0.1, ya, a, ha='left', va='center', fontsize=6.5, color=NAVY_DARK)
            ya -= 0.26

        # Methods
        ym = y + card_h - 1.45
        for m in methods:
            ax.text(x + 0.1, ym, m, ha='left', va='center', fontsize=6.5, color=NAVY_DARK)
            ym -= 0.26

    # Connector arrows
    ax.annotate('', xy=(4.1, 5.8), xytext=(3.6, 5.8),
                arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1, headwidth=4), zorder=5)
    ax.annotate('', xy=(7.4, 5.8), xytext=(6.9, 5.8),
                arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1, headwidth=4), zorder=5)
    ax.annotate('', xy=(2.2, 3.5), xytext=(2.2, 4.5),
                arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1, headwidth=4), zorder=5)
    ax.annotate('', xy=(5.5, 3.5), xytext=(5.5, 4.5),
                arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1, headwidth=4), zorder=5)

    save_fig(fig, "fig4_7_class_hierarchy")


# -------------------------------------------------------------
# 8. Fig 4.8a: DFD Level 0 Context Diagram
# -------------------------------------------------------------
def make_fig_4_8a():
    fig, ax = plt.subplots(figsize=(11, 6.0), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.0)

    # Center Process 0.0
    center = patches.Circle((5.5, 3.0), 1.2, facecolor=BLUE_BG, edgecolor=BLUE_BORDER, linewidth=2.0, zorder=3)
    ax.add_patch(center)
    ax.text(5.5, 3.25, "0.0\nQuantNiti Platform", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=NAVY_DARK, zorder=4)
    ax.text(5.5, 2.65, "Core Quantitative Engine", ha='center', va='center',
            fontsize=7.5, color=SLATE_BORDER, zorder=4)

    # External Entities (Rectangles)
    def draw_entity(x, y, label, w=2.4, h=0.9):
        rect = patches.Rectangle((x - w/2, y - h/2), w, h, facecolor="#F8FAFC", edgecolor=NAVY_DARK, linewidth=1.5, zorder=3)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold', color=NAVY_DARK, zorder=4)

    draw_entity(1.6, 4.8, "Retail Investor")
    draw_entity(1.6, 1.2, "Novice Learner")
    draw_entity(9.4, 4.8, "yFinance / NSE Feed")
    draw_entity(9.4, 1.2, "Google Gemini LLM")

    # Data flows
    # User -> System
    ax.annotate('', xy=(4.35, 3.5), xytext=(2.8, 4.6),
                arrowprops=dict(facecolor=BLUE_BORDER, edgecolor=BLUE_BORDER, width=1.2, headwidth=4.5), zorder=5)
    ax.text(3.4, 4.35, "Quiz, Capital, Persona", fontsize=7, color=NAVY_DARK, rotation=-28, ha='center')

    # System -> User
    ax.annotate('', xy=(2.8, 5.0), xytext=(4.35, 3.8),
                arrowprops=dict(facecolor=EMERALD_BORDER, edgecolor=EMERALD_BORDER, width=1.2, headwidth=4.5), zorder=5)
    ax.text(3.6, 4.8, "Order Sheet, Trust Card", fontsize=7, color=NAVY_DARK, rotation=-28, ha='center')

    # Learner -> System
    ax.annotate('', xy=(4.4, 2.4), xytext=(2.8, 1.4),
                arrowprops=dict(facecolor=BLUE_BORDER, edgecolor=BLUE_BORDER, width=1.2, headwidth=4.5), zorder=5)
    ax.text(3.4, 1.7, "RAG Queries, Reviews", fontsize=7, color=NAVY_DARK, rotation=28, ha='center')

    # Market Feed -> System
    ax.annotate('', xy=(6.65, 3.5), xytext=(8.2, 4.6),
                arrowprops=dict(facecolor=BLUE_BORDER, edgecolor=BLUE_BORDER, width=1.2, headwidth=4.5), zorder=5)
    ax.text(7.6, 4.35, "OHLCV Ticks, India VIX", fontsize=7, color=NAVY_DARK, rotation=28, ha='center')

    # Gemini <-> System
    ax.annotate('', xy=(8.2, 1.4), xytext=(6.65, 2.4),
                arrowprops=dict(facecolor=PURPLE_BORDER, edgecolor=PURPLE_BORDER, width=1.2, headwidth=4.5), zorder=5)
    ax.text(7.6, 1.7, "Grounded Telemetry Prompt", fontsize=7, color=NAVY_DARK, rotation=-28, ha='center')

    save_fig(fig, "fig4_8a_dfd_level0")


# -------------------------------------------------------------
# 9. Fig 4.8b: DFD Level 1 System Decomposition
# -------------------------------------------------------------
def make_fig_4_8b():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)

    processes = [
        ("1.0", "Data Ingestion & Cleaning", 2.2, 6.0),
        ("2.0", "Regime & Factor Extraction", 5.5, 6.0),
        ("3.0", "HRP Portfolio Optimizer", 8.8, 6.0),
        ("4.0", "Discrete Allocator & Trust Card", 8.8, 2.2),
        ("5.0", "RAG Chat & Literacy Hub", 5.5, 2.2),
        ("6.0", "Fact-Checked Reviews & Alerts", 2.2, 2.2),
    ]

    for num, label, cx, cy in processes:
        circ = patches.Circle((cx, cy), 0.9, facecolor=BLUE_BG, edgecolor=BLUE_BORDER, linewidth=1.5, zorder=3)
        ax.add_patch(circ)
        ax.text(cx, cy + 0.2, num, ha='center', va='center', fontsize=9, fontweight='bold', color=BLUE_BORDER)
        ax.text(cx, cy - 0.15, label, ha='center', va='center', fontsize=6.8, fontweight='bold', color=NAVY_DARK, wrap=True)

    # Data Store (Open-ended rectangle)
    def draw_datastore(x, y, label, w=2.4, h=0.6):
        ax.plot([x - w/2, x + w/2], [y + h/2, y + h/2], color=NAVY_DARK, linewidth=1.5, zorder=3)
        ax.plot([x - w/2, x + w/2], [y - h/2, y - h/2], color=NAVY_DARK, linewidth=1.5, zorder=3)
        ax.plot([x - w/2, x - w/2], [y - h/2, y + h/2], color=NAVY_DARK, linewidth=1.5, zorder=3)
        ax.fill_between([x - w/2, x + w/2], y - h/2, y + h/2, color="#F1F5F9", zorder=2)
        ax.text(x, y, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color=NAVY_DARK, zorder=4)

    draw_datastore(5.5, 4.1, "D1: SQLite DB (Portfolios & Reviews)")

    # Inter-process arrows
    flows = [
        ((3.1, 6.0), (4.6, 6.0), "Cleaned OHLCV"),
        ((6.4, 6.0), (7.9, 6.0), "Regime π_t & Cov Σ_LW"),
        ((8.8, 5.1), (8.8, 3.1), "Target Weights w*"),
        ((7.9, 2.2), (6.4, 2.2), "Trust Card Payload"),
        ((4.6, 2.2), (3.1, 2.2), "Verified Badge"),
        ((5.5, 4.4), (5.5, 5.1), "Asset Cache"),
        ((5.5, 3.8), (5.5, 3.1), "Chat Context & Reviews"),
    ]

    for p1, p2, label in flows:
        ax.annotate('', xy=p2, xytext=p1,
                    arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1.0, headwidth=4), zorder=5)
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2 + 0.15
        ax.text(mid_x, mid_y, label, ha='center', va='center', fontsize=6.5, color=NAVY_DARK,
                bbox=dict(boxstyle="round,pad=0.1", facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.5))

    save_fig(fig, "fig4_8b_dfd_level1")


# -------------------------------------------------------------
# 10. Fig 4.9: Database Entity-Relationship (ER) Schema
# -------------------------------------------------------------
def make_fig_4_9():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)

    entities = [
        ("users", 1.8, 5.8,
         ["PK  user_id: TEXT", "    persona: TEXT", "    created_at: DATETIME"],
         BLUE_BG, BLUE_BORDER),
        ("portfolios", 5.5, 5.8,
         ["PK  portfolio_id: TEXT", "FK  user_id: TEXT", "    capital: REAL", "    cash_residual: REAL", "    regime_at_creation: TEXT"],
         EMERALD_BG, EMERALD_BORDER),
        ("portfolio_holdings", 9.2, 5.8,
         ["PK  holding_id: TEXT", "FK  portfolio_id: TEXT", "    symbol: TEXT", "    shares: INTEGER", "    avg_price: REAL"],
         AMBER_BG, AMBER_BORDER),
        ("financial_goals", 1.8, 2.0,
         ["PK  goal_id: TEXT", "FK  user_id: TEXT", "    target_amount: REAL", "    horizon_months: INTEGER", "    monthly_sip: REAL"],
         PURPLE_BG, PURPLE_BORDER),
        ("smart_alerts", 5.5, 2.0,
         ["PK  alert_id: TEXT", "FK  portfolio_id: TEXT", "    trigger_type: TEXT", "    message: TEXT", "    is_read: BOOLEAN"],
         ROSE_BG, ROSE_BORDER),
        ("market_reviews", 9.2, 2.0,
         ["PK  review_id: TEXT", "FK  user_id: TEXT", "    symbol: TEXT", "    claimed_return: REAL", "    is_verified: BOOLEAN"],
         SLATE_BG, SLATE_BORDER),
    ]

    card_w, card_h = 2.8, 2.5

    for name, cx, cy, fields, bg, border in entities:
        x = cx - card_w/2
        y = cy - card_h/2
        card = patches.FancyBboxPatch((x, y), card_w, card_h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                      facecolor="#FFFFFF", edgecolor=border, linewidth=1.5, zorder=2)
        ax.add_patch(card)

        # Header bar
        hdr = patches.Rectangle((x, y + card_h - 0.45), card_w, 0.45, facecolor=bg, edgecolor=border, linewidth=1.0, zorder=3)
        ax.add_patch(hdr)
        ax.text(cx, y + card_h - 0.22, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=NAVY_DARK)

        # Fields
        yf = y + card_h - 0.72
        for f in fields:
            is_pk = "PK" in f
            is_fk = "FK" in f
            col = BLUE_BORDER if is_pk else (EMERALD_BORDER if is_fk else NAVY_DARK)
            ax.text(x + 0.12, yf, f, ha='left', va='center', fontsize=6.8, fontweight='bold' if (is_pk or is_fk) else 'normal', color=col)
            yf -= 0.32

    # Cardinality Relationships (Crow's foot / 1:N arrows)
    # users -> portfolios (1:N)
    ax.annotate('', xy=(4.1, 5.8), xytext=(3.2, 5.8),
                arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1.2, headwidth=4), zorder=5)
    ax.text(3.35, 6.0, "1", fontsize=7.5, fontweight='bold')
    ax.text(3.95, 6.0, "N", fontsize=7.5, fontweight='bold')

    # portfolios -> holdings (1:N)
    ax.annotate('', xy=(7.8, 5.8), xytext=(6.9, 5.8),
                arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1.2, headwidth=4), zorder=5)
    ax.text(7.05, 6.0, "1", fontsize=7.5, fontweight='bold')
    ax.text(7.65, 6.0, "N", fontsize=7.5, fontweight='bold')

    # users -> goals (1:N)
    ax.annotate('', xy=(1.8, 3.25), xytext=(1.8, 4.55),
                arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1.2, headwidth=4), zorder=5)
    ax.text(1.95, 4.3, "1", fontsize=7.5, fontweight='bold')
    ax.text(1.95, 3.5, "N", fontsize=7.5, fontweight='bold')

    # portfolios -> alerts (1:N)
    ax.annotate('', xy=(5.5, 3.25), xytext=(5.5, 4.55),
                arrowprops=dict(facecolor=NAVY_DARK, edgecolor=NAVY_DARK, width=1.2, headwidth=4), zorder=5)
    ax.text(5.65, 4.3, "1", fontsize=7.5, fontweight='bold')
    ax.text(5.65, 3.5, "N", fontsize=7.5, fontweight='bold')

    # users -> reviews (1:N)
    ax.plot([3.2, 7.8], [5.2, 2.0], color="#94A3B8", linewidth=1.0, linestyle="--", zorder=2)
    ax.text(3.4, 4.8, "1", fontsize=7.5, fontweight='bold')
    ax.text(7.6, 2.2, "N", fontsize=7.5, fontweight='bold')

    save_fig(fig, "fig4_9_database_er_diagram")


# -------------------------------------------------------------
# 11. Fig 4.10: Cloud & Native Android Deployment Topology Diagram
# -------------------------------------------------------------
def make_fig_4_10():
    fig, ax = plt.subplots(figsize=(11, 6.8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.8)

    # 3 Deployment Nodes
    # Node 1: Client Devices
    box_client = patches.FancyBboxPatch((0.4, 0.6), 3.0, 5.6, boxstyle="round,pad=0.02,rounding_size=0.08",
                                        facecolor=BLUE_BG, edgecolor=BLUE_BORDER, linewidth=1.5, zorder=2)
    ax.add_patch(box_client)
    ax.text(1.9, 5.8, "«device»\nClient Mobile / Web", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=NAVY_DARK)

    pwa_sub = patches.FancyBboxPatch((0.6, 3.3), 2.6, 1.8, boxstyle="round,pad=0.02,rounding_size=0.05",
                                     facecolor="#FFFFFF", edgecolor="#93C5FD", linewidth=1.2, zorder=3)
    ax.add_patch(pwa_sub)
    ax.text(1.9, 4.6, "React 18 + Vite PWA", ha='center', va='center', fontsize=8, fontweight='bold', color=BLUE_BORDER)
    ax.text(1.9, 4.1, "• Zustand State Store\n• Framer Motion Physics\n• Tailwind CSS Theme", ha='center', va='center', fontsize=6.8, color=NAVY_DARK)

    apk_sub = patches.FancyBboxPatch((0.6, 1.1), 2.6, 1.8, boxstyle="round,pad=0.02,rounding_size=0.05",
                                     facecolor="#FFFFFF", edgecolor="#93C5FD", linewidth=1.2, zorder=3)
    ax.add_patch(apk_sub)
    ax.text(1.9, 2.4, "Android APK Container", ha='center', va='center', fontsize=8, fontweight='bold', color=BLUE_BORDER)
    ax.text(1.9, 1.9, "• com.quantniti.app\n• WebViewAssetLoader\n• Hardware Back Interceptor", ha='center', va='center', fontsize=6.8, color=NAVY_DARK)

    # Node 2: AWS Lightsail Server
    box_server = patches.FancyBboxPatch((4.0, 0.6), 3.4, 5.6, boxstyle="round,pad=0.02,rounding_size=0.08",
                                        facecolor=EMERALD_BG, edgecolor=EMERALD_BORDER, linewidth=1.5, zorder=2)
    ax.add_patch(box_server)
    ax.text(5.7, 5.8, "«server: AWS Lightsail (Mumbai)»\nUbuntu 24.04 LTS (ap-south-1)", ha='center', va='center',
            fontsize=9, fontweight='bold', color=NAVY_DARK)

    caddy_sub = patches.FancyBboxPatch((4.2, 3.8), 3.0, 1.3, boxstyle="round,pad=0.02,rounding_size=0.05",
                                       facecolor="#FFFFFF", edgecolor="#6EE7B7", linewidth=1.2, zorder=3)
    ax.add_patch(caddy_sub)
    ax.text(5.7, 4.6, "Caddy v2 Reverse Proxy", ha='center', va='center', fontsize=8, fontweight='bold', color=EMERALD_BORDER)
    ax.text(5.7, 4.15, "• Automated Let's Encrypt TLS\n• Port 443 / quantniti.jayadityadev.tech", ha='center', va='center', fontsize=6.8, color=NAVY_DARK)

    docker_sub = patches.FancyBboxPatch((4.2, 1.1), 3.0, 2.3, boxstyle="round,pad=0.02,rounding_size=0.05",
                                        facecolor="#FFFFFF", edgecolor="#6EE7B7", linewidth=1.2, zorder=3)
    ax.add_patch(docker_sub)
    ax.text(5.7, 3.0, "Docker Multi-Stage Container", ha='center', va='center', fontsize=8, fontweight='bold', color=EMERALD_BORDER)
    ax.text(5.7, 2.3, "• Python 3.12 + FastAPI ASGI\n• GMM, HRP & Quantile Engines\n• SQLite 3 (WAL Mode DB)\n• Port 8000 Internal Binding", ha='center', va='center', fontsize=6.8, color=NAVY_DARK)

    # Node 3: External Cloud APIs
    box_cloud = patches.FancyBboxPatch((8.0, 0.6), 2.6, 5.6, boxstyle="round,pad=0.02,rounding_size=0.08",
                                       facecolor=PURPLE_BG, edgecolor=PURPLE_BORDER, linewidth=1.5, zorder=2)
    ax.add_patch(box_cloud)
    ax.text(9.3, 5.8, "«external cloud»\nThird-Party APIs", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color=NAVY_DARK)

    gemini_sub = patches.FancyBboxPatch((8.2, 3.3), 2.2, 1.8, boxstyle="round,pad=0.02,rounding_size=0.05",
                                        facecolor="#FFFFFF", edgecolor="#D8B4FE", linewidth=1.2, zorder=3)
    ax.add_patch(gemini_sub)
    ax.text(9.3, 4.5, "Google Gemini API", ha='center', va='center', fontsize=8, fontweight='bold', color=PURPLE_BORDER)
    ax.text(9.3, 3.9, "• Gemini 2.5 Flash\n• Grounded RAG Copilot\n• Review Tone Audit", ha='center', va='center', fontsize=6.8, color=NAVY_DARK)

    yfin_sub = patches.FancyBboxPatch((8.2, 1.1), 2.2, 1.8, boxstyle="round,pad=0.02,rounding_size=0.05",
                                      facecolor="#FFFFFF", edgecolor="#D8B4FE", linewidth=1.2, zorder=3)
    ax.add_patch(yfin_sub)
    ax.text(9.3, 2.3, "yFinance / NSE Data", ha='center', va='center', fontsize=8, fontweight='bold', color=PURPLE_BORDER)
    ax.text(9.3, 1.7, "• NIFTY 50 OHLCV\n• Real-Time Market Ticks\n• India VIX Stream", ha='center', va='center', fontsize=6.8, color=NAVY_DARK)

    # Connections
    ax.annotate('', xy=(4.2, 4.4), xytext=(3.4, 4.4),
                arrowprops=dict(facecolor=BLUE_BORDER, edgecolor=BLUE_BORDER, width=1.5, headwidth=5), zorder=5)
    ax.text(3.8, 4.6, "HTTPS / WSS", fontsize=7, fontweight='bold', ha='center')

    ax.annotate('', xy=(8.2, 4.2), xytext=(7.2, 4.2),
                arrowprops=dict(facecolor=PURPLE_BORDER, edgecolor=PURPLE_BORDER, width=1.5, headwidth=5), zorder=5)
    ax.text(7.7, 4.4, "REST / SSL", fontsize=7, fontweight='bold', ha='center')

    ax.annotate('', xy=(8.2, 2.0), xytext=(7.2, 2.0),
                arrowprops=dict(facecolor=PURPLE_BORDER, edgecolor=PURPLE_BORDER, width=1.5, headwidth=5), zorder=5)
    ax.text(7.7, 2.2, "Market Feeds", fontsize=7, fontweight='bold', ha='center')

    save_fig(fig, "fig4_10_deployment_diagram")


if __name__ == "__main__":
    print("Beginning generation of all academic report diagrams...")
    make_fig_2_1()
    make_fig_4_2()
    make_fig_4_3()
    make_fig_4_4()
    make_fig_4_5()
    make_fig_4_6()
    make_fig_4_7()
    make_fig_4_8a()
    make_fig_4_8b()
    make_fig_4_9()
    make_fig_4_10()
    print("All diagrams generated successfully!")
