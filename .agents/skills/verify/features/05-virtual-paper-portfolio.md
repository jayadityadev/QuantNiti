# Virtual Paper Portfolio

The Virtual Paper Portfolio simulates an investment tracker for Indian retail investors, calculating live mark-to-market performance, benchmark alpha against NIFTY 50, and regime-shift rebalance recommendations.

## Sub-features

- `portfolio-holdings-display`: Displays current asset allocations, weights, purchase prices, and live mark-to-market valuations.
- `benchmark-alpha-tracking`: Tracks performance difference relative to NIFTY 50 and Fixed Deposit returns.
- `regime-rebalance-alerts`: Proactively notifies investors when macro regime transitions necessitate portfolio reallocation.

## How to get to it (user POV)

- Open `http://127.0.0.1:8000/`.
- Tap the **Portfolio** tab in the bottom navigation bar.

## Driving it with verify_driver

Preconditions:
- QuantNiti instance is healthy on `http://127.0.0.1:8000`.
- User is onboarded.

Driving steps:
- **Navigate to Portfolio:** Click bottom navigation button `button:has-text('Portfolio')`.
- **Verify Portfolio Summary:** Assert total portfolio value, day change, and asset distribution cards render.
- **Proof:**
  - Screenshot `.audit/verify/portfolio_tracker_ui.png` captured showing the active portfolio tracker.

Run automated recipe:
```powershell
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive virtual-paper-portfolio --port 8000 --output-dir .audit/verify
```

## Gotchas

- If the user has created no custom portfolios, the app displays the Demo Portfolio with synthetic holdings. Assert the existence of holdings rows rather than specific user-created accounts.
