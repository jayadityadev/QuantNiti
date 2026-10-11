# Graph Report - QuantNiti  (2026-10-11)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2201 nodes · 5675 edges · 122 communities (89 shown, 33 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 704 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ba1a500f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- react
- pytest
- ExploreService
- PrimaryButton
- GlassCard
- data/service.py
- app.js
- ExplorePage.tsx
- numpy
- models.py
- backtest/service.py
- PortfolioService
- compounding_engine.py
- create_app
- agent.py
- PortfolioPage.tsx
- MarketTickGenerator
- MarketRegimeType
- universe.py
- lucide-react
- .run
- RegimeService
- AppShell.tsx
- ReviewTargetType
- provider.py
- MarketDataService
- NitiBotService
- os
- hrp.py
- RAGContextBuilder
- pathlib
- alerts.py
- reviews/service.py
- ParquetMarketCache
- routes/portfolio.py
- engine.py
- MockDataProvider
- MarketRegimeClassifier
- streaming.py
- alerts/service.py
- pandas
- storage.py
- ConversationMemoryManager
- FastAPI
- literacy.py
- AlertService
- OnboardingHero.tsx
- DiscreteAllocationEngine
- SmartAlertType
- features.py
- triggerHaptic
- compilerOptions
- package.json
- renderHomeTab
- TestDiscreteAllocationEngine
- assistant/service.py
- MultiHorizonForecaster
- MarketStreamClient
- test_groww_ui_navigation.py
- renderNotificationList
- devDependencies
- rebalance.py
- dependencies
- ReviewSubmissionRequest
- manifest.json
- escapeHtml
- test_pwa_integration.py
- test_report_card_client.py
- test_portfolio_storage.py
- test_pwa_unit.py
- test_end_to_end_integration.py
- asyncio
- test_smart_alerts_client.py
- chat.py
- compute_regime_suitability
- test_client_serving.py
- test_review_verification_agent.py
- scripts
- ReviewVerificationAgent
- test_get_alerts_empty_and_populated
- test_api_routes.py
- asyncio
- asyncio
- test_explore_api.py
- asyncio
- asyncio
- test_day_over_day_mtm.py
- setup.ts
- test_literacy_api.py
- compilerOptions
- .sync_universe
- denormalize_symbol
- MarketStreamClient
- test_explore_stocks_total_and_asset_class_filter
- asyncio
- test_nitibot_edge_cases.py
- vite.config.ts
- configured_app
- test_esg_data.py
- filterBySector
- test_portfolio_full_lifecycle_api
- .get_universe
- loadBasketReviews
- capacitor.config.ts
- get_market_service
- grow_service
- integration_app
- app_instance
- sw.js
- app

## God Nodes (most connected - your core abstractions)
1. `MarketDataService` - 83 edges
2. `react` - 67 edges
3. `MarketRegimeType` - 59 edges
4. `RegimeService` - 58 edges
5. `RiskPersona` - 50 edges
6. `create_app()` - 45 edges
7. `useAppStore` - 45 edges
8. `PortfolioState` - 42 edges
9. `PrimaryButton()` - 42 edges
10. `GlassCard()` - 42 edges

## Surprising Connections (you probably didn't know these)
- `test_list_explore_stocks_and_filter()` --uses--> `ExploreStockSummary`  [INFERRED]
  tests/integration/test_explore_service.py → src/app/core/models.py
- `test_get_stock_profile()` --uses--> `StockIntelligenceProfile`  [INFERRED]
  tests/integration/test_explore_service.py → src/app/core/models.py
- `test_get_latest_quote()` --uses--> `StockQuote`  [INFERRED]
  tests/integration/test_market_service.py → src/app/core/models.py
- `test_train_model()` --uses--> `RegimeTrainResponse`  [INFERRED]
  tests/integration/test_regime_service.py → src/app/core/models.py
- `test_sync_universe_batch()` --uses--> `SyncResult`  [INFERRED]
  tests/integration/test_market_service.py → src/app/core/models.py

## Import Cycles
- None detected.

## Communities (122 total, 33 thin omitted)

### Community 0 - "react"
Cohesion: 0.07
Nodes (34): react, react-dom, react-router-dom, @testing-library/react, @testing-library/user-event, vitest, App(), Theme (+26 more)

### Community 1 - "pytest"
Cohesion: 0.07
Nodes (26): RiskPersona, calculate_basket_growth_projections(), HRPOptimizer, GrowService, test_grow_service_different_risk_personas(), test_grow_service_esg_portfolio_score_and_persona(), test_grow_service_invalid_inputs_raise_error(), test_grow_service_recommend_basket_balanced() (+18 more)

