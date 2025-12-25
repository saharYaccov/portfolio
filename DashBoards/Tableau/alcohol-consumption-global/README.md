# Global Alcohol Data Dashboard – Analytics Command Center (Tableau)

<img width="1481" height="700" alt="image" src="https://github.com/saharYaccov/portfolio/blob/main/DashBoards/Tableau/alcohol-consumption-global/image/image_1.png" />

<img width="1484" height="680" alt="image" src="https://github.com/saharYaccov/portfolio/blob/main/DashBoards/Tableau/alcohol-consumption-global/image/image_2.png" />

---

<img width="1454" height="702" alt="image" src="https://github.com/saharYaccov/portfolio/blob/main/DashBoards/Tableau/alcohol-consumption-global/image/image_3.png" />

<img width="1472" height="686" alt="image" src="https://github.com/saharYaccov/portfolio/blob/main/DashBoards/Tableau/alcohol-consumption-global/image/image_4.png" />

---


[Open Tableau Dashboard Alcohol Type](https://public.tableau.com/app/profile/sahar.yacoov/viz/alcoholtypes/Dashboard1?publish=yes)

[Open Tableau Dashboard Alcohol By Gender](https://public.tableau.com/app/profile/sahar.yacoov/viz/alcoholbygender/Dashboard1)

---

## 🧠 Overview

The **Global Alcohol Data Dashboard** provides a comprehensive, interactive view of **alcohol consumption across countries, beverage types, and demographic groups**.  
This dashboard is designed for **analysts, policymakers, and public health researchers** to explore global drinking patterns, monitor consumption levels, and identify trends over time.  

> **Important Note:** Before building the dashboard, multiple CSV datasets from the **WHO Global Information System on Alcohol and Health (GISAH)** were **cross-referenced and merged**, including both **data files** (consumption indicators) and **code files** (dimensions like country, gender, age group, beverage type). This step ensured consistency and enabled accurate multi-dimensional analysis.

Using Tableau’s visual analytics, users can make **data-driven decisions for public health interventions and policy planning**.

> **Important:** The **Value/NumericValue** in the datasets represents **alcohol consumption per capita in liters of pure alcohol**.

---

## 🔧 Features

- **Interactive Dashboards:** Filter by **country, year, gender, age group**, and **type of alcoholic beverage**.  
- **Rich Visualizations:** Bar charts, line graphs, pie charts, geographic maps, and trend analyses.  
- **KPI Tracking:** Monitor key metrics such as **average intake per capita, beverage-specific consumption, and unrecorded alcohol consumption**.  
- **Trend Analysis:** Detect emerging patterns and historical changes in drinking behavior.  
- **Cross-Platform Data Integration:** Combines multiple data sources including **CSV files from GISAH**, **Excel datasets**, and other national databases.

> **Data Preparation:**  
> - Datasets were initially in separate CSVs for each indicator.  
> - Code files provided mapping for **countries, beverage types, age groups, and gender**.  
> - Data merging, cleaning, and standardization were performed **before analysis**, including handling missing values and aligning time periods.

---

## 🛠 Tools & Technologies

- **Tableau Desktop / Tableau Public:** For creating interactive dashboards and visualizations.  
- **Calculated Fields & Parameters:** For building **custom KPIs** and advanced metrics.  
- **Data Connections:** Supports **CSV, Excel, SQL**, and other structured data sources.

---

## 📈 Use Cases

- **Public Health Monitoring:** Track alcohol consumption patterns across countries, ages, and gender.  
- **Policy Analysis:** Identify **high-risk populations** and beverage trends to guide interventions.  
- **Research & Reporting:** Provide actionable insights for researchers, health organizations, and governments.  
- **Trend Forecasting:** Analyze changes in consumption patterns over time to anticipate future public health challenges.

---

## 📌 Notes

- Requires **Tableau Desktop** or access to **Tableau Public**.  
- Dashboards are optimized for **interactive exploration**, filtering, and drill-down.  
- **Data sources should be refreshed regularly** to maintain up-to-date insights.  
- **Data integration steps are crucial**: without merging the indicator and code files correctly, visualizations may misrepresent values.

---

## 🔗 Additional Resources

- [WHO Global Information System on Alcohol and Health (GISAH)](https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/levels-of-consumption)

---

## ⚡ Summary of Data Processing Steps

1. **Download CSV datasets** from WHO GISAH (indicators and dimension codes).  
2. **Cross-reference** indicator data with dimension codes (countries, beverages, age, gender).  
3. **Merge datasets** into a unified table for Tableau import.  
4. **Clean and standardize data** (handle missing values, ensure consistent units).  
5. **Load into Tableau** and build interactive dashboards with filters, KPIs, and visualizations.  

> This preparation ensures that the dashboard reflects **accurate, multi-dimensional insights on global alcohol consumption**.
