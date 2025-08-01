Project

## Overview

This project contains multiple Python scripts for data processing, machine learning, and visualization. Some scripts depend on files or databases created by previous scripts, so it is important to run them in the correct order.

## Required Python Packages

Before running the scripts, install the following packages:

pip install ydata-profiling
pip install catboost
pip install jupyter-dash
pip install optuna
pip install pyautogui

## Important: Update File Paths

All Python scripts include file paths that are specific to the original developer’s computer.
You must update these paths in each script to match your local machine’s folder structure.

Example:

```python
p = '/Users/shryqb/PycharmProjects/new_project_original/file_1/data/Merged_Bulletin_Data.xlsx'
Change it to your own path:


p = 'C:/Users/YourName/Projects/data/Merged_Bulletin_Data.xlsx'
Running Order of Scripts
To avoid errors and ensure correct data flow, run the scripts in this order:

Data Preparation
Load and clean data, save to database or files.

Model Training
Train machine learning models, evaluate and save reports.

Visualization & Reporting
Generate charts, graphs, and dashboards using saved results.

Data Requirements
The necessary data files are not included in the repository.
Make sure to download or place the required datasets in the correct paths as set in the scripts.

Database Setup
Some scripts use MySQL databases.
Configure your MySQL server credentials (user, password, host, port) in the scripts accordingly.
If you get errors about missing databases or tables, ensure the database is created or the scripts that create it are run first.

Tips & Troubleshooting
To suppress warnings (e.g., SQLAlchemy SAWarning), configure Python’s warnings filter or logging.

If saving files to folders causes errors, create those folders manually or add Python code to create them (os.makedirs(path, exist_ok=True)).

Always verify your environment setup matches the expected dependencies and database availability.

```


## Running Order of Scripts

**You must run the scripts in the following order:**

1. **read data** — Load and prepare the raw data
2. **data understanding** — Explore and profile the data
3. **plot** — Create visualizations and graphs
4. **impute** — Handle missing values and data cleaning
5. **models** — Train machine learning models and generate reports
6. **html** — Generate HTML reports or dashboards
7. **sql** — Manage database interactions and save/load data

Running them out of order may cause errors or missing data.


## Folder Creation

During execution, some scripts **automatically create folders/directories** (e.g., for saving reports, figures, or database exports).
Make sure your working directory has proper write permissions, or create the needed folders manually before running the scripts.

## Data Requirements

Data files are **not included** in the repository.
Download or place the necessary datasets in the correct folders as referenced in the scripts.

## Database Setup

If using MySQL or other databases, update connection credentials (user, password, host, port) in the scripts accordingly.
Make sure the database exists or run the scripts that create it before running dependent scripts.

## Additional Notes

* To suppress warnings (e.g., SQLAlchemy warnings), configure Python’s warnings or logging.
* If saving files to directories, ensure the directories exist or use `os.makedirs(path, exist_ok=True)` in the code.
* Verify your Python environment and dependencies are correctly installed.
