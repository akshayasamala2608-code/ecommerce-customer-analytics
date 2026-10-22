
-- Project: E-commerce Customer Analytics
-- Database: ecommerce_analytics
-- Purpose: Check table availability, row counts, and data quality.

USE ecommerce_analytics;

-- 1. List all tables in the database
SHOW TABLES;

-- 2. Check row counts in the main raw tables
SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM customers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL
SELECT 'order_reviews', COUNT(*) FROM order_reviews
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'sellers', COUNT(*) FROM sellers;

-- 3. Check for duplicate customer IDs
SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- 4. Check for missing customer identifiers
SELECT COUNT(*) AS missing_customer_ids
FROM customers
WHERE customer_id IS NULL
   OR customer_unique_id IS NULL;

-- 5. Check order statuses
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- 6. Check missing purchase timestamps
SELECT COUNT(*) AS missing_purchase_timestamps
FROM orders
WHERE order_purchase_timestamp IS NULL;

-- 7. Check for invalid negative order item prices
SELECT COUNT(*) AS negative_price_rows
FROM order_items
WHERE price < 0;

-- 8. Check for invalid negative freight values
SELECT COUNT(*) AS negative_freight_rows
FROM order_items
WHERE freight_value < 0;
