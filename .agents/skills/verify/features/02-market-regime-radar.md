# Market Regime Radar

The Market Regime Radar classifies the macro-structural state of the Indian equity market (Low-Volatility Bull, High-Volatility Bear, Sideways Consolidation) via unsupervised machine learning, rendering live probabilities and strategy recommendations on the Home tab.

## Sub-features

- `regime-classification`: Unsupervised ML classification based on 20d/50d log returns, Parkinson volatility, and VIX metrics.
- `regime-probabilities`: Tri-state probability breakdown (Bull, Bear, Sideways summing to 1.0).
- `regime-ui-radar`: Visual radar card displaying the dominant regime badge, confidence percentage, and recommended strategy.
- `regime-api-endpoint`: REST endpoint `/api/regime/current` providing structured regime telemetry.

## How to get to it (user POV)

- Open `http://127.0.0.1:8000/` as an onboarded user.
- View the top section of the Home tab beneath Market Pulse to inspect the Regime Radar.

## Driving it with verify_driver

Preconditions:
- QuantNiti instance is healthy on `http://127.0.0.1:8000`.
- Browser context has `quantniti_onboarded = 'true'`.

Driving steps:
- **Load Home Tab:** Navigate to `http://127.0.0.1:8000/`.
- **Inspect Radar Card:** Assert dominant regime heading (e.g. `Low-Volatility Bull`) and confidence indicator render properly.
- **Inspect Strategy:** Confirm recommended strategy text is displayed.
- **Proof:**
  - Screenshot `.audit/verify/regime_radar_ui.png` captured showing the rendered card.
  - JSON response `.audit/verify/regime_radar_api.json` saved from `/api/regime/current`.

Run automated recipe:
```powershell
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive market-regime-radar --port 8000 --output-dir .audit/verify
```

## Gotchas

- Machine learning models calculate regime dynamically from recent market metrics; do not assert a hardcoded static regime name, but rather assert membership in the set of 3 valid regimes.
- Sum of `bull + bear + sideways` probabilities must equal 1.0 within +/- 0.01 tolerance.
