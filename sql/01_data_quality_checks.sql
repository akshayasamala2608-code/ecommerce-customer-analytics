
-- Project: E-commerce Customer Analytics
-- File: 01_data_quality_checks.sql
-- Purpose: Inspect source tables and validate data quality.
-- This script contains read-only checks.

USE ecommerce_analytics;

-- 1. List all database tables
SHOW TABLES;

-- 2. Check row counts for all nine raw dataset tables
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
SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL
SELECT 'geolocation', COUNT(*) FROM geolocation
UNION ALL
SELECT 'product_category_translation', COUNT(*)
FROM product_category_translation;

-- 3. Check duplicate customer IDs
SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- 4. Check missing customer identifiers
SELECT COUNT(*) AS missing_customer_ids
FROM customers
WHERE customer_id IS NULL
   OR customer_unique_id IS NULL;

-- 5. Review order status distribution
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

-- 7. Check negative item prices
SELECT COUNT(*) AS negative_price_rows
FROM order_items
WHERE price < 0;

-- 8. Check negative freight values
SELECT COUNT(*) AS negative_freight_rows
FROM order_items
WHERE freight_value < 0;

-- 9. Check duplicate order item identifiers
SELECT
    order_id,
    order_item_id,
    COUNT(*) AS duplicate_count
FROM order_items
GROUP BY order_id, order_item_id
HAVING COUNT(*) > 1;

-- 10. Check missing order-item order IDs
SELECT COUNT(*) AS missing_order_item_order_ids
FROM order_items
WHERE order_id IS NULL;
