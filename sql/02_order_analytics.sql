
-- Project: E-commerce Customer Analytics
-- File: 02_order_analytics.sql
-- Purpose: Build order-level revenue analytics.
-- Includes delivered orders with valid purchase timestamps.
-- Documentation script: do not rerun if the table already exists.

USE ecommerce_analytics;

CREATE TABLE order_analytics AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_purchase_timestamp AS purchase_date,
    COALESCE(i.product_revenue, 0) AS product_revenue,
    COALESCE(i.freight_revenue, 0) AS freight_revenue,
    COALESCE(i.product_revenue, 0)
        + COALESCE(i.freight_revenue, 0) AS order_value,
    COALESCE(p.payment_total, 0) AS payment_total
FROM orders AS o

-- Aggregate items before joining to prevent duplicated revenue
LEFT JOIN (
    SELECT
        order_id,
        SUM(price) AS product_revenue,
        SUM(freight_value) AS freight_revenue
    FROM order_items
    GROUP BY order_id
) AS i
    ON o.order_id = i.order_id

-- Aggregate payments separately to prevent double counting
LEFT JOIN (
    SELECT
        order_id,
        SUM(payment_value) AS payment_total
    FROM order_payments
    GROUP BY order_id
) AS p
    ON o.order_id = p.order_id

WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp IS NOT NULL;
