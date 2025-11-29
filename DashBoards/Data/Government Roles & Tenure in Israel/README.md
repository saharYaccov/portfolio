# 🇮🇱🏛️ Government Roles & Tenure in Israel Dataset

## 🧠 Overview
This repository contains comprehensive datasets and Python scripts related to the political careers of Israeli politicians, with a focus on their **government roles** and **tenure length**. The primary goal is to analyze the correlation between an individual's background—specifically **academic education** (degrees and fields of study) and **military service** (senior IDF rank)—and their subsequent success and longevity in government positions.

The data was initially collected and processed from **public sources**, primarily **Wikipedia**.

---

## 📊 Data Files
The repository includes several processed **CSV files** derived from a master Excel workbook, focusing on different aspects of the analysis:

| File Name | Description |
|-----------|-------------|
| `Government Roles & Tenure in Israel.xlsx - מיין.csv` | The central dataset, containing every government role (tenure ID) filled by politicians, including the start and end year of the role, party, and category (e.g., 'כלכלי', 'ביטחון'). |
| `Government Roles & Tenure in Israel.xlsx - טבלה1 (2).csv` / `pol_degree.xlsx - Sheet1.csv` | Detailed academic information for each politician, including the type of degree, number of degrees, institutions (מקום1, מקום2), and fields of study (תחום1, תחום2). |
| `Government Roles & Tenure in Israel.xlsx - צבא.csv` | Personal data, including the highest military rank (דרגה ביכרה בצה״ל) and marital status (מצב משפחתי). |
| `Original_degree.csv` | A clean, processed subset of the data, filtered specifically for tenures in recent governments ('34+'). |

---

## 💻 Code Files
| File Name | Description |
|-----------|-------------|
| `find_text_political.py` | A Python script containing the core logic for:
| | - Extracting data from Wikipedia (as suggested by the `extract_politician_data` function).
| | - Cleaning and transforming the data.
| | - Generating the `Original_degree.csv` file, which is filtered for the '34+' government period.

---

## 🔧 Use Cases
- **BI Dashboards**: Visualize role distribution, average tenure length, and degree/rank correlation using tools like **Tableau** or **Power BI**.
- **Quantitative Analysis**: Study the impact of variables like 'Levels of Degrees' and 'Senior IDF Rank' on 'Tenure Length' (שנים).
- **Data Storytelling**: Create narratives around the educational and military backgrounds of senior Israeli political leaders.

---

## 📌 Notes
- The datasets are structured for **cross-referencing** by politician's name or **Tenure ID** (מזהה כהונה).
- Academic degrees and military ranks were **categorized and encoded** for quantitative analysis (as suggested by the Python script's logic).

---

## 🚀 Future Work
- Integrate data from **older governments** (pre-2015).
- Add quantitative metrics for **political experience** (e.g., years in Knesset or local government).
- Implement **statistical models** to predict a politician's likelihood of achieving a senior ministerial role.

---

## 👤 Author
**saharYaccov**
📂 **Project Path**: `portfolio/DashBoards/Data/Government Roles & Tenure in Israel/`
