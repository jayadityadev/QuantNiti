import os
import re
import time
import markdown
from playwright.sync_api import sync_playwright

MD_PATH = os.path.abspath(r"docs\QUANTNITI_MASTER_EXHIBITION_DOCUMENT.md")
HTML_PATH = os.path.abspath(r"docs\QUANTNITI_MASTER_EXHIBITION_DOCUMENT.html")
PDF_PATH = os.path.abspath(r"docs\QUANTNITI_MASTER_EXHIBITION_DOCUMENT.pdf")

def read_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def convert_md_to_html(md_content):
    # Protect LaTeX math blocks from markdown processing
    math_blocks = []
    
    def save_display_math(match):
        math_blocks.append(match.group(0))
        return f"<!--MATH_DISPLAY_{len(math_blocks)-1}-->"

    def save_inline_math(match):
        math_blocks.append(match.group(0))
        return f"<!--MATH_INLINE_{len(math_blocks)-1}-->"

    # Display math: $$ ... $$
    content = re.sub(r"\$\$(.*?)\$\$", save_display_math, md_content, flags=re.DOTALL)
    # Inline math: $ ... $ (avoid matching $$ or escaped \$)
    content = re.sub(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", save_inline_math, content)

    # Convert markdown to HTML with tables, code, and header anchors
    raw_html = markdown.markdown(
        content,
        extensions=["tables", "fenced_code", "nl2br", "toc", "attr_list"]
    )

    # Restore protected math
    for idx, block in enumerate(math_blocks):
        raw_html = raw_html.replace(f"&lt;!--MATH_DISPLAY_{idx}--&gt;", block)
        raw_html = raw_html.replace(f"<!--MATH_DISPLAY_{idx}-->", block)
        raw_html = raw_html.replace(f"&lt;!--MATH_INLINE_{idx}--&gt;", block)
        raw_html = raw_html.replace(f"<!--MATH_INLINE_{idx}-->", block)

    # Enhance blockquotes and styling
    # Convert alert blockquotes into styled alert cards
    raw_html = re.sub(
        r"<blockquote>\s*<p>\s*🌟\s*<strong>The &quot;Kid-Friendly&quot; Story",
        r'<blockquote class="kid-story"><p>🌟 <strong>The "Kid-Friendly" Story',
        raw_html
    )

    return raw_html

def generate_full_html(body_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>QuantNiti — Project Exhibition Master Dossier</title>
<!-- MathJax for rendering LaTeX formulas -->
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true,
    processEnvironments: true
  }},
  options: {{
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }},
  startup: {{
    pageReady: () => {{
      return MathJax.startup.defaultPageReady();
    }}
  }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<style>
  @page {{
    size: A4 portrait;
    margin-top: 18mm;
    margin-bottom: 20mm;
    margin-left: 16mm;
    margin-right: 16mm;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 9.8pt;
    line-height: 1.55;
    color: #1E293B;
    background-color: #FFFFFF;
    margin: 0;
    padding: 0;
  }}

  /* Headings Hierarchy */
  h1 {{
    font-size: 19pt;
    font-weight: 800;
    color: #0F172A;
    border-bottom: 2.5px solid #7C3AED;
    padding-bottom: 6px;
    margin-top: 32px;
    margin-bottom: 14px;
    page-break-after: avoid;
  }}

  /* Page breaks before top-level numbered chapters */
  h1:not(:first-of-type) {{
    page-break-before: always;
  }}

  h2 {{
    font-size: 13.5pt;
    font-weight: 700;
    color: #1E1B4B;
    margin-top: 22px;
    margin-bottom: 10px;
    border-left: 4px solid #6366F1;
    padding-left: 10px;
    page-break-after: avoid;
  }}

  h3 {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #334155;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}

  h4 {{
    font-size: 10.2pt;
    font-weight: 600;
    color: #475569;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 9pt;
    text-align: justify;
  }}

  /* Strong / Bold */
  strong {{
    font-weight: 700;
    color: #0F172A;
  }}

  /* Kid Story Card Styling */
  blockquote.kid-story, blockquote {{
    background: #FAF5FF;
    border-left: 4.5px solid #8B5CF6;
    border-radius: 0 10px 10px 0;
    margin: 12pt 0;
    padding: 10pt 14pt;
    color: #3B0764;
    font-size: 9.5pt;
    line-height: 1.5;
    page-break-inside: avoid;
  }}

  blockquote p {{
    margin-bottom: 4pt;
  }}

  blockquote p:last-child {{
    margin-bottom: 0;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }}

  table, th, td {{
    border: 1px solid #CBD5E1;
  }}

  th {{
    background-color: #1E1B4B;
    color: #FFFFFF;
    font-weight: 600;
    text-align: left;
    padding: 6pt 8pt;
    letter-spacing: 0.3px;
  }}

  td {{
    padding: 5pt 7pt;
    vertical-align: top;
    background-color: #FFFFFF;
  }}

  tr:nth-child(even) td {{
    background-color: #F8FAFC;
  }}

  /* Code & Preformatted */
  pre {{
    background-color: #0F172A;
    color: #F8FAFC;
    padding: 10pt;
    border-radius: 8px;
    overflow-x: auto;
    font-family: "Cascadia Code", "Fira Code", Consolas, Courier, monospace;
    font-size: 8.2pt;
    line-height: 1.45;
    margin: 10pt 0;
    page-break-inside: avoid;
  }}

  code {{
    font-family: "Cascadia Code", "Fira Code", Consolas, Courier, monospace;
    font-size: 8.8pt;
    background-color: #F1F5F9;
    color: #6D28D9;
    padding: 1.5px 4px;
    border-radius: 4px;
    border: 1px solid #E2E8F0;
  }}

  pre code {{
    background-color: transparent;
    color: inherit;
    border: none;
    padding: 0;
  }}

  /* Lists */
  ul, ol {{
    margin-top: 0;
    margin-bottom: 9pt;
    padding-left: 20px;
  }}

  li {{
    margin-bottom: 3.5pt;
  }}

  /* Horizontal Rules */
  hr {{
    border: none;
    border-top: 1.5px solid #E2E8F0;
    margin: 16pt 0;
  }}

  /* Header Badge Container */
  .meta-card {{
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
    color: #FFFFFF;
    padding: 18pt 20pt;
    border-radius: 12px;
    margin-bottom: 18pt;
    border: 1px solid #4338CA;
  }}

  .meta-card h1 {{
    color: #FFFFFF;
    border-bottom: 2px solid #8B5CF6;
    margin-top: 0;
    font-size: 21pt;
  }}

  .meta-card p {{
    color: #E0E7FF;
    font-size: 9.6pt;
    margin-bottom: 4pt;
  }}

  /* Badges */
  .badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 7.8pt;
    font-weight: bold;
    text-transform: uppercase;
  }}
  .badge-bull {{ background: #DCFCE7; color: #15803D; }}
  .badge-bear {{ background: #FEE2E2; color: #B91C1C; }}
  .badge-flat {{ background: #FEF3C7; color: #B45309; }}

  /* MathJax alignment & sizing */
  .mjx-chtml {{
    font-size: 100% !important;
  }}

  /* Q&A section styling */
  h3:has(+ ul) {{
    page-break-after: avoid;
  }}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

def main():
    print("Reading master markdown file...")
    md_content = read_markdown(MD_PATH)
    
    print("Converting Markdown to HTML with math preservation...")
    body_html = convert_md_to_html(md_content)
    full_html = generate_full_html(body_html)
    
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Saved styled HTML to {HTML_PATH}")
    
    print("Launching Playwright Chromium to render publication-grade PDF...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        file_url = f"file:///{HTML_PATH.replace(os.sep, '/')}"
        print(f"Loading {file_url}...")
        page.goto(file_url, wait_until="networkidle")
        
        # Wait for MathJax to finish typesetting
        print("Waiting for MathJax to finish rendering LaTeX...")
        try:
            page.wait_for_function(
                "() => window.MathJax && window.MathJax.startup && window.MathJax.startup.promise",
                timeout=15000
            )
            # Give MathJax 2 seconds to settle all SVG/CHTML layout
            time.sleep(2)
        except Exception as e:
            print("Note: MathJax wait timed out or completed early:", e)
            time.sleep(3)
            
        print("Printing to PDF with high-resolution layout...")
        page.pdf(
            path=PDF_PATH,
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template='''
                <div style="font-size: 7.5pt; color: #94A3B8; width: 100%; text-align: right; padding-right: 16mm; font-family: -apple-system, sans-serif;">
                    QuantNiti (क्वान्टनीति) — Project Exhibition Master Dossier
                </div>
            ''',
            footer_template='''
                <div style="font-size: 7.5pt; color: #94A3B8; width: 100%; display: flex; justify-content: space-between; padding-left: 16mm; padding-right: 16mm; font-family: -apple-system, sans-serif;">
                    <span>K.S. Institute of Technology, Bengaluru • Dept. of CSE • BCS786</span>
                    <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
                </div>
            ''',
            margin={
                "top": "18mm",
                "bottom": "20mm",
                "left": "16mm",
                "right": "16mm"
            }
        )
        browser.close()

    if os.path.exists(PDF_PATH):
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"SUCCESS! Master PDF generated: {PDF_PATH} ({size_kb:.1f} KB)")
    else:
        print("ERROR: PDF was not generated.")

if __name__ == "__main__":
    main()