### Community 2 - "ExploreService"
Cohesion: 0.08
Nodes (21): get_explore_service(), get_growth_forecast(), get_stock_profile(), get_ticker_esg(), list_explore_stocks(), get_history(), get_quote(), get_returns_matrix() (+13 more)

### Community 3 - "PrimaryButton"
Cohesion: 0.11
Nodes (35): chart.js, framer-motion, react-chartjs-2, AllocationDonut(), AllocationDonutProps, AllocationItem, PALETTE, GrowPage() (+27 more)

### Community 4 - "GlassCard"
Cohesion: 0.10
Nodes (27): AdaptiveHomeCard(), AdaptiveHomeCardProps, CompoundingVisualizer(), CompoundingVisualizerProps, LearningHub(), LearningHubProps, isIndianMarketOpen(), MarketPulse() (+19 more)

### Community 5 - "data/service.py"
Cohesion: 0.10
Nodes (7): Settings, MultiHorizonGrowthForecast, get_esg_badge(), get_esg_score_for_symbol(), test_get_growth_forecast(), test_get_stock_profile(), test_list_explore_stocks_and_filter()

### Community 6 - "app.js"
Cohesion: 0.08
Nodes (37): AppState, askNitiBotAboutConcept(), askNitiBotAboutCurrentConcept(), closeCompetitorBenchmarkModal(), closeConceptModal(), closeModalSheet(), closeNitiBotChat(), closeNitiBotModal() (+29 more)

### Community 7 - "ExplorePage.tsx"
Cohesion: 0.08
Nodes (29): ASSETS, ProToolsBacktester(), STRATEGIES, ExploreStockItem, StockCard(), StockCardProps, StockProfileModal(), StockProfileModalProps (+21 more)

### Community 8 - "numpy"
Cohesion: 0.09
Nodes (15): compute_bollinger_bands(), compute_ema(), compute_macd(), compute_max_drawdown(), compute_rsi(), compute_stock_beta_and_alpha(), extract_stock_factors(), sample_stock_and_index() (+7 more)

### Community 9 - "models.py"
Cohesion: 0.11
Nodes (29): BacktestDataPoint, BasketAllocationItem, BasketGrowthProjections, BenchmarkComparisonItem, EvaluateAlertsResponse, LiteracyListResponse, MarketHistoryResponse, OHLCVBar (+21 more)

### Community 10 - "backtest/service.py"
Cohesion: 0.11
Nodes (14): get_backtest_service(), run_backtest_get(), run_backtest_post(), run_quant_lab_backtest_alias(), BacktestRequest, BacktestResponse, StrategyType, BacktestEngine (+6 more)

### Community 11 - "PortfolioService"
Cohesion: 0.09
Nodes (11): BrokerOrderSheet, CreatePortfolioRequest, RebalanceAlert, compute_rebalance_diff(), PortfolioService, portfolio_service(), test_create_and_get_portfolio(), test_get_nonexistent_portfolio_raises_error() (+3 more)

### Community 12 - "compounding_engine.py"
Cohesion: 0.09
Nodes (19): CompoundingMonthlyPoint, CompoundingRequest, CompoundingResponse, CompoundingSummary, CompoundingTippingPoint, CompoundingYearlyPoint, calculate_lump_sum(), calculate_monthly_sip() (+11 more)

### Community 13 - "create_app"
Cohesion: 0.05
Nodes (12): create_app(), app(), app_instance(), app_instance(), app_instance(), test_app(), app(), app_instance() (+4 more)

### Community 14 - "agent.py"
Cohesion: 0.09
Nodes (11): filter_tier1_content(), extract_duration_claim(), extract_return_claim(), audit_tier3_llm(), test_tier1_blocks_email_addresses(), test_tier1_blocks_external_urls(), test_tier1_blocks_phone_numbers(), test_tier1_blocks_profanity() (+3 more)

### Community 15 - "PortfolioPage.tsx"
Cohesion: 0.14
Nodes (22): OrderSheetModalProps, PortfolioReportCardProps, CompoundingTrajectoryChart(), CompoundingTrajectoryChartProps, DemoPortfolio(), DemoPortfolioProps, BenchmarkComparison, CompoundingTrajectoryData (+14 more)

