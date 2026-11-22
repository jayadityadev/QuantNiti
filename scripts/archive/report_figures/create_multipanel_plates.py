"""
Combine individual QuantNiti UI snapshots into high-density 2x2 and 1x2 multi-panel layout plates
for the academic monograph report.
Outputs 300 DPI composite plates to:
- docs/academic_docs/figures/
- docs/academic_docs/report_latex/figures/
"""

import os
from PIL import Image, ImageDraw, ImageFont

FIG_DIR = "docs/academic_docs/figures"
LATEX_FIG_DIR = "docs/academic_docs/report_latex/figures"

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(LATEX_FIG_DIR, exist_ok=True)

BORDER_COLOR = (226, 232, 240) # Slate 200
BG_COLOR = (255, 255, 255)
LABEL_BG = (15, 23, 42) # Slate 900
LABEL_TEXT = (255, 255, 255)


def add_panel_label(img: Image.Image, label: str) -> Image.Image:
    """Add a clean, modern panel badge (e.g. 'Panel A: Behavioral Quiz') to top-left of image."""
    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    # Try default or standard font
    try:
        font = ImageFont.truetype("arial.ttf", 26)
    except Exception:
        font = ImageFont.load_default()
        
    pad = 12
    margin = 16
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    badge_rect = [margin, margin, margin + tw + pad * 2, margin + th + pad * 2]
    # Draw dark rounded badge
    draw.rounded_rectangle(badge_rect, radius=8, fill=(15, 23, 42, 230), outline=(255, 255, 255, 200), width=2)
    draw.text((margin + pad, margin + pad - 2), label, fill=(255, 255, 255, 255), font=font)
    return img.convert("RGB")


def make_2x2_plate(img_paths, labels, out_name, target_cell_size=(1200, 750)):
    """Combine 4 images into a 2x2 grid with consistent sizing and outer frame."""
    cw, ch = target_cell_size
    gap = 24
    outer_pad = 20
    
    total_w = outer_pad * 2 + cw * 2 + gap
    total_h = outer_pad * 2 + ch * 2 + gap
    
    plate = Image.new("RGB", (total_w, total_h), BG_COLOR)
    draw = ImageDraw.Draw(plate)
    
    positions = [
        (outer_pad, outer_pad),
        (outer_pad + cw + gap, outer_pad),
        (outer_pad, outer_pad + ch + gap),
        (outer_pad + cw + gap, outer_pad + ch + gap)
    ]
    
    for i in range(4):
        p = os.path.join(FIG_DIR, img_paths[i])
        if not os.path.exists(p):
            print(f"Warning: {p} missing!")
            continue
        im = Image.open(p)
        # Fit into cell keeping aspect ratio or centered crop
        im.thumbnail((cw, ch), Image.Resampling.LANCZOS)
        
        # Center in cell box
        cell_box = Image.new("RGB", (cw, ch), (248, 250, 252))
        cx = (cw - im.width) // 2
        cy = (ch - im.height) // 2
        cell_box.paste(im, (cx, cy))
        
        # Add badge
        labeled = add_panel_label(cell_box, labels[i])
        
        # Draw subtle border around cell
        cdraw = ImageDraw.Draw(labeled)
        cdraw.rectangle([0, 0, cw - 1, ch - 1], outline=BORDER_COLOR, width=2)
        
        plate.paste(labeled, positions[i])
        
    for d in [FIG_DIR, LATEX_FIG_DIR]:
        out_path = os.path.join(d, out_name)
        plate.save(out_path, dpi=(300, 300), quality=95)
        print(f"Saved {out_path}")


def make_1x2_plate(img_paths, labels, out_name, target_cell_size=(1200, 1000)):
    """Combine 2 tall images side-by-side."""
    cw, ch = target_cell_size
    gap = 24
    outer_pad = 20
    
    total_w = outer_pad * 2 + cw * 2 + gap
    total_h = outer_pad * 2 + ch
    
    plate = Image.new("RGB", (total_w, total_h), BG_COLOR)
    
    positions = [
        (outer_pad, outer_pad),
        (outer_pad + cw + gap, outer_pad)
    ]
    
    for i in range(2):
        p = os.path.join(FIG_DIR, img_paths[i])
        if not os.path.exists(p):
            print(f"Warning: {p} missing!")
            continue
        im = Image.open(p)
        im.thumbnail((cw, ch), Image.Resampling.LANCZOS)
        
        cell_box = Image.new("RGB", (cw, ch), (248, 250, 252))
        cx = (cw - im.width) // 2
        cy = (ch - im.height) // 2
        cell_box.paste(im, (cx, cy))
        
        labeled = add_panel_label(cell_box, labels[i])
        cdraw = ImageDraw.Draw(labeled)
        cdraw.rectangle([0, 0, cw - 1, ch - 1], outline=BORDER_COLOR, width=2)
        
        plate.paste(labeled, positions[i])
        
    for d in [FIG_DIR, LATEX_FIG_DIR]:
        out_path = os.path.join(d, out_name)
        plate.save(out_path, dpi=(300, 300), quality=95)
        print(f"Saved {out_path}")


if __name__ == "__main__":
    print("Generating composite multi-panel snapshot plates...")
    
    # Plate 1: Onboarding, Regime Radar, Grow Input, Allocation
    make_2x2_plate(
        [
            "fig7_1_onboarding_quiz.png",
            "fig7_2_regime_radar.png",
            "fig7_3_grow_step1_capital.png",
            "fig7_4_allocation_results.png"
        ],
        [
            "(a) Behavioral Scenario Quiz",
            "(b) Real-Time Regime Radar",
            "(c) Guided Grow Capital Input",
            "(d) Discrete Knapsack Allocation"
        ],
        "fig7_plate1_onboarding_allocation.png"
    )
    
    # Plate 2: Trust Card, Explore Stocks, Portfolio Tracker, Compounding
    make_2x2_plate(
        [
            "fig7_5_trust_card.png",
            "fig7_6_explore_stocks.png",
            "fig7_7_portfolio_tracking.png",
            "fig7_10_compounding_trajectory.png"
        ],
        [
            "(a) 4-Pillar Explainable Trust Card",
            "(b) Stock Intelligence & Regime Badges",
            "(c) Mark-to-Market Portfolio Tracking",
            "(d) 10-Year Compounding Wealth Cones"
        ],
        "fig7_plate2_transparency_tracking.png"
    )
    
    # Plate 3: NitiBot Copilot & Stock Profile
    make_1x2_plate(
        [
            "fig7_8_nitibot_sheet.png",
            "fig7_9_stock_profile.png"
        ],
        [
            "(a) Context-Grounded NitiBot Copilot",
            "(b) 360-Degree Stock Intelligence"
        ],
        "fig7_plate3_copilot_profile.png",
        target_cell_size=(1000, 1100)
    )
    
    print("Multi-panel plates generated successfully!")
