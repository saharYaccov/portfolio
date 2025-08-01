"""
Data Profiling and Exploratory Analysis Reports

This script provides utility functions to generate comprehensive HTML reports for
data analysis and exploration using two popular libraries: Sweetviz and ydata-profiling.

Functions:

1. sweetviz_html_report(df):
   - Generates a detailed Sweetviz report for the input DataFrame.
   - The report includes summary statistics, distributions, correlations,
     and comparisons if needed.
   - Saves the report as "Sweetviz_report.html" and opens it in the browser.

2. create_html_report(df):
   - Generates a comprehensive ydata-profiling report (formerly pandas-profiling).
   - Provides detailed statistics, visualizations, and data quality insights.
   - The report is titled "Profile Report for the Data" and supports interactive exploration.
   - Saves the report to "Profile data.html".

3. find_missing_values(df):
   - Generates a ydata-profiling report focused on identifying duplicates and missing values.
   - Enables detection of duplicate rows.
   - Saves the report to "Duplicates_report.html".

Usage:
- Pass your pandas DataFrame to any of these functions to create an HTML report.
- Reports provide valuable insights for initial data understanding and cleaning.

Dependencies:
- sweetviz
- ydata-profiling
- pandas
"""


import pandas as pd
from ydata_profiling import ProfileReport
import sweetviz as sv

def sweetviz_html_report(df):
    report = sv.analyze(df)
    report.show_html("Sweetviz_report.html")

def create_html_report(df):
    profile = ProfileReport(df , title="Profile Report for the Data",explorative=True , progress_bar=True)
    profile.to_file("Profile data.html")
def find_missing_values(df):
    profile = ProfileReport(df, duplicates={"enabled": True})
    profile.to_file("Duplicates_report.html")

