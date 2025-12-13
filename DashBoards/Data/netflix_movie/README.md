# Netflix Movies Dataset & Dashboards

🧠 **Overview**  
This repository contains datasets and dashboards related to Netflix movies, focusing on revenue, ratings, popularity, and genre analysis.

The data enables exploration of:

- Movie metrics (budget, revenue, rating, popularity, genre, release year, language, etc.)
- Predictive models for movie revenue and ratings
- Aggregated insights across multiple years and genres

📊 **Data Files**

- `Features_all.csv` – Full dataset containing raw and processed movie-level features.  
- `Target_all.csv` – Target dataset containing revenue and rating values used for predictive modeling.  
- `all_datasets.xlsx` – Consolidated Excel file combining all datasets for easier exploration.  
- `process_df_remove_null.csv` – Processed dataset with missing/null values removed.  
- `total_df.csv` – Final merged dataset used for training and evaluation of models.

🔧 **Use Cases**

- **Interactive Dashboards**: Build BI dashboards in Tableau / Power BI / Plotly Dash.  
- **Predictive Analytics**: Train and test models (Gradient Boosting, Random Forest, CatBoost, etc.) on historical Netflix movie data.  
- **Exploratory Analysis**: Study trends in revenue, ratings, popularity, genres, and release years.  
- **Data Storytelling**: Present insights for movie analytics projects, reports, or entertainment platforms.  

📌 **Notes**

- All datasets are provided in CSV / Excel (XLSX) format for easy integration.  
- For reproducibility, ensure Python ≥ 3.10 with libraries: `pandas`, `scikit-learn`, `matplotlib`, `numpy`, `optuna`, `catboost`.  
- Prediction files are generated from models trained on movie-level features, including text statistics extracted from movie summaries.

🚀 **Future Work**

- Extend dataset with additional movies and streaming platforms.  
- Add temporal metrics like weekly streaming counts.  
- Integrate dashboards with live API feeds for real-time analysis and visualization.  

🌐 **Data Source**

All data was sourced from **[Deep Data Lake](https://deepdatalake.com/details.php?dataset_id=44)**.

👤 **Author**: Sahar Yacoov  
📂 **Project Path**: `portfolio/DashBoards/Data/netflix_movie/`
