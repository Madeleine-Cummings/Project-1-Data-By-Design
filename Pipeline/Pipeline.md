# Pipeline

## Implementing the Model


```python
# Making the structure simular to github in collab
import os

os.makedirs("data/processed", exist_ok=True)
```


```python
from google.colab import files
uploaded = files.upload()
```



     <input type="file" id="files-8433ca85-5af0-4749-a76d-631ec7fdacbb" name="files[]" multiple disabled
        style="border:none" />
     <output id="result-8433ca85-5af0-4749-a76d-631ec7fdacbb">
      Upload widget is only available when the cell has been executed in the
      current browser session. Please rerun this cell to enable.
      </output>
      <script>// Copyright 2017 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Helpers for google.colab Python module.
 */
(function(scope) {
function span(text, styleAttributes = {}) {
  const element = document.createElement('span');
  element.textContent = text;
  for (const key of Object.keys(styleAttributes)) {
    element.style[key] = styleAttributes[key];
  }
  return element;
}

// Max number of bytes which will be uploaded at a time.
const MAX_PAYLOAD_SIZE = 100 * 1024;

function _uploadFiles(inputId, outputId) {
  const steps = uploadFilesStep(inputId, outputId);
  const outputElement = document.getElementById(outputId);
  // Cache steps on the outputElement to make it available for the next call
  // to uploadFilesContinue from Python.
  outputElement.steps = steps;

  return _uploadFilesContinue(outputId);
}

// This is roughly an async generator (not supported in the browser yet),
// where there are multiple asynchronous steps and the Python side is going
// to poll for completion of each step.
// This uses a Promise to block the python side on completion of each step,
// then passes the result of the previous step as the input to the next step.
function _uploadFilesContinue(outputId) {
  const outputElement = document.getElementById(outputId);
  const steps = outputElement.steps;

  const next = steps.next(outputElement.lastPromiseValue);
  return Promise.resolve(next.value.promise).then((value) => {
    // Cache the last promise value to make it available to the next
    // step of the generator.
    outputElement.lastPromiseValue = value;
    return next.value.response;
  });
}

/**
 * Generator function which is called between each async step of the upload
 * process.
 * @param {string} inputId Element ID of the input file picker element.
 * @param {string} outputId Element ID of the output display.
 * @return {!Iterable<!Object>} Iterable of next steps.
 */
function* uploadFilesStep(inputId, outputId) {
  const inputElement = document.getElementById(inputId);
  inputElement.disabled = false;

  const outputElement = document.getElementById(outputId);
  outputElement.innerHTML = '';

  const pickedPromise = new Promise((resolve) => {
    inputElement.addEventListener('change', (e) => {
      resolve(e.target.files);
    });
  });

  const cancel = document.createElement('button');
  inputElement.parentElement.appendChild(cancel);
  cancel.textContent = 'Cancel upload';
  const cancelPromise = new Promise((resolve) => {
    cancel.onclick = () => {
      resolve(null);
    };
  });

  // Wait for the user to pick the files.
  const files = yield {
    promise: Promise.race([pickedPromise, cancelPromise]),
    response: {
      action: 'starting',
    }
  };

  cancel.remove();

  // Disable the input element since further picks are not allowed.
  inputElement.disabled = true;

  if (!files) {
    return {
      response: {
        action: 'complete',
      }
    };
  }

  for (const file of files) {
    const li = document.createElement('li');
    li.append(span(file.name, {fontWeight: 'bold'}));
    li.append(span(
        `(${file.type || 'n/a'}) - ${file.size} bytes, ` +
        `last modified: ${
            file.lastModifiedDate ? file.lastModifiedDate.toLocaleDateString() :
                                    'n/a'} - `));
    const percent = span('0% done');
    li.appendChild(percent);

    outputElement.appendChild(li);

    const fileDataPromise = new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        resolve(e.target.result);
      };
      reader.readAsArrayBuffer(file);
    });
    // Wait for the data to be ready.
    let fileData = yield {
      promise: fileDataPromise,
      response: {
        action: 'continue',
      }
    };

    // Use a chunked sending to avoid message size limits. See b/62115660.
    let position = 0;
    do {
      const length = Math.min(fileData.byteLength - position, MAX_PAYLOAD_SIZE);
      const chunk = new Uint8Array(fileData, position, length);
      position += length;

      const base64 = btoa(String.fromCharCode.apply(null, chunk));
      yield {
        response: {
          action: 'append',
          file: file.name,
          data: base64,
        },
      };

      let percentDone = fileData.byteLength === 0 ?
          100 :
          Math.round((position / fileData.byteLength) * 100);
      percent.textContent = `${percentDone}% done`;

    } while (position < fileData.byteLength);
  }

  // All done.
  yield {
    response: {
      action: 'complete',
    }
  };
}

