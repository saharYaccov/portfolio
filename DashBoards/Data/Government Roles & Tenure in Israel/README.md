# 🇮🇱🏛️ Government Roles & Tenure in Israel Dataset

## 🧠 Overview
This repository contains comprehensive datasets and Python scripts related to the political careers of Israeli politicians, with a focus on their **government roles** and **tenure length**. The primary goal is to analyze the correlation between an individual's background—specifically **academic education** (degrees and fields of study) and **military service** (senior IDF rank)—and their subsequent success and longevity in government positions.

The data was initially collected and processed from **public sources**, primarily **Wikipedia**.

---

## 📊 Data Files
The repository includes several processed **CSV files** (derived from a master Excel workbook) focusing on different aspects of the analysis:

| File Name | Description |
|-----------|-------------|
| `Government Roles & Tenure in Israel.xlsx - מיין.csv` | The central dataset, containing every government role (Tenure ID) filled by politicians, including the start and end year of the role, party, and category (e.g., 'Economic', 'Security'). |
| `Government Roles & Tenure in Israel.xlsx - טבלה1 (2).csv` / `pol_degree.xlsx - Sheet1.csv` | Detailed academic information for each politician, including the type of degree, number of degrees, institutions (e.g., 'Location 1'), and fields of study (e.g., 'Field 1'). |
| `Government Roles & Tenure in Israel.xlsx - צבא.csv` | Personal data, including the **highest military rank (דרגה ביכרה בצה״ל)** and marital status (מצב משפחתי). |
| `Original_degree.csv` | A clean, processed subset of the data, filtered specifically for tenures in recent governments ('34+' Knesset/Government period). |

---

## 📁 Raw Data Output / Reports
| Folder/File | Description |
|---|---|
| `political_reports/` | **Raw output files (originally intended as TXT reports)** that were **scraped directly from the politicians' Wikipedia biographical entries** using the Python script. These files serve as the raw source for the final processed tabular data. |

---

## 💻 Code Files
| File Name | Description |
|-----------|-------------|
| `find_text_political.py` | A Python script containing the core logic for:
| | - **Data Extraction**: Pulling information from public sources (Wikipedia), responsible for generating the files found in the `political_reports/` folder.
| | - **Data Transformation**: Cleaning, mapping, and transforming the raw data into a structured format.
| | - **File Generation**: Filtering the master file to generate the final processed files like `Original_degree.csv`.

---

## 🔧 Use Cases
- **BI Dashboards**: Visualize role distribution, average tenure length, and degree/rank correlation using BI tools like **Tableau** or **Power BI**.
- **Quantitative Analysis**: Study the impact of variables like 'Levels of Degrees' and 'Senior IDF Rank' on 'Tenure Length' (שנים).
- **Data Storytelling**: Create narratives and reports based on the educational and military backgrounds of senior Israeli political leaders.

---

## 📌 Notes
- The datasets are structured for **cross-referencing** by politician's name or **Tenure ID** (מזהה כהונה).
- Academic degrees and military ranks were **categorized and numerically encoded** for simplified quantitative analysis (as seen in the Python script's logic).

---

## 🚀 Future Work
- Integrate data from **older governments** (pre-2015) to increase the historical depth of the analysis.
- Add quantitative metrics for **political experience** (e.g., years served in the Knesset or local government).
- Implement **statistical models** to predict a politician's likelihood of achieving a senior ministerial role.

---

## 👤 Author
**saharYaccov**
📂 **Project Path**: `portfolio/DashBoards/Data/Government Roles & Tenure in Israel/`
