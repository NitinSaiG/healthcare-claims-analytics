-- Basic counts
SELECT claim_type, COUNT(*) AS n_claims, SUM(payment_amount) AS total_payment
FROM claims
GROUP BY claim_type
ORDER BY total_payment DESC;

-- Top 10 DRGs by payment
SELECT drg_code, COUNT(*) n_claims, SUM(payment_amount) AS total_payment, AVG(length_of_stay) AS avg_los
FROM claims
WHERE claim_type='INP'
GROUP BY drg_code
ORDER BY total_payment DESC
LIMIT 10;

-- 30-day readmission rate (inpatient)
SELECT
  ROUND(100.0 * AVG(readmitted_30d), 2) AS readmission_rate_pct
FROM inpatient_readmissions;

-- Monthly trend (payments)
SELECT strftime('%Y-%m', admission_date) AS month, SUM(payment_amount) AS total_payment
FROM claims
GROUP BY month
ORDER BY month;