scope.google = scope.google || {};
scope.google.colab = scope.google.colab || {};
scope.google.colab._files = {
  _uploadFiles,
  _uploadFilesContinue,
};
})(self);
</script> 


    Saving borrowers.csv to borrowers.csv
    Saving credit.csv to credit.csv
    Saving loan_details.csv to loan_details.csv
    Saving loans.csv to loans.csv
    


```python
import shutil

files_list = ["loans.csv", "borrowers.csv", "credit.csv", "loan_details.csv"]

for f in files_list:
    shutil.move(f, f"data/processed/{f}")
```


```python
os.listdir("data/processed")
```




    ['credit.csv', 'loans.csv', 'borrowers.csv', 'loan_details.csv']



Loading in the data


```python
#Load in the data
import duckdb

con = duckdb.connect()

# Create tables from CSVs
con.execute("CREATE TABLE loans AS SELECT * FROM 'data/processed/loans.csv'")
con.execute("CREATE TABLE borrowers AS SELECT * FROM 'data/processed/borrowers.csv'")
con.execute("CREATE TABLE credit AS SELECT * FROM 'data/processed/credit.csv'")
con.execute("CREATE TABLE loan_details AS SELECT * FROM 'data/processed/loan_details.csv'")
```




    <duckdb.duckdb.DuckDBPyConnection at 0x7d7cc5dfe370>




```python
# Query

df = con.execute("""
SELECT
    l.id,
    l.loan_amnt,
    l.int_rate,
    l.default_flag,
    b.annual_inc,
    c.fico_range_low,
    c.dti,
    c.revol_util   -- ADD THIS LINE
FROM loans l
JOIN borrowers b USING(id)
JOIN credit c USING(id)
""").df()
```

Applying low credit condition


```python
# Applying low credit condition
df = con.execute("""
SELECT *
FROM (
    SELECT
        l.id,
        l.loan_amnt,
        l.int_rate,
        l.default_flag,
        b.annual_inc,
        c.fico_range_low,
        c.dti
    FROM loans l
    JOIN borrowers b USING(id)
    JOIN credit c USING(id)
)
WHERE CAST(fico_range_low AS DOUBLE) < 700
""").df()
```


```python

```

Preparing the data


```python

import pandas as pd

df = df.dropna()

df['loan_amnt'] = pd.to_numeric(df['loan_amnt'], errors='coerce')
df['int_rate'] = pd.to_numeric(df['int_rate'], errors='coerce')
df['annual_inc'] = pd.to_numeric(df['annual_inc'], errors='coerce')
df['dti'] = pd.to_numeric(df['dti'], errors='coerce')
df['fico_range_low'] = pd.to_numeric(df['fico_range_low'], errors='coerce')

df = df.dropna()
```


```python
df.head()
```





  <div id="df-90912972-eacc-4fe3-8d25-9d67774b0db5" class="colab-df-container">
    <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>loan_amnt</th>
      <th>int_rate</th>
      <th>default_flag</th>
      <th>annual_inc</th>
      <th>fico_range_low</th>
      <th>dti</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>68407277</td>
      <td>3600.0</td>
      <td>13.99</td>
      <td>0</td>
      <td>55000.0</td>
      <td>675.0</td>
      <td>5.91</td>
    </tr>
    <tr>
      <th>1</th>
      <td>68341763</td>
      <td>20000.0</td>
      <td>10.78</td>
      <td>0</td>
      <td>63000.0</td>
      <td>695.0</td>
      <td>10.78</td>
    </tr>
    <tr>
      <th>2</th>
      <td>68476807</td>
      <td>10400.0</td>
      <td>22.45</td>
      <td>0</td>
      <td>104433.0</td>
      <td>695.0</td>
      <td>25.37</td>
    </tr>
    <tr>
      <th>3</th>
      <td>68426831</td>
      <td>11950.0</td>
      <td>13.44</td>
      <td>0</td>
      <td>34000.0</td>
      <td>690.0</td>
      <td>10.20</td>
    </tr>
    <tr>
      <th>4</th>
      <td>68476668</td>
      <td>20000.0</td>
      <td>9.17</td>
      <td>0</td>
      <td>180000.0</td>
      <td>680.0</td>
      <td>14.67</td>
    </tr>
  </tbody>
