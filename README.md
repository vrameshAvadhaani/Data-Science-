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
│   └── ab_test_evaluator.py            # Z-Test, p-value & SRM Validation
│
├── 05_dashboards/                      # Business Intelligence
│   ├── Search_Relevance_Scorecard.pbix  # Interactive Power BI File
│   └── screenshots/                    # Dashboard Visual Previews
│
└── 06_product_management/              # Agile Product Ownership Artifacts
    └── PRD_Search_Optimization.md      # Product Requirement Document
