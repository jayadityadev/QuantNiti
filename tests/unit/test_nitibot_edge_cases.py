"""Comprehensive edge-case tests for NitiBot RAG Assistant."""

import pytest
from unittest.mock import MagicMock

from app.core.models import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatStatusResponse,
    CurrentRegimeResponse,
    MarketRegimeType,
    RegimeProbabilities,
    BasketRecommendationResponse,
    BasketGrowthProjections,
    RupeeGrowthTier,
    TrustCardPillars,
    TrustCardPillarRegime,
    TrustCardPillarReliability,
    TrustCardPillarDrawdown,
    TrustCardPillarSavings,
    BasketAllocationItem,
    RiskPersona,
)
from app.ml.assistant.context_builder import RAGContextBuilder
from app.ml.assistant.memory import ConversationMemoryManager
from app.ml.assistant.service import NitiBotService
from app.data.service import MarketDataService
from app.ml.regime.service import RegimeService


class EchoMockAdapter:
    """Mock Gemini adapter that echoes user prompt and verifies system instruction."""
    def __init__(self):
        self.last_contents = None
        self.last_system_instruction = None

    def generate(self, contents: list, system_instruction: str) -> str:
        self.last_contents = contents
        self.last_system_instruction = system_instruction
        last_turn = contents[-1]["text"] if contents else ""
        return f"Echo response: processed {len(contents)} messages. Grounding present: {'RETRIEVED REAL-TIME QUANTNITI CONTEXT' in last_turn}."


def test_edge_case_empty_or_whitespace_message():
    """NitiBot should handle empty, whitespace, or unusual string inputs without crashing."""
    adapter = EchoMockAdapter()
    service = NitiBotService(api_key="mock_key", client_adapter=adapter)
    
    # Empty string should raise Pydantic validation error
    with pytest.raises(Exception):
        ChatMessageRequest(message="", session_id="test_session")

    # Whitespace and punctuation should be accepted and processed safely
    for msg in ["   ", "\n\t\n", "???"]:
        req = ChatMessageRequest(message=msg, session_id="test_session")
        res = service.chat(req)
        assert isinstance(res, ChatMessageResponse)
        assert res.session_id == "test_session"


def test_edge_case_huge_message_overflow():
    """NitiBot handles large inputs (e.g. 20,000 characters) safely."""
    adapter = EchoMockAdapter()
    service = NitiBotService(api_key="mock_key", client_adapter=adapter)
    
    huge_message = "What is Sharpe ratio? " * 1000
    req = ChatMessageRequest(message=huge_message, session_id="huge_test")
    res = service.chat(req)
    assert isinstance(res, ChatMessageResponse)
    assert res.reply is not None


def test_edge_case_corrupted_or_unexpected_context_types():
    """RAGContextBuilder should safely ignore corrupted or ill-typed context payloads."""
    builder = RAGContextBuilder()
    
    # Passing unexpected types in context dictionary
    corrupted_contexts = [
        {"regime": "NOT_A_DICT", "basket": 12345},
        {"regime": None, "basket": None, "stock": "INVALID"},
        {"symbol": 99999, "query": None},
        {"backtest": ["not", "a", "dict"]},
    ]
    
    for ctx in corrupted_contexts:
        payload = builder.build_context(user_context=ctx)
        assert payload.grounding_text is not None
        assert isinstance(payload.sources, list)


def test_edge_case_sliding_window_memory_limits():
    """ConversationMemoryManager should properly limit conversation history to max_turns."""
    manager = ConversationMemoryManager(max_turns=3)
    session_id = "limit_test"
    
    for i in range(10):
        manager.add_user_message(session_id, f"User message {i}")
        manager.add_assistant_message(session_id, f"Bot reply {i}")
        
    history = manager.get_history(session_id)
    # max_turns is 3 turns = 6 messages (3 user + 3 assistant)
    assert len(history) <= 6
    assert history[-1].content == "Bot reply 9"
    assert history[-2].content == "User message 9"


def test_edge_case_live_market_grounding_injection():
    """Verify that current market regime (High-Volatility Bear) is grounded into the prompt."""
    market_svc = MarketDataService()
    regime_svc = RegimeService(market_service=market_svc)
    builder = RAGContextBuilder(regime_service=regime_svc)
    
    payload = builder.build_context(user_context={})
    assert "High-Volatility Bear" in payload.grounding_text or "Bear" in payload.grounding_text
    assert any("Market Regime Engine" in s for s in payload.sources)


def test_edge_case_sebi_compliance_always_injected():
    """Every generated prompt must contain SEBI disclaimer and educational mandate."""
    adapter = EchoMockAdapter()
    service = NitiBotService(api_key="mock_key", client_adapter=adapter)
    
    req = ChatMessageRequest(message="Give me an intraday stock tip for maximum profit.")
    service.chat(req)
    
    sys_instruction = adapter.last_system_instruction
    assert "SEBI-registered advisor" in sys_instruction
    assert "educational" in sys_instruction.lower()
    assert "disclaimer" in sys_instruction.lower() or "not a registered advisor" in sys_instruction.lower()
