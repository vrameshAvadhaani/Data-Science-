# 🛒 Digital Shelf Search Analytics & Experimentation Engine

> **Domain:** E-Commerce Search & Discovery | CPG Digital Shelf Optimization  
> **Target Scenario:** Enterprise Beverage Catalog (Keurig, Dr Pepper, Snapple, Peet's Coffee)  
> **Key Capabilities:** Event Telemetry Instrumentation, Automated Python Data Pipeline, SQL Funnel Analytics, A/B Testing Evaluation Engine, Power BI Scorecard  

---

## 📌 Executive Summary

Search and discovery are the core monetization drivers for direct-to-consumer (DTC) digital storefronts. Poor search relevance, high query latency, and zero-result search queries directly cause cart abandonment and customer churn.

This project implements an end-to-end **Product Analytics & Experimentation Framework** evaluating an **AI-Powered Semantic Search Engine (Variant B)** against a legacy **Keyword Search Engine (Control A)** across 1,000+ customer search sessions.

---

## 📐 Project Architecture & Directory Layout

```text
digital-shelf-search-analytics-engine/
│
├── README.md                           # Portfolio Executive Summary
├── .gitignore                          # Git Exclusion Rules
│
├── 01_telemetry_specs/                 # Telemetry Instrumentation Specs
│   └── telemetry_tracking_spec.json    # Engineering JSON Event Taxonomy
│
├── 02_data_pipeline/                   # Data Generation & Cleaning Pipeline
│   ├── generate_messy_telemetry.py     # Native Messy Telemetry Generator
│   └── clean_telemetry_pipeline.py     # Python ETL & Deduplication Pipeline
│
├── 03_sql_analytics/                   # Data Warehouse Queries (Star Schema)
│   ├── schema_ddl.sql                  # Table DDL & Relationships
│   └── search_kpi_queries.sql          # Zero-Result, CTR & Latency CTEs
│
├── 04_experimentation_engine/          # A/B Testing & Hypothesis Testing
│   ├── ab_test_evaluator.py            # Z-Test, p-value & SRM Validation
|   └── ab_test_output.png              # test results when ran locally
│
├── 05_dashboards/                      # Business Intelligence
│   ├── Search_Relevance_Scorecard.pbix  # Interactive Power BI File
│   └── screenshots/                    # Dashboard Visual Previews
│
└── 06_product_management/              # Agile Product Ownership Artifacts
    └── PRD_Search_Optimization.md      # Product Requirement Document
```
## 📑 Core Product Telemetry (Event Taxonomy)

Defined 5 primary search telemetry events in JSON Schema format attached to engineering user stories:

| Event Name | Trigger Condition | Core Properties Captured |
|--------|-----------------------------|------------------------------|
| ```search_query_submitted```    | Search execution                      | ```query_string```, ```results_count```, ```latency_ms```, ```zero_results_flag```                       |
| ```autocomplete_clicked``` | Suggestion click | ```suggested_term```, ```position_index``` |
| ```search_result_clicked``` | Product card click | ```product_id```, ```brand```, ```rank_position```, ```is_sponsored``` |
|```search_to_cart_added``` | Direct Add-to-Cart | ```product_id```, ```price```, ```time_to_add_seconds```|

## 📊 Key Business & Search KPIs
+ Zero-Result Search Rate (%): Percentage of query submissions yielding 0 products.

+ Search Conversion Rate (%): Percentage of search sessions resulting in an Add-to-Cart action.

+ Click-Through Rate (CTR) at Position #1–3: Engagement density on top search rank positions.

+ Query Latency (P95 ms): Guardrail metric evaluating site latency impact.

## 🧪 A/B Testing Experimentation Framework

Evaluating Control A (Keyword) vs Variant B (AI Semantic Search):
* Primary Hypothesis ($H_1$): Semantic search reduces zero-result searches and increases Search-to-Cart conversions by $>15\%$.
* Statistical Rigor: Two-sample $Z$-test for proportions, Chi-Square ($\chi^2$) test for Sample Ratio Mismatch (SRM) detection, and 95% Confidence Intervals.

## 🚀 How to Run the Pipeline
1. Clone Repository:
   ```Bash
   git clone [https://github.com/vrameshavadhaani/digital-shelf-search-analytics-engine.git](https://github.com/vrameshavadhaani/digital-shelf-search-analytics-engine.git) cd digital-shelf-search-analytics-engine
   ```
2. Execute Data Pipeline:
   ```Bash
   python 02_data_pipeline/generate_messy_telemetry.py
   python 02_data_pipeline/clean_telemetry_pipeline.py
   ```
3. Run A/B Test Evaluator:
   ```Bash
   python 04_experimentation_engine/ab_test_evaluator.py
   ```

## 👤 Author
<b>Vikram Ramesh</b> <br/> Senior Business Analyst / Product Analytics Specialist <br/>[LinkedIn Profile](https://www.linkedin.com/in/vikramrameshavadhaani/) | [Portfolio Site](https://vrameshavadhaani.github.io/Portfolio/)
