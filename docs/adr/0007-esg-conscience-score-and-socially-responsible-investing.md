# ESG Conscience Score and Socially Responsible Investing

**Status:** accepted

## Context
Young retail investors increasingly demand ethical alignment in their investments. However, Indian retail platforms surface zero ESG (Environmental, Social, Governance) data at the portfolio level. SEBI's mandate of Business Responsibility and Sustainability Reporting (BRSR) provides public disclosure for top listed companies.

## Decision
1. Curated a standardized ESG dataset for universe assets incorporating composite, environment, social, and governance sub-scores from BRSR disclosures and CRISIL ratings.
2. Introduced the **ESG-Conscious Risk Persona**, which applies an additive weight bias toward high-sustainability companies before HRP bisection.
3. Calculates an aggregate weighted portfolio ESG Conscience Score.

## Consequences
- Directly addresses academic review criteria regarding societal and environmental impact.
- Enables ethical portfolio tilting without sacrificing risk-adjusted diversification.
