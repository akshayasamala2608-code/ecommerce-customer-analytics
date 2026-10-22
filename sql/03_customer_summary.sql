
-- Project: E-commerce Customer Analytics
-- File: 03_customer_summary.sql
-- Purpose: Summarize purchase behavior for each unique customer.

USE ecommerce_analytics;

CREATE TABLE customer_order_summary AS
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT oa.order_id) AS total_orders,
    MIN(oa.purchase_date) AS first_order_date,
    MAX(oa.purchase_date) AS last_order_date,
    SUM(oa.product_revenue) AS total_product_revenue,
    SUM(oa.freight_revenue) AS total_freight_revenue,
    SUM(oa.order_value) AS total_revenue,
    AVG(oa.order_value) AS average_order_value,
    SUM(oa.payment_total) AS total_payment
FROM order_analytics AS oa
JOIN customers AS c
    ON oa.customer_id = c.customer_id
GROUP BY c.customer_unique_id;
