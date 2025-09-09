PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS beneficiaries (
    bene_id TEXT PRIMARY KEY,
    sex TEXT,
    dob DATE,
    state TEXT,
    zip3 TEXT,
    dual_eligible INTEGER,
    chronic_count INTEGER
);

CREATE TABLE IF NOT EXISTS claims (
    claim_id TEXT PRIMARY KEY,
    bene_id TEXT REFERENCES beneficiaries(bene_id),
    claim_type TEXT CHECK (claim_type IN ('INP','OUT','CAR')),
    provider_id TEXT,
    drg_code TEXT,
    admission_date DATE,
    discharge_date DATE,
    length_of_stay INTEGER,
    primary_diagnosis TEXT,
    total_charge REAL,
    allowed_amount REAL,
    payment_amount REAL
);

-- Derived table for inpatient readmissions
CREATE TABLE IF NOT EXISTS inpatient_readmissions AS
SELECT
    c1.claim_id AS index_claim_id,
    c1.bene_id,
    c1.discharge_date AS index_discharge_date,
    MIN(c2.admission_date) AS readmit_admission_date,
    CASE
        WHEN MIN(julianday(c2.admission_date) - julianday(c1.discharge_date)) BETWEEN 0 AND 30
        THEN 1 ELSE 0 END AS readmitted_30d
FROM claims c1
LEFT JOIN claims c2
  ON c1.bene_id = c2.bene_id
 AND c2.claim_type = 'INP'
 AND c2.admission_date > c1.discharge_date
 AND julianday(c2.admission_date) - julianday(c1.discharge_date) <= 30
WHERE c1.claim_type = 'INP'
GROUP BY c1.claim_id, c1.bene_id;

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_claims_bene ON claims(bene_id);
CREATE INDEX IF NOT EXISTS idx_claims_dates ON claims(admission_date, discharge_date);
