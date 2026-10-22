# Graph Report - QuantNiti  (2026-10-22)

## Corpus Check
- 282 files · ~138,541 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 6, .toml 2, .example 1)

## Summary
- 2381 nodes · 5727 edges · 152 communities (116 shown, 36 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 721 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2f3ab5a6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- react
- grow.py
- test_hrp_optimizer.py
- GrowPage.tsx
- GlassCard
- storage.py
- test_cache.py
- ExplorePage.tsx
- extract_stock_factors
- models.py
- StrategyType
- PortfolioService
- compounding_engine.py
- MarketDataService
- agent.py
- PortfolioPage.tsx
- MarketTickGenerator
- MarketRegimeType
- backtest/service.py
- lucide-react
- 🔍 Platform-by-Platform Research (Primary-Source Verified)
- regime/service.py
- AppShell.tsx
- test_review_factchecker.py
- .get_history
- test_literacy_api.py
- ChatMessageRequest
- useAppStore.ts
- hrp.py
- assistant/service.py
- numpy
- alerts.py
- ReviewStatus
- start_all.py
- app.py
- metrics.py
- test_client_serving.py
- MarketRegimeClassifier
- routes/portfolio.py
- alerts/service.py
- pandas
- PortfolioRepository
- test_chat_api.py
- forecasting/service.py
- FastAPI
- TestDiscreteAllocationEngine
- sys
- test_api_routes.py
- universe.py
- ConversationMemoryManager
- GeminiClientAdapter
- compilerOptions
- package.json
- typing
- QuantNiti: Machine Learning & Quantitative Finance Technical Specification
- test_grow_api.py
- AlertService
- MarketStreamClient
- test_backtest_api.py
- os
- devDependencies
- filter_tier1_content
- dependencies
- test_portfolio_storage.py
- manifest.json
- pytest
- test_pwa_integration.py
- compute_regime_suitability
- .generate_tick
- denormalize_symbol
- json
- test_end_to_end_integration.py
- test_explore_api.py
- asyncio
- MultiHorizonGrowthForecast
- data/service.py
- test_pwa_unit.py
- ReviewTargetType
- scripts
- rebalance.py
- test_review_service.py
- stream.py
- .format_sse_event
- streaming.py
- test_multi_asset_integration.py
- test_multi_portfolio_api.py
- test_reviews_api.py
- sync_universe
- setup.ts
- compilerOptions
- QuantNiti: Hosting, Centralized Server & Scalability Guide
- QuantNiti (क्वान्टनीति) 🇮🇳
- .recommend_basket
- get_market_service
- vite.config.ts
- 2. Platform-by-Platform Verified Primary-Source Audit
- 6. Mathematical Formulations & Algorithmic Engines
- 3. Academic Demonstration & Evaluation Scenarios
- QuantNiti: Complete Architectural Blueprint & System Design Document
- capacitor.config.ts
- 2. Audit of the 4 Open-Source Repositories
- 1. Advanced Machine Learning Architecture for Stock & Portfolio Intelligence
- QuantNiti: Master Research Dossier & Academic Foundation Document
- 9. IEEE Research Paper Blueprint (Section-by-Section Outline)
- sw.js
- app
- README.md
- 4.1 Quantitative Factor Extraction Engine
- Spec: QuantNiti Core Platform
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
- get_review_service
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

## Communities (152 total, 36 thin omitted)

### Community 0 - "react"
Cohesion: 0.10
Nodes (20): react, react-dom, react-router-dom, @testing-library/react, @testing-library/user-event, vitest, App(), Theme (+12 more)

### Community 1 - "grow.py"
Cohesion: 0.25
Nodes (6): get_grow_service(), recommend_basket_alias(), recommend_basket_get(), recommend_basket_post(), BasketRecommendationRequest, BasketRecommendationResponse

### Community 2 - "test_hrp_optimizer.py"
Cohesion: 0.09
Nodes (14): compute_shrunk_covariance(), sample_returns_df(), test_compute_hrp_weights_helper_function(), test_compute_shrunk_covariance_fallback_on_degenerate_data(), test_compute_shrunk_covariance_ledoit_wolf(), test_compute_shrunk_covariance_without_shrinkage(), test_hrp_distance_matrix_conditioning_extreme_correlation(), test_hrp_optimizer_all_personas_and_caps() (+6 more)

### Community 3 - "GrowPage.tsx"
Cohesion: 0.07
Nodes (50): chart.js, framer-motion, react-chartjs-2, AllocationDonut(), AllocationDonutProps, AllocationItem, PALETTE, GrowPage() (+42 more)

### Community 4 - "GlassCard"
Cohesion: 0.10
Nodes (27): AdaptiveHomeCard(), AdaptiveHomeCardProps, CompoundingVisualizer(), CompoundingVisualizerProps, LearningHub(), LearningHubProps, isIndianMarketOpen(), MarketPulse() (+19 more)

### Community 5 - "storage.py"
Cohesion: 0.15
Nodes (6): Base, DailySnapshotRecord, HoldingRecord, PortfolioRecord, ReviewRecord, TransactionRecord

### Community 6 - "test_cache.py"
Cohesion: 0.14
Nodes (5): sample_df(), temp_cache_dir(), test_cache_invalidation(), test_cache_save_and_load(), test_cache_ttl_expiration()

### Community 7 - "ExplorePage.tsx"
Cohesion: 0.09
Nodes (26): ASSETS, ProToolsBacktester(), STRATEGIES, ExploreStockItem, StockCard(), StockCardProps, StockProfileModal(), StockProfileModalProps (+18 more)

### Community 8 - "extract_stock_factors"
Cohesion: 0.13
Nodes (13): compute_bollinger_bands(), compute_ema(), compute_macd(), compute_max_drawdown(), compute_rsi(), compute_stock_beta_and_alpha(), extract_stock_factors(), test_compute_bollinger_bands() (+5 more)

### Community 9 - "models.py"
Cohesion: 0.08
Nodes (29): get_history(), get_returns_matrix(), get_universe(), BasketAllocationItem, BasketGrowthProjections, BenchmarkComparisonItem, MarketHistoryResponse, OHLCVBar (+21 more)

### Community 10 - "StrategyType"
Cohesion: 0.10
Nodes (13): BacktestTrade, StrategyType, BacktestEngine, BacktestResultData, compute_rsi(), benchmark_price_series(), sample_price_series(), test_bollinger_bands_strategy() (+5 more)

### Community 11 - "PortfolioService"
Cohesion: 0.13
Nodes (6): CreatePortfolioRequest, PortfolioService, test_create_and_get_portfolio(), test_get_nonexistent_portfolio_raises_error(), test_get_order_sheet(), test_rebalance_diff_and_apply()

### Community 12 - "compounding_engine.py"
Cohesion: 0.09
Nodes (19): CompoundingMonthlyPoint, CompoundingRequest, CompoundingResponse, CompoundingSummary, CompoundingTippingPoint, CompoundingYearlyPoint, calculate_lump_sum(), calculate_monthly_sip() (+11 more)

### Community 13 - "MarketDataService"
Cohesion: 0.05
Nodes (21): create_app(), MarketDataService, HRPOptimizer, GrowService, RegimeService, app_instance(), app_instance(), test_compounding_endpoint_mounted_at_both_prefixes() (+13 more)

### Community 14 - "agent.py"
Cohesion: 0.20
Nodes (5): ReviewVerificationResult, extract_duration_claim(), extract_return_claim(), verify_tier2_fact_check(), audit_tier3_llm()

### Community 15 - "PortfolioPage.tsx"
Cohesion: 0.17
Nodes (20): OrderSheetModalProps, PortfolioReportCardProps, CompoundingTrajectoryChart(), CompoundingTrajectoryChartProps, DemoPortfolio(), DemoPortfolioProps, BenchmarkComparison, CompoundingTrajectoryData (+12 more)

### Community 17 - "MarketRegimeType"
Cohesion: 0.08
Nodes (22): BenchmarkComparisonLive, MarketRegimeType, PortfolioHolding, PortfolioState, RiskPersona, calculate_day_over_day_mtm(), create_portfolio_from_allocations(), PortfolioSimulator (+14 more)

### Community 18 - "backtest/service.py"
Cohesion: 0.10
Nodes (13): get_backtest_service(), run_backtest_get(), run_backtest_post(), run_quant_lab_backtest_alias(), BacktestDataPoint, BacktestRequest, BacktestResponse, BacktestService (+5 more)

### Community 19 - "lucide-react"
Cohesion: 0.14
Nodes (27): lucide-react, COMPARISON_ROWS, CompetitorBenchmarkModal(), CompetitorBenchmarkModalProps, ConceptDetailData, ConceptDetailModal(), ConceptDetailModalProps, ModalRoot() (+19 more)

### Community 20 - "🔍 Platform-by-Platform Research (Primary-Source Verified)"
Cohesion: 0.07
Nodes (27): 1. Groww (groww.in), 2. Zerodha Streak (streak.tech), 3. Smallcase (smallcase.com), 4. INDmoney (indmoney.com), 5. MoneyControl Pro / Super Pro (moneycontrol.com), 6. TradingView (tradingview.com), Bank FD Rates vs. Equity Returns (2025–2026 Context), 🎯 Consolidated Competitive Matrix (10 Dimensions) (+19 more)

### Community 21 - "regime/service.py"
Cohesion: 0.08
Nodes (11): get_current_regime(), get_regime_history(), get_regime_service(), train_regime_model(), TrainRegimeRequest, CurrentRegimeResponse, RegimeHistoricalPoint, RegimeHistoryResponse (+3 more)

### Community 22 - "AppShell.tsx"
Cohesion: 0.13
Nodes (22): AppShell(), BottomNav(), BottomNavProps, NAV_ITEMS, NavItem, triggerHaptic(), Header(), HeaderProps (+14 more)

### Community 23 - "test_review_factchecker.py"
Cohesion: 0.14
Nodes (6): test_extract_duration_claim(), test_extract_return_claim(), test_tier2_approves_pure_qualitative_reviews(), test_tier2_approves_verified_claim_within_tolerance(), test_tier2_flags_borderline_discrepancy(), test_tier2_rejects_exaggerated_return_claims()

### Community 25 - "test_literacy_api.py"
Cohesion: 0.29
Nodes (6): app(), test_dual_routing_api_prefix(), test_get_all_literacy_cards_category_filter(), test_get_all_literacy_cards_v1(), test_get_literacy_card_by_unknown_key_returns_404(), test_get_literacy_card_by_valid_key()

### Community 26 - "ChatMessageRequest"
Cohesion: 0.09
Nodes (16): get_chat_status(), get_nitibot_service(), post_chat_message(), ChatMessageRequest, ChatMessageResponse, ChatStatusResponse, EchoMockAdapter, test_edge_case_empty_or_whitespace_message() (+8 more)

### Community 27 - "useAppStore.ts"
Cohesion: 0.14
Nodes (16): SAMPLE_REVIEWS, Step5DeepDiveProps, ACTIVE_PORTFOLIO_ID_STORAGE_KEY, AppStoreState, loadActivePortfolioId(), loadIsOnboarded(), loadLearnedConcepts(), loadPortfolios() (+8 more)

### Community 28 - "hrp.py"
Cohesion: 0.14
Nodes (6): apply_weight_caps(), compute_hrp_weights(), get_cluster_variance(), get_quasi_diag_order(), _traverse(), recursive_bisection()

### Community 29 - "assistant/service.py"
Cohesion: 0.09
Nodes (13): RAGContextPayload, RAGContextBuilder, _load_env_file_if_present(), NitiBotService, create_sample_regime(), test_rag_context_builder_builds_complete_grounding(), test_rag_context_builder_esg_enrichment(), test_rag_context_builder_fallback_defaults() (+5 more)

### Community 30 - "numpy"
Cohesion: 0.08
Nodes (13): draw_card(), draw_ellipse(), calculate_parkinson_volatility(), calculate_realized_volatility(), calculate_rolling_log_returns(), extract_regime_features(), sample_stock_and_index(), sample_market_data() (+5 more)

### Community 31 - "alerts.py"
Cohesion: 0.13
Nodes (12): clear_alerts(), evaluate_alerts_micro_batch(), get_alert_service(), get_vapid_public_key(), list_alerts(), mark_alert_read(), mark_all_alerts_read(), send_test_push_notification() (+4 more)

### Community 33 - "start_all.py"
Cohesion: 0.11
Nodes (18): auto_open_emulator_in_background(), _watcher(), build_web_assets_if_needed(), find_android_tool(), get_lan_ip(), get_python_exe(), get_running_devices(), is_server_ready() (+10 more)

### Community 35 - "metrics.py"
Cohesion: 0.14
Nodes (8): BacktestMetrics, RegimePerformanceBreakdown, calculate_backtest_metrics(), calculate_regime_breakdown(), mock_backtest_result(), test_calculate_backtest_metrics_values(), test_calculate_regime_breakdown(), create_sample_backtest()

### Community 36 - "test_client_serving.py"
Cohesion: 0.23
Nodes (6): test_app(), test_app_route_serves_html(), test_competitor_benchmark_assets_served(), test_root_serves_html(), test_static_assets_served(), test_vite_build_assets_served()

### Community 37 - "MarketRegimeClassifier"
Cohesion: 0.17
Nodes (4): MarketRegimeClassifier, test_classifier_fit_and_predict(), test_classifier_probabilities_sum_to_one(), test_classifier_state_label_determinism()

### Community 38 - "routes/portfolio.py"
Cohesion: 0.13
Nodes (13): apply_rebalance_endpoint(), calculate_compounding_endpoint(), create_portfolio_endpoint(), delete_portfolio_endpoint(), get_order_sheet_endpoint(), get_portfolio_endpoint(), get_portfolio_service(), get_rebalance_diff_endpoint() (+5 more)

### Community 39 - "alerts/service.py"
Cohesion: 0.11
Nodes (18): AlertSeverity, LiteracyCategory, SmartAlert, SmartAlertType, evaluate_52w_high_breakout(), evaluate_drawdown_breach(), evaluate_factor_anomaly(), evaluate_portfolio_drift() (+10 more)

### Community 40 - "pandas"
Cohesion: 0.13
Nodes (9): align_to_trading_calendar(), calculate_returns(), sanitize_raw_provider_data(), validate_ohlcv_dataframe(), test_align_to_trading_calendar(), test_calculate_returns(), test_validate_ohlcv_dataframe_drops_invalid_rows(), test_validate_ohlcv_dataframe_valid_data() (+1 more)

### Community 42 - "test_chat_api.py"
Cohesion: 0.22
Nodes (7): configured_app(), MockGeminiAdapter, test_chat_endpoint_graceful_degradation_503(), test_chat_endpoint_success(), test_chat_status_endpoint(), test_chat_status_endpoint_when_disabled(), unconfigured_app()

### Community 43 - "forecasting/service.py"
Cohesion: 0.12
Nodes (15): get_explore_service(), get_growth_forecast(), get_stock_profile(), get_ticker_esg(), list_explore_stocks(), get_quote(), BenchmarkComparison, ESGScoreResponse (+7 more)

### Community 44 - "FastAPI"
Cohesion: 0.14
Nodes (7): health_check(), get_all_literacy_cards(), _get_cards_dict(), get_literacy_card_by_key(), _get_literacy_data(), LiteracyCard, LiteracyListResponse

### Community 46 - "sys"
Cohesion: 0.22
Nodes (5): main(), run_command(), get_lan_ip(), main(), print_qr_code()

### Community 47 - "test_api_routes.py"
Cohesion: 0.29
Nodes (8): app(), test_get_history_endpoint(), test_get_quote_endpoint(), test_get_returns_matrix_endpoint(), test_get_universe_endpoint(), test_get_universe_filtered_by_sector(), test_health_endpoint(), test_sync_endpoint()

### Community 48 - "universe.py"
Cohesion: 0.08
Nodes (15): AssetClass, get_asset_class_for_symbol(), get_sector_for_symbol(), get_universe_symbols(), test_asset_class_enum_members(), test_commodity_etfs_constituents(), test_defense_constituents(), test_expanded_universe_total_count() (+7 more)

### Community 49 - "ConversationMemoryManager"
Cohesion: 0.22
Nodes (7): ConversationMemoryManager, MessageTurn, test_edge_case_sliding_window_memory_limits(), test_memory_manager_add_and_retrieve_turns(), test_memory_manager_clear_session(), test_memory_manager_format_for_gemini(), test_memory_manager_sliding_window_limit()

### Community 51 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+10 more)

### Community 52 - "package.json"
Cohesion: 0.11
Nodes (17): name, private, type, version, autoprefixer, @capacitor/android, @capacitor/core, clsx (+9 more)

### Community 53 - "typing"
Cohesion: 0.25
Nodes (4): ReviewItem, ReviewsListResponse, ReviewSubmissionResponse, ReviewService

### Community 54 - "QuantNiti: Machine Learning & Quantitative Finance Technical Specification"
Cohesion: 0.11
Nodes (18): 10. End-to-End Execution Flowchart & Mathematical Reference, 3.1 Feature Engineering Matrix, 3.2 GMM Formulation & Expectation-Maximization (EM), 3.3 Deterministic State Mapping via Return-to-Volatility Centroids, 3. Unsupervised Market Regime Classification Engine (GMM & Features), 5.1 Formulation, 5.2 Ridge Regularization Layer, 5. Covariance Matrix Regularization: Ledoit-Wolf Shrinkage (+10 more)

### Community 55 - "test_grow_api.py"
Cohesion: 0.21
Nodes (5): test_get_grow_recommend_success(), test_grow_recommend_esg_conscious_api(), test_grow_recommend_validation_errors(), test_post_baskets_recommend_alias(), test_post_grow_recommend_success()

### Community 57 - "MarketStreamClient"
Cohesion: 0.15
Nodes (5): marketStream, MarketStreamClient, MarketTick, TickListener, MockEventSource

### Community 58 - "test_backtest_api.py"
Cohesion: 0.24
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

### Community 65 - "pytest"
Cohesion: 0.13
Nodes (10): test_grow_service_different_risk_personas(), test_grow_service_esg_portfolio_score_and_persona(), test_grow_service_invalid_inputs_raise_error(), test_grow_service_recommend_basket_balanced(), test_get_current_regime_route(), test_get_regime_history_route(), test_train_regime_model_route(), test_get_current_regime() (+2 more)

### Community 66 - "test_pwa_integration.py"
Cohesion: 0.17
Nodes (6): test_app(), test_index_html_contains_pwa_metadata_and_elements(), test_manifest_endpoint_served_with_correct_mime(), test_offline_page_endpoint(), test_pwa_icons_served(), test_service_worker_endpoint_served_with_allowed_header()

### Community 67 - "compute_regime_suitability"
Cohesion: 0.33
Nodes (5): RegimeSuitability, compute_regime_suitability(), test_suitability_in_bear_regime(), test_suitability_in_bull_regime(), test_suitability_score_bounds()

### Community 68 - ".generate_tick"
Cohesion: 0.28
Nodes (3): MarketTick, test_generate_single_tick(), test_live_fallback_to_synthetic()

### Community 69 - "denormalize_symbol"
Cohesion: 0.10
Nodes (3): denormalize_symbol(), test_symbol_normalization_and_validation(), test_denormalize_symbol_for_provider()

### Community 70 - "json"
Cohesion: 0.15
Nodes (6): test_stream_ticks_alias_route(), test_stream_ticks_endpoint_headers_and_event(), test_stream_ticks_symbol_filter(), test_invalid_literacy_card_fails_validation(), test_literacy_cards_schema_and_count(), test_manifest_file_exists_and_valid()

### Community 71 - "test_end_to_end_integration.py"
Cohesion: 0.19
Nodes (5): test_app(), test_e2e_explore_stock_to_quant_lab_backtest_journey(), test_e2e_grow_basket_to_virtual_portfolio_lifecycle(), test_e2e_quant_lab_multi_strategy_suite(), test_e2e_regime_radar_history_endpoint()

### Community 72 - "test_explore_api.py"
Cohesion: 0.39
Nodes (7): test_explore_stocks_contain_esg_fields(), test_get_explore_stocks_filtered(), test_get_explore_stocks_route(), test_get_growth_forecast_route(), test_get_stock_profile_route(), test_get_ticker_esg_endpoint(), test_stock_profile_contains_esg()

### Community 74 - "MultiHorizonGrowthForecast"
Cohesion: 0.17
Nodes (8): HorizonForecastCone, MultiHorizonGrowthForecast, MultiHorizonForecaster, mock_stock_forecasts(), _create_forecast(), test_forecast_all_four_horizons(), test_forecast_cone_widening_over_longer_horizons(), test_strict_quantile_monotonicity()

### Community 75 - "data/service.py"
Cohesion: 0.06
Nodes (19): Settings, ParquetMarketCache, MarketDataProvider, MockDataProvider, YahooFinanceProvider, test_app(), test_get_growth_forecast(), test_get_stock_profile() (+11 more)

### Community 76 - "test_pwa_unit.py"
Cohesion: 0.20
Nodes (4): test_desktop_responsive_css_rules(), test_icon_assets_exist(), test_offline_page_exists_and_styled(), test_service_worker_script_structure()

### Community 77 - "ReviewTargetType"
Cohesion: 0.12
Nodes (12): test_all(), ReviewSubmissionRequest, ReviewTargetType, ReviewVerificationAgent, agent(), test_agent_approves_and_verifies_authentic_review(), test_agent_approves_qualitative_review(), test_agent_blocks_stock_tipping_at_tier1() (+4 more)

### Community 78 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, apk:build, build, cap:open, cap:sync, dev, mobile:serve, preview (+1 more)

### Community 79 - "rebalance.py"
Cohesion: 0.13
Nodes (4): RebalanceItemDiff, DiscreteAllocationEngine, DiscreteAllocationResult, compute_rebalance_diff()

### Community 80 - "test_review_service.py"
Cohesion: 0.25
Nodes (3): review_service(), test_service_rejects_and_does_not_publish_exaggerated_review(), test_service_submits_and_stores_verified_review()

### Community 84 - "test_multi_asset_integration.py"
Cohesion: 0.24
Nodes (3): test_explore_profiles_for_etf_and_defense(), test_explore_stocks_total_and_asset_class_filter(), test_explore_theme_filter_chips()

### Community 85 - "test_multi_portfolio_api.py"
Cohesion: 0.24
Nodes (4): test_create_and_list_multiple_portfolios(), test_delete_portfolio_lifecycle(), test_dual_prefix_routing_portfolios(), test_portfolio_detail_mtm_metrics()

### Community 86 - "test_reviews_api.py"
Cohesion: 0.17
Nodes (6): test_app(), test_get_reviews_endpoint(), test_stock_review_flow(), test_submit_exaggerated_review_rejected(), test_submit_prohibited_spam_rejected(), test_submit_verified_review()

### Community 88 - "setup.ts"
Cohesion: 0.25
Nodes (3): @testing-library/jest-dom, localStorageMock, sessionStorageMock

### Community 90 - "compilerOptions"
Cohesion: 0.25
Nodes (7): compilerOptions, allowSyntheticDefaultImports, composite, module, moduleResolution, skipLibCheck, include

### Community 91 - "QuantNiti: Hosting, Centralized Server & Scalability Guide"
Cohesion: 0.13
Nodes (14): 1. Architectural Overview, 2. 1-Click Cloud Deployment Guides, 3. Running with Docker & Docker Compose (Any VPS / Local Machine), 4. Connecting Standalone Clients (Mobile APK & PWAs), 5. Horizontal & Vertical Scalability, ASGI Concurrency, Direct Docker Run, Memory Optimization (+6 more)

### Community 92 - "QuantNiti (क्वान्टनीति) 🇮🇳"
Cohesion: 0.13
Nodes (15): 1. Prerequisites, 2. Installation, 3. Running Locally, AI-Driven Regime-Adaptive Portfolio Intelligence & Quantitative Decision Support System, 🎯 Core Mathematical & Algorithmic Methodologies, Development Mode (Hot Reloading Frontend & Backend):, 📱 Key Product Capabilities, 📄 License & Attribution (+7 more)

### Community 93 - ".recommend_basket"
Cohesion: 0.12
Nodes (6): get_esg_badge(), get_esg_score_for_symbol(), get_universe_metadata(), test_esg_badge_thresholds(), test_esg_data_covers_all_50_nifty_constituents(), test_get_universe_metadata()

### Community 98 - "2. Platform-by-Platform Verified Primary-Source Audit"
Cohesion: 0.17
Nodes (11): 1. Executive Summary: The Structural Gap in Indian WealthTech, 2. Platform-by-Platform Verified Primary-Source Audit, 3. Comprehensive 10-Dimension Competitive Matrix, 4. Key Takeaways for Academic & Industry Evaluation, A. MoneyControl (Pro & Super Pro), B. Zerodha (Kite + Streak), C. Groww (Stocks & Portfolio Analysis), D. INDmoney (+3 more)

### Community 100 - "6. Mathematical Formulations & Algorithmic Engines"
Cohesion: 0.18
Nodes (11): 6.4 Ledoit-Wolf Covariance Matrix Regularization, 6.6.1 Greedy Deficit-Minimization Sizing (Primary Real-Time Algorithm), 6.6.2 Mixed-Integer Linear Programming (MILP Formulation), 6.6 Discrete Integer Share Sizing & Cash Buffer Optimization, 6.7.1 Stochastic Differential Equation (SDE), 6.7.2 Monthly Systematic Investment Plan (SIP) with Annual Step-Up, 6.7.3 The Compounding Tipping Point, 6.7 Geometric Brownian Motion Compounding & Analytical Tipping Point (+3 more)

### Community 102 - "3. Academic Demonstration & Evaluation Scenarios"
Cohesion: 0.18
Nodes (10): 1. System Overview, 2. Launching the Application, 3. Academic Demonstration & Evaluation Scenarios, 4-Tab Navigation Architecture, 4. Test Suite Execution, Demonstration 1: Retail Investor Flow (`Grow` Tab), Demonstration 2: Stock Explorer Flow (`Explore` Tab), Demonstration 3: Quant Lab Strategy Studio (`Quant Lab` Tab) (+2 more)

### Community 103 - "QuantNiti: Complete Architectural Blueprint & System Design Document"
Cohesion: 0.20
Nodes (10): 1. Executive Summary & Problem Context, 2. Full-Stack System Architecture, 4.1. The 5-Step Guided Grow Experience, 4.2. Universal Financial & Brand Color Palette, 4.3. Lifecycle Management & Race Condition Guards, 4. Frontend Architecture & Design Engineering, 5. Security, Reliability & Verification Matrix, 6. Deployment & Operations (+2 more)

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

### Community 123 - "4.1 Quantitative Factor Extraction Engine"
Cohesion: 0.25
Nodes (8): 1. Momentum Pillar, 2. Volatility & Risk Pillar, 3. Market Sensitivity Pillar (CAPM), 4.1 Quantitative Factor Extraction Engine, 4.2 Multi-Factor Drift & Volatility Blending, 4.3 Quantile Cones & Strict Monotonicity Enforcement, 4. Multi-Factor Asset Extraction & Quantile Growth Forecasting Cones, 4. Sustainability Pillar (ESG Conscience)

### Community 124 - "Spec: QuantNiti Core Platform"
Cohesion: 0.25
Nodes (8): Further Notes, Implementation Decisions, Out of Scope, Problem Statement, Solution, Spec: QuantNiti Core Platform, Testing Decisions, User Stories

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

### Community 133 - "Cross-Platform PWA with Adaptive Desktop Layout"
Cohesion: 0.40
Nodes (4): Consequences, Context, Cross-Platform PWA with Adaptive Desktop Layout, Decision

### Community 134 - "Portfolio Intelligence Platform over Strategy Testing Platform"
Cohesion: 0.40
Nodes (4): Consequences, Considered Options, Context, Portfolio Intelligence Platform over Strategy Testing Platform

### Community 135 - "Multi-Asset Investment Universe with Commodity ETFs"
Cohesion: 0.40
Nodes (4): Consequences, Considered Options, Context, Multi-Asset Investment Universe with Commodity ETFs

### Community 136 - "Server-Side ML Computation with Thin-Client Mobile Delivery"
Cohesion: 0.40
Nodes (4): Consequences, Considered Options, Context, Server-Side ML Computation with Thin-Client Mobile Delivery

### Community 137 - "AI Review Verification and Ground-Truth Fact-Checking Agent"
Cohesion: 0.40
Nodes (4): AI Review Verification and Ground-Truth Fact-Checking Agent, Consequences, Considered Options, Context

### Community 138 - "6. Portfolio Optimization: Hierarchical Risk Parity (HRP) Algorithm"
Cohesion: 0.40
Nodes (5): 6.4 Risk Persona & ESG Allocation Constraints, 6. Portfolio Optimization: Hierarchical Risk Parity (HRP) Algorithm, Stage 1: Correlation Metric & Tree Clustering, Stage 2: Quasi-Diagonalization, Stage 3: Recursive Bisection

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

### Community 144 - "get_review_service"
Cohesion: 0.25
Nodes (4): get_review_service(), get_target_reviews(), preview_verification(), submit_review()

### Community 146 - "1. Foundational Problem Statement & Financial Econometrics"
Cohesion: 0.50
Nodes (4): 1.1 The Markowitz "Error Maximizer" Curse, 1.2 Non-Stationarity & Structural Regime Breaks, 1.3 The Flaw of Single-Point Deterministic Targets, 1. Foundational Problem Statement & Financial Econometrics

### Community 147 - "2. Datasets, Ingestion Architecture & Preprocessing Justifications"
Cohesion: 0.50
Nodes (4): 2.1 Asset Universe Composition, 2.2 Why These Datasets?, 2.3 Mathematical Data Preprocessing, 2. Datasets, Ingestion Architecture & Preprocessing Justifications

### Community 148 - "8. Geometric Brownian Motion (GBM) Long-Horizon Wealth Compounding"
Cohesion: 0.50
Nodes (4): 8.1 Stochastic Differential Equation (SDE), 8.2 Monthly SIP Compounding with Step-Up Dynamics, 8.3 The Compounding Tipping Point, 8. Geometric Brownian Motion (GBM) Long-Horizon Wealth Compounding

### Community 149 - "1. Academic Metadata & Proposed Paper Formulations"
Cohesion: 0.50
Nodes (4): 1.1 Candidate Paper Titles, 1.2 Structured Abstract (IEEE Standard), 1.3 IEEE Indexing Terms & Keywords, 1. Academic Metadata & Proposed Paper Formulations

### Community 150 - "6.1 Unsupervised Market Regime Classifier (GMM & Parkinson Volatility)"
Cohesion: 0.50
Nodes (4): 6.1.1 Feature Vector Construction, 6.1.2 Gaussian Mixture Model Formulation, 6.1.3 Deterministic State Mapping via Return-to-Volatility Centroid Ranking, 6.1 Unsupervised Market Regime Classifier (GMM & Parkinson Volatility)

### Community 151 - "6.3 Multi-Horizon Quantile Growth Forecaster & Isotonic Regularization"
Cohesion: 0.50
Nodes (4): 6.3.1 Blended Expected Drift & Volatility, 6.3.2 Closed-Form Geometric Brownian Motion Quantile Cones, 6.3.3 Isotonic Monotonicity Regularization, 6.3 Multi-Horizon Quantile Growth Forecaster & Isotonic Regularization

## Knowledge Gaps
- **13 isolated node(s):** `@capacitor/android`, `@capacitor/core`, `clsx`, `tailwind-merge`, `@types/node` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1117 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MarketDataService` connect `MarketDataService` to `models.py`, `PortfolioService`, `MarketTickGenerator`, `backtest/service.py`, `regime/service.py`, `.get_history`, `test_literacy_api.py`, `assistant/service.py`, `app.py`, `test_client_serving.py`, `alerts/service.py`, `test_chat_api.py`, `forecasting/service.py`, `test_api_routes.py`, `universe.py`, `AlertService`, `test_pwa_integration.py`, `test_end_to_end_integration.py`, `MultiHorizonGrowthForecast`, `data/service.py`, `ReviewTargetType`, `streaming.py`, `test_reviews_api.py`, `sync_universe`, `.recommend_basket`, `get_market_service`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 53 inferred relationships involving `MarketDataService` (e.g. with `test_all()` and `get_history()`) actually correct?**
  _`MarketDataService` has 53 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@capacitor/android`, `@capacitor/core`, `clsx` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `react` be split into smaller, more focused modules?**
  _Cohesion score 0.09608843537414966 - nodes in this community are weakly interconnected._
- **Why does `RegimeService` connect `MarketDataService` to `app.py`, `MarketRegimeClassifier`, `alerts/service.py`, `MultiHorizonGrowthForecast`, `forecasting/service.py`, `PortfolioService`, `ReviewTargetType`, `data/service.py`, `MarketRegimeType`, `backtest/service.py`, `regime/service.py`, `AlertService`, `assistant/service.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `MarketRegimeType` (e.g. with `PortfolioRepository` and `evaluate_regime_transition()`) actually correct?**
  _`MarketRegimeType` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `test_hrp_optimizer.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08739495798319327 - nodes in this community are weakly interconnected._