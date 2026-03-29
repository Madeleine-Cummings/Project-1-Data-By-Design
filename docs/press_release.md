# When Credit Falls Short, Data Can Fill the Gap


## Hook

How do you prove that your trustworthy when you have no history to be evaluated on? For a lot of people, they are unable to get loans not because they are financially risky, but because they lack the credit history to be evaluated using current metrics.

## Problem statement
Traditional loan risk models heavily rely on using past credit history to evaluate borrowers.  For those with little to no credit history this proves a problem, as they lack a key peice of the evaluation.  While there are other ways to be evaluated, they prove harder and make more work for the financial institutions and the borrower.  As a result, many people struggle to get loans even though they may be financially responsible.

## Solution description

This project proposes an alternative approach for evaluating borrowers who have little or no credit history. By analyzing borrower financial characteristics and loan attributes, the project develops a predictive model that estimates the likelihood that a borrower will default on a loan. This approach provides a more standardized method for assessing risk, helping lenders make fairer and more informed loan decisions. In addition, the model could help potential borrowers better understand their likelihood of receiving a loan, allowing them to plan their financial decisions more effectively.  

### item 5

As seen below, around 45 million people in the US are credit invisible.
https://www.cnbc.com/2015/05/05/credit-invisible-26-million-have-no-credit-score.html

```python
import matplotlib.pyplot as plt

categories = ["No Credit History", "Unscorable Credit History"]
values = [26, 19]

plt.figure(figsize=(6,4))
plt.bar(categories, values)
plt.ylabel("Millions of Americans")
plt.title("Americans Without a Credit Score")
plt.show()
```
