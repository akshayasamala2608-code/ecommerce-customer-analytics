
-- Project: E-commerce Customer Analytics
-- File: 04_rfm_analysis.sql
-- Purpose: Calculate customer-level RFM metrics and scores.

USE ecommerce_analytics;

-- Calculate Recency, Frequency, and Monetary Value
CREATE TABLE customer_rfm AS
SELECT
    customer_unique_id,
    DATEDIFF(
        (SELECT MAX(purchase_date) FROM order_analytics),
        MAX(purchase_date)
    ) AS recency_days,
    COUNT(DISTINCT order_id) AS frequency,
    SUM(order_value) AS monetary
FROM (
    SELECT
        c.customer_unique_id,
        oa.order_id,
        oa.purchase_date,
        oa.order_value
    FROM order_analytics AS oa
    JOIN customers AS c
        ON oa.customer_id = c.customer_id
) AS customer_orders
GROUP BY customer_unique_id;

-- Assign RFM scores from 1 to 5.
-- Higher recency score means a more recent purchase.
CREATE TABLE customer_rfm_scored AS
SELECT
    customer_unique_id,
    recency_days,
    frequency,
    monetary,
    6 - NTILE(5) OVER (
        ORDER BY recency_days ASC
    ) AS R_score,
    NTILE(5) OVER (
        ORDER BY frequency ASC
    ) AS F_score,
    NTILE(5) OVER (
        ORDER BY monetary ASC
    ) AS M_score
FROM customer_rfm;
