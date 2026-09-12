---
name: paper-builder
description: Build publication-grade, codebase-grounded academic research papers (IEEE conference/transactions, ACM, NeurIPS) from any project codebase. Generates reproducible vector figures, full LaTeX source, BibTeX references, and enforces strict page budgets through visual PDF smoke-testing.
---

# Paper Builder: End-to-End Academic Research Paper Engineering

Use this skill when tasked with writing, refining, formatting, or updating a publication-grade academic research paper for a codebase or project.

---

## Core Process Lifecycle

```
[Phase 1: Codebase Ground Truth] ──> [Phase 2: Literature & BibTeX] ──> [Phase 3: Reproducible Figures]
                                                                                   │
[Phase 6: Clean Git Hygiene]     <── [Phase 5: Visual Smoke-Test]    <── [Phase 4: LaTeX Engineering]
```

---

### Phase 1: Deep Codebase Ground-Truth Extraction (Any Repository Layout)

Never invent theoretical claims, extrapolate unverifiable capabilities, or rely solely on high-level documentation. Repositories will not always follow clean `src/` conventions; they may be flat root directories, monorepos (`packages/*`, `apps/*`, `libs/*`), data science projects centered around exploratory notebooks (`notebooks/`, `experiments/`), or legacy, cluttered directories with mixed files and scripts.

Extract the paper's foundations directly from code reality using this triage hierarchy:

1. **Agnostic Structure & Manifest Triage:**
   - Inspect build manifests and dependency files (`pyproject.toml`, `setup.py`, `package.json`, `Cargo.toml`, `go.mod`, `CMakeLists.txt`, `Makefile`, `Dockerfile`) to identify project name, dependencies, entry points, and module hierarchies.
   - If a knowledge graph or community map exists (e.g. `graphify-out/`), query high-centrality "god nodes" and key concepts first to cut through repository noise.
   - If the repo is flat or cluttered, use pattern search across code extensions (`*.py`, `*.ts`, `*.cpp`, `*.rs`, `*.go`, `*.jl`, `*.ipynb`) to locate core logic, algorithms, and evaluation scripts.
2. **Algorithmic Core Discovery:**
   - Locate and inspect production implementations wherever they live to uncover objective functions, loss formulations, statistical regularizations (e.g. shrinkage, Kalman filters, clustering, convex/discrete optimization), and constraints.
   - Transcribe mathematical formulations into clean, standard academic notation.
3. **Empirical Validation & Evidence Triangulation:**
   - In cluttered or data-science codebases, ground-truth metrics may reside in evaluation scripts (`eval_*.py`), Jupyter notebook outputs (`.ipynb`), benchmark logs, or artifact files (`results/`, `logs/`, `outputs/`, `metrics.json`, `.csv`, `.parquet`).
   - Extract real empirical numbers (e.g. CAGR, Sharpe, Sortino, MaxDD, Accuracy, F1, Loss, Latency, Memory) directly from these sources. Never guess or hallucinate performance figures.
4. **End-to-End Pipeline Architecture:**
   - Synthesize the disparate scripts and modules into a coherent multi-stage architectural pipeline (e.g., Ingestion/Regime Detection → Feature/Quantile Engine → Optimization/Allocation → Execution/Inference → Governance/XAI).

---

### Phase 2: Literature Benchmarking & BibTeX Grounding

1. **Primary Literature Selection:**
   - Foundational theory: Foundational econometric and mathematical papers establishing the core methodologies (e.g. Markowitz 1952, Ledoit-Wolf 2004, Lopez de Prado 2016, Hamilton 1989).
   - Modern baselines: Recent peer-reviewed deep learning and quantitative benchmarks (e.g. LSTM-DNN, CNN-LSTM, Transformer architectures).
   - Regulatory & market reports: Authoritative industry sources (e.g. SEBI, SEC, Bloomberg, Federal Reserve).
2. **BibTeX Library (`references.bib`):**
   - Construct complete, standard BibTeX entries with exact author rosters, article titles, journal/conference venues, volume/number, page ranges, and publication years.
   - Avoid placeholder or unverified citations.
