# ShopData ETL Pipeline & Analytics Assessment

## Overview
This project implements an end-to-end Data Engineering pipeline for "ShopData Inc." to migrate legacy order management data into a clean analytical data warehouse (`analytics.db`). It features automated extraction, data cleaning, currency conversion, orchestration via Prefect, and unit testing with Pytest.

---

## Deliverables Structure
1. `pipeline.py`: Prefect ETL pipeline orchestration.
2. `test_pipeline.py`: Unit tests for transformation logic.
3. `exploration.sql`: Initial SQL script for data discovery and anomaly detection.
4. `clv_report.sql`: Analytical SQL query for calculating Customer Lifetime Value (CLV).
5. `requirements.txt`: Python package dependencies.
6. `README.md`: Project documentation and findings summary.

---

## Data Exploration Findings (Part 1)
Based on `exploration.sql`, the following data quality issues were identified in the raw views:
1. **Duplicate Customer Records**: Multiple entries for the same customer name with varying signup dates, requiring deduplication based on the most recent `signup_date`.
2. **Missing or Malformed Contact Info**: Several records contained missing/empty emails and phone numbers structured with special characters (e.g., `+1 (555)...`), requiring cleaning to keep only numeric digits and fallback unknown emails.
3. **Invalid Transactional Amounts**: Presence of orders with negative or zero `total_amount` values, which are system errors and must be filtered out.

---

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt