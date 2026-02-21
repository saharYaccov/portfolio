# 🎓 Global Female vs Male Academic Performance Dashboard (Tableau)

---

## 📊 Dashboard Previews

![Dashboard Preview 1](Image/image_1.jpeg)
*Preview 1: Global gender-based academic performance overview.*

![Dashboard Preview 2](Image/image_2.jpeg)
*Preview 2: Regional performance comparison.*

![Dashboard Preview 3](Image/image_3.jpeg)
*Preview 3: Country-specific gender gap analysis.*

![Dashboard Preview 4](Image/image_4.jpeg)
*Preview 4: Longitudinal trends in academic metrics.*

---

## 🧠 Overview

The **Global Female vs Male Academic Performance Dashboard** provides a **data-driven analysis** of academic performance differences between genders across countries and regions. This project integrates **statistical analysis, data preprocessing, and interactive visualization** to explore global education trends.

The dashboard is designed for **researchers, analysts, policymakers, and data enthusiasts** seeking to understand patterns in academic achievement.

### Key Insights
- Gender-based academic performance comparisons
- Cross-country educational metrics
- Regional disparities and global trends
- Longitudinal patterns in academic indicators

---

## 🎯 Project Objectives

- Identify performance gaps between female and male students.
- Compare academic outcomes across countries and regions.
- Detect global and regional trends in educational metrics.
- Provide clear, interactive visual storytelling for decision-makers.

---

## 🔧 Key Features

### 📌 Interactive Filtering
- Filter by **country, region, or academic indicator**.
- Drill down into **specific comparisons**.
- Explore **dynamic breakdowns by gender**.

### 📊 Comparative Visualizations
- Side-by-side gender comparisons.
- Distribution analysis across countries.
- Trend-based insights over time.

### 🌍 Global Perspective
- Cross-country performance mapping.
- Identification of high-performing and low-performing regions.
- Regional clustering insights.

### 📈 Statistical Integration
- Data cleaning and preprocessing using **Python (Pandas, NumPy)**.
- Structured datasets prepared in **CSV/Excel** format.
- Aggregations and calculated fields implemented in **Tableau**.

---

## 🛠 Tools & Technologies
   Tool/Technology          | Purpose                                                                 |
 |-------------------------|-------------------------------------------------------------------------|
 | **Tableau Desktop/Public** | Dashboard creation and interactive visualization.                     |
 | **Python (Pandas, NumPy)** | Data preprocessing, cleaning, and transformation.                    |
 | **Excel / CSV**          | Structured academic datasets.                                          |
 | **Statistical Analysis** | Comparative metrics and aggregated indicators.                       |

---

## 📂 Project Structure

```bash
portfolio/DashBoards/Tableau/Globlal-Fe.Male-Academic/
├── Data/
│   ├── 2020-2026_uns_rnk.csv
│   └── 2020-2026_uns_rnk.xlsx
│
├── Image/
│   ├── image_1.jpeg
│   ├── image_2.jpeg
│   ├── image_3.jpeg
│   └── image_4.jpeg
│
├── Python_Analysis/
│   ├── class_uns.py
│   └── run_class_uns.py
│
├── Globlal Fe.Male Academic.twb
└── README.md


📊 Analytical Use Cases
🎓 Academic Research

Study gender-based performance gaps.
Identify educational inequality patterns.
Support policy analysis.
🏛 Policy & Decision Making

Assist governments and institutions in evaluating gender parity.
Highlight regions requiring educational intervention.
Provide evidence-based insights for funding allocation.
📈 Data Science Portfolio

Demonstrates:

Data preprocessing workflow
Statistical comparison techniques
Business intelligence storytelling
Clean dashboard design principles


🔍 Methodology Summary

Data Collection: Structured academic datasets from 2020-2026.
Cleaning & Normalization: Using Python (Pandas, NumPy).
Aggregation: Gender-based indicators and regional metrics.
Visualization: Import into Tableau for interactive dashboards.
Analysis: Comparative and trend-based insights.

💻 Python Code
class_uns.py
python
Copy

import pandas as pd
import numpy as np

class AcademicDataProcessor:
    """
    A class to process academic performance data.
    Handles cleaning, normalization, and aggregation of gender-based metrics.
    """
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def clean_data(self):
        """Remove duplicates, handle missing values, and normalize columns."""
        self.data.drop_duplicates(inplace=True)
        self.data.fillna(method='ffill', inplace=True)
        return self.data

    def aggregate_by_gender(self):
        """Aggregate academic metrics by gender."""
        return self.data.groupby('gender').mean()

run_class_uns.py
python
Copy

from class_uns import AcademicDataProcessor

def main():
    # Initialize data processor
    processor = AcademicDataProcessor("Data/2020-2026_uns_rnk.csv")

    # Clean and aggregate data
    cleaned_data = processor.clean_data()
    aggregated_data = processor.aggregate_by_gender()

    # Save processed data
    cleaned_data.to_csv("Data/cleaned_academic_data.csv", index=False)
    aggregated_data.to_csv("Data/aggregated_gender_metrics.csv")

if __name__ == "__main__":
    main()


📌 Notes

The dashboard file is provided as .twb (Tableau Workbook).
Requires Tableau Desktop or Tableau Public for interactive exploration.
Ensure data sources in the Data/ folder are correctly connected if opening locally.
Python scripts in Python_Analysis/ contain preprocessing logic used before visualization.

🚀 Future Improvements

Integration of predictive modeling for academic trend forecasting.
Inclusion of additional years and countries.
Deployment to Tableau Public with live updates.
Expanded statistical benchmarking.

👤 Author
saharYaccov
Data Analyst | Information Systems | Machine Learning & BI
📂 Project Path:
portfolio/DashBoards/Tableau/Globlal-Fe.Male-Academic/


This project highlights the power of combining statistical thinking, clean data engineering, and visual storytelling to uncover meaningful global insights.