3. **Dialectical Related Work (Section II):**
   - Structure literature reviews to highlight systemic gaps in current approaches that the proposed system solves:
     - *Point Target Fallacy:* Single-price deep learning point predictions fail under financial heteroskedasticity.
     - *Single-Asset Isolation:* Predictive models overlook cross-asset co-movements and covariance structures.
     - *Covariance Singularity:* Inverting empirical sample covariance matrices magnifies estimation noise into unstable corner solutions.
     - *Continuous Fractional Execution Fallacy:* Theoretical models assume continuous fractional quantities that retail brokers prohibit.

---

### Phase 3: Reproducible Vector Figure Generation Engine

Author standalone Python scripts in `scripts/paper_figures/` to generate high-resolution figures. Save both `.pdf` (vector graphics) and 300 DPI `.png` with `bbox_inches='tight'`:

1. **Figure 1 (System Architecture Flow Diagram):**
   - Use clean, modular pipeline cards with distinct color accents (e.g. Blue `#1E40AF`, Teal `#0E7490`, Amber `#B45309`, Magenta `#BE185D`).
   - Draw prominent inter-stage directional arrow connectors showing pipeline progression.
   - Separate cross-cutting foundation tiers (Explainable AI, Trust Cards, Fact-Checking NLP) into distinct, spacious sub-cards.
   - **Crucial Anti-Clutter Rule:** Avoid long, unwrapped text strings that cause horizontal container collisions. Avoid cramped sub-pills; use clean, bold typography and readable bullet points.
2. **Quantitative Results Figures (Figures 2–7):**
   - Figure 2 & 3: Unsupervised cluster phase space and historical timeline regime partitioning.
   - Figure 4: Hierarchical clustering dendrogram paired with quasi-diagonalized correlation heatmaps.
   - Figure 5: Multi-horizon probabilistic quantile growth cones enforcing strict isotonic monotonicity ($Q_{0.10} \le Q_{0.50} \le Q_{0.90}$).
   - Figure 6: Out-of-sample cumulative wealth trajectories + underwater drawdown profiles.
   - Figure 7: Analytical compounding tipping point solver curves.
3. **Styling Standards:**
   - Professional font choices (sans-serif or Times matching the document).
   - High contrast, colorblind-accessible palettes.
   - Zero overlapping text labels or cramped legends.

---

### Phase 4: LaTeX Document Engineering & Formatting Invariants

Targeting official templates (e.g. `IEEEtran.cls` for IEEE conference/transactions):

1. **Document Class & Core Packages:**
   ```latex
   \documentclass[conference]{IEEEtran}
   \IEEEoverridecommandlockouts
   \usepackage{cite}
   \usepackage{amsmath,amssymb,amsfonts}
   \usepackage{algorithmic}
   \usepackage{graphicx}
   \usepackage{textcomp}
   \usepackage{xcolor}
   \usepackage{booktabs}
   \usepackage{microtype}
   \usepackage{balance}
   ```
2. **Column Separation & Spacing:**
   - Set standard column separation: `\setlength{\columnsep}{0.63cm}`.
   - Mathematical equation breathing room:
     ```latex
     \setlength{\abovedisplayskip}{5pt plus 2pt minus 2pt}
     \setlength{\belowdisplayskip}{5pt plus 2pt minus 2pt}
     \setlength{\abovedisplayshortskip}{2.5pt plus 1pt minus 1pt}
     \setlength{\belowdisplayshortskip}{2.5pt plus 1pt minus 1pt}
     ```
   - Float spacing to prevent page spill:
     ```latex
     \setlength{\textfloatsep}{8pt plus 2pt minus 2pt}
     \setlength{\floatsep}{8pt plus 2pt minus 2pt}
     \setlength{\intextsep}{6pt plus 2pt minus 2pt}
     ```
