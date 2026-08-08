-- =========================================================================
-- Financial Analytics & Risk Assessment Dashboard
-- SQL Schema, Load Scripts, and Analytical Queries
-- =========================================================================
-- This file is database-agnostic (PostgreSQL / SQL Server compatible).
-- It provides:
--   1. Schema DDL
--   2. Data load (COPY / BULK INSERT placeholders)
--   3. Analytical queries that power the dashboard KPIs
-- =========================================================================

-- -------------------------------------------------------------------------
-- 1. SCHEMA
-- -------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id          VARCHAR(20) PRIMARY KEY,
    customer_name        VARCHAR(100),
    age                  INT,
    gender               CHAR(1),
    region               VARCHAR(20),
    employment_status    VARCHAR(20),
    annual_income        NUMERIC(14,2),
    credit_score         INT,
    debt_to_income_ratio NUMERIC(5,3),
    account_open_date    DATE
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id    VARCHAR(20) PRIMARY KEY,
    customer_id       VARCHAR(20) REFERENCES customers(customer_id),
    transaction_date  DATE,
    transaction_type  VARCHAR(20),
    amount            NUMERIC(14,2),
    product_category  VARCHAR(30),
    region            VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id              VARCHAR(20) PRIMARY KEY,
    customer_id          VARCHAR(20) REFERENCES customers(customer_id),
    loan_type            VARCHAR(20),
    loan_amount          NUMERIC(14,2),
    interest_rate        NUMERIC(5,2),
    term_months          INT,
    monthly_payment      NUMERIC(14,2),
    remaining_balance    NUMERIC(14,2),
    open_date            DATE,
    status               VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS revenue (
    month                  VARCHAR(7) PRIMARY KEY,
    month_start            DATE,
    revenue                NUMERIC(14,2),
    operating_expenses     NUMERIC(14,2),
    profit                 NUMERIC(14,2),
    interest_income        NUMERIC(14,2),
    fee_income             NUMERIC(14,2),
    loan_loss_provision    NUMERIC(14,2)
);

-- -------------------------------------------------------------------------
-- 2. LOAD (PostgreSQL COPY syntax — adjust for SQL Server BULK INSERT)
-- -------------------------------------------------------------------------
-- \COPY customers   FROM '../data/customers_clean.csv'   CSV HEADER;
-- \COPY transactions FROM '../data/transactions_clean.csv' CSV HEADER;
-- \COPY loans        FROM '../data/loans_clean.csv'      CSV HEADER;
-- \COPY revenue      FROM '../data/revenue.csv'          CSV HEADER;

-- -------------------------------------------------------------------------
-- 3. ANALYTICAL QUERIES
-- -------------------------------------------------------------------------

-- 3a. Revenue Growth (month-over-month %)
SELECT
    r.month,
    r.revenue,
    LAG(r.revenue) OVER (ORDER BY r.month_start) AS prev_revenue,
    ROUND(
        (r.revenue - LAG(r.revenue) OVER (ORDER BY r.month_start))
        / LAG(r.revenue) OVER (ORDER BY r.month_start) * 100,
        2
    ) AS revenue_growth_pct,
    r.profit,
    ROUND(r.profit / r.revenue * 100, 2) AS profit_margin_pct
FROM revenue r
ORDER BY r.month_start;

-- 3b. Profitability (net margin by month)
SELECT
    month,
    revenue,
    operating_expenses,
    profit,
    ROUND(profit / revenue * 100, 2) AS net_margin_pct,
    ROUND(loan_loss_provision / revenue * 100, 2) AS llr_ratio_pct
FROM revenue
ORDER BY month_start;

-- 3c. Loan Default Rate (overall + by type)
SELECT
    loan_type,
    COUNT(*) AS total_loans,
    SUM(CASE WHEN status = 'Defaulted' THEN 1 ELSE 0 END) AS defaulted,
    ROUND(
        SUM(CASE WHEN status = 'Defaulted' THEN 1 ELSE 0 END)::numeric
        / COUNT(*) * 100, 2
    ) AS default_rate_pct
FROM loans
GROUP BY loan_type
ORDER BY default_rate_pct DESC;

-- 3d. Customer Risk Score summary (joined view for the dashboard)
-- (Assumes a customer_risk_scores table exists — created by the Python script)
CREATE TABLE IF NOT EXISTS customer_risk_scores (
    customer_id          VARCHAR(20) PRIMARY KEY,
    customer_name        VARCHAR(100),
    age                  INT,
    gender               CHAR(1),
    region               VARCHAR(20),
    employment_status    VARCHAR(20),
    annual_income        NUMERIC(14,2),
    credit_score         INT,
    debt_to_income_ratio NUMERIC(5,3),
    total_txn_amount     NUMERIC(14,2),
    txn_count            INT,
    avg_txn_amount       NUMERIC(14,2),
    outlier_txn_count    INT,
    total_loan_amount    NUMERIC(14,2),
    active_loans         INT,
    defaulted_loans      INT,
    late_loans           INT,
    risk_score           NUMERIC(5,2),
    risk_band            VARCHAR(10)
);

-- 3e. Transaction trends (monthly volume by type)
SELECT
    TO_CHAR(transaction_date, 'YYYY-MM') AS year_month,
    transaction_type,
    COUNT(*) AS txn_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM transactions
GROUP BY TO_CHAR(transaction_date, 'YYYY-MM'), transaction_type
ORDER BY year_month, transaction_type;

-- 3f. Financial anomalies (amount > mean + 3 * std)
SELECT *
FROM transactions t
JOIN (
    SELECT
        transaction_type,
        AVG(amount) + 3 * STDDEV(amount) AS threshold
    FROM transactions
    GROUP BY transaction_type
) thr ON t.transaction_type = thr.transaction_type
WHERE t.amount > thr.threshold
ORDER BY t.amount DESC;

-- 3g. Regional revenue & risk summary
SELECT
    c.region,
    ROUND(SUM(t.amount), 2) AS total_transaction_value,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    ROUND(AVG(cr.risk_score), 2) AS avg_risk_score
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
LEFT JOIN customer_risk_scores cr ON c.customer_id = cr.customer_id
GROUP BY c.region
ORDER BY total_transaction_value DESC;

-- 3h. Top 10 highest-risk customers
SELECT
    customer_id,
    customer_name,
    credit_score,
    debt_to_income_ratio,
    defaulted_loans,
    risk_score,
    risk_band
FROM customer_risk_scores
ORDER BY risk_score DESC
LIMIT 10;
