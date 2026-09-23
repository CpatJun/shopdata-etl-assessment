SELECT 
    c.customer_id,
    c.full_name,
    COUNT(o.order_id) AS total_orders_placed,
    ROUND(SUM(o.usd_amount), 2) AS lifetime_value_usd,
    STRFTIME('%Y-%m', c.signup_date) AS customer_cohort
FROM dim_customers c
LEFT JOIN fct_orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.full_name, customer_cohort
ORDER BY lifetime_value_usd DESC;