</table>
</div>
    <div class="colab-df-buttons">

  <div class="colab-df-container">
    <button class="colab-df-convert" onclick="convertToInteractive('df-90912972-eacc-4fe3-8d25-9d67774b0db5')"
            title="Convert this dataframe to an interactive table."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
    <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
  </svg>
    </button>

  <style>
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

    <script>
      const buttonEl =
        document.querySelector('#df-90912972-eacc-4fe3-8d25-9d67774b0db5 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-90912972-eacc-4fe3-8d25-9d67774b0db5');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    </script>
  </div>


    </div>
  </div>





```python
# Checking if Fico score is a good indicator of default (it is not)
print(df.groupby('default_flag')['fico_range_low'].mean())
```

    default_flag
    0    675.953090
    1    674.343387
    Name: fico_range_low, dtype: float64
    

The fico score does not seem to be a good indicator as there is a small difference between a defaulted fico score vs a non defaulted one


```python
# Checking how many defaults there are compared to the non defaults

df['default_flag'].value_counts()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>count</th>
    </tr>
    <tr>
      <th>default_flag</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>57728</td>
    </tr>
    <tr>
      <th>1</th>
      <td>15085</td>
    </tr>
  </tbody>
</table>
</div><br><label><b>dtype:</b> int64</label>




```python
df['fico_range_low'] = pd.to_numeric(df['fico_range_low'], errors='coerce')

# Define low credit threshold
df_low = df[df['fico_range_low'] < 700]
```

Creating multiple models


```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Clean data
df = df.dropna()

# Convert to numeric
cols = ['loan_amnt', 'int_rate', 'annual_inc', 'dti', 'fico_range_low']
for c in cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

df = df.dropna()

# Features + Target
X = df_low[['loan_amnt', 'int_rate', 'annual_inc', 'dti', 'fico_range_low']]
y = df_low['default_flag']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# ---------------------------
# Model 1: Baseline
# ---------------------------
model_base = LogisticRegression(max_iter=1000)
model_base.fit(X_train, y_train)
y_pred_base = model_base.predict(X_test)

print("===== Baseline Logistic Regression =====")
print("Accuracy:", accuracy_score(y_test, y_pred_base))
print(classification_report(y_test, y_pred_base))

# ---------------------------
# Model 2: Balanced
# ---------------------------
model_balanced = LogisticRegression(max_iter=1000, class_weight='balanced')
model_balanced.fit(X_train, y_train)
y_pred_balanced = model_balanced.predict(X_test)

print("\n===== Balanced Logistic Regression =====")
print("Accuracy:", accuracy_score(y_test, y_pred_balanced))
print(classification_report(y_test, y_pred_balanced))

# ---------------------------
# Model 3: Random Forest
# ---------------------------
model_rf = RandomForestClassifier(n_estimators=100)
model_rf.fit(X_train, y_train)
y_pred_rf = model_rf.predict(X_test)

print("\n===== Random Forest =====")
print("Accuracy:", accuracy_score(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))
```

    ===== Baseline Logistic Regression =====
    Accuracy: 0.7935178191306737
                  precision    recall  f1-score   support
    
               0       0.80      0.99      0.88     11578
               1       0.45      0.03      0.06      2985
    
        accuracy                           0.79     14563
       macro avg       0.62      0.51      0.47     14563
    weighted avg       0.73      0.79      0.72     14563
    
    
    ===== Balanced Logistic Regression =====
    Accuracy: 0.6416947057611756
                  precision    recall  f1-score   support
    
               0       0.85      0.66      0.75     11578
               1       0.30      0.56      0.39      2985
    
        accuracy                           0.64     14563
       macro avg       0.58      0.61      0.57     14563
    weighted avg       0.74      0.64      0.67     14563
    
    
    ===== Random Forest =====
    Accuracy: 0.7837670809585937
                  precision    recall  f1-score   support
    
               0       0.80      0.97      0.88     11578
               1       0.34      0.06      0.10      2985
    
        accuracy                           0.78     14563
       macro avg       0.57      0.51      0.49     14563
    weighted avg       0.71      0.78      0.72     14563
    
    

## Analysis Rationale

The objective of this analysis is to predict loan default risk specifically for borrowers with lower credit history. To align with this goal, the dataset was filtered to include only borrowers with FICO scores below 700.

Feature selection focused on variables that are both predictive and available at the time of loan approval. These include loan characteristics (loan amount, interest rate), borrower financial information (annual income, debt-to-income ratio), and credit indicators (FICO score). Variables that could introduce bias or would not be known at the time of decision-making were excluded. This ensures that the model reflects a realistic lending scenario while maintaining interpretability.

A logistic regression model was selected as a baseline due to its interpretability and common use in risk modeling. However, because loan default is a relatively rare event (approximately 20% of observations), the dataset is imbalanced. This leads to misleadingly high accuracy when using a standard model. The baseline model achieved an accuracy of approximately 79%, but a recall of only 3% for default cases, indicating that it failed to effectively identify high-risk borrowers.

To address this, a class-balanced logistic regression model was implemented to better capture default cases. This approach prioritizes recall for default predictions, which is more important in a risk context where failing to identify high-risk borrowers can have significant consequences. The balanced model improved recall for default cases to 56%, although overall accuracy decreased to approximately 64%. This tradeoff reflects a more meaningful model for risk prediction.

A random forest model was also tested to explore whether a more flexible model could improve performance. While the random forest achieved relatively high accuracy (~78%), it still performed poorly in identifying default cases, with recall remaining around 6%. These results indicate that addressing class imbalance has a greater impact on performance than increasing model complexity.


## Visualization


```python
from sklearn.metrics import classification_report
import pandas as pd

