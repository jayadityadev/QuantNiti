# -*- coding: utf-8 -*-
"""
build_final_presentation.py
Generates the definitive Final Review (Review 3 / Viva-Voce) Presentation Deck for QuantNiti.
Complies 100% with KSIT / VTU official presentation template guidelines.
Generates:
  1. docs/review/ours/final_review_presentation.pptx
  2. docs/review/ours/final_review_presentation.pdf (via PowerPoint COM)
  3. docs/review/ours/final_slides_png/Slide1.PNG ... Slide17.PNG (1080p high-res images)
"""

import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Base Paths
BASE_DIR = r"D:\Codebase\QuantNiti"
OUTPUT_DIR = os.path.join(BASE_DIR, "docs", "review", "ours")
EXTRACTED_DIR = os.path.join(OUTPUT_DIR, "extracted_assets")
REPORT_FIG_DIR = os.path.join(BASE_DIR, "docs", "academic_docs", "project_phase_2_report", "figures")
SLIDES_PNG_DIR = os.path.join(OUTPUT_DIR, "final_slides_png")

BASE_PPTX = os.path.join(OUTPUT_DIR, "review2.pptx")
TARGET_PPTX = os.path.join(OUTPUT_DIR, "final_review_presentation.pptx")
TARGET_PDF = os.path.join(OUTPUT_DIR, "final_review_presentation.pdf")

# Standard Colors
COLOR_MAROON = RGBColor(192, 0, 0)       # #C00000 (KSIT official crimson/maroon)
COLOR_DARK_BLUE = RGBColor(27, 54, 93)   # #1B365D (Academic primary navy)
COLOR_TEXT_MAIN = RGBColor(40, 40, 40)   # #282828 (Charcoal body text)
COLOR_MUTED = RGBColor(100, 100, 100)    # #646464 (Subtitles)
COLOR_BORDER = RGBColor(215, 215, 215)   # #D7D7D7 (Card borders)
COLOR_BG_CARD = RGBColor(248, 249, 250)  # #F8F9FA (Card background)
COLOR_GREEN = RGBColor(0, 128, 55)       # #008037 (Alpha / positive metrics)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_HIGHLIGHT = RGBColor(232, 245, 233)# #E8F5E9 (Light green highlight)

# Geometry Constants (12192000 x 6858000)
FRAME_LEFT = 120072
FRAME_TOP = 90089
FRAME_WIDTH = 11942619
FRAME_HEIGHT = 6677822

LOGO_LEFT = 404889
LOGO_TOP = 187720
LOGO_WIDTH = 873901
LOGO_HEIGHT = 1000553

TITLE_LEFT = 1554370
TITLE_TOP = 187720
TITLE_WIDTH = 9358840
TITLE_HEIGHT = 896145

SLIDE_NUM_LEFT = 8610600
SLIDE_NUM_TOP = 6356350
SLIDE_NUM_WIDTH = 2743200
SLIDE_NUM_HEIGHT = 365125


def add_base_decorations(slide, title_text, slide_no, logo_path):
    """Adds the outer boundary, KSIT logo, title, and slide number."""
    # Outer subtle boundary rectangle
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, FRAME_LEFT, FRAME_TOP, FRAME_WIDTH, FRAME_HEIGHT)
    rect.fill.background()
    rect.line.color.rgb = COLOR_BORDER
    rect.line.width = Pt(1)

    # KSIT Crest Logo
    if os.path.exists(logo_path):
        slide.shapes.add_picture(logo_path, LOGO_LEFT, LOGO_TOP, LOGO_WIDTH, LOGO_HEIGHT)

    # Title Box
    tx_box = slide.shapes.add_textbox(TITLE_LEFT, TITLE_TOP, TITLE_WIDTH, TITLE_HEIGHT)
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Bookman Old Style"
    p.font.size = Pt(25)
    p.font.bold = True
    p.font.color.rgb = COLOR_MAROON

    # Slide Number Box
    num_box = slide.shapes.add_textbox(SLIDE_NUM_LEFT, SLIDE_NUM_TOP, SLIDE_NUM_WIDTH, SLIDE_NUM_HEIGHT)
    tf_num = num_box.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.text = str(slide_no)
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.font.name = "Times New Roman"
    p_num.font.size = Pt(13)
    p_num.font.color.rgb = COLOR_MUTED


