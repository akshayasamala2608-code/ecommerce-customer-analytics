
-- Project: E-commerce Customer Analytics
-- File: 03_customer_summary.sql
-- Purpose: Summarize delivered orders for each unique customer.
-- Documentation script: review before executing.

USE ecommerce_analytics;

CREATE TABLE customer_order_summary AS
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT c.customer_id) AS customer_id_count,
    COUNT(DISTINCT oa.order_id) AS delivered_order_count,
    MIN(oa.purchase_date) AS first_order_date,
    MAX(oa.purchase_date) AS last_order_date,
    SUM(oa.product_revenue) AS total_product_revenue,
    SUM(oa.freight_revenue) AS total_freight,
    SUM(oa.order_value) AS total_order_value,
    AVG(oa.order_value) AS average_order_value,
    SUM(oa.payment_total) AS total_payment_value
FROM order_analytics AS oa
JOIN customers AS c
    ON oa.customer_id = c.customer_id
GROUP BY c.customer_unique_id;
