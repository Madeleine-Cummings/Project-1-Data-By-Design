import duckdb
import os

# ---------------------------
# Setup paths
# ---------------------------
RAW_PATH = "data/raw/accepted_2007_to_2018Q4.csv.gz"
FINAL_PATH = "data/final/"

# Create folders if they don't exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs(FINAL_PATH, exist_ok=True)

print("Starting data creation pipeline...")

# ---------------------------
# Check for raw data
# ---------------------------
if not os.path.exists(RAW_PATH):
    print("Raw data not found.")
    print("Please download the Lending Club dataset and place it in:")
    print("data/raw/accepted_2007_to_2018Q4.csv.gz")
    print("Skipping pipeline execution.")
    exit()

# ---------------------------
# Connect to DuckDB
# ---------------------------
con = duckdb.connect()

# ---------------------------
# Load raw data
# ---------------------------
print("Loading raw data...")

con.execute(f"""
    CREATE TABLE loans_raw AS
    SELECT *
    FROM read_csv_auto(
        '{RAW_PATH}',
        all_varchar=true,
        ignore_errors=true
    )
""")

# ---------------------------
# Clean data
# ---------------------------
print("Cleaning data...")

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

# ---------------------------
# Create target variable
# ---------------------------
print("Creating target variable...")

con.execute("""
    CREATE TABLE loans_final AS
    SELECT *,
        CASE
            WHEN loan_status = 'Charged Off' THEN 1
            ELSE 0
        END AS default_flag
    FROM loans_clean
""")

# ---------------------------
# Create relational tables
# ---------------------------
print("Creating relational tables...")

con.execute("""
    CREATE TABLE loans AS
    SELECT
        id,
        loan_amnt,
        term,
        int_rate,
        installment,
        loan_status,
        default_flag
    FROM loans_final
""")

con.execute("""
    CREATE TABLE borrowers AS
    SELECT
        id,
        emp_length,
        home_ownership,
        annual_inc
    FROM loans_final
""")

con.execute("""
    CREATE TABLE credit AS
    SELECT
        id,
        fico_range_low,
        fico_range_high,
        open_acc,
        pub_rec,
        revol_bal,
        revol_util,
        total_acc,
        dti
    FROM loans_final
""")

con.execute("""
    CREATE TABLE loan_details AS
    SELECT
        id,
        purpose,
        grade,
        sub_grade
    FROM loans_final
""")

# ---------------------------
# Export tables
# ---------------------------
print("Exporting tables...")

con.execute(f"COPY loans TO '{FINAL_PATH}loans.csv' (HEADER, DELIMITER ',')")
con.execute(f"COPY borrowers TO '{FINAL_PATH}borrowers.csv' (HEADER, DELIMITER ',')")
con.execute(f"COPY credit TO '{FINAL_PATH}credit.csv' (HEADER, DELIMITER ',')")
con.execute(f"COPY loan_details TO '{FINAL_PATH}loan_details.csv' (HEADER, DELIMITER ',')")

print("Data creation pipeline completed successfully.")
