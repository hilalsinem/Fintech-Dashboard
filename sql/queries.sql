-- 1. Daily Transaction Volume
SELECT 
    DATE(transaction_date) as transaction_day,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN status = 'SUCCESS' THEN amount ELSE 0 END) as total_amount,
    AVG(CASE WHEN status = 'SUCCESS' THEN amount END) as avg_amount
FROM transactions
GROUP BY DATE(transaction_date)
ORDER BY transaction_day;

-- 2. Revenue by Category
SELECT 
    merchant_category,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN status = 'SUCCESS' THEN amount ELSE 0 END) as total_revenue,
    AVG(CASE WHEN status = 'SUCCESS' THEN amount END) as avg_transaction_size
FROM transactions
GROUP BY merchant_category
ORDER BY total_revenue DESC;

-- 3. Customer Spending Analysis
SELECT 
    customer_id,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN status = 'SUCCESS' THEN amount ELSE 0 END) as total_spent,
    AVG(CASE WHEN status = 'SUCCESS' THEN amount END) as avg_transaction_size
FROM transactions
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 20;

-- 4. Fraud Detection Patterns
SELECT 
    merchant_category,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN status = 'FRAUD_DETECTED' THEN 1 ELSE 0 END) as fraud_count,
    ROUND(SUM(CASE WHEN status = 'FRAUD_DETECTED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as fraud_percentage
FROM transactions
GROUP BY merchant_category
HAVING SUM(CASE WHEN status = 'FRAUD_DETECTED' THEN 1 ELSE 0 END) > 0
ORDER BY fraud_percentage DESC;

-- 5. Failed Transaction Analysis
SELECT 
    transaction_type,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed_count,
    ROUND(SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as failure_rate
FROM transactions
GROUP BY transaction_type
ORDER BY failure_rate DESC;

-- 6. Monthly Growth Rate
WITH monthly_data AS (
    SELECT 
        DATE_TRUNC('month', transaction_date) as month,
        COUNT(*) as transaction_count,
        SUM(CASE WHEN status = 'SUCCESS' THEN amount ELSE 0 END) as total_amount
    FROM transactions
    GROUP BY DATE_TRUNC('month', transaction_date)
)
SELECT 
    month,
    transaction_count,
    total_amount,
    LAG(transaction_count) OVER (ORDER BY month) as prev_month_count,
    ROUND((transaction_count - LAG(transaction_count) OVER (ORDER BY month)) * 100.0 / 
          LAG(transaction_count) OVER (ORDER BY month), 2) as growth_rate
FROM monthly_data
ORDER BY month;

-- 7. Top Merchants by Volume
SELECT 
    merchant_id,
    merchant_category,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN status = 'SUCCESS' THEN amount ELSE 0 END) as total_volume
FROM transactions
GROUP BY merchant_id, merchant_category
ORDER BY total_volume DESC
LIMIT 15;

-- 8. Customer Retention (Monthly Active Users)
WITH monthly_active AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', transaction_date) as month,
        COUNT(*) as transaction_count
    FROM transactions
    WHERE status = 'SUCCESS'
    GROUP BY customer_id, DATE_TRUNC('month', transaction_date)
)
SELECT 
    month,
    COUNT(DISTINCT customer_id) as active_customers,
    LAG(COUNT(DISTINCT customer_id)) OVER (ORDER BY month) as prev_month_active,
    ROUND((COUNT(DISTINCT customer_id) - LAG(COUNT(DISTINCT customer_id)) OVER (ORDER BY month)) * 100.0 / 
          LAG(COUNT(DISTINCT customer_id)) OVER (ORDER BY month), 2) as growth_rate
FROM monthly_active
GROUP BY month
ORDER BY month;