-- ====================================================================
-- SEARCH KPI & FUNNEL ANALYTICS QUERIES
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: Overall Search Discovery KPIs by Experiment Variant
-- Calculates: Total Searches, Zero-Result Rate %, Search-to-Cart Conversion %, Avg Latency
-- --------------------------------------------------------------------
WITH search_sessions AS (
    SELECT 
        experiment_variant,
        COUNT(DISTINCT session_id) AS total_search_sessions,
        COUNT(DISTINCT CASE WHEN zero_results_flag = TRUE THEN session_id END) AS zero_result_sessions,
        AVG(latency_ms) AS avg_query_latency_ms
    FROM fact_search_telemetry
    WHERE event_name = 'search_query_submitted'
    GROUP BY experiment_variant
),
converted_sessions AS (
    SELECT 
        experiment_variant,
        COUNT(DISTINCT session_id) AS cart_add_sessions,
        SUM(cart_price) AS total_search_revenue
    FROM fact_search_telemetry
    WHERE event_name = 'search_to_cart_added'
    GROUP BY experiment_variant
)
SELECT 
    s.experiment_variant,
    s.total_search_sessions,
    s.zero_result_sessions,
    ROUND((s.zero_result_sessions * 100.0 / s.total_search_sessions), 2) AS zero_result_rate_pct,
    COALESCE(c.cart_add_sessions, 0) AS converted_cart_sessions,
    ROUND((COALESCE(c.cart_add_sessions, 0) * 100.0 / s.total_search_sessions), 2) AS search_to_cart_conversion_pct,
    ROUND(s.avg_query_latency_ms, 1) AS avg_latency_ms,
    ROUND(COALESCE(c.total_search_revenue, 0), 2) AS total_revenue
FROM search_sessions s
LEFT JOIN converted_sessions c ON s.experiment_variant = c.experiment_variant;


-- --------------------------------------------------------------------
-- QUERY 2: Click-Through Rate (CTR) Density by Search Result Position Rank
-- Demonstrates how Variant B (AI Search) improves top-3 rank click relevance
-- --------------------------------------------------------------------
SELECT 
    experiment_variant,
    CASE 
        WHEN rank_position BETWEEN 1 AND 3 THEN 'Top 3 (Positions #1-3)'
        WHEN rank_position BETWEEN 4 AND 6 THEN 'Mid Rank (Positions #4-6)'
        ELSE 'Lower Rank (Position #7+)'
    END AS rank_bucket,
    COUNT(event_id) AS total_clicks,
    ROUND(COUNT(event_id) * 100.0 / SUM(COUNT(event_id)) OVER(PARTITION BY experiment_variant), 2) AS click_share_pct
FROM fact_search_telemetry
WHERE event_name = 'search_result_clicked'
GROUP BY experiment_variant, rank_bucket
ORDER BY experiment_variant, MIN(rank_position);


-- --------------------------------------------------------------------
-- QUERY 3: Top Abandoned Search Queries (Zero-Result Bottlenecks)
-- Identifies high-volume search strings yielding 0 products for catalog merchandising teams
-- --------------------------------------------------------------------
SELECT 
    query_string,
    COUNT(session_id) AS total_failed_searches,
    experiment_variant
FROM fact_search_telemetry
WHERE event_name = 'search_query_submitted' AND zero_results_flag = TRUE
GROUP BY query_string, experiment_variant
ORDER BY total_failed_searches DESC
LIMIT 10;
