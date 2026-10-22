
-- Project: E-commerce Customer Analytics
-- File: 05_customer_segmentation.sql
-- Purpose: Group customers using their RFM scores.

USE ecommerce_analytics;

CREATE TABLE customer_segments AS
SELECT
    customer_unique_id,
    recency_days,
    frequency,
    monetary,
    R_score,
    F_score,
    M_score,
    CASE
        WHEN R_score >= 4 AND F_score >= 4 AND M_score >= 4
            THEN 'Champions'
        WHEN R_score >= 3 AND F_score >= 4
            THEN 'Loyal Customers'
        WHEN R_score >= 4 AND F_score >= 2
            THEN 'Potential Loyalists'
        WHEN R_score = 5 AND F_score = 1
            THEN 'Recent Customers'
        WHEN R_score <= 2 AND F_score >= 3
            THEN 'At Risk'
        WHEN R_score <= 2 AND F_score <= 2
            THEN 'Hibernating'
        ELSE 'Needs Attention'
    END AS customer_segment
FROM customer_rfm_scored;
