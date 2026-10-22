
-- Project: E-commerce Customer Analytics
-- File: 06_monthly_activity_retention.sql
-- Purpose: Analyze monthly customer activity and cohort retention.
-- Documentation script: review before executing.

USE ecommerce_analytics;

-- 1. Monthly activity for each customer
CREATE TABLE customer_monthly_activity AS
SELECT
    c.customer_unique_id,
    STR_TO_DATE(
        DATE_FORMAT(oa.purchase_date, '%Y-%m-01'),
        '%Y-%m-%d'
    ) AS activity_month,
    COUNT(DISTINCT oa.order_id) AS delivered_orders,
    SUM(oa.product_revenue) AS product_revenue
FROM order_analytics AS oa
JOIN customers AS c
    ON oa.customer_id = c.customer_id
GROUP BY
    c.customer_unique_id,
    STR_TO_DATE(
        DATE_FORMAT(oa.purchase_date, '%Y-%m-01'),
        '%Y-%m-%d'
    );

-- 2. Cohort retention
CREATE TABLE customer_cohort_retention AS
WITH customer_cohorts AS (
    SELECT
        customer_unique_id,
        MIN(activity_month) AS cohort_month
    FROM customer_monthly_activity
    GROUP BY customer_unique_id
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_unique_id) AS cohort_customers
    FROM customer_cohorts
    GROUP BY cohort_month
),
cohort_activity AS (
    SELECT
        cc.cohort_month,
        ma.activity_month,
        TIMESTAMPDIFF(
            MONTH,
            cc.cohort_month,
            ma.activity_month
        ) AS months_since_first_purchase,
        COUNT(DISTINCT ma.customer_unique_id) AS active_customers
    FROM customer_cohorts AS cc
    JOIN customer_monthly_activity AS ma
        ON cc.customer_unique_id = ma.customer_unique_id
    GROUP BY
        cc.cohort_month,
        ma.activity_month,
        TIMESTAMPDIFF(
            MONTH,
            cc.cohort_month,
            ma.activity_month
        )
)
SELECT
    ca.cohort_month,
    ca.activity_month,
    ca.months_since_first_purchase,
    cs.cohort_customers,
    ca.active_customers,
    ROUND(
        100.0 * ca.active_customers / NULLIF(cs.cohort_customers, 0),
        2
    ) AS retention_rate_pct
FROM cohort_activity AS ca
JOIN cohort_sizes AS cs
    ON ca.cohort_month = cs.cohort_month;
