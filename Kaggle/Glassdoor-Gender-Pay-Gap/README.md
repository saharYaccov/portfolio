# Glassdoor & Mock Data Salary Analysis and Prediction 💵🪙

This project analyzes salary datasets and builds predictive regression models for estimating base salaries. The datasets include **Glassdoor Gender Pay Gap** data and a **mock employee dataset**.

---

## 📦 Libraries Used

- **Data manipulation & computation**
  - `pandas` – for dataframes and CSV reading
  - `numpy` – for numerical computations
- **Visualization**
  - `matplotlib.pyplot` – for plotting graphs
  - `seaborn` – for statistical data visualization
  - `wordcloud` – for generating word clouds of categorical columns
- **Machine Learning**
  - `scikit-learn`:
    - `train_test_split` – for splitting data into train/test sets
    - `RandomForestRegressor` – regression model
    - `OneHotEncoder` – encode categorical variables
    - `MinMaxScaler` – normalize numerical features
    - `mean_squared_error`, `r2_score` – regression evaluation metrics
  - `xgboost`:
    - `XGBRegressor` – gradient boosting regression
- **Persistence**
  - `joblib` – for saving and loading trained models

---

## 📂 Datasets

1. **Glassdoor Gender Pay Gap**
   - Columns: `JobTitle`, `Gender`, `Age`, `PerfEval`, `Education`, `Dept`, `Seniority`, `BasePay`, `Bonus`
2. **Mock Employee Data**
   - Columns: `job`, `gender`, `age`, `country`, `salary`, `smoking`

---

## 🛠 Data Preparation

- Function `make_df(path)` reads CSV files into Pandas DataFrames.
- Columns were selected for analysis and model training:
  ```python
  df_1 = df1[['JobTitle', 'Gender', 'Age', 'Education','Seniority', 'BasePay']]
Missing values were checked using:


📊 Exploratory Data Analysis (EDA)

Histograms: Age distribution

Bar plots: BasePay by JobTitle, Bonus by JobTitle, BasePay by Department

Box plots: Performance evaluation and salary by gender

Scatter plots: BasePay vs Seniority, Salary vs Age

Pie charts: Average salary by gender

Word clouds: Most frequent categories in columns like JobTitle, Gender, Education, Dept

Visualization was done using matplotlib, seaborn and wordcloud.

🤖 Regression Modeling
1️⃣ Random Forest Regression
Function create_reg_model(df, features, target, test_size, plot, prints):

Selects features and target

Applies One-Hot Encoding to categorical variables

Splits dataset into train/test sets

Trains a RandomForestRegressor

Returns MSE and R² metrics

Optionally plots Actual vs Predicted


Best results were selected by evaluating multiple test_size values.


MSE (Mean Squared Error): measures average squared difference between predicted and actual values

R² (R-squared): proportion of variance explained by the model

Plots: Scatter plots of Actual vs Predicted values help visualize model accuracy

🔄 Combining Datasets
Columns were aligned between df1 and df2

Only common columns were retained

Datasets were concatenated vertically using pd.concat

Regression models were retrained on combined datasets for salary prediction

📌 Key Notes
One-Hot Encoding is essential for categorical variables (JobTitle, Gender, etc.)

RandomForestRegressor is simple and robust; XGBRegressor often gives better performance for tabular data

Always normalize numerical features for gradient boosting models

Multiple test sizes were evaluated to find the optimal split

🛠 Tools Summary
EDA & Visualization: matplotlib, seaborn, wordcloud

Data Processing: pandas, numpy, sklearn.preprocessing

Modeling: RandomForestRegressor, XGBRegressor

Persistence: joblib

This notebook provides a complete workflow for analyzing salary data, training regression models, and evaluating their performance with proper visualizations.

<img width="328" height="179" alt="image" src="https://github.com/user-attachments/assets/39463ede-c99c-43a2-95e2-3180771ac78f" />

---

<img width="723" height="454" alt="image" src="https://github.com/user-attachments/assets/427de080-7135-4197-804b-eb9596e86641" />

---

<img width="514" height="456" alt="image" src="https://github.com/user-attachments/assets/980b7906-ba69-4e55-afbe-8487d8d08fc5" />

---

<img width="724" height="495" alt="image" src="https://github.com/user-attachments/assets/ab0f014e-a193-4468-920d-25b42f1b62ea" />

---

<img width="552" height="384" alt="image" src="https://github.com/user-attachments/assets/f86f82ab-9707-4bff-8ab5-cbff6f3b9694" />

---

<img width="569" height="538" alt="image" src="https://github.com/user-attachments/assets/5a4ea40b-f911-4264-9ceb-460090f657b5" />







