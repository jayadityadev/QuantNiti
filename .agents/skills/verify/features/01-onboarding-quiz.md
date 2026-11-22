# Onboarding Quiz

The Onboarding Quiz guides first-time retail investors through a multi-question interactive risk assessment, calibrating their risk persona (Conservative, Balanced, Aggressive, ESG-Conscious) and persisting their profile in local storage.

## Sub-features

- `quiz-display`: Renders introductory questions upon first visit when no profile exists in local storage.
- `quiz-persona-selection`: Dynamically evaluates answers to assign an investor risk persona.
- `quiz-persistence`: Stores `quantniti_onboarded` and `quantniti_risk_persona` in `localStorage`.
- `quiz-skip-subsequent`: Bypasses the onboarding screen on subsequent visits to directly display the Home tab.

## How to get to it (user POV)

- Open `http://127.0.0.1:8000/` in a fresh browser session with cleared local storage.
- Navigate to the welcome screen when `localStorage.getItem('quantniti_onboarded')` is null.

## Driving it with verify_driver

Preconditions:
- QuantNiti instance is healthy on `http://127.0.0.1:8000`.
- Browser context has `localStorage` cleared.

Driving steps:
- **Open Onboarding:** Navigate to `http://127.0.0.1:8000/`.
- **Answer Questions:** Choose options across investment horizon, risk tolerance, and ESG preference.
- **Complete Quiz:** Click final action button to save persona and transition to Home dashboard.
- **Proof:** Screenshot `.audit/verify/onboarding_quiz_ui.png` captured showing the interactive quiz cards.

Run automated recipe:
```powershell
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive onboarding-quiz --port 8000 --output-dir .audit/verify
```

## Gotchas

- If `quantniti_onboarded` is already set to `'true'`, the app immediately renders the Home tab. Clear `localStorage` before testing onboarding.
- LocalStorage keys must match exact naming (`quantniti_onboarded`, `quantniti_risk_persona`).
