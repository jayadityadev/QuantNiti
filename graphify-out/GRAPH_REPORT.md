# Graph Report - QuantNiti  (2026-10-25)

## Corpus Check
- 284 files · ~140,994 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: (none) 8, .toml 2, .example 1)

## Summary
- 2432 nodes · 5780 edges · 144 communities (120 shown, 24 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 721 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `587cc8cd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- react
- grow.py
- pytest
- GrowPage.tsx
- GlassCard
- reviews_repo.py
- ParquetMarketCache
- ExplorePage.tsx
- extract_stock_factors
- models.py
- PortfolioState
- PortfolioService
- compounding_engine.py
- create_app
- ReviewStatus
- PortfolioPage.tsx
- TestDiscreteAllocationEngine
- MarketRegimeType
- backtest/service.py
- lucide-react
- 🔍 Platform-by-Platform Research (Primary-Source Verified)
- RegimeService
- AppShell.tsx
- streaming.py
- get_esg_score_for_symbol
- Base
- NitiBotService
- useAppStore.ts
- hrp.py
- RAGContextBuilder
- pandas
- AlertService
- asyncio
- pathlib
- test_portfolio_full_lifecycle_api
- BacktestEngine
- ⚡ Quick Start
- MarketRegimeClassifier
- routes/portfolio.py
- alerts/service.py
- provider.py
- PortfolioRepository
- test_chat_api.py
- 3. Academic Demonstration & Evaluation Scenarios
- literacy.py
- test_market_service.py
- Cloud Deployment via AWS Lightsail, Caddy SSL & Custom Domain
- Native Android Container via WebViewAssetLoader & Automated APK CI/CD
- ExploreService
- ConversationMemoryManager
- assistant/service.py
- compilerOptions
- package.json
- ReviewSubmissionRequest
- QuantNiti: Machine Learning & Quantitative Finance Technical Specification
- asyncio
- Interactive Financial Literacy Hub & Playable Video Explainer Architecture
- MarketStreamClient
- asyncio
- fig6_backtest_comparison.py
- devDependencies
- filter_tier1_content
- dependencies
- test_portfolio_storage.py
- manifest.json
- Multi-Condition Quantitative Smart Alert Engine with Web Push
- asyncio
- compute_regime_suitability
- MarketTickGenerator
- MarketDataProvider
- test_stream_api.py
- asyncio
- .format_sse_event
- forecaster.py
- data/service.py
- test_pwa_unit.py
- ReviewTargetType
- scripts
- DiscreteAllocationEngine
- test_review_service.py
- test_multi_asset_universe.py
- AssetClass
- asyncio
- test_reviews_api.py
- MarketDataService
- setup.ts
- test_hrp_optimizer.py
- compilerOptions
- QuantNiti: Production Hosting, Cloud Architecture & Scalability Guide
- QuantNiti
- chat.py
- FastAPI
- vite.config.ts
- 2. Platform-by-Platform Verified Primary-Source Audit
- 6. Mathematical Formulations & Algorithmic Engines
- test_tick_generator.py
- 2. Accessing & Launching the Application
- QuantNiti: Complete Architectural Blueprint & System Design Document
- capacitor.config.ts
- 2. Audit of the 4 Open-Source Repositories
- 1. Advanced Machine Learning Architecture for Stock & Portfolio Intelligence
- QuantNiti: Master Research Dossier & Academic Foundation Document
- 9. IEEE Research Paper Blueprint (Section-by-Section Outline)
- sw.js
- app
- README.md
- Spec: QuantNiti Core Platform
- Agent skills
- Domain Docs
- Issue tracker: Local Markdown
- 3. Mathematical & Quantitative Algorithmic Deep-Dive
- 3. Related Work & Comprehensive Literature Benchmark
- 8. Empirical Results, Verification & Benchmarks
- RAG-Powered Conversational Assistant (NitiBot)
- ESG Conscience Score and Socially Responsible Investing
- Cross-Platform Progressive Web App (PWA) with Responsive Layout
- Prioritizing Portfolio Intelligence Over Pure Strategy Testing
- Multi-Asset Universe Expansion with Defensive Commodity ETFs
- Server-Side Quantitative ML Computation with Asynchronous ASGI Gateway
- Autonomous AI Ground-Truth Review Fact-Checking Agent
- 6.2 Multi-Factor Econometric Extraction Engine
- 2. Introduction, Problem Statement & Socio-Economic Context
- 4. Dataset Engineering & Multi-Asset Universe
- 5. End-to-End System Architecture
- 6.5 Hierarchical Risk Parity (HRP) Optimization Algorithm
- 1. Academic Metadata & Proposed Paper Formulations
- 6.1 Unsupervised Market Regime Classifier (GMM & Parkinson Volatility)
- 6.3 Multi-Horizon Quantile Growth Forecaster & Isotonic Regularization
- Pivot from Technical Backtesting to Portfolio Growth Intelligence
- Progressive Disclosure UX: 4-Tab Architecture and Embedded Quant Lab Pro Tools
- Virtual Paper Portfolio with Regime-Shift Rebalance Alerts
- Explainable AI Trust Card and Disintermediation Moat
- Discrete Integer Allocation and Ledoit-Wolf Covariance Shrinkage
- triage-labels.md

## God Nodes (most connected - your core abstractions)
1. `MarketDataService` - 80 edges
2. `react` - 67 edges
3. `MarketRegimeType` - 59 edges
4. `RegimeService` - 59 edges
5. `RiskPersona` - 51 edges
6. `useAppStore` - 49 edges
7. `PortfolioState` - 43 edges
8. `lucide-react` - 42 edges
9. `ExploreService` - 42 edges
10. `normalize_symbol()` - 42 edges

## Surprising Connections (you probably didn't know these)
- `4.3. Lifecycle Management & Race Condition Guards` --references--> `useAbortableRequest()`  [INFERRED]
  docs/ARCHITECTURE.md → src/frontend/hooks/useAbortableRequest.ts
- `5.4 Lifecycle Guards, Concurrency, and AbortController Management` --references--> `useAbortableRequest()`  [INFERRED]
  docs/RESEARCH_PAPER_MASTER_DOSSIER.md → src/frontend/hooks/useAbortableRequest.ts
- `IV. SYSTEM ARCHITECTURE & DESIGN` --references--> `useAbortableRequest()`  [INFERRED]
  docs/RESEARCH_PAPER_MASTER_DOSSIER.md → src/frontend/hooks/useAbortableRequest.ts
- `test_get_universe()` --uses--> `UniverseStock`  [INFERRED]
  tests/integration/test_market_service.py → src/app/core/models.py
- `test_get_latest_quote()` --uses--> `StockQuote`  [INFERRED]
  tests/integration/test_market_service.py → src/app/core/models.py

## Import Cycles
- None detected.

## Communities (144 total, 24 thin omitted)

### Community 0 - "react"
Cohesion: 0.10
Nodes (20): react, react-dom, react-router-dom, @testing-library/react, @testing-library/user-event, vitest, App(), Theme (+12 more)

### Community 1 - "grow.py"
Cohesion: 0.25
Nodes (6): get_grow_service(), recommend_basket_alias(), recommend_basket_get(), recommend_basket_post(), BasketRecommendationRequest, BasketRecommendationResponse

### Community 2 - "pytest"
Cohesion: 0.18
Nodes (8): GrowService, test_grow_service_different_risk_personas(), test_grow_service_esg_portfolio_score_and_persona(), test_grow_service_invalid_inputs_raise_error(), test_grow_service_recommend_basket_balanced(), test_grow_service_bear_regime_allocates_defensive_commodity(), test_get_current_regime(), test_get_regime_history()

### Community 3 - "GrowPage.tsx"
Cohesion: 0.07
Nodes (50): chart.js, framer-motion, react-chartjs-2, AllocationDonut(), AllocationDonutProps, AllocationItem, PALETTE, GrowPage() (+42 more)

### Community 4 - "GlassCard"
Cohesion: 0.10
Nodes (27): AdaptiveHomeCard(), AdaptiveHomeCardProps, CompoundingVisualizer(), CompoundingVisualizerProps, LearningHub(), LearningHubProps, isIndianMarketOpen(), MarketPulse() (+19 more)

### Community 5 - "reviews_repo.py"
Cohesion: 0.15
Nodes (3): ReviewSummary, ReviewRepository, ReviewRecord

### Community 6 - "ParquetMarketCache"
Cohesion: 0.16
Nodes (6): ParquetMarketCache, sample_df(), temp_cache_dir(), test_cache_invalidation(), test_cache_save_and_load(), test_cache_ttl_expiration()

### Community 7 - "ExplorePage.tsx"
Cohesion: 0.09
Nodes (26): ASSETS, ProToolsBacktester(), STRATEGIES, ExploreStockItem, StockCard(), StockCardProps, StockProfileModal(), StockProfileModalProps (+18 more)

### Community 8 - "extract_stock_factors"
Cohesion: 0.13
Nodes (13): compute_bollinger_bands(), compute_ema(), compute_macd(), compute_max_drawdown(), compute_rsi(), compute_stock_beta_and_alpha(), extract_stock_factors(), test_compute_bollinger_bands() (+5 more)

### Community 9 - "models.py"
Cohesion: 0.12
Nodes (22): BasketAllocationItem, BasketGrowthProjections, BenchmarkComparisonItem, HorizonForecastCone, MultiHorizonGrowthForecast, PushSubscriptionKeys, RupeeGrowthTier, TrustCardPillarDrawdown (+14 more)

### Community 10 - "PortfolioState"
Cohesion: 0.12
Nodes (11): BrokerOrderItem, BrokerOrderSheet, PortfolioState, RebalanceAlert, RebalanceItemDiff, compute_rebalance_diff(), execute_rebalance(), generate_broker_order_sheet() (+3 more)

### Community 11 - "PortfolioService"
Cohesion: 0.14
Nodes (7): CreatePortfolioRequest, PortfolioService, portfolio_service(), test_create_and_get_portfolio(), test_get_nonexistent_portfolio_raises_error(), test_get_order_sheet(), test_rebalance_diff_and_apply()

### Community 12 - "compounding_engine.py"
Cohesion: 0.09
Nodes (19): CompoundingMonthlyPoint, CompoundingRequest, CompoundingResponse, CompoundingSummary, CompoundingTippingPoint, CompoundingYearlyPoint, calculate_lump_sum(), calculate_monthly_sip() (+11 more)

### Community 13 - "create_app"
Cohesion: 0.05
Nodes (19): create_app(), MockDataProvider, test_app(), app(), app_instance(), test_app(), app_instance(), test_app() (+11 more)

### Community 14 - "ReviewStatus"
Cohesion: 0.11
Nodes (12): ReviewStatus, ReviewVerificationResult, extract_duration_claim(), extract_return_claim(), verify_tier2_fact_check(), audit_tier3_llm(), test_extract_duration_claim(), test_extract_return_claim() (+4 more)

### Community 15 - "PortfolioPage.tsx"
Cohesion: 0.17
Nodes (20): OrderSheetModalProps, PortfolioReportCardProps, CompoundingTrajectoryChart(), CompoundingTrajectoryChartProps, DemoPortfolio(), DemoPortfolioProps, BenchmarkComparison, CompoundingTrajectoryData (+12 more)

### Community 17 - "MarketRegimeType"
Cohesion: 0.10
Nodes (16): BenchmarkComparisonLive, MarketRegimeType, PortfolioHolding, RiskPersona, calculate_day_over_day_mtm(), create_portfolio_from_allocations(), PortfolioSimulator, update_portfolio_mark_to_market() (+8 more)

### Community 18 - "backtest/service.py"
Cohesion: 0.11
Nodes (14): get_backtest_service(), run_backtest_get(), run_backtest_post(), run_quant_lab_backtest_alias(), BacktestDataPoint, BacktestRequest, BacktestResponse, StrategyType (+6 more)

### Community 19 - "lucide-react"
Cohesion: 0.14
Nodes (27): lucide-react, COMPARISON_ROWS, CompetitorBenchmarkModal(), CompetitorBenchmarkModalProps, ConceptDetailData, ConceptDetailModal(), ConceptDetailModalProps, ModalRoot() (+19 more)

### Community 20 - "🔍 Platform-by-Platform Research (Primary-Source Verified)"
Cohesion: 0.07
Nodes (27): 1. Groww (groww.in), 2. Zerodha Streak (streak.tech), 3. Smallcase (smallcase.com), 4. INDmoney (indmoney.com), 5. MoneyControl Pro / Super Pro (moneycontrol.com), 6. TradingView (tradingview.com), Bank FD Rates vs. Equity Returns (2025–2026 Context), 🎯 Consolidated Competitive Matrix (10 Dimensions) (+19 more)

### Community 21 - "RegimeService"
Cohesion: 0.09
Nodes (13): get_current_regime(), get_regime_history(), get_regime_service(), train_regime_model(), TrainRegimeRequest, CurrentRegimeResponse, RegimeHistoricalPoint, RegimeHistoryResponse (+5 more)

### Community 22 - "AppShell.tsx"
Cohesion: 0.13
Nodes (22): AppShell(), BottomNav(), BottomNavProps, NAV_ITEMS, NavItem, triggerHaptic(), Header(), HeaderProps (+14 more)

### Community 23 - "streaming.py"
Cohesion: 0.15
Nodes (3): get_tick_generator(), stream_ticks(), is_indian_market_open()

### Community 25 - "Base"
Cohesion: 0.18
Nodes (5): Base, DailySnapshotRecord, HoldingRecord, PortfolioRecord, TransactionRecord

### Community 26 - "NitiBotService"
Cohesion: 0.12
Nodes (13): ChatMessageRequest, ChatMessageResponse, NitiBotService, EchoMockAdapter, test_edge_case_empty_or_whitespace_message(), test_edge_case_huge_message_overflow(), test_edge_case_sebi_compliance_always_injected(), MockGeminiAdapter (+5 more)

### Community 27 - "useAppStore.ts"
Cohesion: 0.14
Nodes (16): SAMPLE_REVIEWS, Step5DeepDiveProps, ACTIVE_PORTFOLIO_ID_STORAGE_KEY, AppStoreState, loadActivePortfolioId(), loadIsOnboarded(), loadLearnedConcepts(), loadPortfolios() (+8 more)

### Community 28 - "hrp.py"
Cohesion: 0.16
Nodes (6): apply_weight_caps(), compute_hrp_weights(), get_cluster_variance(), get_quasi_diag_order(), _traverse(), recursive_bisection()

### Community 29 - "RAGContextBuilder"
Cohesion: 0.14
Nodes (12): RAGContextPayload, RAGContextBuilder, create_sample_backtest(), create_sample_regime(), test_rag_context_builder_builds_complete_grounding(), test_rag_context_builder_esg_enrichment(), test_rag_context_builder_fallback_defaults(), test_edge_case_corrupted_or_unexpected_context_types() (+4 more)

### Community 30 - "pandas"
Cohesion: 0.08
Nodes (16): draw_ellipse(), calculate_parkinson_volatility(), calculate_realized_volatility(), calculate_rolling_log_returns(), extract_regime_features(), benchmark_price_series(), sample_price_series(), sample_stock_and_index() (+8 more)

### Community 31 - "AlertService"
Cohesion: 0.06
Nodes (14): clear_alerts(), evaluate_alerts_micro_batch(), get_alert_service(), get_vapid_public_key(), list_alerts(), mark_alert_read(), mark_all_alerts_read(), send_test_push_notification() (+6 more)

### Community 32 - "asyncio"
Cohesion: 0.22
Nodes (4): test_compounding_endpoint_mounted_at_both_prefixes(), test_compounding_endpoint_standalone_post(), test_compounding_endpoint_validation_errors(), test_compounding_endpoint_with_portfolio_id()

### Community 33 - "pathlib"
Cohesion: 0.06
Nodes (25): main(), run_command(), get_lan_ip(), main(), print_qr_code(), log_test(), run_full_analysis(), auto_open_emulator_in_background() (+17 more)

### Community 35 - "BacktestEngine"
Cohesion: 0.07
Nodes (17): BacktestMetrics, BacktestTrade, RegimePerformanceBreakdown, BacktestEngine, BacktestResultData, compute_rsi(), calculate_backtest_metrics(), calculate_regime_breakdown() (+9 more)

### Community 36 - "⚡ Quick Start"
Cohesion: 0.22
Nodes (9): 1. Prerequisites, 2. Installation, 3. Running Locally, 4. Running the Native Android App, Development Mode (Hot Reloading Frontend & Backend):, Option A: Direct APK Download, Option B: Compile with Android SDK, Production Unified Mode: (+1 more)

### Community 37 - "MarketRegimeClassifier"
Cohesion: 0.14
Nodes (5): MarketRegimeClassifier, synthetic_regime_features(), test_classifier_fit_and_predict(), test_classifier_probabilities_sum_to_one(), test_classifier_state_label_determinism()

### Community 38 - "routes/portfolio.py"
Cohesion: 0.16
Nodes (9): apply_rebalance_endpoint(), calculate_compounding_endpoint(), create_portfolio_endpoint(), delete_portfolio_endpoint(), get_order_sheet_endpoint(), get_portfolio_endpoint(), get_portfolio_service(), get_rebalance_diff_endpoint() (+1 more)

### Community 39 - "alerts/service.py"
Cohesion: 0.10
Nodes (19): AlertSeverity, SmartAlert, SmartAlertType, evaluate_52w_high_breakout(), evaluate_drawdown_breach(), evaluate_factor_anomaly(), evaluate_portfolio_drift(), evaluate_regime_transition() (+11 more)

### Community 40 - "provider.py"
Cohesion: 0.05
Nodes (33): align_to_trading_calendar(), calculate_returns(), sanitize_raw_provider_data(), validate_ohlcv_dataframe(), test_get_history_endpoint(), test_get_quote_endpoint(), test_get_returns_matrix_endpoint(), test_get_universe_endpoint() (+25 more)

### Community 42 - "test_chat_api.py"
Cohesion: 0.22
Nodes (7): configured_app(), MockGeminiAdapter, test_chat_endpoint_graceful_degradation_503(), test_chat_endpoint_success(), test_chat_status_endpoint(), test_chat_status_endpoint_when_disabled(), unconfigured_app()

### Community 43 - "3. Academic Demonstration & Evaluation Scenarios"
Cohesion: 0.29
Nodes (7): 3. Academic Demonstration & Evaluation Scenarios, Demonstration 1: First-Time Onboarding & Behavioral Persona Quiz, Demonstration 2: Interactive Financial Literacy & Video Explainer Hub (`Home` Tab), Demonstration 3: 5-Step Guided Grow Wizard (`Grow` Tab), Demonstration 4: Stock Explorer & Quant Lab Backtesting (`Explore` Tab), Demonstration 5: Dual-State Portfolio Tracking & Smart Alerts (`Portfolio` Tab), Demonstration 6: NitiBot Grounded Conversational AI Copilot

### Community 44 - "literacy.py"
Cohesion: 0.20
Nodes (6): get_all_literacy_cards(), _get_cards_dict(), get_literacy_card_by_key(), _get_literacy_data(), LiteracyCard, LiteracyListResponse

### Community 45 - "test_market_service.py"
Cohesion: 0.22
Nodes (4): mock_service(), test_get_latest_quote(), test_get_universe(), test_sync_universe_batch()

### Community 46 - "Cloud Deployment via AWS Lightsail, Caddy SSL & Custom Domain"
Cohesion: 0.40
Nodes (4): Cloud Deployment via AWS Lightsail, Caddy SSL & Custom Domain, Consequences, Context, Decision

### Community 47 - "Native Android Container via WebViewAssetLoader & Automated APK CI/CD"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Native Android Container via WebViewAssetLoader & Automated APK CI/CD

### Community 48 - "ExploreService"
Cohesion: 0.10
Nodes (17): get_explore_service(), get_growth_forecast(), get_stock_profile(), get_ticker_esg(), list_explore_stocks(), BenchmarkComparison, ESGScoreResponse, ExploreStockSummary (+9 more)

### Community 49 - "ConversationMemoryManager"
Cohesion: 0.22
Nodes (7): ConversationMemoryManager, MessageTurn, test_edge_case_sliding_window_memory_limits(), test_memory_manager_add_and_retrieve_turns(), test_memory_manager_clear_session(), test_memory_manager_format_for_gemini(), test_memory_manager_sliding_window_limit()

### Community 51 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+10 more)

### Community 52 - "package.json"
Cohesion: 0.11
Nodes (17): name, private, type, version, autoprefixer, @capacitor/android, @capacitor/core, clsx (+9 more)

### Community 53 - "ReviewSubmissionRequest"
Cohesion: 0.15
Nodes (9): get_review_service(), get_target_reviews(), preview_verification(), submit_review(), ReviewItem, ReviewsListResponse, ReviewSubmissionRequest, ReviewSubmissionResponse (+1 more)

### Community 54 - "QuantNiti: Machine Learning & Quantitative Finance Technical Specification"
Cohesion: 0.04
Nodes (47): 10. End-to-End Execution Flowchart & Mathematical Reference, 11.1 The Six Deterministic Mathematical Triggers, 11.2 Asymmetric Pinball Quantile Loss (LightGBM), 11.3 4-Pillar Explainable AI (XAI) Trust Card Equations, 11. Multi-Condition Quantitative Smart Alert Engine & XAI Formulations, 1.1 The Markowitz "Error Maximizer" Curse, 1.2 Non-Stationarity & Structural Regime Breaks, 1.3 The Flaw of Single-Point Deterministic Targets (+39 more)

### Community 55 - "asyncio"
Cohesion: 0.18
Nodes (5): test_get_grow_recommend_success(), test_grow_recommend_esg_conscious_api(), test_grow_recommend_validation_errors(), test_post_baskets_recommend_alias(), test_post_grow_recommend_success()

### Community 56 - "Interactive Financial Literacy Hub & Playable Video Explainer Architecture"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Interactive Financial Literacy Hub & Playable Video Explainer Architecture

### Community 57 - "MarketStreamClient"
Cohesion: 0.15
Nodes (5): marketStream, MarketStreamClient, MarketTick, TickListener, MockEventSource

### Community 58 - "asyncio"
Cohesion: 0.22
Nodes (4): test_backtest_validation_errors(), test_get_backtest_run_success(), test_post_backtest_run_success(), test_post_quant_lab_backtest_alias()

### Community 60 - "devDependencies"
Cohesion: 0.13
Nodes (15): devDependencies, autoprefixer, jsdom, postcss, tailwindcss, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event (+7 more)

### Community 61 - "filter_tier1_content"
Cohesion: 0.13
Nodes (8): filter_tier1_content(), test_tier1_blocks_email_addresses(), test_tier1_blocks_external_urls(), test_tier1_blocks_phone_numbers(), test_tier1_blocks_profanity(), test_tier1_blocks_prohibited_stock_tips(), test_tier1_blocks_telegram_and_social_handles(), test_tier1_clean_reviews_pass()

### Community 62 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, @capacitor/android, @capacitor/cli, @capacitor/core, chart.js, clsx, framer-motion, lucide-react (+6 more)

### Community 63 - "test_portfolio_storage.py"
Cohesion: 0.15
Nodes (5): repo(), test_delete_portfolio_cascades(), test_list_portfolios(), test_portfolio_schema_creation(), test_save_and_get_portfolio()

### Community 64 - "manifest.json"
Cohesion: 0.14
Nodes (13): background_color, categories, description, display, icons, id, name, orientation (+5 more)

### Community 65 - "Multi-Condition Quantitative Smart Alert Engine with Web Push"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Multi-Condition Quantitative Smart Alert Engine with Web Push

### Community 66 - "asyncio"
Cohesion: 0.18
Nodes (5): test_index_html_contains_pwa_metadata_and_elements(), test_manifest_endpoint_served_with_correct_mime(), test_offline_page_endpoint(), test_pwa_icons_served(), test_service_worker_endpoint_served_with_allowed_header()

### Community 67 - "compute_regime_suitability"
Cohesion: 0.33
Nodes (5): RegimeSuitability, compute_regime_suitability(), test_suitability_in_bear_regime(), test_suitability_in_bull_regime(), test_suitability_score_bounds()

### Community 68 - "MarketTickGenerator"
Cohesion: 0.19
Nodes (3): MarketTick, MarketTickGenerator, test_live_fallback_to_synthetic()

### Community 69 - "MarketDataProvider"
Cohesion: 0.07
Nodes (9): MarketDataProvider, YahooFinanceProvider, denormalize_symbol(), test_denormalize_symbol_for_provider(), test_get_sector_for_symbol(), test_get_universe_metadata(), test_get_universe_symbols(), test_is_valid_symbol() (+1 more)

### Community 70 - "test_stream_api.py"
Cohesion: 0.19
Nodes (5): test_stream_ticks_alias_route(), test_stream_ticks_endpoint_headers_and_event(), test_stream_ticks_symbol_filter(), test_invalid_literacy_card_fails_validation(), test_literacy_cards_schema_and_count()

### Community 71 - "asyncio"
Cohesion: 0.22
Nodes (4): test_e2e_explore_stock_to_quant_lab_backtest_journey(), test_e2e_grow_basket_to_virtual_portfolio_lifecycle(), test_e2e_quant_lab_multi_strategy_suite(), test_e2e_regime_radar_history_endpoint()

### Community 74 - "forecaster.py"
Cohesion: 0.21
Nodes (4): MultiHorizonForecaster, test_forecast_all_four_horizons(), test_forecast_cone_widening_over_longer_horizons(), test_strict_quantile_monotonicity()

### Community 75 - "data/service.py"
Cohesion: 0.07
Nodes (10): Settings, get_esg_badge(), get_sector_for_symbol(), get_universe_metadata(), get_universe_symbols(), test_get_growth_forecast(), test_get_current_regime_route(), test_get_regime_history_route() (+2 more)

### Community 76 - "test_pwa_unit.py"
Cohesion: 0.17
Nodes (5): test_desktop_responsive_css_rules(), test_icon_assets_exist(), test_manifest_file_exists_and_valid(), test_offline_page_exists_and_styled(), test_service_worker_script_structure()

### Community 77 - "ReviewTargetType"
Cohesion: 0.10
Nodes (11): test_all(), ReviewTargetType, ReviewVerificationAgent, agent(), test_agent_approves_and_verifies_authentic_review(), test_agent_approves_qualitative_review(), test_agent_blocks_stock_tipping_at_tier1(), test_agent_blocks_tier1_spam_immediately() (+3 more)

### Community 78 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, apk:build, build, cap:open, cap:sync, dev, mobile:serve, preview (+1 more)

### Community 80 - "test_review_service.py"
Cohesion: 0.25
Nodes (3): review_service(), test_service_rejects_and_does_not_publish_exaggerated_review(), test_service_submits_and_stores_verified_review()

### Community 83 - "test_multi_asset_universe.py"
Cohesion: 0.12
Nodes (7): test_asset_class_enum_members(), test_commodity_etfs_constituents(), test_defense_constituents(), test_expanded_universe_total_count(), test_factor_extractor_on_multi_asset_universe(), test_ledoit_wolf_covariance_on_multi_asset_matrix(), test_metals_constituents()

### Community 84 - "AssetClass"
Cohesion: 0.15
Nodes (7): AssetClass, LiteracyCategory, get_asset_class_for_symbol(), test_explore_profiles_for_etf_and_defense(), test_explore_stocks_total_and_asset_class_filter(), test_explore_theme_filter_chips(), test_taxonomy_and_sector_lookup_helpers()

### Community 85 - "asyncio"
Cohesion: 0.22
Nodes (4): test_create_and_list_multiple_portfolios(), test_delete_portfolio_lifecycle(), test_dual_prefix_routing_portfolios(), test_portfolio_detail_mtm_metrics()

### Community 86 - "test_reviews_api.py"
Cohesion: 0.17
Nodes (6): test_app(), test_get_reviews_endpoint(), test_stock_review_flow(), test_submit_exaggerated_review_rejected(), test_submit_prohibited_spam_rejected(), test_submit_verified_review()

### Community 87 - "MarketDataService"
Cohesion: 0.07
Nodes (16): get_history(), get_market_service(), get_quote(), get_returns_matrix(), get_universe(), sync_universe(), SyncRequest, MarketHistoryResponse (+8 more)

### Community 88 - "setup.ts"
Cohesion: 0.25
Nodes (3): @testing-library/jest-dom, localStorageMock, sessionStorageMock

### Community 89 - "test_hrp_optimizer.py"
Cohesion: 0.09
Nodes (14): compute_shrunk_covariance(), HRPOptimizer, sample_returns_df(), test_compute_hrp_weights_helper_function(), test_compute_shrunk_covariance_ledoit_wolf(), test_compute_shrunk_covariance_without_shrinkage(), test_hrp_distance_matrix_conditioning_extreme_correlation(), test_hrp_optimizer_all_personas_and_caps() (+6 more)

### Community 90 - "compilerOptions"
Cohesion: 0.25
Nodes (7): compilerOptions, allowSyntheticDefaultImports, composite, module, moduleResolution, skipLibCheck, include

### Community 91 - "QuantNiti: Production Hosting, Cloud Architecture & Scalability Guide"
Cohesion: 0.11
Nodes (18): 1. Production Architecture Overview, 2.1. Host Configuration, 2.2. Caddy Reverse Proxy Configuration (`/etc/caddy/Caddyfile`), 2.3. Docker Container Execution, 2.4. Production Healthcheck Verification, 2. Production AWS Lightsail Deployment Setup, 3. Automated Continuous Deployment (GitHub Actions), 4.1. Automated GitHub Actions APK Build (+10 more)

### Community 92 - "QuantNiti"
Cohesion: 0.22
Nodes (9): AI-Driven Regime-Adaptive Portfolio Intelligence & Quantitative Decision Support System, 🎯 Core Mathematical & Algorithmic Methodologies, 📱 Key Product Capabilities, 📄 License & Attribution, 📂 Project Structure, QuantNiti, 🏗️ System Architecture, 📚 Technical Documentation Links (+1 more)

### Community 94 - "chat.py"
Cohesion: 0.31
Nodes (4): get_chat_status(), get_nitibot_service(), post_chat_message(), ChatStatusResponse

### Community 98 - "2. Platform-by-Platform Verified Primary-Source Audit"
Cohesion: 0.17
Nodes (11): 1. Executive Summary: The Structural Gap in Indian WealthTech, 2. Platform-by-Platform Verified Primary-Source Audit, 3. Comprehensive 10-Dimension Competitive Matrix, 4. Key Takeaways for Academic & Industry Evaluation, A. MoneyControl (Pro & Super Pro), B. Zerodha (Kite + Streak), C. Groww (Stocks & Portfolio Analysis), D. INDmoney (+3 more)

### Community 100 - "6. Mathematical Formulations & Algorithmic Engines"
Cohesion: 0.18
Nodes (11): 6.4 Ledoit-Wolf Covariance Matrix Regularization, 6.6.1 Greedy Deficit-Minimization Sizing (Primary Real-Time Algorithm), 6.6.2 Mixed-Integer Linear Programming (MILP Formulation), 6.6 Discrete Integer Share Sizing & Cash Buffer Optimization, 6.7.1 Stochastic Differential Equation (SDE), 6.7.2 Monthly Systematic Investment Plan (SIP) with Annual Step-Up, 6.7.3 The Compounding Tipping Point, 6.7 Geometric Brownian Motion Compounding & Analytical Tipping Point (+3 more)

### Community 101 - "test_tick_generator.py"
Cohesion: 0.20
Nodes (5): market_service(), test_generate_batch_ticks(), test_generate_single_tick(), test_tick_consecutive_price_movement(), tick_generator()

### Community 102 - "2. Accessing & Launching the Application"
Cohesion: 0.20
Nodes (9): 1. System Overview, 2. Accessing & Launching the Application, 4-Tab Navigation Architecture, 4. Test Suite Execution & Verification, Option A: Live Production Cloud (Recommended), Option B: Native Android App (APK), Option C: Mobile Progressive Web App (PWA), Option D: Local Development Mode (+1 more)

### Community 103 - "QuantNiti: Complete Architectural Blueprint & System Design Document"
Cohesion: 0.15
Nodes (13): 1. Executive Summary & Problem Context, 2. Full-Stack System Architecture, 4.1. The 5-Step Guided Grow Experience, 4.2. Universal Financial & Brand Color Palette, 4.3. Lifecycle Management & Race Condition Guards, 4. Frontend Architecture & Design Engineering, 5. Security, Reliability & Verification Matrix, 6. Cloud Infrastructure & Production Operations (+5 more)

### Community 106 - "2. Audit of the 4 Open-Source Repositories"
Cohesion: 0.20
Nodes (9): 1. Indian & Global Competitor Analysis: What They Provide vs. What They Lack, 2. Audit of the 4 Open-Source Repositories, 3. Synthesis: How QuantNiti Stands Above the Rest, A. `PyPortfolio/PyPortfolioOpt` (Quantitative Gold Standard), B. `agent7898/stock_predictor` (ARIMA + LSTM + Technical Sentiment), C. `AnnaSkarpalezou/Portfolio-Optimization-using-Machine-Learning` (PCA + LSTM), Comprehensive Research: Competitor Matrix & Open-Source Codebase Audit, D. `arunchavan4499/Trading-Assistant` (Professional Quant Trading Assistant) (+1 more)

### Community 107 - "1. Advanced Machine Learning Architecture for Stock & Portfolio Intelligence"
Cohesion: 0.20
Nodes (9): 1. Advanced Machine Learning Architecture for Stock & Portfolio Intelligence, 2. Competitive Moat: Algorithmic Transparency & Disintermediation, 3. Product Features & User Flow Design, 3-Step Guided Journey for Zero-Finance Retail Users, A. Return & Growth Forecasting: Beyond Basic LSTM-DNN, B. Unsupervised Market Regime Detection, C. Portfolio Construction & Allocation, Research: Advanced ML Modeling & Disintermediation Moat (+1 more)

### Community 108 - "QuantNiti: Master Research Dossier & Academic Foundation Document"
Cohesion: 0.20
Nodes (9): 10. Academic References & Bibliography, 7.1 The Four-Pillar Trust Card Framework, 7.2 Grounded Retrieval-Augmented Generation (RAG) Copilot: NitiBot, 7.3 Financial Literacy Microlearning, 7. Explainable AI (XAI) & Human-in-the-Loop Trust Architecture, Comprehensive Technical, Mathematical, Algorithmic, Econometric, and Empirical Specification for IEEE Format Research Publication, Executive Guide for the Research Paper Authoring Agent, QuantNiti: Master Research Dossier & Academic Foundation Document (+1 more)

### Community 109 - "9. IEEE Research Paper Blueprint (Section-by-Section Outline)"
Cohesion: 0.22
Nodes (9): 9. IEEE Research Paper Blueprint (Section-by-Section Outline), I. INTRODUCTION, II. RELATED WORK, III. DATASET ENGINEERING & MULTI-ASSET TAXONOMY, IV. SYSTEM ARCHITECTURE & DESIGN, V. MATHEMATICAL FORMULATION & ALGORITHMIC PIPELINE, VI. EXPERIMENTAL SETUP & EMPIRICAL RESULTS, VII. EXPLAINABLE AI (XAI) & USER TRUST FRAMEWORK (+1 more)

### Community 122 - "README.md"
Cohesion: 0.25
Nodes (3): Core Product Concepts, Language, QuantNiti: Domain Glossary

### Community 124 - "Spec: QuantNiti Core Platform"
Cohesion: 0.29
Nodes (7): Implementation Decisions, Out of Scope, Problem Statement, Solution, Spec: QuantNiti Core Platform, Testing Decisions, User Stories

### Community 125 - "Agent skills"
Cohesion: 0.33
Nodes (5): Agent skills, Domain docs, graphify, Issue tracker, Triage labels

### Community 126 - "Domain Docs"
Cohesion: 0.33
Nodes (5): Before exploring, read these, Domain Docs, File structure, Flag ADR conflicts, Use the glossary's vocabulary

### Community 127 - "Issue tracker: Local Markdown"
Cohesion: 0.33
Nodes (5): Conventions, Issue tracker: Local Markdown, Wayfinding operations, When a skill says "fetch the relevant ticket", When a skill says "publish to the issue tracker"

### Community 128 - "3. Mathematical & Quantitative Algorithmic Deep-Dive"
Cohesion: 0.33
Nodes (6): 3.1. Market Regime Classification (Unsupervised GMM), 3.2. Ledoit-Wolf Covariance Matrix Shrinkage, 3.3. Hierarchical Risk Parity (HRP), 3.4. Multi-Horizon Quantile Growth Forecaster, 3.5. Greedy Integer Discrete Allocation, 3. Mathematical & Quantitative Algorithmic Deep-Dive

### Community 129 - "3. Related Work & Comprehensive Literature Benchmark"
Cohesion: 0.33
Nodes (6): 3.1 Base Paper Deconstruction: Alam et al. (IEEE Access 2024), 3.2 Literature Review: Regime-Switching Models, 3.3 Literature Review: Covariance Regularization & Ill-Conditioning, 3.4 Literature Review: Machine Learning Portfolio Optimization (HRP), 3.5 Exhaustive Industry & Platform Benchmark Matrix (10 Dimensions), 3. Related Work & Comprehensive Literature Benchmark

### Community 130 - "8. Empirical Results, Verification & Benchmarks"
Cohesion: 0.33
Nodes (6): 8.1 Performance Comparison: MVO vs. 1/N Equal Weight vs. HRP, 8.2 Macro Regime Classification Accuracy & Historical Stress Tests, 8.3 Disintermediation Fee Savings Econometric Projections, 8.4 Verification Seams: Pytest (272 Tests) & Vitest (132 Tests), 8. Empirical Results, Verification & Benchmarks, Analysis:

### Community 131 - "RAG-Powered Conversational Assistant (NitiBot)"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, RAG-Powered Conversational Assistant (NitiBot)

### Community 132 - "ESG Conscience Score and Socially Responsible Investing"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, ESG Conscience Score and Socially Responsible Investing

### Community 133 - "Cross-Platform Progressive Web App (PWA) with Responsive Layout"
Cohesion: 0.40
Nodes (4): Consequences, Context, Cross-Platform Progressive Web App (PWA) with Responsive Layout, Decision

### Community 134 - "Prioritizing Portfolio Intelligence Over Pure Strategy Testing"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Prioritizing Portfolio Intelligence Over Pure Strategy Testing

### Community 135 - "Multi-Asset Universe Expansion with Defensive Commodity ETFs"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Multi-Asset Universe Expansion with Defensive Commodity ETFs

### Community 136 - "Server-Side Quantitative ML Computation with Asynchronous ASGI Gateway"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Server-Side Quantitative ML Computation with Asynchronous ASGI Gateway

### Community 137 - "Autonomous AI Ground-Truth Review Fact-Checking Agent"
Cohesion: 0.40
Nodes (4): Autonomous AI Ground-Truth Review Fact-Checking Agent, Consequences, Context, Decision

### Community 139 - "6.2 Multi-Factor Econometric Extraction Engine"
Cohesion: 0.40
Nodes (5): 1. Momentum Pillar, 2. Volatility & Risk Pillar, 3. Market Sensitivity Pillar (CAPM), 4. Sustainability Pillar (ESG Conscience), 6.2 Multi-Factor Econometric Extraction Engine

### Community 140 - "2. Introduction, Problem Statement & Socio-Economic Context"
Cohesion: 0.40
Nodes (5): 2.1 The Retail Investor Crisis in Emerging Markets (The Indian Context), 2.2 The Three Fundamental Dilemmas of Retail Investors, 2.3 Econometric Failures of Classical Models, 2.4 Research Objectives & Core Contributions, 2. Introduction, Problem Statement & Socio-Economic Context

### Community 141 - "4. Dataset Engineering & Multi-Asset Universe"
Cohesion: 0.40
Nodes (5): 4.1 Canonical 58-Asset Universe Taxonomy, 4.2 Benchmark & Macro Volatility Indices, 4.3 Data Preprocessing & Return Formalisms, 4.4 Environmental, Social, and Governance (ESG) Conscience Dataset, 4. Dataset Engineering & Multi-Asset Universe

### Community 142 - "5. End-to-End System Architecture"
Cohesion: 0.40
Nodes (5): 5.1 Decoupled Full-Stack Architecture, 5.2 Four-Tier Quantitative Data Pipeline, 5.3 UX State Machine & Mobile-First PWA Engineering, 5.4 Lifecycle Guards, Concurrency, and AbortController Management, 5. End-to-End System Architecture

### Community 143 - "6.5 Hierarchical Risk Parity (HRP) Optimization Algorithm"
Cohesion: 0.40
Nodes (5): 6.5 Hierarchical Risk Parity (HRP) Optimization Algorithm, Phase 1: Correlation Distance & Hierarchical Tree Clustering, Phase 2: Quasi-Diagonalization (Seriation), Phase 3: Recursive Bisection, Risk Persona Allocation Constraints & ESG Tilting

### Community 149 - "1. Academic Metadata & Proposed Paper Formulations"
Cohesion: 0.50
Nodes (4): 1.1 Candidate Paper Titles, 1.2 Structured Abstract (IEEE Standard), 1.3 IEEE Indexing Terms & Keywords, 1. Academic Metadata & Proposed Paper Formulations

### Community 150 - "6.1 Unsupervised Market Regime Classifier (GMM & Parkinson Volatility)"
Cohesion: 0.50
Nodes (4): 6.1.1 Feature Vector Construction, 6.1.2 Gaussian Mixture Model Formulation, 6.1.3 Deterministic State Mapping via Return-to-Volatility Centroid Ranking, 6.1 Unsupervised Market Regime Classifier (GMM & Parkinson Volatility)

### Community 151 - "6.3 Multi-Horizon Quantile Growth Forecaster & Isotonic Regularization"
Cohesion: 0.50
Nodes (4): 6.3.1 Blended Expected Drift & Volatility, 6.3.2 Closed-Form Geometric Brownian Motion Quantile Cones, 6.3.3 Isotonic Monotonicity Regularization, 6.3 Multi-Horizon Quantile Growth Forecaster & Isotonic Regularization

### Community 153 - "Pivot from Technical Backtesting to Portfolio Growth Intelligence"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Pivot from Technical Backtesting to Portfolio Growth Intelligence

### Community 154 - "Progressive Disclosure UX: 4-Tab Architecture and Embedded Quant Lab Pro Tools"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Progressive Disclosure UX: 4-Tab Architecture and Embedded Quant Lab Pro Tools

### Community 155 - "Virtual Paper Portfolio with Regime-Shift Rebalance Alerts"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Virtual Paper Portfolio with Regime-Shift Rebalance Alerts

### Community 156 - "Explainable AI Trust Card and Disintermediation Moat"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Explainable AI Trust Card and Disintermediation Moat

### Community 157 - "Discrete Integer Allocation and Ledoit-Wolf Covariance Shrinkage"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, Discrete Integer Allocation and Ledoit-Wolf Covariance Shrinkage

## Knowledge Gaps
- **13 isolated node(s):** `@capacitor/android`, `@capacitor/core`, `clsx`, `tailwind-merge`, `@types/node` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1154 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `useAbortableRequest()` connect `GlassCard` to `react`, `GrowPage.tsx`, `QuantNiti: Complete Architectural Blueprint & System Design Document`, `9. IEEE Research Paper Blueprint (Section-by-Section Outline)`, `5. End-to-End System Architecture`, `PortfolioPage.tsx`, `lucide-react`, `useAppStore.ts`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 53 inferred relationships involving `MarketDataService` (e.g. with `test_all()` and `get_history()`) actually correct?**
  _`MarketDataService` has 53 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@capacitor/android`, `@capacitor/core`, `clsx` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `react` be split into smaller, more focused modules?**
  _Cohesion score 0.09608843537414966 - nodes in this community are weakly interconnected._
- **Why does `MarketDataService` connect `MarketDataService` to `pytest`, `ParquetMarketCache`, `PortfolioService`, `create_app`, `backtest/service.py`, `RegimeService`, `streaming.py`, `get_esg_score_for_symbol`, `RAGContextBuilder`, `AlertService`, `BacktestEngine`, `MarketRegimeClassifier`, `alerts/service.py`, `PortfolioRepository`, `test_chat_api.py`, `test_market_service.py`, `ExploreService`, `MarketTickGenerator`, `MarketDataProvider`, `forecaster.py`, `data/service.py`, `ReviewTargetType`, `test_multi_asset_universe.py`, `test_reviews_api.py`, `test_hrp_optimizer.py`, `test_tick_generator.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `MarketRegimeType` (e.g. with `PortfolioRepository` and `evaluate_regime_transition()`) actually correct?**
  _`MarketRegimeType` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `GrowPage.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.07111501316944688 - nodes in this community are weakly interconnected._