# RAG-Powered Conversational Assistant (NitiBot)

**Status:** accepted

## Context
Retail investors need interactive explanations when reviewing portfolio allocations. Static tooltips cannot answer nuanced user inquiries such as *"Why did the AI allocate to Infosys?"* or *"What happens if the market crashes?"*. Generic LLM chatbots hallucinate and lack access to real-time market regimes.

## Decision
We implemented **NitiBot**, a Retrieval-Augmented Generation (RAG) assistant:
1. Aggregates live system state (active regime probabilities, portfolio weights, growth projections, Trust Card metrics) into a grounded RAG payload.
2. Passes context to Google Gemini (gemini-2.5-flash) with an immutable SEBI-compliant educational system prompt.
3. Accessible from any screen via a persistent floating action button (FAB).
4. Gracefully degrades if `GEMINI_API_KEY` is omitted.

## Consequences
- Eliminates AI hallucination by grounding responses in QuantNiti's live mathematical models.
- Strictly adheres to financial educational guidelines without offering speculative trading advice.
