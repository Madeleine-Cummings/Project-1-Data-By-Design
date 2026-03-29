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
