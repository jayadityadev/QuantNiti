# Grow AI Basket Recommendation

The Grow AI Basket engine generates personalized, regime-conditioned, hierarchical risk parity (HRP) weighted portfolios of Indian equities and commodity ETFs, accompanied by probabilistic growth cones and explainable Trust Cards.

## Sub-features

- `grow-wizard-flow`: Step-by-step wizard to configure capital amount, investment horizon (1M, 3M, 6M, 12M), and risk persona.
- `hrp-portfolio-optimization`: Machine-learning covariance clustering and Ledoit-Wolf shrinkage to produce integer whole-share allocations.
- `probabilistic-growth-projections`: 10th (pessimistic), 50th (base), and 90th (optimistic) percentile rupee trajectories and stress drawdown limits.
- `trust-card-explainability`: Disintermediation fee savings, 5-year backtested directional hit rate, and historical stress drawdown bounds.

## How to get to it (user POV)

- Open `http://127.0.0.1:8000/`.
- Tap the **Grow** tab in the bottom navigation bar.
- Progress through Step 1 (Capital) -> Step 2 (Horizon) -> Step 3 (Persona) -> Tap **Review & Generate**.

## Driving it with verify_driver

Preconditions:
- QuantNiti instance is healthy on `http://127.0.0.1:8000`.
- User is onboarded with a valid risk persona.

Driving steps:
- **Select Grow Tab:** Click `button:has-text('Grow')`.
- **Configure Horizon & Persona:** Step through the wizard inputs.
- **Generate AI Basket:** Click `button:has-text('Review & Generate')`.
- **Inspect Basket Results:** Verify asset allocations list, rupee investment sum, and base return percentage.
- **Proof:**
  - Screenshot `.audit/verify/grow_ai_basket_results.png` captured showing the full results card.
  - JSON response `.audit/verify/grow_ai_basket_api.json` from `POST /api/v1/grow/recommend`.

Run automated recipe:
```powershell
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive grow-ai-basket --port 8000 --output-dir .audit/verify
```

## Gotchas

- HRP optimization and quantile calculation may take 1-3 seconds on first execution; ensure browser wait states accommodate the computation.
- Whole-share rounding means allocated amount may differ slightly from target capital; verify that unallocated cash buffer is within expected limits (< 2%).
