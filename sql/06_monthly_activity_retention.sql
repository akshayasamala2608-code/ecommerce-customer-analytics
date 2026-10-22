
-- Project: E-commerce Customer Analytics
-- File: 06_monthly_activity_retention.sql
-- Purpose: Analyze monthly customer activity and cohort retention.

USE ecommerce_analytics;

-- 1. Monthly customer activity
CREATE TABLE customer_monthly_activity AS
SELECT
    DATE_FORMAT(oa.purchase_date, '%Y-%m-01') AS activity_month,
    c.customer_unique_id,
    COUNT(DISTINCT oa.order_id) AS total_orders,
    SUM(oa.order_value) AS total_revenue
FROM order_analytics AS oa
JOIN customers AS c
    ON oa.customer_id = c.customer_id
GROUP BY
    DATE_FORMAT(oa.purchase_date, '%Y-%m-01'),
    c.customer_unique_id;

-- 2. Cohort retention
-- Cohort month = month of the customer's first purchase.
CREATE TABLE customer_cohort_retention AS
SELECT
    cohort.cohort_month,
    activity.activity_month,
    TIMESTAMPDIFF(
        MONTH,
        cohort.cohort_month,
        activity.activity_month
    ) AS cohort_age_months,
    COUNT(DISTINCT activity.customer_unique_id) AS active_customers
FROM (
    SELECT
        customer_unique_id,
        MIN(activity_month) AS cohort_month
    FROM customer_monthly_activity
    GROUP BY customer_unique_id
) AS cohort
JOIN customer_monthly_activity AS activity
    ON cohort.customer_unique_id = activity.customer_unique_id
GROUP BY
    cohort.cohort_month,
    activity.activity_month,
    TIMESTAMPDIFF(
        MONTH,
        cohort.cohort_month,
        activity.activity_month
    );