### Community 16 - "MarketTickGenerator"
Cohesion: 0.08
Nodes (9): get_tick_generator(), stream_ticks(), MarketTick, is_indian_market_open(), MarketTickGenerator, test_format_sse_event(), test_generate_single_tick(), test_live_fallback_to_synthetic() (+1 more)

### Community 17 - "MarketRegimeType"
Cohesion: 0.12
Nodes (11): BenchmarkComparisonLive, MarketRegimeType, PortfolioHolding, PortfolioState, PortfolioRepository, calculate_day_over_day_mtm(), create_portfolio_from_allocations(), PortfolioSimulator (+3 more)

### Community 18 - "universe.py"
Cohesion: 0.08
Nodes (16): AssetClass, get_asset_class_for_symbol(), get_sector_for_symbol(), get_universe_metadata(), get_universe_symbols(), test_asset_class_enum_members(), test_commodity_etfs_constituents(), test_defense_constituents() (+8 more)

### Community 19 - "lucide-react"
Cohesion: 0.16
Nodes (23): lucide-react, COMPARISON_ROWS, CompetitorBenchmarkModal(), CompetitorBenchmarkModalProps, ConceptDetailData, ConceptDetailModal(), ConceptDetailModalProps, ModalRoot() (+15 more)

### Community 20 - ".run"
Cohesion: 0.10
Nodes (9): compute_rsi(), benchmark_price_series(), sample_price_series(), test_bollinger_bands_strategy(), test_buy_and_hold_strategy(), test_dual_momentum_strategy(), test_ma_crossover_strategy(), test_rsi_mean_reversion_strategy() (+1 more)

### Community 21 - "RegimeService"
Cohesion: 0.11
Nodes (9): get_current_regime(), get_regime_history(), get_regime_service(), train_regime_model(), TrainRegimeRequest, CurrentRegimeResponse, RegimeHistoryResponse, RegimeProbabilities (+1 more)

### Community 22 - "AppShell.tsx"
Cohesion: 0.13
Nodes (22): AppShell(), BottomNav(), BottomNavProps, NAV_ITEMS, NavItem, triggerHaptic(), Header(), HeaderProps (+14 more)

### Community 23 - "ReviewTargetType"
Cohesion: 0.11
Nodes (13): LiteracyCategory, ReviewStatus, ReviewTargetType, verify_tier2_fact_check(), test_extract_duration_claim(), test_extract_return_claim(), test_tier2_approves_pure_qualitative_reviews(), test_tier2_approves_verified_claim_within_tolerance() (+5 more)

### Community 24 - "provider.py"
Cohesion: 0.09
Nodes (13): test_chat_endpoint_graceful_degradation_503(), test_chat_endpoint_success(), test_chat_status_endpoint(), test_chat_status_endpoint_when_disabled(), test_get_latest_quote(), test_get_universe(), test_sync_universe_batch(), test_get_current_regime_route() (+5 more)

### Community 25 - "MarketDataService"
Cohesion: 0.10
Nodes (6): MarketDataProvider, YahooFinanceProvider, MarketDataService, test_factor_extractor_on_multi_asset_universe(), test_historical_ohlcv_data_exists_for_all_assets(), test_ledoit_wolf_covariance_on_multi_asset_matrix()

### Community 26 - "NitiBotService"
Cohesion: 0.15
Nodes (12): ChatMessageRequest, ChatMessageResponse, NitiBotService, test_edge_case_empty_or_whitespace_message(), test_edge_case_huge_message_overflow(), test_edge_case_sebi_compliance_always_injected(), MockGeminiAdapter, test_nitibot_service_chat_raises_when_unavailable() (+4 more)

### Community 27 - "os"
Cohesion: 0.12
Nodes (7): main(), run_command(), get_lan_ip(), main(), print_qr_code(), test_app_js_exports_report_functions(), test_report_blob_generation_and_share_flow_headless()

### Community 28 - "hrp.py"
Cohesion: 0.11
Nodes (8): apply_weight_caps(), compute_hrp_weights(), compute_shrunk_covariance(), get_cluster_variance(), get_quasi_diag_order(), _traverse(), recursive_bisection(), test_compute_shrunk_covariance_fallback_on_degenerate_data()

### Community 29 - "RAGContextBuilder"
Cohesion: 0.14
Nodes (12): RAGContextPayload, RAGContextBuilder, create_sample_backtest(), create_sample_regime(), test_rag_context_builder_builds_complete_grounding(), test_rag_context_builder_esg_enrichment(), test_rag_context_builder_fallback_defaults(), test_edge_case_corrupted_or_unexpected_context_types() (+4 more)

