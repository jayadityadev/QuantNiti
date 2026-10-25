# Autonomous AI Ground-Truth Review Fact-Checking Agent

**Status:** accepted

## Context
Online investment communities are inundated with fraudulent testimonials, fabricated P&L screenshots, and deceptive stock tips. SEBI guidelines strictly prohibit unverified financial performance claims and fraudulent solicitations in investment platforms.

## Decision
We deployed an autonomous 3-tier NLP Review Fact-Checking Agent:
1. **Entity Extraction**: Parses numerical return claims (e.g., "+24%") and holding periods from user reviews.
2. **Ground-Truth Cross-Examination**: Checks claimed returns against historical market return distributions for that asset and timeframe.
3. **Verification Badging**: Awards a verified badge if within a ±3% empirical tolerance, flags subjective reviews, and automatically rejects fabricated claims (>8% discrepancy) and spam solicitations.

## Consequences
- Enforces strict compliance with SEBI advertising regulations.
- Protects novice users from misleading community claims.
