USE DigikalaDB;

-- 1. Core counts (KPIs)
SELECT
    COUNT(*)                    AS row_count,
    COUNT(DISTINCT order_id)    AS unique_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT item_id)     AS unique_items
FROM orders;

-- 2. Yearly orders and sales
-- Line total = amount * quantity (amount appears to be a per-unit price)
SELECT
    year,
    COUNT(DISTINCT order_id) AS orders,
    SUM(amount * quantity)   AS total_sales
FROM orders
GROUP BY year
ORDER BY year;

-- 3. Top 10 cities by sales
SELECT TOP 10
    city,
    COUNT(DISTINCT order_id) AS orders,
    SUM(amount * quantity)   AS total_sales
FROM orders
GROUP BY city
ORDER BY total_sales DESC;

-- 4. Customers grouped by number of orders
SELECT
    CASE WHEN order_count >= 5 THEN '5+'
         ELSE CAST(order_count AS VARCHAR(2)) END AS orders_per_customer,
    COUNT(*) AS customers
FROM (
    SELECT customer_id, COUNT(DISTINCT order_id) AS order_count
    FROM orders
    GROUP BY customer_id
) AS t
GROUP BY CASE WHEN order_count >= 5 THEN '5+'
              ELSE CAST(order_count AS VARCHAR(2)) END
ORDER BY MIN(order_count);