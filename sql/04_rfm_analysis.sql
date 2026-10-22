
-- Project: E-commerce Customer Analytics
-- File: 04_rfm_analysis.sql
-- Purpose: Calculate customer RFM metrics and scores.
-- Documentation script: review before executing.

USE ecommerce_analytics;

-- 1. Calculate customer-level RFM metrics
CREATE TABLE customer_rfm AS
SELECT
    c.customer_unique_id,
    DATEDIFF(
        (SELECT MAX(purchase_date) FROM order_analytics),
        MAX(oa.purchase_date)
    ) AS recency_days,
    COUNT(DISTINCT oa.order_id) AS frequency,
    SUM(oa.order_value) AS monetary_value,
    MIN(oa.purchase_date) AS first_order_date,
    MAX(oa.purchase_date) AS last_order_date
FROM order_analytics AS oa
JOIN customers AS c
    ON oa.customer_id = c.customer_id
GROUP BY c.customer_unique_id;

-- 2. Assign RFM scores from 1 to 5
CREATE TABLE customer_rfm_scored AS
SELECT
    customer_unique_id,
    recency_days,
    frequency,
    monetary_value,
    first_order_date,
    last_order_date,
    6 - NTILE(5) OVER (
        ORDER BY recency_days ASC
    ) AS R_score,
    NTILE(5) OVER (
        ORDER BY frequency ASC
    ) AS F_score,
    NTILE(5) OVER (
        ORDER BY monetary_value ASC
    ) AS M_score
FROM customer_rfm;