### Community 31 - "alerts.py"
Cohesion: 0.15
Nodes (9): clear_alerts(), evaluate_alerts_micro_batch(), get_alert_service(), get_vapid_public_key(), list_alerts(), mark_alert_read(), mark_all_alerts_read(), send_test_push_notification() (+1 more)

### Community 32 - "reviews/service.py"
Cohesion: 0.12
Nodes (6): ReviewItem, ReviewsListResponse, ReviewSubmissionResponse, ReviewRepository, ReviewService, review_service()

### Community 33 - "ParquetMarketCache"
Cohesion: 0.16
Nodes (6): ParquetMarketCache, sample_df(), temp_cache_dir(), test_cache_invalidation(), test_cache_save_and_load(), test_cache_ttl_expiration()

### Community 34 - "routes/portfolio.py"
Cohesion: 0.16
Nodes (9): apply_rebalance_endpoint(), calculate_compounding_endpoint(), create_portfolio_endpoint(), delete_portfolio_endpoint(), get_order_sheet_endpoint(), get_portfolio_endpoint(), get_portfolio_service(), get_rebalance_diff_endpoint() (+1 more)

### Community 35 - "engine.py"
Cohesion: 0.15
Nodes (8): BacktestMetrics, BacktestTrade, BacktestResultData, calculate_backtest_metrics(), calculate_regime_breakdown(), mock_backtest_result(), test_calculate_backtest_metrics_values(), test_calculate_regime_breakdown()

### Community 36 - "MockDataProvider"
Cohesion: 0.08
Nodes (12): MockDataProvider, test_app(), test_app(), test_app(), app(), explore_service(), mock_service(), app() (+4 more)

### Community 37 - "MarketRegimeClassifier"
Cohesion: 0.14
Nodes (5): MarketRegimeClassifier, synthetic_regime_features(), test_classifier_fit_and_predict(), test_classifier_probabilities_sum_to_one(), test_classifier_state_label_determinism()

### Community 38 - "streaming.py"
Cohesion: 0.12
Nodes (5): test_stream_ticks_alias_route(), test_stream_ticks_endpoint_headers_and_event(), test_stream_ticks_symbol_filter(), test_generate_batch_ticks(), test_tick_consecutive_price_movement()

### Community 39 - "alerts/service.py"
Cohesion: 0.24
Nodes (8): AlertSeverity, SmartAlert, evaluate_52w_high_breakout(), evaluate_drawdown_breach(), evaluate_factor_anomaly(), evaluate_portfolio_drift(), evaluate_regime_transition(), evaluate_rsi_extreme()

### Community 40 - "pandas"
Cohesion: 0.16
Nodes (9): align_to_trading_calendar(), calculate_returns(), sanitize_raw_provider_data(), validate_ohlcv_dataframe(), test_align_to_trading_calendar(), test_calculate_returns(), test_validate_ohlcv_dataframe_drops_invalid_rows(), test_validate_ohlcv_dataframe_valid_data() (+1 more)

### Community 41 - "storage.py"
Cohesion: 0.14
Nodes (6): Base, DailySnapshotRecord, HoldingRecord, PortfolioRecord, ReviewRecord, TransactionRecord

### Community 42 - "ConversationMemoryManager"
Cohesion: 0.22
Nodes (7): ConversationMemoryManager, MessageTurn, test_edge_case_sliding_window_memory_limits(), test_memory_manager_add_and_retrieve_turns(), test_memory_manager_clear_session(), test_memory_manager_format_for_gemini(), test_memory_manager_sliding_window_limit()

### Community 43 - "FastAPI"
Cohesion: 0.16
Nodes (7): get_grow_service(), recommend_basket_alias(), recommend_basket_get(), recommend_basket_post(), health_check(), BasketRecommendationRequest, BasketRecommendationResponse

### Community 44 - "literacy.py"
Cohesion: 0.14
Nodes (7): get_all_literacy_cards(), _get_cards_dict(), get_literacy_card_by_key(), _get_literacy_data(), LiteracyCard, test_invalid_literacy_card_fails_validation(), test_literacy_cards_schema_and_count()

### Community 46 - "OnboardingHero.tsx"
Cohesion: 0.19
Nodes (16): HorizonOption, Step2HorizonProps, PersonaCardDef, Step3PersonaProps, SummaryPillsProps, OnboardingHeroProps, calculatePersonaResult(), PERSONA_DETAILS (+8 more)

