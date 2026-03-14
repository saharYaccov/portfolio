import pandas as pd
import numpy as np

# -----------------------------
# Load data
# -----------------------------

df = pd.read_csv("record.csv")   # הקובץ צריך להיות באותה תיקייה

# -----------------------------
# Prepare report
# -----------------------------

report = []

report.append("====================================")
report.append("DATA ANALYSIS REPORT")
report.append("====================================\n")

# Basic info
report.append("----- BASIC DATA INFO -----\n")
report.append(f"Number of rows: {df.shape[0]}")
report.append(f"Number of columns: {df.shape[1]}\n")

report.append("Column names:")
report.append(str(list(df.columns)) + "\n")

report.append("Data types:")
report.append(str(df.dtypes) + "\n")

# Missing values
report.append("----- MISSING VALUES -----\n")
report.append(str(df.isnull().sum()) + "\n")

# Descriptive statistics
report.append("----- DESCRIPTIVE STATISTICS -----\n")
report.append(str(df.describe(include='all')) + "\n")

# Numeric statistics
numeric_df = df.select_dtypes(include=np.number)

report.append("----- MEAN -----\n")
report.append(str(numeric_df.mean()) + "\n")

report.append("----- STANDARD DEVIATION -----\n")
report.append(str(numeric_df.std()) + "\n")

report.append("----- VARIANCE -----\n")
report.append(str(numeric_df.var()) + "\n")

# Correlation matrix
report.append("----- CORRELATION MATRIX -----\n")
report.append(str(numeric_df.corr()) + "\n")

# Unique values
report.append("----- UNIQUE VALUES -----\n")
report.append(str(df.nunique()) + "\n")

# -----------------------------
# Save report in same folder
# -----------------------------

with open("data_analysis_report.txt", "w", encoding="utf-8") as f:
    for line in report:
        f.write(line + "\n")

print("Analysis complete.")
print("Report saved as data_analysis_report.txt in the current folder.")