3. **Multi-Author Staggered Alignment (3 + 2 Pattern):**
   When 5 authors share the same institution, format Row 1 with 3 authors and Row 2 with 2 authors centered beneath the column gaps using `\linebreakand`:
   ```latex
   \makeatletter
   \newcommand{\linebreakand}{%
     \end{@IEEEauthorhalign}
     \hfill\mbox{}\par
     \vspace{0.7em}
     \mbox{}\hfill\begin{@IEEEauthorhalign}
   }
   \makeatother
   ```
   Wrap long department lines across two lines (`\textit{Department of Computer} \\ \textit{Science and Engineering}`) to prevent the author block from collapsing into unwanted column wraps.
4. **Neutralizing PDF Reader Auto-Mailto Hyperlinks:**
   PDF readers (Adobe Acrobat, Chrome, Edge, Preview) aggressively scan for `name@domain.com` strings and automatically inject clickable `mailto:` links. Defeat viewer regex pattern matching while preserving flawless visual text by inserting imperceptible sub-point kerning before domain dots:
   ```latex
   {\small user@institution\hspace{0.15em}.edu\hspace{0.15em}.in}
   ```
5. **Exact Font Size Specifications:**
   Enforce standard 8 pt font for the bibliography:
   ```latex
   \begin{thebibliography}{00}
   \fontsize{8pt}{9.0pt}\selectfont
   \setlength{\itemsep}{0pt plus 0.2pt}
   \setlength{\parskip}{0pt}
   ```
6. **Table Engineering:**
   - Spanning multi-column benchmark matrices use `\begin{table*}` with clean `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`).
   - Single-column metric tables use `\begin{table}` with compact column padding (`\setlength{\tabcolsep}{3.5pt}`).

---

### Phase 5: Visual Smoke-Testing & Page-Budget Convergence Loop

Never declare a paper complete based purely on zero compiler errors. Always visually inspect rendered pages:

1. **Compile:**
   ```powershell
   pdflatex -interaction=nonstopmode -enable-installer <paper>.tex
   ```
2. **Render Pages to High-Res PNGs:**
   ```powershell
   pdftoppm -png -r 150 <paper>.pdf page_out
   ```
3. **Page-by-Page Visual Audit:**
   Use visual inspection tools to check every single page:
   - **Page 1:** Title centering, author block alignment (3 top, 2 staggered bottom), abstract/keywords bounding, column separation (`0.63cm`).
   - **Page 2:** Figure 1 layout—ensure zero horizontal text overflow, crisp text boxes, clean flow connectors.
   - **Intermediate Pages:** Check equations for cramped subscripts or missing display math spacing; ensure 2-column tables do not exceed margin boundaries.
   - **Final Page:** Ensure the References section terminates strictly on the target page budget (e.g. Page 6 of a 6-page limit) with balanced bottom margins.
4. **Convergence Tuning:**
   If references spill over onto an extra page by 2–5 lines:
   - Tighten verbose descriptions or bullet points in the XAI/Conclusion sections by 2–3 lines.
   - Reduce list vertical padding (`\itemsep=0pt`, `\topsep=0pt`).
   - Re-compile, re-render, and verify until the page count is exact.

---

### Phase 6: Clean Repository Hygiene

1. **Ignore LaTeX Build Cache:**
   Add intermediate build artifacts to `.gitignore`:
   ```gitignore
   *.aux
   *.log
   *.bbl
   *.blg
   *.out
   *.synctex.gz
   ```
2. **Clean Temporary Previews:**
   Delete temporary render files (`page_out-*.png`).
3. **Isolate Paper Assets & Clean Commits:**
   - Always isolate paper files into a dedicated directory (e.g. `docs/research_paper/` or `paper/`) and reproduction scripts into a dedicated folder (e.g. `scripts/paper_figures/`).
   - Stage and commit only permanent paper assets: `.tex` source, `.bib` library, document class (`IEEEtran.cls`), generated `figures/`, reproduction scripts, and the camera-ready `.pdf`.
4. **Universal Non-Destructive Invariant:**
   - Strictly NEVER modify any existing project code, configuration, scripts, notebooks, or data files—regardless of how cluttered, legacy, or unstructured the repository is. The paper builder operates strictly as a read-only analyst of the project code, writing only to its designated publication and figure script directories.