### Community 48 - "SmartAlertType"
Cohesion: 0.14
Nodes (8): SmartAlertType, test_alert_service_deduplication(), test_trigger_1_regime_transition(), test_trigger_2_portfolio_drift(), test_trigger_3_rsi_extremes(), test_trigger_4_drawdown_breach(), test_trigger_5_52w_high_breakout(), test_trigger_6_factor_score_anomaly()

### Community 49 - "features.py"
Cohesion: 0.16
Nodes (9): calculate_parkinson_volatility(), calculate_realized_volatility(), calculate_rolling_log_returns(), extract_regime_features(), sample_market_data(), test_calculate_parkinson_volatility(), test_calculate_realized_volatility(), test_calculate_rolling_log_returns() (+1 more)

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

### Community 56 - "MultiHorizonForecaster"
Cohesion: 0.17
Nodes (7): HorizonForecastCone, MultiHorizonForecaster, mock_stock_forecasts(), _create_forecast(), test_forecast_all_four_horizons(), test_forecast_cone_widening_over_longer_horizons(), test_strict_quantile_monotonicity()

### Community 57 - "MarketStreamClient"
Cohesion: 0.15
Nodes (5): marketStream, MarketStreamClient, MarketTick, TickListener, MockEventSource

### Community 58 - "test_groww_ui_navigation.py"
Cohesion: 0.16
Nodes (7): test_adaptive_home_tab_components(), test_advanced_analysis_drawer_in_explore_tab(), test_android_physics_and_haptics_in_js(), test_compounding_visualizer_and_wealth_engine_ui(), test_four_tab_navigation_structure(), test_groww_theme_and_dual_theme_tokens(), test_multi_portfolio_storage_and_mtm_ui()

### Community 59 - "renderNotificationList"
Cohesion: 0.17
Nodes (16): clearAllNotifications(), downloadBlob(), downloadPortfolioReportPDF(), filterNotifications(), formatAlertTime(), generatePortfolioReportBlob(), initNotificationCenter(), loadNotifications() (+8 more)

### Community 60 - "devDependencies"
Cohesion: 0.13
Nodes (15): devDependencies, autoprefixer, jsdom, postcss, tailwindcss, @testing-library/jest-dom, @testing-library/react, @testing-library/user-event (+7 more)

### Community 61 - "rebalance.py"
Cohesion: 0.18
Nodes (5): BrokerOrderItem, execute_rebalance(), generate_broker_order_sheet(), test_execute_rebalance_updates_holdings(), test_generate_broker_order_sheet()

### Community 62 - "dependencies"
Cohesion: 0.14
Nodes (14): dependencies, @capacitor/android, @capacitor/cli, @capacitor/core, chart.js, clsx, framer-motion, lucide-react (+6 more)

### Community 63 - "ReviewSubmissionRequest"
Cohesion: 0.24
Nodes (5): get_review_service(), get_target_reviews(), preview_verification(), submit_review(), ReviewSubmissionRequest

### Community 64 - "manifest.json"
Cohesion: 0.14
Nodes (13): background_color, categories, description, display, icons, id, name, orientation (+5 more)

### Community 65 - "escapeHtml"
Cohesion: 0.21
Nodes (13): escapeHtml(), filterLearningCategory(), filterReviewsList(), initLearningHub(), openConceptModal(), renderLearningCards(), renderLearningHub(), renderReviewsList() (+5 more)

### Community 66 - "test_pwa_integration.py"
Cohesion: 0.21
Nodes (5): test_index_html_contains_pwa_metadata_and_elements(), test_manifest_endpoint_served_with_correct_mime(), test_offline_page_endpoint(), test_pwa_icons_served(), test_service_worker_endpoint_served_with_allowed_header()

### Community 67 - "test_report_card_client.py"
Cohesion: 0.21
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

### Community 73 - "test_smart_alerts_client.py"
Cohesion: 0.24
Nodes (4): test_app_js_contains_market_stream_client(), test_html_contains_notification_bell_drawer_and_toasts(), test_service_worker_push_event_listeners(), test_styles_contain_tick_flash_and_drawer()

### Community 74 - "chat.py"
Cohesion: 0.31
Nodes (4): get_chat_status(), get_nitibot_service(), post_chat_message(), ChatStatusResponse

### Community 75 - "compute_regime_suitability"
Cohesion: 0.33
Nodes (5): RegimeSuitability, compute_regime_suitability(), test_suitability_in_bear_regime(), test_suitability_in_bull_regime(), test_suitability_score_bounds()

