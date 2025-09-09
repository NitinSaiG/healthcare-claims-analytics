Project Overview
This project analyzes healthcare claims data to provide actionable insights for hospital providers, payers, and healthcare analysts. Using Python, SQL, and Power BI, the project demonstrates end-to-end data processing, analysis, and visualization, including total payments, readmissions, and patient demographics.

Dataset
 Sample Data: claims.csv and beneficiaries.csv (for initial analysis)
 Optional Realistic Data: CMS Medicare Synthetic Public Use Files (SynPUF)
 Key Columns:
  provider_id, provider_name
  beneficiary_id, sex, age
  claim_type, drg_code, total_charge, admission_date, readmitted_30d
  length_of_stay

Technologies Used
 Python & Pandas – Data cleaning and ETL
 SQLite – Storing and querying claims data
 SQL – Aggregation and analysis queries
 Power BI – Interactive dashboards
 Git/GitHub – Project version control

Project Workflow
 1. Data Cleaning & ETL (Python)
     Load claims and beneficiaries CSVs.
     Clean missing values and format dates.
     Compute derived fields like 30-day readmission.
     Export cleaned CSV for Power BI: claims_for_bi.csv
      python src/etl.py --input data/claims.csv --beneficiaries data/beneficiaries.csv --db data/claims.db
2. SQL Analysis
   Example queries:
     Total claims per provider
     Average claim amount per DRG
     Readmission rate per provider
3. Power BI Dashboard Visuals
     Cards (KPIs)
     Total Claims
     Total Payments
     Readmission Rate
   Bar Chart
     Top 10 Providers by Total Payments
   Pie Chart
     Claim Amount by Beneficiary Gender
   Line Chart
     Monthly Payments Trend
   Matrix
     Provider × Claim Type (Payments, LOS)
   Slicers
     Readmission (readmitted_30d)
     Year, Claim Type, DRG

4. Key Insights
    Identify top providers by total claims and payments.
    Analyze readmission patterns to highlight high-risk providers.
    Track monthly claim trends for hospital operations planning.
    Compare claim distributions by gender and DRG.

5. How to Run
    Clone the repo.
    Create Python environment:
       conda create -n claims python=3.11 -y
       conda activate claims
       pip install -r requirements.txt
    Run ETL to generate cleaned CSV:
       python src/etl.py --input data/claims.csv --beneficiaries data/beneficiaries.csv --db data/claims.db
Open Power BI → Get Data → Text/CSV → data/clean/claims_for_bi.csv → load dashboard visuals.

6. Folder Structure
healthcare-claims-analytics/
├── data/
│   ├── claims.csv
│   ├── beneficiaries.csv
│   └── clean/claims_for_bi.csv
├── dashboards/
│   └── powerbi/Claims_Analytics.pbix
├── sql/queries.sql
├── src/etl.py
├── src/run_sql.py
├── requirements.txt
└── README.md
