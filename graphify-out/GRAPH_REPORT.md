# Graph Report - QuantNiti  (2026-10-11)

## Corpus Check
- 284 files · ~157,691 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .toml 2, .css 2)

## Summary
- 2554 nodes · 6054 edges · 157 communities (127 shown, 30 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 707 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a15ec591`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- react
- RiskPersona
- models.py
- PrimaryButton
- GlassCard
- test_portfolio_full_lifecycle_api
- app.js
- ExplorePage.tsx
- extract_stock_factors
- growth_calculator.py
- StrategyType
- PortfolioService
- compounding_engine.py
- create_app
- agent.py
- PortfolioPage.tsx
- MarketTickGenerator
- PortfolioState
- BacktestService
- lucide-react
- 🔍 Platform-by-Platform Research (Primary-Source Verified)
- regime.py
- AppShell.tsx
- test_review_factchecker.py
- test_market_service.py
- test_multi_asset_universe.py
- NitiBotService
- rebalance.py
- hrp.py
- RAGContextBuilder
- pathlib
- AlertService
- storage.py
- start_all.py
- routes/portfolio.py
- BacktestEngine
- pytest
- MarketRegimeClassifier
- streaming.py
- alerts/service.py
- pandas
- PortfolioRepository
- ConversationMemoryManager
- MarketDataService
- literacy.py
- .add_alert
- OnboardingHero.tsx
- DiscreteAllocationEngine
- normalize_symbol
- numpy
- triggerHaptic
- compilerOptions
- package.json
- renderHomeTab
- QuantNiti: Machine Learning & Quantitative Finance Technical Specification
- assistant/service.py
- HorizonForecastCone
- MarketStreamClient
- asyncio
- renderNotificationList
- devDependencies
- test_review_tier1_filters.py
- dependencies
- ReviewTargetType
- manifest.json
- escapeHtml
- asyncio
- asyncio
- test_portfolio_storage.py
- MarketDataProvider
- test_pwa_unit.py
- test_end_to_end_integration.py
- asyncio
- asyncio
- forecaster.py
- MarketRegimeType
- test_client_serving.py
- test_review_verification_agent.py
- scripts
- TestDiscreteAllocationEngine
- test_mark_alert_read_and_clear
- test_api_routes.py
- asyncio
- asyncio
- test_explore_api.py
- asyncio
- asyncio
- test_day_over_day_mtm.py
- setup.ts
- backtest.py
- compilerOptions
- QuantNiti: Hosting, Centralized Server & Scalability Guide
- QuantNiti (क्वान्टनीति) 🇮🇳
- MarketStreamClient
- test_explore_stocks_total_and_asset_class_filter
- asyncio
- test_nitibot_edge_cases.py
- vite.config.ts
- 2. Platform-by-Platform Verified Primary-Source Audit
- grow.py
- 6. Mathematical Formulations & Algorithmic Engines
- filterBySector
- 3. Academic Demonstration & Evaluation Scenarios
- QuantNiti: Complete Architectural Blueprint & System Design Document
- loadBasketReviews
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
1. `MarketDataService` - 83 edges
2. `react` - 67 edges
3. `MarketRegimeType` - 59 edges
4. `RegimeService` - 58 edges
5. `RiskPersona` - 50 edges
6. `create_app()` - 45 edges
7. `useAppStore` - 45 edges
8. `PortfolioState` - 43 edges
9. `lucide-react` - 42 edges
10. `GlassCard()` - 42 edges

## Surprising Connections (you probably didn't know these)
- `4.3. Lifecycle Management & Race Condition Guards` --references--> `useAbortableRequest()`  [INFERRED]
  docs/ARCHITECTURE.md → src/frontend/hooks/useAbortableRequest.ts
- `5.4 Lifecycle Guards, Concurrency, and AbortController Management` --references--> `useAbortableRequest()`  [INFERRED]
  docs/RESEARCH_PAPER_MASTER_DOSSIER.md → src/frontend/hooks/useAbortableRequest.ts
- `IV. SYSTEM ARCHITECTURE & DESIGN` --references--> `useAbortableRequest()`  [INFERRED]
  docs/RESEARCH_PAPER_MASTER_DOSSIER.md → src/frontend/hooks/useAbortableRequest.ts
- `test_get_latest_quote()` --uses--> `StockQuote`  [INFERRED]
  tests/integration/test_market_service.py → src/app/core/models.py
- `test_train_model()` --uses--> `RegimeTrainResponse`  [INFERRED]
  tests/integration/test_regime_service.py → src/app/core/models.py

## Import Cycles
- None detected.

## Communities (157 total, 30 thin omitted)

### Community 0 - "react"
Cohesion: 0.07
Nodes (34): react, react-dom, react-router-dom, @testing-library/react, @testing-library/user-event, vitest, App(), Theme (+26 more)

### Community 1 - "RiskPersona"
Cohesion: 0.10
Nodes (17): RiskPersona, compute_shrunk_covariance(), HRPOptimizer, sample_returns_df(), test_compute_hrp_weights_helper_function(), test_compute_shrunk_covariance_fallback_on_degenerate_data(), test_compute_shrunk_covariance_ledoit_wolf(), test_compute_shrunk_covariance_without_shrinkage() (+9 more)

### Community 2 - "models.py"
Cohesion: 0.17
Nodes (19): BacktestDataPoint, BacktestMetrics, BasketAllocationItem, BenchmarkComparison, BenchmarkComparisonItem, CompoundingResponse, CompoundingTippingPoint, CompoundingYearlyPoint (+11 more)

### Community 3 - "PrimaryButton"
Cohesion: 0.11
Nodes (35): chart.js, framer-motion, react-chartjs-2, AllocationDonut(), AllocationDonutProps, AllocationItem, PALETTE, GrowPage() (+27 more)

### Community 4 - "GlassCard"
Cohesion: 0.10
Nodes (27): AdaptiveHomeCard(), AdaptiveHomeCardProps, CompoundingVisualizer(), CompoundingVisualizerProps, LearningHub(), LearningHubProps, isIndianMarketOpen(), MarketPulse() (+19 more)

### Community 6 - "app.js"
Cohesion: 0.08
Nodes (37): AppState, askNitiBotAboutConcept(), askNitiBotAboutCurrentConcept(), closeCompetitorBenchmarkModal(), closeConceptModal(), closeModalSheet(), closeNitiBotChat(), closeNitiBotModal() (+29 more)

### Community 7 - "ExplorePage.tsx"
Cohesion: 0.08
Nodes (29): ASSETS, ProToolsBacktester(), STRATEGIES, ExploreStockItem, StockCard(), StockCardProps, StockProfileModal(), StockProfileModalProps (+21 more)

### Community 8 - "extract_stock_factors"
Cohesion: 0.13
Nodes (13): compute_bollinger_bands(), compute_ema(), compute_macd(), compute_max_drawdown(), compute_rsi(), compute_stock_beta_and_alpha(), extract_stock_factors(), test_compute_bollinger_bands() (+5 more)

### Community 9 - "growth_calculator.py"
Cohesion: 0.29
Nodes (10): BasketGrowthProjections, RupeeGrowthTier, TrustCardPillarDrawdown, TrustCardPillarRegime, TrustCardPillarReliability, TrustCardPillars, TrustCardPillarSavings, build_trust_card_pillars() (+2 more)

### Community 10 - "StrategyType"
Cohesion: 0.14
Nodes (9): StrategyType, benchmark_price_series(), sample_price_series(), test_bollinger_bands_strategy(), test_buy_and_hold_strategy(), test_dual_momentum_strategy(), test_ma_crossover_strategy(), test_rsi_mean_reversion_strategy() (+1 more)

### Community 11 - "PortfolioService"
Cohesion: 0.14
Nodes (6): CreatePortfolioRequest, RebalanceAlert, PortfolioService, test_create_and_get_portfolio(), test_get_order_sheet(), test_rebalance_diff_and_apply()

### Community 12 - "compounding_engine.py"
Cohesion: 0.10
Nodes (16): CompoundingMonthlyPoint, CompoundingRequest, CompoundingSummary, calculate_lump_sum(), calculate_monthly_sip(), calculate_step_up_sip(), compute_gbm_quantile_cones(), find_compounding_tipping_point() (+8 more)

### Community 13 - "create_app"
Cohesion: 0.05
Nodes (23): create_app(), ParquetMarketCache, MockDataProvider, test_app(), app(), app_instance(), configured_app(), MockGeminiAdapter (+15 more)

### Community 14 - "agent.py"
Cohesion: 0.16
Nodes (6): ReviewVerificationResult, filter_tier1_content(), extract_duration_claim(), extract_return_claim(), verify_tier2_fact_check(), audit_tier3_llm()

### Community 15 - "PortfolioPage.tsx"
Cohesion: 0.14
Nodes (22): OrderSheetModalProps, PortfolioReportCardProps, CompoundingTrajectoryChart(), CompoundingTrajectoryChartProps, DemoPortfolio(), DemoPortfolioProps, BenchmarkComparison, CompoundingTrajectoryData (+14 more)

### Community 16 - "MarketTickGenerator"
Cohesion: 0.09
Nodes (7): get_tick_generator(), stream_ticks(), MarketTick, is_indian_market_open(), MarketTickGenerator, test_generate_single_tick(), test_live_fallback_to_synthetic()

### Community 17 - "PortfolioState"
Cohesion: 0.09
Nodes (13): BenchmarkComparisonLive, PortfolioHolding, PortfolioState, calculate_day_over_day_mtm(), create_portfolio_from_allocations(), PortfolioSimulator, update_portfolio_mark_to_market(), execute_rebalance() (+5 more)

### Community 18 - "BacktestService"
Cohesion: 0.16
Nodes (6): BacktestService, backtest_service(), test_backtest_service_invalid_symbol_raises_error(), test_backtest_service_run_buy_and_hold_nifty(), test_backtest_service_run_ma_crossover_stock(), test_backtest_service_with_date_filter()

### Community 19 - "lucide-react"
Cohesion: 0.16
Nodes (23): lucide-react, COMPARISON_ROWS, CompetitorBenchmarkModal(), CompetitorBenchmarkModalProps, ConceptDetailData, ConceptDetailModal(), ConceptDetailModalProps, ModalRoot() (+15 more)

### Community 20 - "🔍 Platform-by-Platform Research (Primary-Source Verified)"
Cohesion: 0.07
Nodes (27): 1. Groww (groww.in), 2. Zerodha Streak (streak.tech), 3. Smallcase (smallcase.com), 4. INDmoney (indmoney.com), 5. MoneyControl Pro / Super Pro (moneycontrol.com), 6. TradingView (tradingview.com), Bank FD Rates vs. Equity Returns (2025–2026 Context), 🎯 Consolidated Competitive Matrix (10 Dimensions) (+19 more)

### Community 21 - "regime.py"
Cohesion: 0.12
Nodes (6): get_current_regime(), get_regime_history(), get_regime_service(), train_regime_model(), TrainRegimeRequest, RegimeTrainResponse

### Community 22 - "AppShell.tsx"
Cohesion: 0.13
Nodes (22): AppShell(), BottomNav(), BottomNavProps, NAV_ITEMS, NavItem, triggerHaptic(), Header(), HeaderProps (+14 more)

### Community 23 - "test_review_factchecker.py"
Cohesion: 0.14
Nodes (6): test_extract_duration_claim(), test_extract_return_claim(), test_tier2_approves_pure_qualitative_reviews(), test_tier2_approves_verified_claim_within_tolerance(), test_tier2_flags_borderline_discrepancy(), test_tier2_rejects_exaggerated_return_claims()

### Community 24 - "test_market_service.py"
Cohesion: 0.08
Nodes (10): sync_universe(), SyncRequest, SyncResult, UniverseStock, test_get_latest_quote(), test_get_universe(), test_sync_universe_batch(), test_esg_badge_thresholds() (+2 more)

### Community 25 - "test_multi_asset_universe.py"
Cohesion: 0.12
Nodes (7): test_asset_class_enum_members(), test_commodity_etfs_constituents(), test_defense_constituents(), test_expanded_universe_total_count(), test_factor_extractor_on_multi_asset_universe(), test_ledoit_wolf_covariance_on_multi_asset_matrix(), test_metals_constituents()

### Community 26 - "NitiBotService"
Cohesion: 0.12
Nodes (15): get_chat_status(), get_nitibot_service(), post_chat_message(), ChatMessageRequest, ChatMessageResponse, ChatStatusResponse, NitiBotService, test_edge_case_empty_or_whitespace_message() (+7 more)

### Community 27 - "rebalance.py"
Cohesion: 0.16
Nodes (7): BrokerOrderItem, BrokerOrderSheet, compute_rebalance_diff(), generate_broker_order_sheet(), test_compute_rebalance_diff_on_regime_shift(), test_execute_rebalance_updates_holdings(), test_generate_broker_order_sheet()

### Community 28 - "hrp.py"
Cohesion: 0.14
Nodes (6): apply_weight_caps(), compute_hrp_weights(), get_cluster_variance(), get_quasi_diag_order(), _traverse(), recursive_bisection()

### Community 29 - "RAGContextBuilder"
Cohesion: 0.16
Nodes (11): RAGContextBuilder, create_sample_backtest(), create_sample_regime(), test_rag_context_builder_builds_complete_grounding(), test_rag_context_builder_esg_enrichment(), test_rag_context_builder_fallback_defaults(), test_edge_case_corrupted_or_unexpected_context_types(), test_edge_case_live_market_grounding_injection() (+3 more)

### Community 31 - "AlertService"
Cohesion: 0.09
Nodes (11): clear_alerts(), evaluate_alerts_micro_batch(), get_alert_service(), get_vapid_public_key(), list_alerts(), mark_alert_read(), mark_all_alerts_read(), send_test_push_notification() (+3 more)

### Community 32 - "storage.py"
Cohesion: 0.10
Nodes (10): ReviewItem, ReviewStatus, ReviewSummary, ReviewRepository, Base, DailySnapshotRecord, HoldingRecord, PortfolioRecord (+2 more)

### Community 33 - "start_all.py"
Cohesion: 0.05
Nodes (25): main(), run_command(), get_lan_ip(), main(), print_qr_code(), build_web_assets_if_needed(), ensure_emulator_running(), find_android_tool() (+17 more)

### Community 34 - "routes/portfolio.py"
Cohesion: 0.16
Nodes (9): apply_rebalance_endpoint(), calculate_compounding_endpoint(), create_portfolio_endpoint(), delete_portfolio_endpoint(), get_order_sheet_endpoint(), get_portfolio_endpoint(), get_portfolio_service(), get_rebalance_diff_endpoint() (+1 more)

### Community 35 - "BacktestEngine"
Cohesion: 0.11
Nodes (10): BacktestTrade, RegimePerformanceBreakdown, BacktestEngine, BacktestResultData, compute_rsi(), calculate_backtest_metrics(), calculate_regime_breakdown(), mock_backtest_result() (+2 more)

### Community 36 - "pytest"
Cohesion: 0.06
Nodes (20): Settings, test_chat_endpoint_graceful_degradation_503(), test_chat_endpoint_success(), test_chat_status_endpoint(), test_chat_status_endpoint_when_disabled(), test_get_growth_forecast(), test_get_stock_profile(), test_list_explore_stocks_and_filter() (+12 more)

### Community 37 - "MarketRegimeClassifier"
Cohesion: 0.14
Nodes (5): MarketRegimeClassifier, synthetic_regime_features(), test_classifier_fit_and_predict(), test_classifier_probabilities_sum_to_one(), test_classifier_state_label_determinism()

### Community 38 - "streaming.py"
Cohesion: 0.08
Nodes (10): test_stream_ticks_alias_route(), test_stream_ticks_endpoint_headers_and_event(), test_stream_ticks_symbol_filter(), test_app_js_exports_report_functions(), test_report_blob_generation_and_share_flow_headless(), market_service(), test_format_sse_event(), test_generate_batch_ticks() (+2 more)

### Community 39 - "alerts/service.py"
Cohesion: 0.13
Nodes (16): AlertSeverity, SmartAlert, SmartAlertType, evaluate_52w_high_breakout(), evaluate_drawdown_breach(), evaluate_factor_anomaly(), evaluate_portfolio_drift(), evaluate_regime_transition() (+8 more)

### Community 40 - "pandas"
Cohesion: 0.16
Nodes (10): align_to_trading_calendar(), calculate_returns(), sanitize_raw_provider_data(), validate_ohlcv_dataframe(), test_align_to_trading_calendar(), test_calculate_returns(), test_models_validation(), test_validate_ohlcv_dataframe_drops_invalid_rows() (+2 more)

### Community 42 - "ConversationMemoryManager"
Cohesion: 0.22
Nodes (7): ConversationMemoryManager, MessageTurn, test_edge_case_sliding_window_memory_limits(), test_memory_manager_add_and_retrieve_turns(), test_memory_manager_clear_session(), test_memory_manager_format_for_gemini(), test_memory_manager_sliding_window_limit()

### Community 43 - "MarketDataService"
Cohesion: 0.05
Nodes (26): get_explore_service(), CurrentRegimeResponse, ESGScoreResponse, ExploreStockSummary, MultiHorizonGrowthForecast, RegimeHistoricalPoint, RegimeHistoryResponse, RegimeProbabilities (+18 more)

### Community 44 - "literacy.py"
Cohesion: 0.14
Nodes (8): get_all_literacy_cards(), _get_cards_dict(), get_literacy_card_by_key(), _get_literacy_data(), LiteracyCard, LiteracyListResponse, test_invalid_literacy_card_fails_validation(), test_literacy_cards_schema_and_count()

### Community 46 - "OnboardingHero.tsx"
Cohesion: 0.19
Nodes (16): HorizonOption, Step2HorizonProps, PersonaCardDef, Step3PersonaProps, SummaryPillsProps, OnboardingHeroProps, calculatePersonaResult(), PERSONA_DETAILS (+8 more)

### Community 48 - "normalize_symbol"
Cohesion: 0.04
Nodes (29): get_growth_forecast(), get_stock_profile(), get_ticker_esg(), list_explore_stocks(), get_history(), get_market_service(), get_quote(), get_returns_matrix() (+21 more)

### Community 49 - "numpy"
Cohesion: 0.15
Nodes (10): draw_ellipse(), calculate_parkinson_volatility(), calculate_realized_volatility(), calculate_rolling_log_returns(), extract_regime_features(), sample_market_data(), test_calculate_parkinson_volatility(), test_calculate_realized_volatility() (+2 more)

### Community 50 - "triggerHaptic"
Cohesion: 0.12
Nodes (19): backtestCurrentStock(), clearNitiBotChat(), closeStockProfileModal(), copyGrowwFormat(), copyZerodhaFormat(), dismissIOSInstallBanner(), loadVideoFacade(), openCreatePortfolioModal() (+11 more)

### Community 51 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, baseUrl, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+10 more)

### Community 52 - "package.json"
Cohesion: 0.11
Nodes (17): name, private, type, version, autoprefixer, @capacitor/android, @capacitor/core, clsx (+9 more)

### Community 53 - "renderHomeTab"
Cohesion: 0.24
Nodes (18): activateBasketToPortfolio(), applyRebalance(), checkRebalanceDiff(), closeCreatePortfolioModal(), deleteActivePortfolio(), deletePortfolioFromIndexedDB(), handlePortfolioSwitch(), loadPortfoliosFromIndexedDB() (+10 more)

### Community 54 - "QuantNiti: Machine Learning & Quantitative Finance Technical Specification"
Cohesion: 0.11
Nodes (18): 10. End-to-End Execution Flowchart & Mathematical Reference, 3.1 Feature Engineering Matrix, 3.2 GMM Formulation & Expectation-Maximization (EM), 3.3 Deterministic State Mapping via Return-to-Volatility Centroids, 3. Unsupervised Market Regime Classification Engine (GMM & Features), 5.1 Formulation, 5.2 Ridge Regularization Layer, 5. Covariance Matrix Regularization: Ledoit-Wolf Shrinkage (+10 more)

### Community 56 - "HorizonForecastCone"
Cohesion: 0.14
Nodes (7): HorizonForecastCone, build_benchmark_comparisons(), mock_stock_forecasts(), _create_forecast(), test_build_benchmark_comparisons(), test_build_trust_card_pillars(), test_calculate_basket_growth_projections_monotonicity()

### Community 57 - "MarketStreamClient"
Cohesion: 0.15
Nodes (5): marketStream, MarketStreamClient, MarketTick, TickListener, MockEventSource

### Community 58 - "asyncio"
Cohesion: 0.13
Nodes (7): test_adaptive_home_tab_components(), test_advanced_analysis_drawer_in_explore_tab(), test_android_physics_and_haptics_in_js(), test_compounding_visualizer_and_wealth_engine_ui(), test_four_tab_navigation_structure(), test_groww_theme_and_dual_theme_tokens(), test_multi_portfolio_storage_and_mtm_ui()

### Community 59 - "renderNotificationList"
Cohesion: 0.17
Nodes (16): clearAllNotifications(), downloadBlob(), downloadPortfolioReportPDF(), filterNotifications(), formatAlertTime(), generatePortfolioReportBlob(), initNotificationCenter(), loadNotifications() (+8 more)

### Community 60 - "devDependencies"
Cohesion: 0.13
Nodes (15): devDependencies, autoprefixer, jsdom, postcss, tailwindcss, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event (+7 more)

### Community 61 - "test_review_tier1_filters.py"
Cohesion: 0.12
Nodes (7): test_tier1_blocks_email_addresses(), test_tier1_blocks_external_urls(), test_tier1_blocks_phone_numbers(), test_tier1_blocks_profanity(), test_tier1_blocks_prohibited_stock_tips(), test_tier1_blocks_telegram_and_social_handles(), test_tier1_clean_reviews_pass()

### Community 62 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, @capacitor/android, @capacitor/cli, @capacitor/core, chart.js, clsx, framer-motion, lucide-react (+6 more)

### Community 63 - "ReviewTargetType"
Cohesion: 0.13
Nodes (9): ReviewsListResponse, ReviewSubmissionRequest, ReviewSubmissionResponse, ReviewTargetType, ReviewVerificationAgent, ReviewService, review_service(), test_service_rejects_and_does_not_publish_exaggerated_review() (+1 more)

### Community 64 - "manifest.json"
Cohesion: 0.14
Nodes (13): background_color, categories, description, display, icons, id, name, orientation (+5 more)

### Community 65 - "escapeHtml"
Cohesion: 0.21
Nodes (13): escapeHtml(), filterLearningCategory(), filterReviewsList(), initLearningHub(), openConceptModal(), renderLearningCards(), renderLearningHub(), renderReviewsList() (+5 more)

### Community 66 - "asyncio"
Cohesion: 0.18
Nodes (5): test_index_html_contains_pwa_metadata_and_elements(), test_manifest_endpoint_served_with_correct_mime(), test_offline_page_endpoint(), test_pwa_icons_served(), test_service_worker_endpoint_served_with_allowed_header()

### Community 67 - "asyncio"
Cohesion: 0.18
Nodes (5): test_app_js_contains_report_export_and_share_functions(), test_html_contains_download_and_share_buttons(), test_html_contains_portfolio_report_card_template_with_all_sections(), test_html_contains_report_card_cdn_scripts(), test_styles_contain_report_card_layout_rules()

### Community 68 - "test_portfolio_storage.py"
Cohesion: 0.15
Nodes (5): repo(), test_delete_portfolio_cascades(), test_list_portfolios(), test_portfolio_schema_creation(), test_save_and_get_portfolio()

### Community 70 - "test_pwa_unit.py"
Cohesion: 0.17
Nodes (5): test_desktop_responsive_css_rules(), test_icon_assets_exist(), test_manifest_file_exists_and_valid(), test_offline_page_exists_and_styled(), test_service_worker_script_structure()

### Community 71 - "test_end_to_end_integration.py"
Cohesion: 0.24
Nodes (4): test_e2e_explore_stock_to_quant_lab_backtest_journey(), test_e2e_grow_basket_to_virtual_portfolio_lifecycle(), test_e2e_quant_lab_multi_strategy_suite(), test_e2e_regime_radar_history_endpoint()

### Community 72 - "asyncio"
Cohesion: 0.18
Nodes (5): test_get_grow_recommend_success(), test_grow_recommend_esg_conscious_api(), test_grow_recommend_validation_errors(), test_post_baskets_recommend_alias(), test_post_grow_recommend_success()

### Community 73 - "asyncio"
Cohesion: 0.22
Nodes (4): test_app_js_contains_market_stream_client(), test_html_contains_notification_bell_drawer_and_toasts(), test_service_worker_push_event_listeners(), test_styles_contain_tick_flash_and_drawer()

### Community 74 - "forecaster.py"
Cohesion: 0.19
Nodes (5): MultiHorizonForecaster, sample_stock_and_index(), test_forecast_all_four_horizons(), test_forecast_cone_widening_over_longer_horizons(), test_strict_quantile_monotonicity()

### Community 75 - "MarketRegimeType"
Cohesion: 0.22
Nodes (7): LiteracyCategory, MarketRegimeType, RegimeSuitability, compute_regime_suitability(), test_suitability_in_bear_regime(), test_suitability_in_bull_regime(), test_suitability_score_bounds()

### Community 76 - "test_client_serving.py"
Cohesion: 0.29
Nodes (5): test_app_route_serves_html(), test_competitor_benchmark_drawer_served(), test_root_serves_html(), test_static_assets_served(), test_vite_build_assets_served()

### Community 77 - "test_review_verification_agent.py"
Cohesion: 0.17
Nodes (5): agent(), test_agent_approves_and_verifies_authentic_review(), test_agent_approves_qualitative_review(), test_agent_blocks_tier1_spam_immediately(), test_agent_rejects_exaggerated_returns_at_tier2()

### Community 78 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, apk:build, build, cap:open, cap:sync, dev, mobile:serve, preview (+1 more)

### Community 80 - "test_mark_alert_read_and_clear"
Cohesion: 0.29
Nodes (3): test_evaluate_endpoint(), test_mark_alert_read_and_clear(), test_web_push_subscription_and_vapid_key()

### Community 81 - "test_api_routes.py"
Cohesion: 0.24
Nodes (8): health_check(), test_get_history_endpoint(), test_get_quote_endpoint(), test_get_returns_matrix_endpoint(), test_get_universe_endpoint(), test_get_universe_filtered_by_sector(), test_health_endpoint(), test_sync_endpoint()

### Community 82 - "asyncio"
Cohesion: 0.22
Nodes (4): test_backtest_validation_errors(), test_get_backtest_run_success(), test_post_backtest_run_success(), test_post_quant_lab_backtest_alias()

### Community 83 - "asyncio"
Cohesion: 0.22
Nodes (4): test_compounding_endpoint_mounted_at_both_prefixes(), test_compounding_endpoint_standalone_post(), test_compounding_endpoint_validation_errors(), test_compounding_endpoint_with_portfolio_id()

### Community 84 - "test_explore_api.py"
Cohesion: 0.39
Nodes (7): test_explore_stocks_contain_esg_fields(), test_get_explore_stocks_filtered(), test_get_explore_stocks_route(), test_get_growth_forecast_route(), test_get_stock_profile_route(), test_get_ticker_esg_endpoint(), test_stock_profile_contains_esg()

### Community 85 - "asyncio"
Cohesion: 0.22
Nodes (4): test_create_and_list_multiple_portfolios(), test_delete_portfolio_lifecycle(), test_dual_prefix_routing_portfolios(), test_portfolio_detail_mtm_metrics()

### Community 86 - "asyncio"
Cohesion: 0.22
Nodes (4): test_get_reviews_endpoint(), test_submit_exaggerated_review_rejected(), test_submit_prohibited_spam_rejected(), test_submit_verified_review()

### Community 87 - "test_day_over_day_mtm.py"
Cohesion: 0.22
Nodes (3): base_portfolio(), test_aggregate_portfolio_day_over_day_mtm(), test_holding_day_over_day_mtm_formula()

### Community 88 - "setup.ts"
Cohesion: 0.25
Nodes (3): @testing-library/jest-dom, localStorageMock, sessionStorageMock

### Community 89 - "backtest.py"
Cohesion: 0.25
Nodes (6): get_backtest_service(), run_backtest_get(), run_backtest_post(), run_quant_lab_backtest_alias(), BacktestRequest, BacktestResponse

### Community 90 - "compilerOptions"
Cohesion: 0.25
Nodes (7): compilerOptions, allowSyntheticDefaultImports, composite, module, moduleResolution, skipLibCheck, include

### Community 91 - "QuantNiti: Hosting, Centralized Server & Scalability Guide"
Cohesion: 0.13
Nodes (14): 1. Architectural Overview, 2. 1-Click Cloud Deployment Guides, 3. Running with Docker & Docker Compose (Any VPS / Local Machine), 4. Connecting Standalone Clients (Mobile APK & PWAs), 5. Horizontal & Vertical Scalability, ASGI Concurrency, Direct Docker Run, Memory Optimization (+6 more)

### Community 92 - "QuantNiti (क्वान्टनीति) 🇮🇳"
Cohesion: 0.13
Nodes (15): 1. Prerequisites, 2. Installation, 3. Running Locally, AI-Driven Regime-Adaptive Portfolio Intelligence & Quantitative Decision Support System, 🎯 Core Mathematical & Algorithmic Methodologies, Development Mode (Hot Reloading Frontend & Backend):, 📱 Key Product Capabilities, 📄 License & Attribution (+7 more)

### Community 94 - "test_explore_stocks_total_and_asset_class_filter"
Cohesion: 0.29
Nodes (3): test_explore_profiles_for_etf_and_defense(), test_explore_stocks_total_and_asset_class_filter(), test_explore_theme_filter_chips()

### Community 95 - "asyncio"
Cohesion: 0.29
Nodes (3): test_app_js_contains_review_management_functions(), test_html_contains_review_section_and_modal(), test_styles_contain_review_and_badge_classes()

### Community 98 - "2. Platform-by-Platform Verified Primary-Source Audit"
Cohesion: 0.17
Nodes (11): 1. Executive Summary: The Structural Gap in Indian WealthTech, 2. Platform-by-Platform Verified Primary-Source Audit, 3. Comprehensive 10-Dimension Competitive Matrix, 4. Key Takeaways for Academic & Industry Evaluation, A. MoneyControl (Pro & Super Pro), B. Zerodha (Kite + Streak), C. Groww (Stocks & Portfolio Analysis), D. INDmoney (+3 more)

### Community 99 - "grow.py"
Cohesion: 0.25
Nodes (6): get_grow_service(), recommend_basket_alias(), recommend_basket_get(), recommend_basket_post(), BasketRecommendationRequest, BasketRecommendationResponse

### Community 100 - "6. Mathematical Formulations & Algorithmic Engines"
Cohesion: 0.18
Nodes (11): 6.4 Ledoit-Wolf Covariance Matrix Regularization, 6.6.1 Greedy Deficit-Minimization Sizing (Primary Real-Time Algorithm), 6.6.2 Mixed-Integer Linear Programming (MILP Formulation), 6.6 Discrete Integer Share Sizing & Cash Buffer Optimization, 6.7.1 Stochastic Differential Equation (SDE), 6.7.2 Monthly Systematic Investment Plan (SIP) with Annual Step-Up, 6.7.3 The Compounding Tipping Point, 6.7 Geometric Brownian Motion Compounding & Analytical Tipping Point (+3 more)

### Community 101 - "filterBySector"
Cohesion: 0.40
Nodes (5): filterBySector(), filterStocks(), loadExploreStocks(), renderExploreStockGrid(), renderHomeTopPicks()

### Community 102 - "3. Academic Demonstration & Evaluation Scenarios"
Cohesion: 0.18
Nodes (10): 1. System Overview, 2. Launching the Application, 3. Academic Demonstration & Evaluation Scenarios, 4-Tab Navigation Architecture, 4. Test Suite Execution, Demonstration 1: Retail Investor Flow (`Grow` Tab), Demonstration 2: Stock Explorer Flow (`Explore` Tab), Demonstration 3: Quant Lab Strategy Studio (`Quant Lab` Tab) (+2 more)

### Community 103 - "QuantNiti: Complete Architectural Blueprint & System Design Document"
Cohesion: 0.20
Nodes (10): 1. Executive Summary & Problem Context, 2. Full-Stack System Architecture, 4.1. The 5-Step Guided Grow Experience, 4.2. Universal Financial & Brand Color Palette, 4.3. Lifecycle Management & Race Condition Guards, 4. Frontend Architecture & Design Engineering, 5. Security, Reliability & Verification Matrix, 6. Deployment & Operations (+2 more)

### Community 104 - "loadBasketReviews"
Cohesion: 0.50
Nodes (4): closeWriteReviewModal(), loadBasketReviews(), renderReviewsSummary(), submitUserReview()

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
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1156 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `useAbortableRequest()` connect `GlassCard` to `react`, `PrimaryButton`, `QuantNiti: Complete Architectural Blueprint & System Design Document`, `9. IEEE Research Paper Blueprint (Section-by-Section Outline)`, `5. End-to-End System Architecture`, `PortfolioPage.tsx`, `lucide-react`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 56 inferred relationships involving `MarketDataService` (e.g. with `get_history()` and `get_market_service()`) actually correct?**
  _`MarketDataService` has 56 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@capacitor/android`, `@capacitor/core`, `clsx` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `react` be split into smaller, more focused modules?**
  _Cohesion score 0.07272727272727272 - nodes in this community are weakly interconnected._
- **Why does `MarketDataService` connect `MarketDataService` to `RiskPersona`, `pytest`, `MarketDataProvider`, `streaming.py`, `alerts/service.py`, `PortfolioService`, `create_app`, `normalize_symbol`, `MarketTickGenerator`, `BacktestService`, `test_market_service.py`, `test_multi_asset_universe.py`, `RAGContextBuilder`, `AlertService`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `MarketRegimeType` (e.g. with `PortfolioRepository` and `evaluate_regime_transition()`) actually correct?**
  _`MarketRegimeType` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `RiskPersona` be split into smaller, more focused modules?**
  _Cohesion score 0.09743589743589744 - nodes in this community are weakly interconnected._