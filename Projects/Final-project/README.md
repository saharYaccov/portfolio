# 🛡️ Final Project – Cybersecurity Prediction

This project aims to predict future cybersecurity threat events based on real Microsoft security data using advanced machine learning algorithms and an end-to-end ML pipeline.

## 📂 Repository Structure

Projects/
└── Final-project/
├── App-hugging/ # Deployed demo app on Hugging Face Spaces
├── Codes/ # Source code: preprocessing, modeling, evaluation
├── Dashboards/ # Visual dashboards (e.g., Tableau, Power BI)
├── Reports/ # Project documentation & PDF reports
└── README.md # Project overview

yaml
Copy
Edit

---

## 📌 Project Overview

- 🔐 **Domain**: Cybersecurity Event Prediction  
- 🧠 **Tech Stack**: Python, scikit-learn, CatBoost, XGBoost, Optuna, Gradio, Tableau, Power BI  
- 📊 **Data Source**: Real Microsoft security data (~23,000 records, 43 features)  
- ⚙️ **Tasks**: Data cleaning, feature engineering, model selection, optimization, deployment  

---

## 📁 Folders Breakdown

### 📁 [App-hugging](./App-hugging/)
A Hugging Face [Gradio App](https://huggingface.co/spaces/ss331144/Cyber-Predictor) for interactive model predictions.

### 📁 [Codes](./Codes/)
Includes full Python source code:
- `preprocessing.py`: Data cleaning & transformation
- `modeling.py`: Model training & evaluation
- `optuna_tuning.py`: Hyperparameter optimization
- `main_pipeline.py`: Integrated ML pipeline

### 📁 [Dashboards](./Dashboards/)
Visualizations and interactive dashboards:
- Tableau dashboards for KPI monitoring
- Correlation and feature analysis

### 📁 [Reports](./Reports/)
Downloadable PDF documentation:
- 📄 2 - Data Understanding (EDA)
- 📄 3 - Data Preparation
- 📄 4 - Modeling Report
- 📄 5 - Model Evaluation
- 📄 6 - Deployment Report
- 📄 Business Report

---

## 🧪 Models Used

- ✅ CatBoost Regressor  
- ✅ LightGBM  
- ✅ Extra Trees  
- ✅ XGBoost  
- ✅ Random Forest  
- ✅ Neural Network (MLP)  
- ✅ TabNet  
- ✅ AdaBoost  
- ✅ QDA (Quadratic Discriminant Analysis)

All models were evaluated on the same preprocessed data using consistent metrics and visual diagnostics.

---

## 📤 Deployment

Deployed with **Gradio** via Hugging Face Spaces  
▶️ [Launch the app](https://huggingface.co/spaces/ss331144/Cyber-Predictor)

---

## 📧 Contact

**Sahar Yaakov**  
Third-year Information Systems student  
[Yezreel Valley College](https://www.yvc.ac.il)  
GitHub: [@ss331144](https://github.com/ss331144)

---

> © 2025 Sahar Yaakov – All rights reserved.


