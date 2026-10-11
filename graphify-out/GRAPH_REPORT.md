# Graph Report - QuantNiti  (2026-10-11)

## Corpus Check
- 282 files · ~156,652 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .toml 2, .css 2)

## Summary
- 2521 nodes · 5974 edges · 163 communities (132 shown, 31 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 707 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1a147472`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- create_app
- RegimeService
- forecasting/service.py
- test_universe.py
- NitiBotService
- GlassCard
- 🔍 Platform-by-Platform Research (Primary-Source Verified)
- ExplorePage.tsx
- ReviewTargetType
- alerts/service.py
- GrowService
- MarketDataService
- PortfolioPage.tsx
- PrimaryButton
- lucide-react
- PortfolioService
- extract_stock_factors
- PortfolioState
- agent.py
- app.js
- routes/portfolio.py
- compounding_engine.py
- react
- DiscreteAllocationEngine
- AppShell.tsx
- RAGContextBuilder
- reviews/service.py
- AlertService
- MarketTickGenerator
- hrp.py
- simulation/portfolio.py
- forecaster.py
- RiskPersona
- ConversationMemoryManager
- SmartAlertType
- PortfolioRepository
- test_review_tier1_filters.py
- QuantNiti: Hosting, Centralized Server & Scalability Guide
- test_portfolio_storage.py
- pandas
- alerts.py
- fig6_backtest_comparison.py
- test_multi_asset_universe.py
- literacy.py
- BacktestResultData
- ReviewVerificationAgent
- MarketRegimeType
- asyncio
- chat.py
- test_review_factchecker.py
- OnboardingHero.tsx
- scripts
- .__init__
- BacktestService
- test_get_alerts_empty_and_populated
- asyncio
- StrategyType
- test_hrp_optimizer.py
- asyncio
- setup.ts
- MarketDataProvider
- numpy
- triggerHaptic
- test_nitibot_edge_cases.py
- compilerOptions
- vite.config.ts
- test_explore_service.py
- filterBySector
- renderHomeTab
- asyncio
- test_portfolio_full_lifecycle_api
- loadBasketReviews
- package.json
- capacitor.config.ts
- MarketStreamClient
- renderNotificationList
- devDependencies
- asyncio
- backtest.py
- manifest.json
- test_cache.py
- .extract_trades
- escapeHtml
- test_pwa_unit.py
- dependencies
- asyncio
- asyncio
- models.py
- compute_regime_suitability
- test_chat_api.py
- test_client_serving.py
- test_api_routes.py
- asyncio
- asyncio
- test_explore_api.py
- asyncio
- asyncio
- test_literacy_api.py
- compilerOptions
- MarketStreamClient
- asyncio
- os
- storage.py
- sw.js
- app
- QuantNiti: Machine Learning & Quantitative Finance Technical Specification
- QuantNiti (क्वान्टनीति) 🇮🇳
- 2. Platform-by-Platform Verified Primary-Source Audit
- 6. Mathematical Formulations & Algorithmic Engines
- 3. Academic Demonstration & Evaluation Scenarios
- test_stream_api.py
- QuantNiti: Complete Architectural Blueprint & System Design Document
- 2. Audit of the 4 Open-Source Repositories
- 1. Advanced Machine Learning Architecture for Stock & Portfolio Intelligence
- QuantNiti: Master Research Dossier & Academic Foundation Document
- 9. IEEE Research Paper Blueprint (Section-by-Section Outline)
- README.md
- 4.1 Quantitative Factor Extraction Engine
- Spec: QuantNiti Core Platform
- pytest
- Agent skills
- Domain Docs
- Issue tracker: Local Markdown
- 3. Mathematical & Quantitative Algorithmic Deep-Dive
- 3. Related Work & Comprehensive Literature Benchmark
- 8. Empirical Results, Verification & Benchmarks
- RAG-Powered Conversational Assistant (NitiBot)
- ESG Conscience Score and Socially Responsible Investing
- Cross-Platform PWA with Adaptive Desktop Layout
- Portfolio Intelligence Platform over Strategy Testing Platform
- Multi-Asset Investment Universe with Commodity ETFs
- Server-Side ML Computation with Thin-Client Mobile Delivery
- AI Review Verification and Ground-Truth Fact-Checking Agent
- 6. Portfolio Optimization: Hierarchical Risk Parity (HRP) Algorithm
- 6.2 Multi-Factor Econometric Extraction Engine
- 2. Introduction, Problem Statement & Socio-Economic Context
- 4. Dataset Engineering & Multi-Asset Universe
- 5. End-to-End System Architecture
- 6.5 Hierarchical Risk Parity (HRP) Optimization Algorithm
- 1. Foundational Problem Statement & Financial Econometrics
- 2. Datasets, Ingestion Architecture & Preprocessing Justifications
- 8. Geometric Brownian Motion (GBM) Long-Horizon Wealth Compounding
- 1. Academic Metadata & Proposed Paper Formulations
- 6.1 Unsupervised Market Regime Classifier (GMM & Parkinson Volatility)
- 6.3 Multi-Horizon Quantile Growth Forecaster & Isotonic Regularization
- 0001-pivot-from-backtesting-to-portfolio-growth-intelligence.md
- 0002-dual-tabbed-architecture-investor-and-quant-lab.md
- 0003-virtual-paper-portfolio-with-regime-rebalancing-alerts.md
- 0004-explainable-ai-trust-card-and-disintermediation-model.md
- 0005-discrete-allocation-and-ledoit-wolf-covariance-shrinkage.md
- agents/triage-labels.md

## God Nodes (most connected - your core abstractions)
1. `MarketDataService` - 83 edges
2. `react` - 67 edges
3. `MarketRegimeType` - 59 edges
4. `RegimeService` - 58 edges
5. `RiskPersona` - 50 edges
6. `create_app()` - 45 edges
7. `useAppStore` - 45 edges
8. `lucide-react` - 42 edges
9. `PortfolioState` - 42 edges
10. `GlassCard()` - 42 edges

## Surprising Connections (you probably didn't know these)
- `4.3. Lifecycle Management & Race Condition Guards` --references--> `useAbortableRequest()`  [INFERRED]
  docs/ARCHITECTURE.md → src/frontend/hooks/useAbortableRequest.ts
- `5.4 Lifecycle Guards, Concurrency, and AbortController Management` --references--> `useAbortableRequest()`  [INFERRED]
  docs/RESEARCH_PAPER_MASTER_DOSSIER.md → src/frontend/hooks/useAbortableRequest.ts
- `IV. SYSTEM ARCHITECTURE & DESIGN` --references--> `useAbortableRequest()`  [INFERRED]
  docs/RESEARCH_PAPER_MASTER_DOSSIER.md → src/frontend/hooks/useAbortableRequest.ts
- `test_train_model()` --uses--> `RegimeTrainResponse`  [INFERRED]
  tests/integration/test_regime_service.py → src/app/core/models.py
- `test_get_growth_forecast()` --uses--> `MultiHorizonGrowthForecast`  [INFERRED]
  tests/integration/test_explore_service.py → src/app/core/models.py

## Import Cycles
- None detected.

## Communities (163 total, 31 thin omitted)

### Community 0 - "create_app"
Cohesion: 0.06
Nodes (22): create_app(), ParquetMarketCache, MockDataProvider, test_app(), app(), configured_app(), MockGeminiAdapter, unconfigured_app() (+14 more)

### Community 1 - "RegimeService"
Cohesion: 0.07
Nodes (15): get_current_regime(), get_regime_history(), get_regime_service(), train_regime_model(), TrainRegimeRequest, CurrentRegimeResponse, RegimeHistoricalPoint, RegimeHistoryResponse (+7 more)

### Community 2 - "forecasting/service.py"
Cohesion: 0.08
Nodes (20): get_explore_service(), get_growth_forecast(), get_stock_profile(), get_ticker_esg(), list_explore_stocks(), get_history(), BenchmarkComparison, ESGScoreResponse (+12 more)

### Community 3 - "test_universe.py"
Cohesion: 0.08
Nodes (7): denormalize_symbol(), test_denormalize_symbol_for_provider(), test_get_sector_for_symbol(), test_get_universe_metadata(), test_get_universe_symbols(), test_is_valid_symbol(), test_normalize_symbol()

### Community 4 - "NitiBotService"
Cohesion: 0.15
Nodes (12): ChatMessageRequest, ChatMessageResponse, NitiBotService, test_edge_case_empty_or_whitespace_message(), test_edge_case_huge_message_overflow(), test_edge_case_sebi_compliance_always_injected(), MockGeminiAdapter, test_nitibot_service_chat_raises_when_unavailable() (+4 more)

### Community 5 - "GlassCard"
Cohesion: 0.10
Nodes (27): AdaptiveHomeCard(), AdaptiveHomeCardProps, CompoundingVisualizer(), CompoundingVisualizerProps, LearningHub(), LearningHubProps, isIndianMarketOpen(), MarketPulse() (+19 more)

### Community 6 - "🔍 Platform-by-Platform Research (Primary-Source Verified)"
Cohesion: 0.07
Nodes (27): 1. Groww (groww.in), 2. Zerodha Streak (streak.tech), 3. Smallcase (smallcase.com), 4. INDmoney (indmoney.com), 5. MoneyControl Pro / Super Pro (moneycontrol.com), 6. TradingView (tradingview.com), Bank FD Rates vs. Equity Returns (2025–2026 Context), 🎯 Consolidated Competitive Matrix (10 Dimensions) (+19 more)

### Community 7 - "ExplorePage.tsx"
Cohesion: 0.08
Nodes (29): ASSETS, ProToolsBacktester(), STRATEGIES, ExploreStockItem, StockCard(), StockCardProps, StockProfileModal(), StockProfileModalProps (+21 more)

### Community 8 - "ReviewTargetType"
Cohesion: 0.11
Nodes (11): LiteracyCategory, ReviewStatus, ReviewTargetType, test_tier2_approves_pure_qualitative_reviews(), test_tier2_approves_verified_claim_within_tolerance(), test_service_rejects_and_does_not_publish_exaggerated_review(), test_service_submits_and_stores_verified_review(), test_agent_approves_and_verifies_authentic_review() (+3 more)

### Community 9 - "alerts/service.py"
Cohesion: 0.24
Nodes (8): AlertSeverity, SmartAlert, evaluate_52w_high_breakout(), evaluate_drawdown_breach(), evaluate_factor_anomaly(), evaluate_portfolio_drift(), evaluate_regime_transition(), evaluate_rsi_extreme()

### Community 10 - "GrowService"
Cohesion: 0.07
Nodes (15): get_grow_service(), recommend_basket_alias(), recommend_basket_get(), recommend_basket_post(), health_check(), BasketRecommendationResponse, HRPOptimizer, GrowService (+7 more)

### Community 11 - "MarketDataService"
Cohesion: 0.06
Nodes (19): get_market_service(), get_quote(), get_returns_matrix(), get_universe(), sync_universe(), SyncRequest, StockQuote, SyncResult (+11 more)

### Community 12 - "PortfolioPage.tsx"
Cohesion: 0.14
Nodes (22): OrderSheetModalProps, PortfolioReportCardProps, CompoundingTrajectoryChart(), CompoundingTrajectoryChartProps, DemoPortfolio(), DemoPortfolioProps, BenchmarkComparison, CompoundingTrajectoryData (+14 more)

### Community 13 - "PrimaryButton"
Cohesion: 0.11
Nodes (35): chart.js, framer-motion, react-chartjs-2, AllocationDonut(), AllocationDonutProps, AllocationItem, PALETTE, GrowPage() (+27 more)

### Community 14 - "lucide-react"
Cohesion: 0.16
Nodes (23): lucide-react, COMPARISON_ROWS, CompetitorBenchmarkModal(), CompetitorBenchmarkModalProps, ConceptDetailData, ConceptDetailModal(), ConceptDetailModalProps, ModalRoot() (+15 more)

### Community 15 - "PortfolioService"
Cohesion: 0.11
Nodes (7): CreatePortfolioRequest, PortfolioService, portfolio_service(), test_create_and_get_portfolio(), test_get_nonexistent_portfolio_raises_error(), test_get_order_sheet(), test_rebalance_diff_and_apply()

### Community 16 - "extract_stock_factors"
Cohesion: 0.12
Nodes (14): compute_bollinger_bands(), compute_ema(), compute_macd(), compute_max_drawdown(), compute_rsi(), compute_stock_beta_and_alpha(), extract_stock_factors(), sample_stock_and_index() (+6 more)

### Community 17 - "PortfolioState"
Cohesion: 0.16
Nodes (11): BrokerOrderItem, BrokerOrderSheet, PortfolioState, RebalanceAlert, RebalanceItemDiff, compute_rebalance_diff(), execute_rebalance(), generate_broker_order_sheet() (+3 more)

### Community 18 - "agent.py"
Cohesion: 0.16
Nodes (6): ReviewVerificationResult, filter_tier1_content(), extract_duration_claim(), extract_return_claim(), verify_tier2_fact_check(), audit_tier3_llm()

### Community 19 - "app.js"
Cohesion: 0.08
Nodes (37): AppState, askNitiBotAboutConcept(), askNitiBotAboutCurrentConcept(), closeCompetitorBenchmarkModal(), closeConceptModal(), closeModalSheet(), closeNitiBotChat(), closeNitiBotModal() (+29 more)

### Community 20 - "routes/portfolio.py"
Cohesion: 0.15
Nodes (10): apply_rebalance_endpoint(), calculate_compounding_endpoint(), create_portfolio_endpoint(), delete_portfolio_endpoint(), get_order_sheet_endpoint(), get_portfolio_endpoint(), get_portfolio_service(), get_rebalance_diff_endpoint() (+2 more)

### Community 21 - "compounding_engine.py"
Cohesion: 0.10
Nodes (18): CompoundingMonthlyPoint, CompoundingRequest, CompoundingSummary, CompoundingTippingPoint, CompoundingYearlyPoint, calculate_lump_sum(), calculate_monthly_sip(), calculate_step_up_sip() (+10 more)

### Community 22 - "react"
Cohesion: 0.07
Nodes (34): react, react-dom, react-router-dom, @testing-library/react, @testing-library/user-event, vitest, App(), Theme (+26 more)

### Community 23 - "DiscreteAllocationEngine"
Cohesion: 0.08
Nodes (3): DiscreteAllocationEngine, DiscreteAllocationResult, TestDiscreteAllocationEngine

### Community 24 - "AppShell.tsx"
Cohesion: 0.13
Nodes (22): AppShell(), BottomNav(), BottomNavProps, NAV_ITEMS, NavItem, triggerHaptic(), Header(), HeaderProps (+14 more)

### Community 25 - "RAGContextBuilder"
Cohesion: 0.14
Nodes (12): RAGContextPayload, RAGContextBuilder, create_sample_backtest(), create_sample_regime(), test_rag_context_builder_builds_complete_grounding(), test_rag_context_builder_esg_enrichment(), test_rag_context_builder_fallback_defaults(), test_edge_case_corrupted_or_unexpected_context_types() (+4 more)

### Community 26 - "reviews/service.py"
Cohesion: 0.16
Nodes (8): get_review_service(), get_target_reviews(), preview_verification(), submit_review(), ReviewsListResponse, ReviewSubmissionRequest, ReviewSubmissionResponse, ReviewService

### Community 27 - "AlertService"
Cohesion: 0.11
Nodes (3): PushSubscriptionRequest, AlertService, test_alert_service_deduplication()

### Community 28 - "MarketTickGenerator"
Cohesion: 0.09
Nodes (7): get_tick_generator(), stream_ticks(), MarketTick, is_indian_market_open(), MarketTickGenerator, test_generate_single_tick(), test_live_fallback_to_synthetic()

### Community 29 - "hrp.py"
Cohesion: 0.14
Nodes (6): apply_weight_caps(), compute_hrp_weights(), get_cluster_variance(), get_quasi_diag_order(), _traverse(), recursive_bisection()

### Community 30 - "simulation/portfolio.py"
Cohesion: 0.13
Nodes (8): BenchmarkComparisonLive, PortfolioHolding, calculate_day_over_day_mtm(), update_portfolio_mark_to_market(), base_portfolio(), test_aggregate_portfolio_day_over_day_mtm(), test_holding_day_over_day_mtm_formula(), sample_portfolio_state()

### Community 31 - "forecaster.py"
Cohesion: 0.16
Nodes (7): HorizonForecastCone, MultiHorizonForecaster, mock_stock_forecasts(), _create_forecast(), test_forecast_all_four_horizons(), test_forecast_cone_widening_over_longer_horizons(), test_strict_quantile_monotonicity()

### Community 32 - "RiskPersona"
Cohesion: 0.14
Nodes (8): RiskPersona, create_portfolio_from_allocations(), PortfolioSimulator, test_build_trust_card_pillars(), sample_allocations(), test_create_portfolio_from_allocations(), test_update_portfolio_mark_to_market(), bull_portfolio()

### Community 33 - "ConversationMemoryManager"
Cohesion: 0.24
Nodes (7): ConversationMemoryManager, MessageTurn, test_edge_case_sliding_window_memory_limits(), test_memory_manager_add_and_retrieve_turns(), test_memory_manager_clear_session(), test_memory_manager_format_for_gemini(), test_memory_manager_sliding_window_limit()

### Community 34 - "SmartAlertType"
Cohesion: 0.15
Nodes (7): SmartAlertType, test_trigger_1_regime_transition(), test_trigger_2_portfolio_drift(), test_trigger_3_rsi_extremes(), test_trigger_4_drawdown_breach(), test_trigger_5_52w_high_breakout(), test_trigger_6_factor_score_anomaly()

### Community 36 - "test_review_tier1_filters.py"
Cohesion: 0.12
Nodes (7): test_tier1_blocks_email_addresses(), test_tier1_blocks_external_urls(), test_tier1_blocks_phone_numbers(), test_tier1_blocks_profanity(), test_tier1_blocks_prohibited_stock_tips(), test_tier1_blocks_telegram_and_social_handles(), test_tier1_clean_reviews_pass()

### Community 37 - "QuantNiti: Hosting, Centralized Server & Scalability Guide"
Cohesion: 0.13
Nodes (14): 1. Architectural Overview, 2. 1-Click Cloud Deployment Guides, 3. Running with Docker & Docker Compose (Any VPS / Local Machine), 4. Connecting Standalone Clients (Mobile APK & PWAs), 5. Horizontal & Vertical Scalability, ASGI Concurrency, Direct Docker Run, Memory Optimization (+6 more)

### Community 38 - "test_portfolio_storage.py"
Cohesion: 0.15
Nodes (5): repo(), test_delete_portfolio_cascades(), test_list_portfolios(), test_portfolio_schema_creation(), test_save_and_get_portfolio()

### Community 39 - "pandas"
Cohesion: 0.13
Nodes (10): align_to_trading_calendar(), calculate_returns(), sanitize_raw_provider_data(), validate_ohlcv_dataframe(), test_align_to_trading_calendar(), test_calculate_returns(), test_models_validation(), test_validate_ohlcv_dataframe_drops_invalid_rows() (+2 more)

### Community 40 - "alerts.py"
Cohesion: 0.14
Nodes (11): clear_alerts(), evaluate_alerts_micro_batch(), get_alert_service(), get_vapid_public_key(), list_alerts(), mark_alert_read(), mark_all_alerts_read(), send_test_push_notification() (+3 more)

### Community 42 - "test_multi_asset_universe.py"
Cohesion: 0.17
Nodes (5): test_asset_class_enum_members(), test_commodity_etfs_constituents(), test_defense_constituents(), test_expanded_universe_total_count(), test_metals_constituents()

### Community 43 - "literacy.py"
Cohesion: 0.21
Nodes (5): get_all_literacy_cards(), _get_cards_dict(), get_literacy_card_by_key(), _get_literacy_data(), LiteracyCard

### Community 44 - "BacktestResultData"
Cohesion: 0.15
Nodes (9): BacktestMetrics, BacktestTrade, RegimePerformanceBreakdown, BacktestResultData, calculate_backtest_metrics(), calculate_regime_breakdown(), mock_backtest_result(), test_calculate_backtest_metrics_values() (+1 more)

### Community 46 - "ReviewVerificationAgent"
Cohesion: 0.18
Nodes (3): ReviewVerificationAgent, review_service(), agent()

### Community 47 - "MarketRegimeType"
Cohesion: 0.17
Nodes (5): MarketRegimeType, MarketRegimeClassifier, test_classifier_fit_and_predict(), test_classifier_probabilities_sum_to_one(), test_classifier_state_label_determinism()

### Community 48 - "asyncio"
Cohesion: 0.18
Nodes (5): test_get_grow_recommend_success(), test_grow_recommend_esg_conscious_api(), test_grow_recommend_validation_errors(), test_post_baskets_recommend_alias(), test_post_grow_recommend_success()

### Community 49 - "chat.py"
Cohesion: 0.31
Nodes (4): get_chat_status(), get_nitibot_service(), post_chat_message(), ChatStatusResponse

### Community 50 - "test_review_factchecker.py"
Cohesion: 0.20
Nodes (4): test_extract_duration_claim(), test_extract_return_claim(), test_tier2_flags_borderline_discrepancy(), test_tier2_rejects_exaggerated_return_claims()

### Community 51 - "OnboardingHero.tsx"
Cohesion: 0.19
Nodes (16): HorizonOption, Step2HorizonProps, PersonaCardDef, Step3PersonaProps, SummaryPillsProps, OnboardingHeroProps, calculatePersonaResult(), PERSONA_DETAILS (+8 more)

### Community 52 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, apk:build, build, cap:open, cap:sync, dev, mobile:serve, preview (+1 more)

### Community 54 - "BacktestService"
Cohesion: 0.15
Nodes (7): BacktestDataPoint, BacktestService, backtest_service(), test_backtest_service_invalid_symbol_raises_error(), test_backtest_service_run_buy_and_hold_nifty(), test_backtest_service_run_ma_crossover_stock(), test_backtest_service_with_date_filter()

### Community 55 - "test_get_alerts_empty_and_populated"
Cohesion: 0.22
Nodes (4): test_evaluate_endpoint(), test_get_alerts_empty_and_populated(), test_mark_alert_read_and_clear(), test_web_push_subscription_and_vapid_key()

### Community 56 - "asyncio"
Cohesion: 0.22
Nodes (4): test_backtest_validation_errors(), test_get_backtest_run_success(), test_post_backtest_run_success(), test_post_quant_lab_backtest_alias()

### Community 57 - "StrategyType"
Cohesion: 0.14
Nodes (10): StrategyType, BacktestEngine, benchmark_price_series(), sample_price_series(), test_bollinger_bands_strategy(), test_buy_and_hold_strategy(), test_dual_momentum_strategy(), test_ma_crossover_strategy() (+2 more)

### Community 58 - "test_hrp_optimizer.py"
Cohesion: 0.09
Nodes (14): compute_shrunk_covariance(), sample_returns_df(), test_compute_hrp_weights_helper_function(), test_compute_shrunk_covariance_fallback_on_degenerate_data(), test_compute_shrunk_covariance_ledoit_wolf(), test_compute_shrunk_covariance_without_shrinkage(), test_hrp_distance_matrix_conditioning_extreme_correlation(), test_hrp_optimizer_all_personas_and_caps() (+6 more)

### Community 59 - "asyncio"
Cohesion: 0.22
Nodes (4): test_get_reviews_endpoint(), test_submit_exaggerated_review_rejected(), test_submit_prohibited_spam_rejected(), test_submit_verified_review()

### Community 60 - "setup.ts"
Cohesion: 0.25
Nodes (3): @testing-library/jest-dom, localStorageMock, sessionStorageMock

### Community 62 - "numpy"
Cohesion: 0.13
Nodes (11): draw_ellipse(), calculate_parkinson_volatility(), calculate_realized_volatility(), calculate_rolling_log_returns(), extract_regime_features(), sample_stock_and_index(), sample_market_data(), test_calculate_parkinson_volatility() (+3 more)

### Community 63 - "triggerHaptic"
Cohesion: 0.12
Nodes (19): backtestCurrentStock(), clearNitiBotChat(), closeStockProfileModal(), copyGrowwFormat(), copyZerodhaFormat(), dismissIOSInstallBanner(), loadVideoFacade(), openCreatePortfolioModal() (+11 more)

### Community 65 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+10 more)

### Community 67 - "test_explore_service.py"
Cohesion: 0.33
Nodes (4): explore_service(), test_get_growth_forecast(), test_get_stock_profile(), test_list_explore_stocks_and_filter()

### Community 68 - "filterBySector"
Cohesion: 0.40
Nodes (5): filterBySector(), filterStocks(), loadExploreStocks(), renderExploreStockGrid(), renderHomeTopPicks()

### Community 69 - "renderHomeTab"
Cohesion: 0.24
Nodes (18): activateBasketToPortfolio(), applyRebalance(), checkRebalanceDiff(), closeCreatePortfolioModal(), deleteActivePortfolio(), deletePortfolioFromIndexedDB(), handlePortfolioSwitch(), loadPortfoliosFromIndexedDB() (+10 more)

### Community 72 - "loadBasketReviews"
Cohesion: 0.50
Nodes (4): closeWriteReviewModal(), loadBasketReviews(), renderReviewsSummary(), submitUserReview()

### Community 73 - "package.json"
Cohesion: 0.11
Nodes (17): name, private, type, version, autoprefixer, @capacitor/android, @capacitor/core, clsx (+9 more)

### Community 75 - "MarketStreamClient"
Cohesion: 0.15
Nodes (5): marketStream, MarketStreamClient, MarketTick, TickListener, MockEventSource

### Community 79 - "renderNotificationList"
Cohesion: 0.17
Nodes (16): clearAllNotifications(), downloadBlob(), downloadPortfolioReportPDF(), filterNotifications(), formatAlertTime(), generatePortfolioReportBlob(), initNotificationCenter(), loadNotifications() (+8 more)

### Community 83 - "devDependencies"
Cohesion: 0.13
Nodes (15): devDependencies, autoprefixer, jsdom, postcss, tailwindcss, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event (+7 more)

### Community 87 - "asyncio"
Cohesion: 0.13
Nodes (7): test_adaptive_home_tab_components(), test_advanced_analysis_drawer_in_explore_tab(), test_android_physics_and_haptics_in_js(), test_compounding_visualizer_and_wealth_engine_ui(), test_four_tab_navigation_structure(), test_groww_theme_and_dual_theme_tokens(), test_multi_portfolio_storage_and_mtm_ui()

### Community 91 - "backtest.py"
Cohesion: 0.25
Nodes (6): get_backtest_service(), run_backtest_get(), run_backtest_post(), run_quant_lab_backtest_alias(), BacktestRequest, BacktestResponse

### Community 92 - "manifest.json"
Cohesion: 0.14
Nodes (13): background_color, categories, description, display, icons, id, name, orientation (+5 more)

### Community 95 - "test_cache.py"
Cohesion: 0.14
Nodes (5): sample_df(), temp_cache_dir(), test_cache_invalidation(), test_cache_save_and_load(), test_cache_ttl_expiration()

### Community 97 - "escapeHtml"
Cohesion: 0.21
Nodes (13): escapeHtml(), filterLearningCategory(), filterReviewsList(), initLearningHub(), openConceptModal(), renderLearningCards(), renderLearningHub(), renderReviewsList() (+5 more)

### Community 107 - "test_pwa_unit.py"
Cohesion: 0.17
Nodes (5): test_desktop_responsive_css_rules(), test_icon_assets_exist(), test_manifest_file_exists_and_valid(), test_offline_page_exists_and_styled(), test_service_worker_script_structure()

### Community 114 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, @capacitor/android, @capacitor/cli, @capacitor/core, chart.js, clsx, framer-motion, lucide-react (+6 more)

### Community 116 - "asyncio"
Cohesion: 0.18
Nodes (5): test_index_html_contains_pwa_metadata_and_elements(), test_manifest_endpoint_served_with_correct_mime(), test_offline_page_endpoint(), test_pwa_icons_served(), test_service_worker_endpoint_served_with_allowed_header()

### Community 117 - "asyncio"
Cohesion: 0.18
Nodes (5): test_app_js_contains_report_export_and_share_functions(), test_html_contains_download_and_share_buttons(), test_html_contains_portfolio_report_card_template_with_all_sections(), test_html_contains_report_card_cdn_scripts(), test_styles_contain_report_card_layout_rules()

### Community 118 - "models.py"
Cohesion: 0.13
Nodes (24): BasketAllocationItem, BasketGrowthProjections, BasketRecommendationRequest, BenchmarkComparisonItem, LiteracyListResponse, MarketHistoryResponse, MultiHorizonGrowthForecast, OHLCVBar (+16 more)

### Community 123 - "compute_regime_suitability"
Cohesion: 0.33
Nodes (5): RegimeSuitability, compute_regime_suitability(), test_suitability_in_bear_regime(), test_suitability_in_bull_regime(), test_suitability_score_bounds()

### Community 124 - "test_chat_api.py"
Cohesion: 0.43
Nodes (4): test_chat_endpoint_graceful_degradation_503(), test_chat_endpoint_success(), test_chat_status_endpoint(), test_chat_status_endpoint_when_disabled()

### Community 125 - "test_client_serving.py"
Cohesion: 0.29
Nodes (5): test_app_route_serves_html(), test_competitor_benchmark_drawer_served(), test_root_serves_html(), test_static_assets_served(), test_vite_build_assets_served()

### Community 132 - "test_api_routes.py"
Cohesion: 0.39
Nodes (7): test_get_history_endpoint(), test_get_quote_endpoint(), test_get_returns_matrix_endpoint(), test_get_universe_endpoint(), test_get_universe_filtered_by_sector(), test_health_endpoint(), test_sync_endpoint()

### Community 134 - "asyncio"
Cohesion: 0.22
Nodes (4): test_compounding_endpoint_mounted_at_both_prefixes(), test_compounding_endpoint_standalone_post(), test_compounding_endpoint_validation_errors(), test_compounding_endpoint_with_portfolio_id()

### Community 135 - "asyncio"
Cohesion: 0.22
Nodes (4): test_e2e_explore_stock_to_quant_lab_backtest_journey(), test_e2e_grow_basket_to_virtual_portfolio_lifecycle(), test_e2e_quant_lab_multi_strategy_suite(), test_e2e_regime_radar_history_endpoint()

### Community 136 - "test_explore_api.py"
Cohesion: 0.39
Nodes (7): test_explore_stocks_contain_esg_fields(), test_get_explore_stocks_filtered(), test_get_explore_stocks_route(), test_get_growth_forecast_route(), test_get_stock_profile_route(), test_get_ticker_esg_endpoint(), test_stock_profile_contains_esg()

### Community 137 - "asyncio"
Cohesion: 0.22
Nodes (4): test_create_and_list_multiple_portfolios(), test_delete_portfolio_lifecycle(), test_dual_prefix_routing_portfolios(), test_portfolio_detail_mtm_metrics()

### Community 139 - "asyncio"
Cohesion: 0.22
Nodes (4): test_app_js_contains_market_stream_client(), test_html_contains_notification_bell_drawer_and_toasts(), test_service_worker_push_event_listeners(), test_styles_contain_tick_flash_and_drawer()

### Community 144 - "test_literacy_api.py"
Cohesion: 0.39
Nodes (5): test_dual_routing_api_prefix(), test_get_all_literacy_cards_category_filter(), test_get_all_literacy_cards_v1(), test_get_literacy_card_by_unknown_key_returns_404(), test_get_literacy_card_by_valid_key()

### Community 145 - "compilerOptions"
Cohesion: 0.25
Nodes (7): compilerOptions, allowSyntheticDefaultImports, composite, module, moduleResolution, skipLibCheck, include

### Community 148 - "asyncio"
Cohesion: 0.29
Nodes (3): test_app_js_contains_review_management_functions(), test_html_contains_review_section_and_modal(), test_styles_contain_review_and_badge_classes()

### Community 151 - "os"
Cohesion: 0.11
Nodes (7): main(), run_command(), get_lan_ip(), main(), print_qr_code(), test_app_js_exports_report_functions(), test_report_blob_generation_and_share_flow_headless()

### Community 161 - "storage.py"
Cohesion: 0.09
Nodes (8): ReviewItem, ReviewRepository, Base, DailySnapshotRecord, HoldingRecord, PortfolioRecord, ReviewRecord, TransactionRecord

### Community 258 - "QuantNiti: Machine Learning & Quantitative Finance Technical Specification"
Cohesion: 0.11
Nodes (18): 10. End-to-End Execution Flowchart & Mathematical Reference, 3.1 Feature Engineering Matrix, 3.2 GMM Formulation & Expectation-Maximization (EM), 3.3 Deterministic State Mapping via Return-to-Volatility Centroids, 3. Unsupervised Market Regime Classification Engine (GMM & Features), 5.1 Formulation, 5.2 Ridge Regularization Layer, 5. Covariance Matrix Regularization: Ledoit-Wolf Shrinkage (+10 more)

### Community 281 - "QuantNiti (क्वान्टनीति) 🇮🇳"
Cohesion: 0.13
Nodes (15): 1. Prerequisites, 2. Installation, 3. Running Locally, AI-Driven Regime-Adaptive Portfolio Intelligence & Quantitative Decision Support System, 🎯 Core Mathematical & Algorithmic Methodologies, Development Mode (Hot Reloading Frontend & Backend):, 📱 Key Product Capabilities, 📄 License & Attribution (+7 more)

### Community 313 - "2. Platform-by-Platform Verified Primary-Source Audit"
Cohesion: 0.17
Nodes (11): 1. Executive Summary: The Structural Gap in Indian WealthTech, 2. Platform-by-Platform Verified Primary-Source Audit, 3. Comprehensive 10-Dimension Competitive Matrix, 4. Key Takeaways for Academic & Industry Evaluation, A. MoneyControl (Pro & Super Pro), B. Zerodha (Kite + Streak), C. Groww (Stocks & Portfolio Analysis), D. INDmoney (+3 more)

### Community 320 - "6. Mathematical Formulations & Algorithmic Engines"
Cohesion: 0.18
Nodes (11): 6.4 Ledoit-Wolf Covariance Matrix Regularization, 6.6.1 Greedy Deficit-Minimization Sizing (Primary Real-Time Algorithm), 6.6.2 Mixed-Integer Linear Programming (MILP Formulation), 6.6 Discrete Integer Share Sizing & Cash Buffer Optimization, 6.7.1 Stochastic Differential Equation (SDE), 6.7.2 Monthly Systematic Investment Plan (SIP) with Annual Step-Up, 6.7.3 The Compounding Tipping Point, 6.7 Geometric Brownian Motion Compounding & Analytical Tipping Point (+3 more)

### Community 321 - "3. Academic Demonstration & Evaluation Scenarios"
Cohesion: 0.18
Nodes (10): 1. System Overview, 2. Launching the Application, 3. Academic Demonstration & Evaluation Scenarios, 4-Tab Navigation Architecture, 4. Test Suite Execution, Demonstration 1: Retail Investor Flow (`Grow` Tab), Demonstration 2: Stock Explorer Flow (`Explore` Tab), Demonstration 3: Quant Lab Strategy Studio (`Quant Lab` Tab) (+2 more)

### Community 322 - "test_stream_api.py"
Cohesion: 0.10
Nodes (10): test_stream_ticks_alias_route(), test_stream_ticks_endpoint_headers_and_event(), test_stream_ticks_symbol_filter(), test_invalid_literacy_card_fails_validation(), test_literacy_cards_schema_and_count(), market_service(), test_format_sse_event(), test_generate_batch_ticks() (+2 more)

### Community 339 - "QuantNiti: Complete Architectural Blueprint & System Design Document"
Cohesion: 0.20
Nodes (10): 1. Executive Summary & Problem Context, 2. Full-Stack System Architecture, 4.1. The 5-Step Guided Grow Experience, 4.2. Universal Financial & Brand Color Palette, 4.3. Lifecycle Management & Race Condition Guards, 4. Frontend Architecture & Design Engineering, 5. Security, Reliability & Verification Matrix, 6. Deployment & Operations (+2 more)

### Community 340 - "2. Audit of the 4 Open-Source Repositories"
Cohesion: 0.20
Nodes (9): 1. Indian & Global Competitor Analysis: What They Provide vs. What They Lack, 2. Audit of the 4 Open-Source Repositories, 3. Synthesis: How QuantNiti Stands Above the Rest, A. `PyPortfolio/PyPortfolioOpt` (Quantitative Gold Standard), B. `agent7898/stock_predictor` (ARIMA + LSTM + Technical Sentiment), C. `AnnaSkarpalezou/Portfolio-Optimization-using-Machine-Learning` (PCA + LSTM), Comprehensive Research: Competitor Matrix & Open-Source Codebase Audit, D. `arunchavan4499/Trading-Assistant` (Professional Quant Trading Assistant) (+1 more)

### Community 341 - "1. Advanced Machine Learning Architecture for Stock & Portfolio Intelligence"
Cohesion: 0.20
Nodes (9): 1. Advanced Machine Learning Architecture for Stock & Portfolio Intelligence, 2. Competitive Moat: Algorithmic Transparency & Disintermediation, 3. Product Features & User Flow Design, 3-Step Guided Journey for Zero-Finance Retail Users, A. Return & Growth Forecasting: Beyond Basic LSTM-DNN, B. Unsupervised Market Regime Detection, C. Portfolio Construction & Allocation, Research: Advanced ML Modeling & Disintermediation Moat (+1 more)

### Community 342 - "QuantNiti: Master Research Dossier & Academic Foundation Document"
Cohesion: 0.20
Nodes (9): 10. Academic References & Bibliography, 7.1 The Four-Pillar Trust Card Framework, 7.2 Grounded Retrieval-Augmented Generation (RAG) Copilot: NitiBot, 7.3 Financial Literacy Microlearning, 7. Explainable AI (XAI) & Human-in-the-Loop Trust Architecture, Comprehensive Technical, Mathematical, Algorithmic, Econometric, and Empirical Specification for IEEE Format Research Publication, Executive Guide for the Research Paper Authoring Agent, QuantNiti: Master Research Dossier & Academic Foundation Document (+1 more)

### Community 347 - "9. IEEE Research Paper Blueprint (Section-by-Section Outline)"
Cohesion: 0.22
Nodes (9): 9. IEEE Research Paper Blueprint (Section-by-Section Outline), I. INTRODUCTION, II. RELATED WORK, III. DATASET ENGINEERING & MULTI-ASSET TAXONOMY, IV. SYSTEM ARCHITECTURE & DESIGN, V. MATHEMATICAL FORMULATION & ALGORITHMIC PIPELINE, VI. EXPERIMENTAL SETUP & EMPIRICAL RESULTS, VII. EXPLAINABLE AI (XAI) & USER TRUST FRAMEWORK (+1 more)

### Community 361 - "README.md"
Cohesion: 0.25
Nodes (3): Core Product Concepts, Language, QuantNiti: Domain Glossary

### Community 362 - "4.1 Quantitative Factor Extraction Engine"
Cohesion: 0.25
Nodes (8): 1. Momentum Pillar, 2. Volatility & Risk Pillar, 3. Market Sensitivity Pillar (CAPM), 4.1 Quantitative Factor Extraction Engine, 4.2 Multi-Factor Drift & Volatility Blending, 4.3 Quantile Cones & Strict Monotonicity Enforcement, 4. Multi-Factor Asset Extraction & Quantile Growth Forecasting Cones, 4. Sustainability Pillar (ESG Conscience)

### Community 363 - "Spec: QuantNiti Core Platform"
Cohesion: 0.25
Nodes (8): Further Notes, Implementation Decisions, Out of Scope, Problem Statement, Solution, Spec: QuantNiti Core Platform, Testing Decisions, User Stories

### Community 381 - "pytest"
Cohesion: 0.06
Nodes (14): Settings, AssetClass, get_asset_class_for_symbol(), get_sector_for_symbol(), get_universe_metadata(), get_universe_symbols(), test_explore_stocks_total_and_asset_class_filter(), test_get_current_regime_route() (+6 more)

### Community 382 - "Agent skills"
Cohesion: 0.33
Nodes (5): Agent skills, Domain docs, graphify, Issue tracker, Triage labels

### Community 392 - "Domain Docs"
Cohesion: 0.33
Nodes (5): Before exploring, read these, Domain Docs, File structure, Flag ADR conflicts, Use the glossary's vocabulary

### Community 393 - "Issue tracker: Local Markdown"
Cohesion: 0.33
Nodes (5): Conventions, Issue tracker: Local Markdown, Wayfinding operations, When a skill says "fetch the relevant ticket", When a skill says "publish to the issue tracker"

### Community 394 - "3. Mathematical & Quantitative Algorithmic Deep-Dive"
Cohesion: 0.33
Nodes (6): 3.1. Market Regime Classification (Unsupervised GMM), 3.2. Ledoit-Wolf Covariance Matrix Shrinkage, 3.3. Hierarchical Risk Parity (HRP), 3.4. Multi-Horizon Quantile Growth Forecaster, 3.5. Greedy Integer Discrete Allocation, 3. Mathematical & Quantitative Algorithmic Deep-Dive

### Community 395 - "3. Related Work & Comprehensive Literature Benchmark"
Cohesion: 0.33
Nodes (6): 3.1 Base Paper Deconstruction: Alam et al. (IEEE Access 2024), 3.2 Literature Review: Regime-Switching Models, 3.3 Literature Review: Covariance Regularization & Ill-Conditioning, 3.4 Literature Review: Machine Learning Portfolio Optimization (HRP), 3.5 Exhaustive Industry & Platform Benchmark Matrix (10 Dimensions), 3. Related Work & Comprehensive Literature Benchmark

### Community 396 - "8. Empirical Results, Verification & Benchmarks"
Cohesion: 0.33
Nodes (6): 8.1 Performance Comparison: MVO vs. 1/N Equal Weight vs. HRP, 8.2 Macro Regime Classification Accuracy & Historical Stress Tests, 8.3 Disintermediation Fee Savings Econometric Projections, 8.4 Verification Seams: Pytest (272 Tests) & Vitest (132 Tests), 8. Empirical Results, Verification & Benchmarks, Analysis:

### Community 406 - "RAG-Powered Conversational Assistant (NitiBot)"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, RAG-Powered Conversational Assistant (NitiBot)

### Community 407 - "ESG Conscience Score and Socially Responsible Investing"
Cohesion: 0.40
Nodes (4): Consequences, Context, Decision, ESG Conscience Score and Socially Responsible Investing

### Community 408 - "Cross-Platform PWA with Adaptive Desktop Layout"
Cohesion: 0.40
Nodes (4): Consequences, Context, Cross-Platform PWA with Adaptive Desktop Layout, Decision

### Community 409 - "Portfolio Intelligence Platform over Strategy Testing Platform"
Cohesion: 0.40
Nodes (4): Consequences, Considered Options, Context, Portfolio Intelligence Platform over Strategy Testing Platform

### Community 410 - "Multi-Asset Investment Universe with Commodity ETFs"
Cohesion: 0.40
Nodes (4): Consequences, Considered Options, Context, Multi-Asset Investment Universe with Commodity ETFs

### Community 411 - "Server-Side ML Computation with Thin-Client Mobile Delivery"
Cohesion: 0.40
Nodes (4): Consequences, Considered Options, Context, Server-Side ML Computation with Thin-Client Mobile Delivery

### Community 412 - "AI Review Verification and Ground-Truth Fact-Checking Agent"
Cohesion: 0.40
Nodes (4): AI Review Verification and Ground-Truth Fact-Checking Agent, Consequences, Considered Options, Context

### Community 413 - "6. Portfolio Optimization: Hierarchical Risk Parity (HRP) Algorithm"
Cohesion: 0.40
Nodes (5): 6.4 Risk Persona & ESG Allocation Constraints, 6. Portfolio Optimization: Hierarchical Risk Parity (HRP) Algorithm, Stage 1: Correlation Metric & Tree Clustering, Stage 2: Quasi-Diagonalization, Stage 3: Recursive Bisection

### Community 414 - "6.2 Multi-Factor Econometric Extraction Engine"
Cohesion: 0.40
Nodes (5): 1. Momentum Pillar, 2. Volatility & Risk Pillar, 3. Market Sensitivity Pillar (CAPM), 4. Sustainability Pillar (ESG Conscience), 6.2 Multi-Factor Econometric Extraction Engine

### Community 415 - "2. Introduction, Problem Statement & Socio-Economic Context"
Cohesion: 0.40
Nodes (5): 2.1 The Retail Investor Crisis in Emerging Markets (The Indian Context), 2.2 The Three Fundamental Dilemmas of Retail Investors, 2.3 Econometric Failures of Classical Models, 2.4 Research Objectives & Core Contributions, 2. Introduction, Problem Statement & Socio-Economic Context

### Community 416 - "4. Dataset Engineering & Multi-Asset Universe"
Cohesion: 0.40
Nodes (5): 4.1 Canonical 58-Asset Universe Taxonomy, 4.2 Benchmark & Macro Volatility Indices, 4.3 Data Preprocessing & Return Formalisms, 4.4 Environmental, Social, and Governance (ESG) Conscience Dataset, 4. Dataset Engineering & Multi-Asset Universe

### Community 417 - "5. End-to-End System Architecture"
Cohesion: 0.40
Nodes (5): 5.1 Decoupled Full-Stack Architecture, 5.2 Four-Tier Quantitative Data Pipeline, 5.3 UX State Machine & Mobile-First PWA Engineering, 5.4 Lifecycle Guards, Concurrency, and AbortController Management, 5. End-to-End System Architecture

### Community 418 - "6.5 Hierarchical Risk Parity (HRP) Optimization Algorithm"
Cohesion: 0.40
Nodes (5): 6.5 Hierarchical Risk Parity (HRP) Optimization Algorithm, Phase 1: Correlation Distance & Hierarchical Tree Clustering, Phase 2: Quasi-Diagonalization (Seriation), Phase 3: Recursive Bisection, Risk Persona Allocation Constraints & ESG Tilting

### Community 429 - "1. Foundational Problem Statement & Financial Econometrics"
Cohesion: 0.50
Nodes (4): 1.1 The Markowitz "Error Maximizer" Curse, 1.2 Non-Stationarity & Structural Regime Breaks, 1.3 The Flaw of Single-Point Deterministic Targets, 1. Foundational Problem Statement & Financial Econometrics

### Community 430 - "2. Datasets, Ingestion Architecture & Preprocessing Justifications"
Cohesion: 0.50
Nodes (4): 2.1 Asset Universe Composition, 2.2 Why These Datasets?, 2.3 Mathematical Data Preprocessing, 2. Datasets, Ingestion Architecture & Preprocessing Justifications

### Community 431 - "8. Geometric Brownian Motion (GBM) Long-Horizon Wealth Compounding"
Cohesion: 0.50
Nodes (4): 8.1 Stochastic Differential Equation (SDE), 8.2 Monthly SIP Compounding with Step-Up Dynamics, 8.3 The Compounding Tipping Point, 8. Geometric Brownian Motion (GBM) Long-Horizon Wealth Compounding

### Community 432 - "1. Academic Metadata & Proposed Paper Formulations"
Cohesion: 0.50
Nodes (4): 1.1 Candidate Paper Titles, 1.2 Structured Abstract (IEEE Standard), 1.3 IEEE Indexing Terms & Keywords, 1. Academic Metadata & Proposed Paper Formulations

### Community 433 - "6.1 Unsupervised Market Regime Classifier (GMM & Parkinson Volatility)"
Cohesion: 0.50
Nodes (4): 6.1.1 Feature Vector Construction, 6.1.2 Gaussian Mixture Model Formulation, 6.1.3 Deterministic State Mapping via Return-to-Volatility Centroid Ranking, 6.1 Unsupervised Market Regime Classifier (GMM & Parkinson Volatility)

### Community 434 - "6.3 Multi-Horizon Quantile Growth Forecaster & Isotonic Regularization"
Cohesion: 0.50
Nodes (4): 6.3.1 Blended Expected Drift & Volatility, 6.3.2 Closed-Form Geometric Brownian Motion Quantile Cones, 6.3.3 Isotonic Monotonicity Regularization, 6.3 Multi-Horizon Quantile Growth Forecaster & Isotonic Regularization

## Knowledge Gaps
- **13 isolated node(s):** `@capacitor/android`, `@capacitor/core`, `clsx`, `tailwind-merge`, `@types/node` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1142 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MarketDataService` connect `MarketDataService` to `create_app`, `RegimeService`, `forecasting/service.py`, `alerts/service.py`, `GrowService`, `PortfolioService`, `PortfolioState`, `RAGContextBuilder`, `AlertService`, `MarketTickGenerator`, `forecaster.py`, `PortfolioRepository`, `MarketRegimeType`, `BacktestService`, `MarketDataProvider`, `test_stream_api.py`, `test_explore_service.py`, `.get_esg_score`, `pytest`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 56 inferred relationships involving `MarketDataService` (e.g. with `get_history()` and `get_market_service()`) actually correct?**
  _`MarketDataService` has 56 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@capacitor/android`, `@capacitor/core`, `clsx` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `create_app` be split into smaller, more focused modules?**
  _Cohesion score 0.05925925925925926 - nodes in this community are weakly interconnected._
- **Why does `useAbortableRequest()` connect `GlassCard` to `5. End-to-End System Architecture`, `PortfolioPage.tsx`, `PrimaryButton`, `lucide-react`, `QuantNiti: Complete Architectural Blueprint & System Design Document`, `react`, `9. IEEE Research Paper Blueprint (Section-by-Section Outline)`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `MarketRegimeType` (e.g. with `PortfolioRepository` and `evaluate_regime_transition()`) actually correct?**
  _`MarketRegimeType` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `RegimeService` be split into smaller, more focused modules?**
  _Cohesion score 0.07317073170731707 - nodes in this community are weakly interconnected._