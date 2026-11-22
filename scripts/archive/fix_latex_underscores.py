import glob
import re

for fpath in glob.glob('docs/academic_docs/report_latex/**/*.tex', recursive=True):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace markdown-style backticks `code_word` with \texttt{code\_word}
    def repl_backtick(m):
        inner = m.group(1).replace('_', r'\_')
        return r'\texttt{' + inner + '}'

    new_content = re.sub(r'`([^`\n]+)`', repl_backtick, content)

    # Specific known terms
    replacements = [
        ('PRAGMA journal_mode=WAL', r'PRAGMA journal\_mode=WAL'),
        ('HIGH_VOLATILITY_BEAR', r'HIGH\_VOLATILITY\_BEAR'),
        ('LOW_VOLATILITY_BULL', r'LOW\_VOLATILITY\_BULL'),
        ('SIDEWAYS_CONSOLIDATION', r'SIDEWAYS\_CONSOLIDATION'),
        ('REGIME_SHIFT', r'REGIME\_SHIFT'),
        ('STOP_LOSS_BREACH', r'STOP\_LOSS\_BREACH'),
        ('WEIGHT_DRIFT', r'WEIGHT\_DRIFT'),
        ('2026_CSE_01', r'2026\_CSE\_01'),
        ('x86_64', r'x86\_64'),
        ('x86_64', r'x86\_64'),
    ]
    for old, new in replacements:
        new_content = new_content.replace(old, new)

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {fpath}")