def add_card(slide, left, top, width, height, bg_color=COLOR_BG_CARD, border_color=COLOR_BORDER):
    """Draws a rectangular card shape with background and border."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card


def add_bullet_point(tf, bold_prefix, text, font_size=15, space_after=8):
    """Adds a structured bullet paragraph with bold prefix."""
    p = tf.add_paragraph()
    p.space_after = Pt(space_after)
    p.level = 0
    run_bold = p.add_run()
    run_bold.text = bold_prefix + " "
    run_bold.font.name = "Times New Roman"
    run_bold.font.size = Pt(font_size)
    run_bold.font.bold = True
    run_bold.font.color.rgb = COLOR_TEXT_MAIN

    run_text = p.add_run()
    run_text.text = text
    run_text.font.name = "Times New Roman"
    run_text.font.size = Pt(font_size)
    run_text.font.bold = False
    run_text.font.color.rgb = COLOR_TEXT_MAIN


def style_table(table, col_widths, headers, data, highlight_row_idx=-1):
    """Applies clean academic styling to a python-pptx Table."""
    for idx, width in enumerate(col_widths):
        table.columns[idx].width = width

    # Format Headers
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_MAROON
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = h_text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Bookman Old Style"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    # Format Data Rows
    for r_idx, row_data in enumerate(data):
        is_highlight = (r_idx == highlight_row_idx)
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            if is_highlight:
                cell.fill.fore_color.rgb = COLOR_HIGHLIGHT
            elif r_idx % 2 == 1:
                cell.fill.fore_color.rgb = RGBColor(245, 247, 250)
            else:
                cell.fill.fore_color.rgb = COLOR_WHITE

            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = str(val)
            p.alignment = PP_ALIGN.CENTER if (c_idx > 0 and len(val) < 15) else PP_ALIGN.LEFT
            p.font.name = "Times New Roman"
            p.font.size = Pt(10.5)
            p.font.bold = is_highlight
            if is_highlight and c_idx > 0 and ('%' in val or val.replace('.', '', 1).isdigit()):
                p.font.color.rgb = COLOR_GREEN
            else:
                p.font.color.rgb = COLOR_TEXT_MAIN


def build_presentation():
    print(f"Loading base presentation from {BASE_PPTX}...")
    prs = pptx.Presentation(BASE_PPTX)
    logo_path = os.path.join(EXTRACTED_DIR, "slide1_Picture 8.jpg")

    # Update Slide 1 (Title Slide)
    print("Formatting Slide 1: Title Slide (Review 3 update)...")
    s1 = prs.slides[0]
    for sh in s1.shapes:
        if sh.has_text_frame and "MAJOR PROJECT PHASE II" in sh.text_frame.text:
            text = sh.text_frame.text
            text = text.replace("Review 2", "Review 3")
            sh.text_frame.text = text
            # Re-apply styling to first paragraph
            p0 = sh.text_frame.paragraphs[0]
            p0.font.name = "Times New Roman"
            p0.font.size = Pt(18)
            p0.font.bold = True

    # Delete existing slides 2 to 15 (indices 1 to end)
    print("Clearing slides 2 through 15 to reconstruct official 17-slide structure...")
    while len(prs.slides) > 1:
        rId = prs.slides._sldIdLst[1].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[1]

    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 2: Contents
    # =========================================================================
    print("Building Slide 2: Contents (12 Official Sections)...")
    s2 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s2, "Contents", 2, logo_path)

    sections_left = [
        "1. Introduction & Socio-Economic Crisis",
        "2. Literature Review & Platform Audit",
        "3. Formal Problem Statement",
        "4. Engineering Objectives",
        "5. System Architecture & Interfacing",
        "6. Innovation & Technical Contribution",
    ]
    sections_right = [
        "7. Experimentation and Testing",
        "8. Results and Analysis",
        "9. Demonstration Snapshots",
        "10. Future Work",
        "11. Conclusion",
        "12. References",
    ]

    card_left = add_card(s2, Inches(1.0), Inches(1.6), Inches(5.4), Inches(4.7))
    tf_l = card_left.text_frame
    tf_l.word_wrap = True
    tf_l.paragraphs[0].text = "Core Foundations & Methodology"
    tf_l.paragraphs[0].font.name = "Bookman Old Style"
    tf_l.paragraphs[0].font.size = Pt(16)
    tf_l.paragraphs[0].font.bold = True
    tf_l.paragraphs[0].font.color.rgb = COLOR_MAROON
    tf_l.paragraphs[0].space_after = Pt(14)
    for sec in sections_left:
        p = tf_l.add_paragraph()
        p.text = sec
        p.font.name = "Times New Roman"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(12)

    card_right = add_card(s2, Inches(6.8), Inches(1.6), Inches(5.4), Inches(4.7))
    tf_r = card_right.text_frame
    tf_r.word_wrap = True
    tf_r.paragraphs[0].text = "Verification, Results & Roadmap"
    tf_r.paragraphs[0].font.name = "Bookman Old Style"
    tf_r.paragraphs[0].font.size = Pt(16)
    tf_r.paragraphs[0].font.bold = True
    tf_r.paragraphs[0].font.color.rgb = COLOR_MAROON
    tf_r.paragraphs[0].space_after = Pt(14)
    for sec in sections_right:
        p = tf_r.add_paragraph()
        p.text = sec
        p.font.name = "Times New Roman"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 3: Introduction: Socio-Economic Crisis & Retail Dilemma
    # =========================================================================
    print("Building Slide 3: Introduction...")
    s3 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s3, "Socio-Economic Crisis: The Retail Capital Dilemma", 3, logo_path)

    # 3 Metric Cards on Top
    metrics = [
        ("240.6M+ DEMAT", "24+ Crore demat accounts in India; 122M unique retail investors (NSE 2026)."),
        ("89% TO 93% LOSSES", "Active retail traders in net losses (Official SEBI empirical study)."),
        ("27% LITERACY", "National financial literacy benchmark rate (NCFE-FLIS benchmark)."),
    ]
    card_w = Inches(3.6)
    for idx, (title_m, desc_m) in enumerate(metrics):
        c_left = Inches(1.0 + idx * 3.8)
        card_m = add_card(s3, c_left, Inches(1.5), card_w, Inches(1.6))
        tf = card_m.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title_m
        p0.alignment = PP_ALIGN.CENTER
        p0.font.name = "Bookman Old Style"
        p0.font.size = Pt(18)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_MAROON
        p0.space_after = Pt(6)
        p1 = tf.add_paragraph()
        p1.text = desc_m
        p1.alignment = PP_ALIGN.CENTER
        p1.font.name = "Times New Roman"
        p1.font.size = Pt(12)
        p1.font.color.rgb = COLOR_TEXT_MAIN

    # Bottom Detailed Narrative Card
    bot_card = add_card(s3, Inches(1.0), Inches(3.3), Inches(11.2), Inches(3.0))
    tf_b = bot_card.text_frame
    tf_b.word_wrap = True
    p_b0 = tf_b.paragraphs[0]
    p_b0.text = "The Core Socio-Economic Bottlenecks:"
    p_b0.font.name = "Bookman Old Style"
    p_b0.font.size = Pt(16)
    p_b0.font.bold = True
    p_b0.font.color.rgb = COLOR_MAROON
    p_b0.space_after = Pt(10)

    add_bullet_point(tf_b, "• The Average Loss:",
                     "Retail participants lose an average of ₹1.1 Lakh per year due to speculative tips, emotional panic-selling, and hyper-frequent trading.",
                     font_size=14, space_after=10)
    add_bullet_point(tf_b, "• The Advisory Trap:",
                     "Bank wealth managers charge 1.5%–2.5% annual AUM fees, eroding 25%–35% of compounding returns over 10 years, with minimum barrier bars of ₹5 Lakhs+.",
                     font_size=14, space_after=10)
    add_bullet_point(tf_b, "• Social Mission:",
                     "To provide 24 crore everyday Indian citizens with free, regime-aware, explainable quantitative wealth defense for capital as low as ₹5,000.",
                     font_size=14, space_after=10)

    # =========================================================================
    # SLIDE 4: Literature Review (Part I) - Academic Foundations
    # =========================================================================
    print("Building Slide 4: Literature Review (Part I - Academic)...")
    s4 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s4, "Literature Review: Academic Foundations & Prior Art", 4, logo_path)

    academic_works = [
        ("Markowitz Mean-Variance Optimization (1952)",
         "Classic quadratic programming minimizes portfolio variance for a target return.\n\n"
         "• Econometric Flaw: Acts as an 'Error Maximizer' in finite empirical samples.\n"
         "• Mathematical Failure: Inverting sample covariance (Σ⁻¹) exponentially magnifies estimation error, resulting in unstable, corner-solution allocations."),
        
        ("Ledoit-Wolf Shrinkage Regularization (2004)",
         "Replaces empirical sample covariance with optimal linear shrinkage target F.\n\n"
         "• Mathematical Formulation: Σ_LW = δ* F + (1 - δ*) S + 10⁻⁷ I_N.\n"
         "• Invariant Guarantee: Ensures strict positive definiteness (λ_min > 0) and non-singularity, conditioning noisy Indian market covariance matrices."),
        
        ("Hierarchical Risk Parity — López de Prado (2018)",
         "Applies graph tree-clustering (single linkage dendrograms) and recursive bisection.\n\n"
         "• Core Innovation: Allocates capital top-down across hierarchical asset clusters.\n"
         "• Key Advantage: Completely eliminates matrix inversion (Σ⁻¹), guaranteeing numerical robustness during extreme macro market crashes."),
        
        ("Regime-Switching Macro Models (Hamilton 1989)",
         "Models market phases as latent statistical states (Bull, Bear, Sideways).\n\n"
         "• Adaptation: QuantNiti formulates an unsupervised 3-State Gaussian Mixture Model (GMM) with posterior vector π_t = [π_Bull, π_Bear, π_Flat].\n"
         "• Factor Tilting: Dynamically modulates risk vs. momentum exposure."),
    ]

    for idx, (title_a, text_a) in enumerate(academic_works):
        r = idx // 2
        c = idx % 2
        card_l = Inches(1.0 + c * 5.8)
        card_t = Inches(1.5 + r * 2.45)
        card_a = add_card(s4, card_l, card_t, Inches(5.5), Inches(2.3))
        tf = card_a.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title_a
        p0.font.name = "Bookman Old Style"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_MAROON
        p0.space_after = Pt(4)
        for line in text_a.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Times New Roman"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 5: Literature Review (Part II) - Platform Audit
    # =========================================================================
    print("Building Slide 5: Literature Review (Part II - Platform Audit)...")
    s5 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s5, "Platform Audit: Why Existing Solutions Fail Retail Users", 5, logo_path)

    p_headers = ["Platform", "Forward Growth\nProjections", "Macro Regime\nDetection", "Portfolio\nOptimization", "Budget Sizing\n(Whole Shares)", "Dynamic\nRebalance", "Cost to\nRetail"]
    p_widths = [Inches(1.4), Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.5), Inches(1.1)]
    p_data = [
        ["Groww", "Retrospective XIRR only; 0 forward forecast.", "Static; shows daily index % change only.", "Manual; user picks stock quantities.", "Manual input; order fails if cash is short.", "100% manual trade execution.", "₹20/trade"],
        ["Zerodha (Streak)", "Rule hit-rate only; no price cones.", "Manual 200 EMA/RSI rules per stock.", "Single-stock only; cannot balance baskets.", "Fixed lot per rule; no basket sizing.", "Indicator alerts; no portfolio diff.", "₹690–₹1,400/mo + ₹20/trade"],
        ["Moneycontrol (Pro)", "Consensus broker targets; 0 cones.", "News & editorial opinion; no quant ML.", "Heuristic 'X-Ray'; zero quant math.", "Manual logging only; no sizing engine.", "Price/news alerts; no diff engine.", "Free (Ad bloat) / ₹399–₹999/yr"],
        ["INDmoney", "Past net worth & XIRR tracking only.", "News summaries; no structural break ML.", "Passive tracking; sector pie charts only.", "Broker redirect; no integer engine.", "Mutual fund Robo-STP only; no equity diff.", "Free (Advisory funnels)"],
        ["TradingView", "Historical bar replay; no forward cones.", "Manual overlay of India VIX on charts.", "Single-asset charts; zero portfolio math.", "Fractional theory (e.g. 2.34 shares).", "Script price alerts; no basket diff.", "$180–$720/yr + 15m delay"],
        ["QuantNiti", "3-Tier Quantile Cones (Q10, Q50, Q90)", "Unsupervised GMM Radar (Bull/Bear/Flat)", "Hierarchical Risk Parity (HRP)", "Greedy Whole Shares (n_i ∈ ℤ⁺)", "Event-Triggered Regime Diffs", "100% Free / 0% Fee"],
    ]

    table_shape_p = s5.shapes.add_table(len(p_data) + 1, len(p_headers), Inches(1.0), Inches(1.45), Inches(11.2), Inches(4.8))
    style_table(table_shape_p.table, p_widths, p_headers, p_data, highlight_row_idx=5)

    # =========================================================================
    # SLIDE 6: Formal Problem Statement
    # =========================================================================
    print("Building Slide 6: Formal Problem Statement...")
    s6 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s6, "Formal Problem Statement", 6, logo_path)

    prob_cards = [
        ("1. The Retail Information Vacuum",
         "Retail investors in India's equity market lack forward-looking, regime-adaptive decision support tools—leaving them vulnerable to catastrophic drawdowns during macroeconomic shifts.\n\n"
         "• Over 90% of retail participants experience severe capital drawdown during structural market transitions due to backward-looking trailing returns and social media speculative tips."),
        
        ("2. Econometric Failure of Classical Models",
         "Textbook Markowitz Mean-Variance Optimization (MVO) acts as an 'Error Maximizer' in real markets: inverting noisy sample covariance matrices (Σ⁻¹) magnifies estimation error, producing extreme, unstable stock weights.\n\n"
         "• Covariance matrix singularity leads to unhedged risk exposure and unrealistic extreme allocations in finite historical periods."),
        
        ("3. The Practical Execution Gap",
         "Institutional quantitative research assumes continuous fractional share trading. Indian exchanges legally require discrete integer shares (n_i ∈ ℤ⁺) making theoretical models unexecutable for modest retail capital budgets (₹5,000–₹50,000).\n\n"
         "• Converting continuous weights w* to whole shares without mathematical optimization results in cash drag or budget breaches."),
    ]

    for idx, (p_title, p_body) in enumerate(prob_cards):
        card_p = add_card(s6, Inches(1.0), Inches(1.5 + idx * 1.6), Inches(11.2), Inches(1.45))
        tf = card_p.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = p_title
        p0.font.name = "Bookman Old Style"
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_MAROON
        p0.space_after = Pt(4)
        for line in p_body.split('\n'):
            if line:
                p = tf.add_paragraph()
                p.text = line
                p.font.name = "Times New Roman"
                p.font.size = Pt(12)
                p.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 7: Engineering Objectives
    # =========================================================================
    print("Building Slide 7: Engineering Objectives...")
    s7 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s7, "Engineering Objectives", 7, logo_path)

    objectives = [
        ("1. Unsupervised Regime Detection",
         "Detect latent macroeconomic regimes (Bull, Bear, Sideways) using GMM on rolling returns, realized volatility, Parkinson volatility, and India VIX."),
        ("2. Multi-Horizon Quantile Forecaster",
         "Compute 1M, 3M, 6M, and 12M probabilistic growth cones adhering to strict isotonic monotonicity (Q10 ≤ Q50 ≤ Q90)."),
        ("3. Inversion-Free Portfolio Construction",
         "Replace fragile Markowitz quadratic optimization with graph-clustered Hierarchical Risk Parity over Ledoit-Wolf shrinkage covariance."),
        ("4. Discrete Execution Sizing",
         "Formulate a greedy integer programming allocator converting continuous weights into whole shares (n_i ∈ ℤ⁺) with minimal residual cash buffers."),
        ("5. Explainable AI Trust Card & RAG Copilot",
         "Synthesize a 4-pillar trust model and grounded conversational assistant (NitiBot) to contextualize recommendations without hallucination."),
    ]

    for idx, (o_title, o_desc) in enumerate(objectives):
        card_o = add_card(s7, Inches(1.0), Inches(1.5 + idx * 0.98), Inches(11.2), Inches(0.88))
        tf = card_o.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = o_title + ": "
        p0.font.name = "Bookman Old Style"
        p0.font.size = Pt(13.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_MAROON
        run_desc = p0.add_run()
        run_desc.text = o_desc
        run_desc.font.name = "Times New Roman"
        run_desc.font.size = Pt(12.5)
        run_desc.font.bold = False
        run_desc.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 8: End-to-End System Architecture
    # =========================================================================
    print("Building Slide 8: End-to-End System Architecture...")
    s8 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s8, "End-to-End System Architecture", 8, logo_path)

    arch_img_path = os.path.join(EXTRACTED_DIR, "slide8_architecture.png")
    if not os.path.exists(arch_img_path):
        arch_img_path = os.path.join(EXTRACTED_DIR, "image7.png")
    if os.path.exists(arch_img_path):
        s8.shapes.add_picture(arch_img_path, Inches(1.0), Inches(1.4), Inches(11.2), Inches(4.9))

    # =========================================================================
    # SLIDE 9: Demonstration with Performance Validation: Model Interfacing
    # =========================================================================
    print("Building Slide 9: Model Interfacing & Data Contracts...")
    s9 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s9, "Demonstration with Performance Validation: Model Interfacing", 9, logo_path)

    i_headers = ["Interface Boundary", "Sending Component\n(Producer)", "Receiving Component\n(Consumer)", "Mathematical Payload & Data Contract"]
    i_widths = [Inches(2.2), Inches(2.4), Inches(2.4), Inches(4.2)]
    i_data = [
        ["Interface 1:\nMacro ➔ Asset",
         "Unsupervised GMM Classifier\n(classifier.py)",
         "Multi-Factor Feature Ranker\n(factors.py)",
         "Regime Posterior Vector: π_t = [π_Bull, π_Bear, π_Sideways]. Dynamically modulates Momentum vs. Defensive factor weights."],
        ["Interface 2:\nAsset ➔ Optimizer",
         "Quantile Forecaster +\nLedoit-Wolf Covariance\n(covariance.py)",
         "Hierarchical Risk Parity Solver\n(hrp.py)",
         "Expected Return Vector μ* ∈ ℝᴺ & Regularized Covariance Σ_LW = δ* F + (1 - δ*) S + 10⁻⁷ I_N."],
        ["Interface 3:\nPortfolio ➔ Sizing",
         "HRP Optimization Solver\n(hrp.py)",
         "Greedy Integer Allocator\n(discrete.py)",
         "Continuous Target Weights w* ∈ [0, 1]ᴺ (Σ w_i = 1) ingested with capital C and live spot prices P_i."],
        ["Interface 4:\nExecution ➔ Client",
         "Discrete Allocator +\nTrust Card Generator\n(trust_card.py)",
         "FastAPI ASGI Gateway ➔\nReact 18 PWA",
         "Discrete Order Sheet n_i ∈ ℤ⁺, Cash Buffer C_residual + 4-Pillar Trust Card JSON payload over REST/SSE."],
    ]

    t_shape_i = s9.shapes.add_table(len(i_data) + 1, len(i_headers), Inches(1.0), Inches(1.5), Inches(11.2), Inches(4.7))
    style_table(t_shape_i.table, i_widths, i_headers, i_data)

    # =========================================================================
    # SLIDE 10: Innovation & Technical Contribution
    # =========================================================================
    print("Building Slide 10: Innovation & Technical Contribution...")
    s10 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s10, "Innovation & Technical Contribution", 10, logo_path)

    innovations = [
        ("1. Regime-Adaptive Dynamic Modulation",
         "• Problem Solved: Retail investors panic-sell or over-trade during sudden market cycle turns.\n"
         "• Technical Innovation: Unsupervised 3-state Gaussian Mixture Model (GMM) with posterior probability vector π_t.\n"
         "• System Impact: Dynamically tilts asset selection between aggressive momentum and capital preservation without human bias."),
        
        ("2. Inversion-Free Quasi-Diagonalization",
         "• Problem Solved: Textbook Markowitz MVO fails due to singular/ill-conditioned covariance matrices (Σ⁻¹).\n"
         "• Technical Innovation: Hierarchical Risk Parity (HRP) machine learning tree-clustering combined with Ledoit-Wolf shrinkage.\n"
         "• System Impact: Strictly positive definite stability (λ_min > 0) with zero matrix inversion, preventing catastrophic allocation blowups."),
        
        ("3. Greedy Whole-Share Integer Knapsack",
         "• Problem Solved: Theoretical quant models assume continuous fractional shares (2.34 shares) illegal in India.\n"
         "• Technical Innovation: Formulated a priority-ranked greedy integer knapsack allocator (n_i ∈ ℤ⁺).\n"
         "• System Impact: Bridges theory to reality for retail budgets down to ₹5,000 with minimal residual cash buffers."),
        
        ("4. Deterministic 4-Pillar XAI & Grounded RAG",
         "• Problem Solved: Deep learning and black-box quant models cause severe investor distrust and LLM hallucinations.\n"
         "• Technical Innovation: Synthesized a 4-Pillar Trust Card (Regime, Hit Rate, Stress Drawdown, Disintermediation) + Grounded RAG.\n"
         "• System Impact: NitiBot powered by Gemini Flash answers queries grounded in local metrics with strict SEBI disclaimers."),
    ]

    for idx, (title_in, desc_in) in enumerate(innovations):
        r = idx // 2
        c = idx % 2
        card_in = add_card(s10, Inches(1.0 + c * 5.8), Inches(1.5 + r * 2.45), Inches(5.5), Inches(2.3))
        tf = card_in.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title_in
        p0.font.name = "Bookman Old Style"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_MAROON
        p0.space_after = Pt(4)
        for line in desc_in.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Times New Roman"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 11: Experimentation and Testing
    # =========================================================================
    print("Building Slide 11: Experimentation and Testing...")
    s11 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s11, "Experimentation and Testing: Subsystem Invariant Proofs & Test Harness", 11, logo_path)

    # Subtitle Card
    sub_card = add_card(s11, Inches(1.0), Inches(1.4), Inches(11.2), Inches(0.55), bg_color=COLOR_HIGHLIGHT)
    tf_sub = sub_card.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Comprehensive Test Suite: 504 Automated Tests (99% Backend Coverage) Verifying Invariants Across 6 Seams"
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = "Bookman Old Style"
    p_sub.font.size = Pt(12)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_GREEN

    test_headers = ["Subsystem Seam", "Tests", "Mathematical Invariants Verified Across Seams"]
    test_widths = [Inches(2.5), Inches(1.0), Inches(7.7)]
    test_data = [
        ["GMM Regime Engine", "42", "Probability simplex constraint (Σ π_k = 1.0); deterministic centroid ordering; EM convergence stability."],
        ["Quantile Forecaster", "38", "Isotonic monotonicity invariant (Q10 ≤ Q50 ≤ Q90) strictly enforced across all 58 assets."],
        ["Ledoit-Wolf & HRP", "73", "Positive-definiteness (λ_min > 0); budget conservation (Σ w_i = 1.0); persona weight bounds."],
        ["Discrete Allocator", "31", "Non-negative cash buffer (C_residual ≥ 0); integer constraint (n_i ∈ ℤ⁺); capital conservation."],
        ["Backtest Engine", "36", "Zero lookahead bias; strict T+1 execution; 0.05% slippage and 0.10% transaction taxes; Sharpe/Sortino mathematical integrity."],
        ["AI Fact-Checker", "23", "Regex claim extraction; ground-truth discrepancy thresholds (3% verified, 8% flagged)."],
    ]

    t_shape_t = s11.shapes.add_table(len(test_data) + 1, len(test_headers), Inches(1.0), Inches(2.1), Inches(11.2), Inches(4.2))
    style_table(t_shape_t.table, test_widths, test_headers, test_data)

    # =========================================================================
    # SLIDE 12: Results and Analysis (Part I) - Benchmark Outperformance
    # =========================================================================
    print("Building Slide 12: Results and Analysis (Part I - Benchmark)...")
    s12 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s12, "Results and Analysis: Empirical Comparative Benchmark", 12, logo_path)

    r_headers = ["Strategy / Model", "Annual Return\n(CAGR)", "Sharpe Ratio\n(R_f = 6.5%)", "Sortino\nRatio", "Maximum\nDrawdown (MDD)", "Calmar\nRatio"]
    r_widths = [Inches(3.2), Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.6)]
    r_data = [
        ["QuantNiti HRP (Regime-Adaptive)", "18.4%", "1.42", "2.31", "-12.4%", "1.48"],
        ["Classical Markowitz MVO", "14.2%", "0.88", "1.14", "-28.6%", "0.50"],
        ["Equal Weight (1/N)", "15.8%", "1.05", "1.47", "-21.8%", "0.72"],
        ["NIFTY 50 Buy & Hold", "13.1%", "0.79", "0.98", "-38.4%", "0.34"],
    ]

    t_shape_r = s12.shapes.add_table(len(r_data) + 1, len(r_headers), Inches(1.0), Inches(1.5), Inches(11.2), Inches(2.6))
    style_table(t_shape_r.table, r_widths, r_headers, r_data, highlight_row_idx=0)

    # 3 Callout Cards for Analysis
    r_cards = [
        ("+530 bps Alpha Outperformance",
         "QuantNiti achieved an 18.4% annualized return, outperforming the benchmark NIFTY 50 Buy & Hold (13.1%) by +530 bps per year over the 8-year cycle (2018–2026)."),
        ("67.7% Tail Loss Reduction",
         "Maximum drawdown was strictly capped at -12.4%, compared to -38.4% for NIFTY 50 and -28.6% for Markowitz MVO, providing institutional-grade capital defense."),
        ("Exceptional Sortino Ratio (2.31)",
         "The Sortino ratio of 2.31 reflects asymmetric protection against downside volatility, achieving 2.3x excess return per unit of downside risk vs 0.98 for NIFTY 50."),
    ]

    for idx, (rc_title, rc_desc) in enumerate(r_cards):
        card_rc = add_card(s12, Inches(1.0 + idx * 3.8), Inches(4.3), Inches(3.6), Inches(2.0))
        tf = card_rc.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = rc_title
        p0.alignment = PP_ALIGN.CENTER
        p0.font.name = "Bookman Old Style"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_MAROON
        p0.space_after = Pt(6)
        p1 = tf.add_paragraph()
        p1.text = rc_desc
        p1.alignment = PP_ALIGN.LEFT
        p1.font.name = "Times New Roman"
        p1.font.size = Pt(11)
        p1.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 13: Results and Analysis (Part II) - Equity & Drawdown Curves
    # =========================================================================
    print("Building Slide 13: Results and Analysis (Part II - Charts & Dynamics)...")
    s13 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s13, "Results and Analysis: Equity Curves & Tail Risk Dynamics", 13, logo_path)

    eq_path = os.path.join(REPORT_FIG_DIR, "fig6_1_equity_curves.png")
    dd_path = os.path.join(REPORT_FIG_DIR, "fig6_2_drawdown_profile.png")

    if os.path.exists(eq_path):
        s13.shapes.add_picture(eq_path, Inches(1.0), Inches(1.4), Inches(5.5), Inches(3.0))
    if os.path.exists(dd_path):
        s13.shapes.add_picture(dd_path, Inches(6.7), Inches(1.4), Inches(5.5), Inches(3.0))

    # Analytical Findings Card
    dyn_card = add_card(s13, Inches(1.0), Inches(4.55), Inches(11.2), Inches(1.85))
    tf_dyn = dyn_card.text_frame
    tf_dyn.word_wrap = True
    p0 = tf_dyn.paragraphs[0]
    p0.text = "Macroeconomic Stress Cycle Breakdown:"
    p0.font.name = "Bookman Old Style"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_MAROON
    p0.space_after = Pt(4)

    add_bullet_point(tf_dyn, "• March 2020 COVID Shock:",
                     "QuantNiti GMM detected high-volatility regime, rotating capital into defensive cash/gold buffers. Sustained only -9.1% drawdown vs. -38.4% collapse in NIFTY 50.",
                     font_size=11.5, space_after=4)
    add_bullet_point(tf_dyn, "• 2022 Inflationary Bear Cycle:",
                     "Captured sector rotation into defensive value equities, protecting gains while classical MVO suffered severe whipsaws (-28.6% MDD).",
                     font_size=11.5, space_after=4)
    add_bullet_point(tf_dyn, "• 2023–2025 Structural Bull Expansion:",
                     "Dynamic regime adaptation rotated exposure into high-momentum equities, compounding upside alpha to reach 18.4% CAGR.",
                     font_size=11.5, space_after=4)

    # =========================================================================
    # SLIDE 14: Demonstration Snapshots (Part I) - Production UI & Workflow
    # =========================================================================
    print("Building Slide 14: Demonstration Snapshots (Part I)...")
    s14 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s14, "Demonstration Snapshots: Multi-Device Production UI", 14, logo_path)

    # 4 Mobile Screen Pictures
    img_names = ["image11.png", "image12.png", "image13.png", "image14.png"]
    captions = [
        "1. Onboarding & Risk Persona",
        "2. Capital Budget & Horizon",
        "3. Donut & Whole Shares",
        "4. Live Portfolio Tracker"
    ]
    for idx, (img_n, cap) in enumerate(zip(img_names, captions)):
        i_path = os.path.join(EXTRACTED_DIR, img_n)
        if os.path.exists(i_path):
            s14.shapes.add_picture(i_path, Inches(1.0 + idx * 2.85), Inches(1.4), Inches(2.65), Inches(4.6))
        # Add small caption below
        cap_box = s14.shapes.add_textbox(Inches(1.0 + idx * 2.85), Inches(6.05), Inches(2.65), Inches(0.4))
        p = cap_box.text_frame.paragraphs[0]
        p.text = cap
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Times New Roman"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_MAROON

    # =========================================================================
    # SLIDE 15: Demonstration Snapshots (Part II) - XAI Trust Card & NitiBot
    # =========================================================================
    print("Building Slide 15: Demonstration Snapshots (Part II - XAI & NitiBot)...")
    s15 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s15, "Explainable AI: The 4-Pillar Trust Card & NitiBot Copilot", 15, logo_path)

    # Left: Trust Card Explanation
    tc_card = add_card(s15, Inches(1.0), Inches(1.45), Inches(5.4), Inches(4.9))
    tf_tc = tc_card.text_frame
    tf_tc.word_wrap = True
    p_tc = tf_tc.paragraphs[0]
    p_tc.text = "THE 4-PILLAR EXPLAINABLE TRUST CARD"
    p_tc.font.name = "Bookman Old Style"
    p_tc.font.size = Pt(14)
    p_tc.font.bold = True
    p_tc.font.color.rgb = COLOR_MAROON
    p_tc.space_after = Pt(10)

    trust_pillars = [
        ("1. Regime Context", "Active state (e.g. Bull) transparently justifies momentum factor tilt over defensives."),
        ("2. Empirical Reliability", "5-Year Historical Directional Hit Rate disclosed to retail user (64.2% 1M, 71.8% 6M)."),
        ("3. Stress Drawdown Bound", "Simulated maximum loss bound calculated and presented (-12.4% vs -28.6% classical MVO)."),
        ("4. Disintermediation Value", "Explicit quantification of ₹72,400+ saved over 10Y vs. 2% bank advisory fees."),
    ]
    for p_name, p_desc in trust_pillars:
        add_bullet_point(tf_tc, f"• {p_name}:", p_desc, font_size=11.5, space_after=8)

    # Right: NitiBot UI Picture & Explanations
    bot_img_path = os.path.join(EXTRACTED_DIR, "image15.png")
    if os.path.exists(bot_img_path):
        s15.shapes.add_picture(bot_img_path, Inches(6.8), Inches(1.45), Inches(5.4), Inches(2.9))

    bot_card = add_card(s15, Inches(6.8), Inches(4.45), Inches(5.4), Inches(1.9))
    tf_bot = bot_card.text_frame
    tf_bot.word_wrap = True
    p_b0 = tf_bot.paragraphs[0]
    p_b0.text = "NitiBot RAG Conversational Copilot:"
    p_b0.font.name = "Bookman Old Style"
    p_b0.font.size = Pt(13)
    p_b0.font.bold = True
    p_b0.font.color.rgb = COLOR_MAROON
    p_b0.space_after = Pt(4)

    add_bullet_point(tf_bot, "• Google Gemini 2.5 Flash:", "Grounded in local portfolio weights, GMM regime, and backtest logs.", font_size=11, space_after=4)
    add_bullet_point(tf_bot, "• Zero Hallucination:", "Mathematical fact-checker prevents fabricated financial advice.", font_size=11, space_after=4)
    add_bullet_point(tf_bot, "• Regulatory Compliance:", "Hard-coded statutory SEBI disclaimers on every recommendation.", font_size=11, space_after=4)

    # =========================================================================
    # SLIDE 16: Future Work & Conclusion
    # =========================================================================
    print("Building Slide 16: Future Work & Conclusion...")
    s16 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s16, "Conclusion & Future Roadmap", 16, logo_path)

    # Left Column: Conclusion & Deliverables Completed
    conc_card = add_card(s16, Inches(1.0), Inches(1.5), Inches(5.4), Inches(4.8))
    tf_c = conc_card.text_frame
    tf_c.word_wrap = True
    p_c0 = tf_c.paragraphs[0]
    p_c0.text = "Phase II Project Deliverables Completed:"
    p_c0.font.name = "Bookman Old Style"
    p_c0.font.size = Pt(15)
    p_c0.font.bold = True
    p_c0.font.color.rgb = COLOR_MAROON
    p_c0.space_after = Pt(10)

    deliverables = [
        "• Successfully designed, implemented, and empirically verified an AI-driven regime-adaptive quantitative intelligence platform.",
        "• Solved the Markowitz covariance inversion singularity using Ledoit-Wolf optimal shrinkage and Hierarchical Risk Parity (HRP).",
        "• Formulated a greedy whole-share integer knapsack allocator (n_i ∈ ℤ⁺) for retail capital budgets down to ₹5,000.",
        "• Verified system robustness across 504 full-stack automated tests (99% backend test coverage) and 8 years of historical stress backtesting.",
        "• Delivered +530 bps annual alpha over NIFTY 50 and reduced maximum drawdown by 67.7% at 0% advisory fee.",
    ]
    for d in deliverables:
        p = tf_c.add_paragraph()
        p.text = d
        p.font.name = "Times New Roman"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(8)

    # Right Column: Future Roadmap
    road_card = add_card(s16, Inches(6.8), Inches(1.5), Inches(5.4), Inches(4.8))
    tf_rd = road_card.text_frame
    tf_rd.word_wrap = True
    p_rd0 = tf_rd.paragraphs[0]
    p_rd0.text = "Production Future Roadmap:"
    p_rd0.font.name = "Bookman Old Style"
    p_rd0.font.size = Pt(15)
    p_rd0.font.bold = True
    p_rd0.font.color.rgb = COLOR_MAROON
    p_rd0.space_after = Pt(10)

    roadmap_items = [
        ("• Broker API Execution:", "Automated zero-click order execution via Zerodha Kite Connect, Upstox, and Groww Trade APIs upon explicit user consent."),
        ("• Multilingual Localization:", "Extending NitiBot conversational engine and microlearning cards to Hindi, Kannada, and Tamil for tier-2/3 retail investors."),
        ("• Universe Expansion:", "Incorporating Sovereign Gold Bonds (SGBs), REITs, InvITs, and NIFTY Midcap 150 equity universe."),
        ("• Automated Tax-Loss Harvesting:", "Dynamic STCG and LTCG tax optimization engine adhering to Indian Union Budget tax slabs."),
    ]
    for r_head, r_body in roadmap_items:
        add_bullet_point(tf_rd, r_head, r_body, font_size=12, space_after=10)

    # =========================================================================
    # SLIDE 17: Academic References
    # =========================================================================
    print("Building Slide 17: Academic References...")
    s17 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s17, "Academic References", 17, logo_path)

    ref_card = add_card(s17, Inches(1.0), Inches(1.45), Inches(11.2), Inches(4.9))
    tf_ref = ref_card.text_frame
    tf_ref.word_wrap = True

    sections = [
        ("Journal Papers:", [
            "[1] K. Alam, M. H. Bhuiyan, I. U. Haque, M. F. Monir, and T. Ahmed, \"Enhancing Stock Market Prediction: A Robust LSTM-DNN Model Analysis on 26 Real-Life Datasets\", in IEEE Access, ISSN: 2169-3536, Vol-12, pp. 45210-45228, July 2024.",
            "[2] M. Wang, Y. H. Lin, and I. Mikhelson, \"Regime-Switching Factor Investing with Hidden Markov Models\", in Journal of Risk and Financial Management, ISSN: 1911-8074, Vol-15, Issue-11, pp. 1-19, November 2022.",
        ]),
        ("Conference Paper:", [
            "[3] S. Mehtab and J. Sen, \"Stock Price Prediction Using CNN and LSTM-Based Deep Learning Models\", International Conference on Decision Aid Sciences and Applications (DASA 2020), University of Bahrain, Sakheer, Bahrain, November 8th and 9th 2020.",
        ]),
        ("Book:", [
            "[4] \"Advances in Financial Machine Learning\", Marcos López de Prado, John Wiley & Sons Inc., published: 2018.",
        ]),
        ("Regulatory & Industry Reports:", [
            "[5] Securities and Exchange Board of India (SEBI), \"Study on Retail Trader Performance in Equity Markets\", Reports and Statistics, https://www.sebi.gov.in/reports-and-statistics/",
            "[6] National Centre for Financial Education (NCFE), \"Financial Literacy and Inclusion Survey (NCFE-FLIS) Benchmark Report\", https://www.ncfe.org.in/reports/",
        ]),
    ]

    p_first = tf_ref.paragraphs[0]
    p_first.text = sections[0][0]
    p_first.font.name = "Bookman Old Style"
    p_first.font.size = Pt(13)
    p_first.font.bold = True
    p_first.font.color.rgb = COLOR_MAROON
    p_first.space_after = Pt(2)
    for ref in sections[0][1]:
        p = tf_ref.add_paragraph()
        p.text = ref
        p.font.name = "Times New Roman"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(4)

    for sec_title, sec_refs in sections[1:]:
        p_h = tf_ref.add_paragraph()
        p_h.text = sec_title
        p_h.font.name = "Bookman Old Style"
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_MAROON
        p_h.space_before = Pt(4)
        p_h.space_after = Pt(2)
        for ref in sec_refs:
            p = tf_ref.add_paragraph()
            p.text = ref
            p.font.name = "Times New Roman"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(4)

    # Save PPTX
    print(f"Saving finalized presentation to: {TARGET_PPTX}...")
    prs.save(TARGET_PPTX)
    print(f"Successfully generated {TARGET_PPTX} with {len(prs.slides)} slides!")


def export_pdf_and_images():
    """Exports PPTX to PDF and high-res PNG slide gallery via PowerPoint COM."""
    print("Initializing PowerPoint COM Automation for PDF and PNG export...")
    try:
        import win32com.client
        ppt = win32com.client.Dispatch("PowerPoint.Application")
        prs_com = ppt.Presentations.Open(TARGET_PPTX, WithWindow=False)

        # Export to PDF (Format type 32 = ppSaveAsPDF)
        print(f"Exporting presentation to PDF: {TARGET_PDF}...")
        prs_com.SaveAs(TARGET_PDF, 32)
        print("PDF export complete!")

        # Export slide images
        os.makedirs(SLIDES_PNG_DIR, exist_ok=True)
        print(f"Exporting 1080p slide images to: {SLIDES_PNG_DIR}...")
        for i in range(1, prs_com.Slides.Count + 1):
            slide_img_path = os.path.join(SLIDES_PNG_DIR, f"Slide{i}.PNG")
            prs_com.Slides(i).Export(slide_img_path, "PNG", 1920, 1080)
            print(f"  Slide {i} exported -> {slide_img_path}")

        prs_com.Close()
        ppt.Quit()
        print("PowerPoint COM export completed successfully!")
    except Exception as e:
        print(f"Error during PowerPoint COM export: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    build_presentation()
    export_pdf_and_images()
