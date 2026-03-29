# DS 4320 Project 1:  INSERT NAME

## Data

This dataset is stored in a UVA One drive folder due to file size restraints 
[Access Data Folder](https://myuva-my.sharepoint.com/:f:/g/personal/uwg9at_virginia_edu/IgBmAq3QAvxeT59EnEGAwvdnAbbKbjczKylQS1X1a_0abNY?e=Oa1FoP)

---
## Problem Definition

**General Problem:**  
Can we predict whether an individual will default on a loan based on a variety of borrower characteristics?

**Refined Problem:**  
Can we estimate the probability of loan default for borrowers with little or no credit history using alternative financial indicators (e.g., income, debt-to-income ratio) and loan attributes, in the absence of traditional credit score data?


### Rationale for Refinement
The general problem of predicting loan default risk is broad and applies to many types of borrowers and lending contexts. Existing models often rely heavily on credit history as a primary predictor of default. However, this approach becomes less effective when evaluating borrowers with limited credit history, as they lack sufficient historical data for traditional credit scoring methods. By narrowing the focus to this group, the project addresses a meaningful gap in current risk models and explores how alternative financial characteristics and loan attributes can be used to assess default risk when traditional credit signals are incomplete.

### Motivation
Predicting loan default risk is essential for financial institutions seeking to minimize losses while expanding lending opportunities. Current evaluation methods disadvantage individuals with limited credit history, making it difficult for them to access loans and build credit over time. This project aims to explore alternative approaches to evaluating borrower risk by leveraging additional financial and loan-related features. By improving risk assessment for these individuals, the project supports more inclusive lending practices while maintaining effective risk management.


### Press Release

**Headline:**  
When Credit Falls Short, Data Can Fill the Gap  

**Link:**  
[View Press Release](docs/press_release.md)

--- 

## Domain Exposition 
For a more detailed analysis, see:  
[Full Domain Exposition Notebook](notebooks/Domain_Exposition.ipynb)

This project operates in the domain of credit risk analysis and financial lending. Financial institutions must evaluate whether to lend money to individuals while minimizing the risk of financial loss. Traditionally, this evaluation relies heavily on credit history, as borrowers with strong credit histories are generally less likely to default. However, this creates challenges for individuals with limited or no credit history, as they lack the historical data typically used to assess risk.  

To address this gap, modern data science techniques incorporate alternative financial and behavioral indicators to better estimate default risk and support more inclusive and accurate lending decisions.

### Key Terminology

| Term | Definition |
|------|-----------|
| Loan Default | Failure of a borrower to repay a loan on time |
| Credit History | Record of past borrowing and repayment behavior used to assess creditworthiness |
| Limited Credit History | Little or no prior credit activity, making evaluation difficult |
| Debt-to-Income Ratio (DTI) | Ratio of debt payments to income used to assess repayment ability |
| Interest Rate | Percentage charged for borrowing money |
| Loan Term | Length of time over which a loan is repaid |
| Credit Score | Numerical measure of creditworthiness |
| Default Probability | Predicted likelihood a borrower will fail to repay |
| Borrower | Individual or entity receiving a loan |
| Loan Attributes | Characteristics such as loan amount, rate, and term |


### Background Reading

Supporting materials are available in the [Background Reading](./Background%20Reading/).

| Title | Description | Link |
|------|------------|------|
| Machine Learning and Metaheuristics Approach for Individual Credit Risk Assessment | Reviews machine learning approaches for predicting credit risk | [PDF](Background%20Reading/Machine%20Learning%20and%20Metaheuristics%20Approach%20for%20Individual%20Credit%20Risk%20Assessment_%20A%20Systematic%20Literature%20Review%20-%20PMC%20(1).pdf) |
| Credit Scoring Alternatives for Those Without Credit | Explores alternative methods for evaluating borrowers without credit scores | [PDF](Background%20Reading/Credit%20Scoring%20Alternatives%20for%20Those%20Without%20Credit%20_%20U.S.%20GAO%20(1).pdf) |
| 3 Ways Lenders Can Evaluate Credit Invisibles | Discusses fintech approaches to assessing limited-credit borrowers | [PDF](Background%20Reading/3%20ways%20lenders%20can%20evaluate%20credit%20invisibles%20_%20Plaid%20(1).pdf) |
| The Importance of Loan Risk Rating Systems | Explains institutional risk rating systems for loans | [PDF](Background%20Reading/The%20Importance%20of%20Loan%20Risk%20Rating%20Systems%20(1).pdf) |
| Lending Risk Analysis: Key Considerations | Covers modern tools including ML and advanced analytics in lending | [PDF](Background%20Reading/Lending%20Risk%20Analysis_%20Key%20Considerations%20(1).pdf) |

---

## Data Creation

### Overview

The dataset used in this project is derived from LendingClub loan data and focuses on predicting loan default risk using accepted loan records. Due to the size and complexity of the dataset, a structured data creation pipeline was developed to clean, transform, and organize the data into a relational format suitable for analysis.

The raw dataset is not stored directly in this repository due to size constraints. It is available via UVA OneDrive:

**Raw Data Link:**
[https://myuva-my.sharepoint.com/:u:/g/personal/uwg9at_virginia_edu/IQCyWiKPDUB7Ro0gxu6LDfrxAcvt49M7NXSkXUGDtt4b-0M?e=zHcFJo](https://myuva-my.sharepoint.com/:u:/g/personal/uwg9at_virginia_edu/IQCyWiKPDUB7Ro0gxu6LDfrxAcvt49M7NXSkXUGDtt4b-0M?e=zHcFJo)

To reproduce the dataset, place the raw file in:

```id="91d2rm"
data/raw/accepted_2007_to_2018Q4.csv.gz
```


### Data Creation Pipeline

The full data creation process — including data ingestion, cleaning, feature selection, target variable creation, and relational table construction — is implemented in the notebook below:

* [Data Creation Notebook](notebooks/Data_Creation_.ipynb)

This notebook contains:

* Detailed data provenance and processing steps
* Code used to construct the dataset
* Bias identification and mitigation discussion
* Rationale for key data decisions

### Output Data

The final processed datasets are included in this repository:

```id="k4gtn1"
data/final/
    loans.csv
    borrowers.csv
    credit.csv
    loan_details.csv
```

These tables are structured using the relational model and serve as the primary dataset for downstream analysis.


### Notes on Reproducibility

The data creation pipeline is designed to be reproducible given access to the raw dataset. DuckDB is used to efficiently query and process the compressed data without requiring full in-memory loading.

---

## Metadata

### Schema 

![ER Diagram](docs/ER%20Diagram.png)

### Data


| Table Name   | Description                                                                                                 | Link                                                                                                             |
| ------------ | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| loans        | Core loan-level data including loan amount, interest rate, status, and target variable (`default_flag`)     | [View](https://github.com/Madeleine-Cummings/Project-1-Data-By-Design/blob/main/data/processed/loans.csv)        |
| borrowers    | Borrower demographic and financial information such as income, employment length, and home ownership        | [View](https://github.com/Madeleine-Cummings/Project-1-Data-By-Design/blob/main/data/processed/borrowers.csv)    |
| credit       | Credit history and financial behavior metrics including FICO range, utilization, and delinquency indicators | [View](https://github.com/Madeleine-Cummings/Project-1-Data-By-Design/blob/main/data/processed/credit.csv)       |
| loan_details | Loan-specific categorical attributes such as purpose, grade, and sub-grade                                  | [View](https://github.com/Madeleine-Cummings/Project-1-Data-By-Design/blob/main/data/processed/loan_details.csv) |


### Data Dictionary: Features

| Name            | Data Type        | Description                              | Example              |
| --------------- | ---------------- | ---------------------------------------- | -------------------- |
| id              | integer          | Unique identifier for each loan/borrower | 123456               |
| loan_amnt       | float            | Total loan amount requested              | 10000.0              |
| term            | string           | Loan duration                            | "36 months"          |
| int_rate        | float            | Interest rate (%)                        | 13.56                |
| installment     | float            | Monthly loan payment                     | 340.12               |
| loan_status     | string           | Loan outcome/status                      | "Fully Paid"         |
| default_flag    | integer (binary) | Default indicator (1 = default, 0 = not) | 1                    |
| emp_length      | string           | Employment length                        | "5 years"            |
| home_ownership  | string           | Home ownership status                    | "RENT"               |
| annual_inc      | float            | Annual income                            | 65000.0              |
| fico_range_low  | integer          | Lower bound of FICO score                | 680                  |
| fico_range_high | integer          | Upper bound of FICO score                | 699                  |
| open_acc        | integer          | Number of open credit accounts           | 8                    |
| pub_rec         | integer          | Number of public records                 | 0                    |
| revol_bal       | float            | Revolving credit balance                 | 12000.0              |
| revol_util      | float            | Credit utilization (%)                   | 45.3                 |
| total_acc       | integer          | Total credit accounts                    | 20                   |
| dti             | float            | Debt-to-income ratio                     | 18.5                 |
| purpose         | string           | Loan purpose                             | "debt_consolidation" |
| grade           | string           | Credit grade                             | "B"                  |
| sub_grade       | string           | Detailed credit grade                    | "B3"                 |

### Data dictionary: Quantification of Uncertainty 


| Feature         | Missing (%) | Std Dev  | Source of Uncertainty              | Notes                                         |
| --------------- | ----------- | -------- | ---------------------------------- | --------------------------------------------- |
| loan_amnt       | 0.00%       | 8643.76  | Borrower choice + loan structuring | Wide spread in loan sizes                     |
| int_rate        | 0.00%       | —        | Assigned by platform               | Minimal uncertainty                           |
| installment     | 0.00%       | —        | Derived variable                   | Deterministic from loan terms                 |
| annual_inc      | 0.00%       | 87805.72 | Self-reported income               | High variability and potential reporting bias |
| fico_range_low  | 0.00%       | —        | Range-based measurement            | Does not capture exact score                  |
| fico_range_high | 0.00%       | —        | Range-based measurement            | Interval uncertainty                          |
| open_acc        | 0.00%       | —        | Reporting lag                      | May not reflect real-time accounts            |
| pub_rec         | 0.00%       | —        | Reporting accuracy                 | Rare but may be underreported                 |
| revol_bal       | 0.00%       | —        | Reporting + updates                | Can fluctuate over time                       |
| revol_util      | 0.04%       | —        | Derived + reporting                | Small amount of missing data                  |
| total_acc       | 0.00%       | —        | Credit history reporting           | Generally reliable                            |
| delinq_2yrs     | 0.00%       | —        | Time window limitation             | Only recent delinquencies included            |
| inq_last_6mths  | 0.00%       | —        | Time window limitation             | Limited to recent credit inquiries            |
| dti             | 0.002%      | 9.51     | Derived + income uncertainty       | Sensitive to income accuracy                  |

Uncertainty in this dataset’s numerical features is assessed through missingness and variability, measured using standard deviation. Overall, the dataset contains very little missing data, indicating a high level of completeness. However, certain features, such as annual income, exhibit substantial variability, reflecting the wide range of borrower financial situations in real life. Additionally, some variables may introduce uncertainty due to being self-reported or derived, and the data collection process itself presents potential sources of bias that should be considered during analysis.
