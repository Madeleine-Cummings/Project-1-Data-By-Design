import duckdb
import os

# Create connection
con = duckdb.connect()

# Paths (FIXED)
RAW_PATH = "data/raw/accepted_2007_to_2018Q4.csv.gz"
PROCESSED_PATH = "data/processed/"
FINAL_PATH = "data/final/"

# Make sure folders exist
os.makedirs(PROCESSED_PATH, exist_ok=True)
os.makedirs(FINAL_PATH, exist_ok=True)

# -------------------------------
# LOAD DATA
# -------------------------------
con.execute(f"""
    CREATE TABLE loans_raw AS
    SELECT *
    FROM read_csv_auto(
        '{RAW_PATH}',
        all_varchar=true,
        ignore_errors=true
    )
""")

# Preview
print(con.execute("SELECT * FROM loans_raw LIMIT 5").fetchdf())

# -------------------------------
# CLEAN DATA
# -------------------------------
con.execute("""
    CREATE TABLE loans_clean AS
    SELECT
        id,
        loan_amnt,
        term,
        int_rate,
        installment,
        loan_status,
        emp_length,
        home_ownership,
        annual_inc,
        verification_status,
        purpose,
        grade,
        sub_grade,
        application_type,
        dti,
        fico_range_low,
        fico_range_high,
        open_acc,
        pub_rec,
        revol_bal,
        revol_util,
        total_acc,
        delinq_2yrs,
        inq_last_6mths
    FROM loans_raw
    WHERE loan_status IS NOT NULL
""")

# -------------------------------
# CREATE TARGET
# -------------------------------
con.execute("""
    CREATE TABLE loans_final AS
    SELECT *,
        CASE
            WHEN loan_status = 'Charged Off' THEN 1
            ELSE 0
        END AS default_flag
    FROM loans_clean
""")

# Save full dataset
con.execute(f"""
    COPY loans_final
    TO '{PROCESSED_PATH}loans_dataset.csv.gz'
    (HEADER, DELIMITER ',', COMPRESSION 'gzip')
""")

# -------------------------------
# CREATE RELATIONAL TABLES
# -------------------------------

# loans
con.execute("""
    CREATE TABLE loans AS
    SELECT id, loan_amnt, term, int_rate, installment, loan_status, default_flag
    FROM loans_final
""")

# borrowers
con.execute("""
    CREATE TABLE borrowers AS
    SELECT id, emp_length, home_ownership, annual_inc
    FROM loans_final
""")

# credit
con.execute("""
    CREATE TABLE credit AS
    SELECT id, fico_range_low, fico_range_high, open_acc, pub_rec,
           revol_bal, revol_util, total_acc, dti
    FROM loans_final
""")

# loan details
con.execute("""
    CREATE TABLE loan_details AS
    SELECT id, purpose, grade, sub_grade
    FROM loans_final
""")

# -------------------------------
# EXPORT TABLES
# -------------------------------

con.execute(f"COPY loans TO '{FINAL_PATH}loans.csv' (HEADER)")
con.execute(f"COPY borrowers TO '{FINAL_PATH}borrowers.csv' (HEADER)")
con.execute(f"COPY credit TO '{FINAL_PATH}credit.csv' (HEADER)")
con.execute(f"COPY loan_details TO '{FINAL_PATH}loan_details.csv' (HEADER)")

# -------------------------------
# VALIDATION (FOR NOTEBOOK OUTPUT)
# -------------------------------

print("\nMissing Values:")
print(con.execute("""
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN loan_amnt IS NULL THEN 1 ELSE 0 END)*1.0 / COUNT(*) AS loan_amnt_missing,
    SUM(CASE WHEN int_rate IS NULL THEN 1 ELSE 0 END)*1.0 / COUNT(*) AS int_rate_missing,
    SUM(CASE WHEN annual_inc IS NULL THEN 1 ELSE 0 END)*1.0 / COUNT(*) AS annual_inc_missing,
    SUM(CASE WHEN dti IS NULL THEN 1 ELSE 0 END)*1.0 / COUNT(*) AS dti_missing
FROM loans_final;
""").fetchdf())

print("\nSummary Stats:")
print(con.execute("""
SELECT
    AVG(CAST(loan_amnt AS DOUBLE)) AS avg_loan,
    STDDEV(CAST(loan_amnt AS DOUBLE)) AS std_loan,
    AVG(CAST(annual_inc AS DOUBLE)) AS avg_income,
    STDDEV(CAST(annual_inc AS DOUBLE)) AS std_income,
    AVG(CAST(dti AS DOUBLE)) AS avg_dti,
    STDDEV(CAST(dti AS DOUBLE)) AS std_dti
FROM loans_final;
""").fetchdf())
