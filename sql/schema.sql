-- Create database (run this separately if needed)
-- CREATE DATABASE fintech_dashboard;

-- Create tables
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    merchant_category VARCHAR(50) NOT NULL,
    merchant_id VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    location VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    registration_date DATE,
    country VARCHAR(50),
    tier VARCHAR(20) DEFAULT 'STANDARD'
);

CREATE TABLE IF NOT EXISTS merchants (
    merchant_id VARCHAR(20) PRIMARY KEY,
    merchant_name VARCHAR(100),
    category VARCHAR(50),
    country VARCHAR(50)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_merchant ON transactions(merchant_id);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(merchant_category);