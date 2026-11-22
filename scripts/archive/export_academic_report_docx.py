# -*- coding: utf-8 -*-
"""
Exports the complete 15,500+ word QuantNiti Academic Report from HTML into 
docs/academic_docs/QuantNiti_Major_Project_Phase_II_Report.docx
Adheres strictly to VTU / KSIT guidelines:
- Times New Roman throughout
- 1.5 line spacing, justified body (12pt)
- Heading hierarchy: 18pt / 16pt / 14pt / 12pt Bold
- Formatted native Word tables with header shading
- Figure placeholders and captions
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from bs4 import BeautifulSoup, NavigableString, Tag

TEMPLATE_PATH = "docs/academic_docs/templates/project_report_template.docx"
HTML_PATH = "docs/academic_docs/project_phase_2_report/QuantNiti_Academic_Report.html"
OUTPUT_PATH = "docs/academic_docs/QuantNiti_Major_Project_Phase_II_Report.docx"

def set_run_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color

def style_paragraph(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.5):
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing

def add_inline_runs(paragraph, element, base_size=12, default_bold=False, default_italic=False, default_color=None):
    for child in element.contents:
        if isinstance(child, NavigableString):
            text = str(child)
            if text:
                r = paragraph.add_run(text)
                set_run_font(r, size=base_size, bold=default_bold, italic=default_italic, color=default_color)
        elif isinstance(child, Tag):
            is_bold = default_bold or child.name in ['b', 'strong']
            is_italic = default_italic or child.name in ['i', 'em']
            # Recurse for nested tags
            for sub in child.contents:
                if isinstance(sub, NavigableString):
                    text = str(sub)
                    if text:
                        r = paragraph.add_run(text)
                        set_run_font(r, size=base_size, bold=is_bold, italic=is_italic, color=default_color)
                elif isinstance(sub, Tag):
                    sub_bold = is_bold or sub.name in ['b', 'strong']
                    sub_italic = is_italic or sub.name in ['i', 'em']
                    r = paragraph.add_run(sub.get_text())
                    set_run_font(r, size=base_size, bold=sub_bold, italic=sub_italic, color=default_color)

def main():
    print(f"Loading template from {TEMPLATE_PATH}...")
    doc = docx.Document(TEMPLATE_PATH)

    # 1. Update front matter metadata in existing template paragraphs
    print("Populating front matter metadata...")
    project_title = "QUANTNITI: AN INSTITUTIONAL-GRADE REGIME-ADAPTIVE PORTFOLIO INTELLIGENCE, QUANTITATIVE OPTIMIZATION, AND WEALTH COMPOUNDING PLATFORM FOR RETAIL INVESTORS"
    students_text = "ARYAMAN TIWARI (1KS21CS023)\nCHIRAG T (1KS21CS035)\nDURGASHREE M (1KS21CS043)\nJAYADITYA DEV (1KS21CS054)"

    for p in doc.paragraphs:
        if "PROJECT TITLE" in p.text:
            p.text = p.text.replace("PROJECT TITLE", project_title)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                set_run_font(r, size=14, bold=True)
        if "STUDENT NAME 1" in p.text:
            p.text = students_text
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                set_run_font(r, size=11, bold=True)
        if "Guide Name" in p.text:
            p.text = p.text.replace("Guide Name", "Mrs. Beena K").replace("Designation", "Assistant Professor")
            for r in p.runs:
                set_run_font(r, size=11, bold=True)

    # 2. Trim template placeholder text starting after the preliminary pages (from Chapter 1)
    cut_idx = None
    for idx, p in enumerate(doc.paragraphs):
        if ("Chapter 1" in p.text or "INTRODUCTION" in p.text) and idx > 35:
            cut_idx = idx
            break

    if cut_idx is not None:
        p_elements = [p._p for p in doc.paragraphs[cut_idx:]]
        for pe in p_elements:
            pe.getparent().remove(pe)
        print(f"Trimmed {len(p_elements)} template placeholder paragraphs.")

    # 3. Parse HTML content
    print(f"Reading full report HTML from {HTML_PATH}...")
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    body = soup.find("body")
    if not body:
        print("Error: <body> not found in HTML!")
        return

    print("Converting report chapters, sections, tables, and figures into Word document...")
    
    # Process top-level children in body
    for element in body.children:
        if isinstance(element, NavigableString):
            continue
        if not isinstance(element, Tag):
            continue

        classes = element.get("class", [])

        # Page Break
        if "page-break" in classes:
            doc.add_page_break()
            continue

        # Chapter Number (16pt bold, left-aligned)
        if "chapter-no" in classes:
            p = doc.add_paragraph()
            style_paragraph(p, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=18, space_after=2, line_spacing=1.0)
            r = p.add_run(element.get_text().strip())
            set_run_font(r, size=16, bold=True)
            continue

        # Chapter Title (18pt bold, centered, uppercase)
        if "chapter-name" in classes:
            p = doc.add_paragraph()
            style_paragraph(p, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=18, line_spacing=1.15)
            r = p.add_run(element.get_text().strip().upper())
            set_run_font(r, size=18, bold=True)
            continue

        # Main Sub-heading Level 1 (14pt bold, left-aligned)
        if element.name == "h2" or "sub-heading" in classes:
            p = doc.add_paragraph()
            style_paragraph(p, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6, line_spacing=1.15)
            r = p.add_run(element.get_text().strip())
            set_run_font(r, size=14, bold=True)
            continue

        # Inner Sub-heading Level 2 (12pt bold, left-aligned)
        if element.name == "h3" or "inner-heading" in classes:
            p = doc.add_paragraph()
            style_paragraph(p, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, line_spacing=1.15)
            r = p.add_run(element.get_text().strip())
            set_run_font(r, size=12, bold=True)
            continue

        # Standard Paragraph (12pt, 1.5 spacing, justified)
        if element.name == "p":
            text = element.get_text().strip()
            if not text:
                continue

            # Check if this is a figure placeholder block
            if text.startswith("[Figure") or text.startswith("[Fig."):
                p = doc.add_paragraph()
                style_paragraph(p, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=8, line_spacing=1.15)
                r = p.add_run(text)
                set_run_font(r, size=11, bold=True, color=RGBColor(128, 0, 0))
                continue

            p = doc.add_paragraph()
            style_paragraph(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.5)
            add_inline_runs(p, element, base_size=12)
            continue

        # Lists (ul, ol)
        if element.name in ["ul", "ol"]:
            is_ordered = (element.name == "ol")
            for idx, li in enumerate(element.find_all("li", recursive=False)):
                p = doc.add_paragraph()
                style_paragraph(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3, line_spacing=1.5)
                p.paragraph_format.left_indent = Inches(0.35)
                
                # Bullet or number prefix
                prefix = f"{idx + 1}. " if is_ordered else "•  "
                r_pre = p.add_run(prefix)
                set_run_font(r_pre, size=12, bold=True)
                
                add_inline_runs(p, li, base_size=12)
            continue

        # Tables
        if element.name == "table":
            rows = element.find_all("tr")
            if not rows:
                continue
            
            # Determine num columns
            first_row_cells = rows[0].find_all(["th", "td"])
            num_cols = len(first_row_cells)
            if num_cols == 0:
                continue

            table = doc.add_table(rows=0, cols=num_cols)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = True

            for r_idx, row in enumerate(rows):
                cells = row.find_all(["th", "td"])
                if len(cells) != num_cols:
                    continue
                
                row_cells = table.add_row().cells
                is_header = (r_idx == 0 or bool(row.find_all("th")))

                for c_idx, cell in enumerate(cells):
                    cell_text = cell.get_text().strip()
                    row_cells[c_idx].text = cell_text
                    
                    # Styling background
                    if is_header:
                        shd_color = "800000"  # KSIT Maroon
                        text_color = RGBColor(255, 255, 255)
                        text_bold = True
                    else:
                        shd_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
                        text_color = RGBColor(17, 17, 17)
                        text_bold = (c_idx == 0 and num_cols > 3)

                    shading = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), shd_color))
                    row_cells[c_idx]._tc.get_or_add_tcPr().append(shading)

                    p = row_cells[c_idx].paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_header or c_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_before = Pt(3)
                    p.paragraph_format.space_after = Pt(3)
                    p.paragraph_format.line_spacing = 1.15
                    for r in p.runs:
                        set_run_font(r, size=9.5 if is_header else 9.0, bold=text_bold, color=text_color)
            
            # Add small spacing after table
            p_spacer = doc.add_paragraph()
            style_paragraph(p_spacer, space_before=0, space_after=8, line_spacing=1.0)
            continue

    print(f"Saving compiled final DOCX to {OUTPUT_PATH}...")
    doc.save(OUTPUT_PATH)
    print("Done! Generated QuantNiti_Major_Project_Phase_II_Report.docx successfully.")

if __name__ == "__main__":
    main()