### Community 76 - "test_client_serving.py"
Cohesion: 0.29
Nodes (5): test_app_route_serves_html(), test_competitor_benchmark_drawer_served(), test_root_serves_html(), test_static_assets_served(), test_vite_build_assets_served()

### Community 77 - "test_review_verification_agent.py"
Cohesion: 0.20
Nodes (4): agent(), test_agent_approves_and_verifies_authentic_review(), test_agent_blocks_tier1_spam_immediately(), test_agent_rejects_exaggerated_returns_at_tier2()

### Community 78 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, apk:build, build, cap:open, cap:sync, dev, mobile:serve, preview (+1 more)

### Community 80 - "test_get_alerts_empty_and_populated"
Cohesion: 0.22
Nodes (4): test_evaluate_endpoint(), test_get_alerts_empty_and_populated(), test_mark_alert_read_and_clear(), test_web_push_subscription_and_vapid_key()

### Community 81 - "test_api_routes.py"
Cohesion: 0.39
Nodes (7): test_get_history_endpoint(), test_get_quote_endpoint(), test_get_returns_matrix_endpoint(), test_get_universe_endpoint(), test_get_universe_filtered_by_sector(), test_health_endpoint(), test_sync_endpoint()

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

### Community 89 - "test_literacy_api.py"
Cohesion: 0.39
Nodes (5): test_dual_routing_api_prefix(), test_get_all_literacy_cards_category_filter(), test_get_all_literacy_cards_v1(), test_get_literacy_card_by_unknown_key_returns_404(), test_get_literacy_card_by_valid_key()

### Community 90 - "compilerOptions"
Cohesion: 0.25
Nodes (7): compilerOptions, allowSyntheticDefaultImports, composite, module, moduleResolution, skipLibCheck, include

### Community 94 - "test_explore_stocks_total_and_asset_class_filter"
Cohesion: 0.29
Nodes (3): test_explore_profiles_for_etf_and_defense(), test_explore_stocks_total_and_asset_class_filter(), test_explore_theme_filter_chips()

### Community 95 - "asyncio"
Cohesion: 0.29
Nodes (3): test_app_js_contains_review_management_functions(), test_html_contains_review_section_and_modal(), test_styles_contain_review_and_badge_classes()

### Community 98 - "configured_app"
Cohesion: 0.33
Nodes (3): configured_app(), MockGeminiAdapter, unconfigured_app()

### Community 101 - "filterBySector"
Cohesion: 0.40
Nodes (5): filterBySector(), filterStocks(), loadExploreStocks(), renderExploreStockGrid(), renderHomeTopPicks()

### Community 104 - "loadBasketReviews"
Cohesion: 0.50
Nodes (4): closeWriteReviewModal(), loadBasketReviews(), renderReviewsSummary(), submitUserReview()

## Knowledge Gaps
- **13 isolated node(s):** `app`, `autoprefixer`, `@capacitor/android`, `@capacitor/core`, `clsx` (+8 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 905 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MarketDataService` connect `MarketDataService` to `pytest`, `ExploreService`, `data/service.py`, `models.py`, `backtest/service.py`, `PortfolioService`, `create_app`, `MarketTickGenerator`, `MarketRegimeType`, `RegimeService`, `RAGContextBuilder`, `ParquetMarketCache`, `MockDataProvider`, `MarketRegimeClassifier`, `streaming.py`, `alerts/service.py`, `AlertService`, `MultiHorizonForecaster`, `.sync_universe`, `configured_app`, `.get_universe`, `get_market_service`, `grow_service`, `integration_app`, `app_instance`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 56 inferred relationships involving `MarketDataService` (e.g. with `get_history()` and `get_market_service()`) actually correct?**
  _`MarketDataService` has 56 INFERRED edges - model-reasoned connections that need verification._
- **What connects `app`, `autoprefixer`, `@capacitor/android` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `react` be split into smaller, more focused modules?**
  _Cohesion score 0.07272727272727272 - nodes in this community are weakly interconnected._
- **Why does `normalize_symbol()` connect `ExploreService` to `ParquetMarketCache`, `.fetch_history`, `streaming.py`, `data/service.py`, `alerts/service.py`, `backtest/service.py`, `MarketTickGenerator`, `universe.py`, `provider.py`, `MarketDataService`, `.sync_universe`, `denormalize_symbol`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `MarketRegimeType` (e.g. with `PortfolioRepository` and `evaluate_regime_transition()`) actually correct?**
  _`MarketRegimeType` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `pytest` be split into smaller, more focused modules?**
  _Cohesion score 0.06646825396825397 - nodes in this community are weakly interconnected._