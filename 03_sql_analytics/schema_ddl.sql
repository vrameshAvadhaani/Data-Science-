-- ====================================================================
-- STAR SCHEMA DDL: Digital Shelf Search Analytics Engine
-- ====================================================================

-- 1. Dimension Table: Product Catalog
CREATE TABLE IF NOT EXISTS dim_product_catalog (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);

-- 2. Fact Table: Cleaned Search Clickstream Telemetry
CREATE TABLE IF NOT EXISTS fact_search_telemetry (
    event_id VARCHAR(50) PRIMARY KEY,
    event_name VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    session_id VARCHAR(50) NOT NULL,
    user_pseudo_id VARCHAR(50) NOT NULL,
    device_type VARCHAR(20) NOT NULL,
    experiment_variant VARCHAR(50) NOT NULL,
    query_string VARCHAR(255) NOT NULL,
    results_count INT NULL,
    zero_results_flag BOOLEAN NULL,
    latency_ms INT NULL,
    product_id VARCHAR(50) NULL,
    rank_position INT NULL,
    cart_price DECIMAL(10,2) NULL,
    FOREIGN KEY (product_id) REFERENCES dim_product_catalog(product_id)
);

-- Indexes for Query Performance Optimization
CREATE INDEX idx_telemetry_session ON fact_search_telemetry(session_id);
CREATE INDEX idx_telemetry_variant ON fact_search_telemetry(experiment_variant);
CREATE INDEX idx_telemetry_event ON fact_search_telemetry(event_name);