# Convert reports to dictionaries
report_base = classification_report(y_test, y_pred_base, output_dict=True)
report_balanced = classification_report(y_test, y_pred_balanced, output_dict=True)
report_rf = classification_report(y_test, y_pred_rf, output_dict=True)

# Extract recall for class 1 (defaults)
recall_base = report_base['1']['recall']
recall_balanced = report_balanced['1']['recall']
recall_rf = report_rf['1']['recall']

# Put into dataframe
results_df = pd.DataFrame({
    'Model': ['Baseline', 'Balanced', 'Random Forest'],
    'Recall': [recall_base, recall_balanced, recall_rf]
})

results_df
```





  <div id="df-9f368183-1171-419c-a6f7-7548955ede05" class="colab-df-container">
    <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Model</th>
      <th>Recall</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Baseline</td>
      <td>0.031826</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Balanced</td>
      <td>0.556114</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Random Forest</td>
      <td>0.057621</td>
    </tr>
  </tbody>
</table>
</div>
    <div class="colab-df-buttons">

  <div class="colab-df-container">
    <button class="colab-df-convert" onclick="convertToInteractive('df-9f368183-1171-419c-a6f7-7548955ede05')"
            title="Convert this dataframe to an interactive table."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
    <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
  </svg>
    </button>

  <style>
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

    <script>
      const buttonEl =
        document.querySelector('#df-9f368183-1171-419c-a6f7-7548955ede05 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-9f368183-1171-419c-a6f7-7548955ede05');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    </script>
  </div>


  <div id="id_1ff42c12-812e-4fbb-af62-3c146b01c6a7">
    <style>
      .colab-df-generate {
        background-color: #E8F0FE;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        fill: #1967D2;
        height: 32px;
        padding: 0 0 0 0;
        width: 32px;
      }

      .colab-df-generate:hover {
        background-color: #E2EBFA;
        box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
        fill: #174EA6;
      }

      [theme=dark] .colab-df-generate {
        background-color: #3B4455;
        fill: #D2E3FC;
      }

      [theme=dark] .colab-df-generate:hover {
        background-color: #434B5C;
        box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
        filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
        fill: #FFFFFF;
      }
    </style>
    <button class="colab-df-generate" onclick="generateWithVariable('results_df')"
            title="Generate code using this dataframe."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
       width="24px">
    <path d="M7,19H8.4L18.45,9,17,7.55,7,17.6ZM5,21V16.75L18.45,3.32a2,2,0,0,1,2.83,0l1.4,1.43a1.91,1.91,0,0,1,.58,1.4,1.91,1.91,0,0,1-.58,1.4L9.25,21ZM18.45,9,17,7.55Zm-12,3A5.31,5.31,0,0,0,4.9,8.1,5.31,5.31,0,0,0,1,6.5,5.31,5.31,0,0,0,4.9,4.9,5.31,5.31,0,0,0,6.5,1,5.31,5.31,0,0,0,8.1,4.9,5.31,5.31,0,0,0,12,6.5,5.46,5.46,0,0,0,6.5,12Z"/>
  </svg>
    </button>
    <script>
      (() => {
      const buttonEl =
        document.querySelector('#id_1ff42c12-812e-4fbb-af62-3c146b01c6a7 button.colab-df-generate');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      buttonEl.onclick = () => {
        google.colab.notebook.generateWithVariable('results_df');
      }
      })();
    </script>
  </div>

    </div>
  </div>





```python
import pandas as pd
import matplotlib.pyplot as plt

# Clean DTI
df_low['dti'] = pd.to_numeric(df_low['dti'], errors='coerce')
df_low = df_low[df_low['dti'] < 100]
df_low = df_low.dropna(subset=['dti', 'default_flag'])

# Better bins
df_low['dti_bin'] = pd.qcut(df_low['dti'], q=5)

# Default rate
default_rate = df_low.groupby('dti_bin')['default_flag'].mean()

# Plot
plt.figure(figsize=(8,5))
bars = default_rate.plot(kind='bar')

# Labels
for i, v in enumerate(default_rate):
    plt.text(i, v, f"{v:.2f}", ha='center', va='bottom')

plt.title("Default Risk Increases with Financial Burden (Low Credit Borrowers)", fontsize=14)
plt.xlabel("Debt-to-Income Ratio (Grouped)", fontsize=12)
plt.ylabel("Default Rate", fontsize=12)

plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
```

    /tmp/ipykernel_21619/1695563270.py:13: FutureWarning: The default of observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
      default_rate = df_low.groupby('dti_bin')['default_flag'].mean()
    


    
![png](Pipeline_files/Pipeline_23_1.png)
    



```python
import matplotlib.pyplot as plt

# Extract metrics again (from your actual results)
acc_base = accuracy_score(y_test, y_pred_base)
acc_bal = accuracy_score(y_test, y_pred_balanced)
acc_rf = accuracy_score(y_test, y_pred_rf)

rec_base = classification_report(y_test, y_pred_base, output_dict=True)['1']['recall']
rec_bal = classification_report(y_test, y_pred_balanced, output_dict=True)['1']['recall']
rec_rf = classification_report(y_test, y_pred_rf, output_dict=True)['1']['recall']

models = ['Baseline', 'Balanced', 'Random Forest']
accuracy = [acc_base, acc_bal, acc_rf]
recall = [rec_base, rec_bal, rec_rf]

# Plot
plt.figure(figsize=(7,5))
plt.scatter(accuracy, recall)

# Label points
for i, model in enumerate(models):
    plt.text(accuracy[i], recall[i], model)

plt.xlabel("Accuracy")
plt.ylabel("Recall (Default Detection)")
plt.title("Model Tradeoff: Accuracy vs Default Detection")

plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
```


    
![png](Pipeline_files/Pipeline_24_0.png)
    



```python
import matplotlib.pyplot as plt

# Convert to percentages
accuracy_pct = [a * 100 for a in accuracy]
recall_pct = [r * 100 for r in recall]

plt.figure(figsize=(7,5))
plt.scatter(accuracy_pct, recall_pct)

# Label points
for i, model in enumerate(models):
    plt.text(accuracy_pct[i], recall_pct[i], model)

plt.xlabel("Accuracy (%)")
plt.ylabel("Recall (Default Detection, %)")
plt.title("Model Tradeoff: Accuracy vs Default Detection")

plt.xlim(0, 100)   # KEY CHANGE
plt.ylim(0, 70)

plt.annotate("Better default detection",
             xy=(accuracy_pct[1], recall_pct[1]),
             xytext=(50, 60),
             arrowprops=dict(arrowstyle="->"))

plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
```


    
![png](Pipeline_files/Pipeline_25_0.png)
    


## Visualization Rationale

Three visualizations were used to support data understanding and model evaluation.

The first visualization examines default rates across debt-to-income (DTI) groups within the low-credit borrower population. This chart reveals a clear upward trend, showing that borrowers with higher financial burden are more likely to default, with default rates increasing from approximately 16% in the lowest DTI group to around 27% in the highest. This provides an important data-driven explanation for why defaults occur and supports the inclusion of DTI as a key predictive feature.

The second visualization compares model performance using recall for default prediction. This highlights a critical limitation of standard models, which achieve high overall accuracy but fail to identify default cases effectively. By focusing on recall, the visualization aligns evaluation with the project’s objective of detecting high-risk borrowers.

The third visualization presents the tradeoff between accuracy and recall across models. While the baseline and random forest models achieve higher accuracy (approximately 78–80%), they perform poorly in detecting default cases, with recall below 10%. In contrast, the balanced logistic regression model achieves significantly higher recall (approximately 56%) despite a lower accuracy (around 64%). This demonstrates that the reduction in accuracy is justified, as the balanced model is far more effective at identifying high-risk borrowers. In the context of loan default prediction, failing to detect defaults is more costly than incorrectly predicting non-default cases, making recall a more appropriate metric than accuracy.

Together, these visualizations provide a cohesive narrative: financial burden drives default risk, traditional models fail to capture that risk, and adjusting for class imbalance leads to more effective and meaningful predictions.
