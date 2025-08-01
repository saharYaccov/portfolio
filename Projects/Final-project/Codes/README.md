# Cybersecurity Prediction Project 🔐

This project leverages real-world data from Microsoft Security Bulletins (2001–2017) to predict cybersecurity attack events using advanced machine learning techniques.

---

## 📁 Repository Structure

This folder contains the core code and assets used in the final project:

| File/Folder | Description |
|-------------|-------------|
| `Bulletin Search (2001 - 2008).xlsx` | Microsoft Security Bulletin data from 2001 to 2008 |
| `Bulletin Search (2008 - 2017).xlsx` | Microsoft Security Bulletin data from 2008 to 2017 |
| `read_data.py` | Loads and preprocesses the raw Excel files |
| `Data_understanding.py` | Exploratory Data Analysis (EDA) and data profiling |
| `Impute.py` | Missing value handling and feature engineering |
| `Plots.py` | Visualization of data distributions and insights |
| `SQL.py` | Functions for saving or interacting with a database |
| `Models.py` | Training multiple machine learning models, including CatBoost |
| `my_catboost_model.cbm` | Pre-trained CatBoost model file |
| `Html_gradio.py` | Gradio-based web interface for model inference |
| `קישור לקוד Microsoft Security.pdf` | PDF with direct link and explanation of the GitHub repository |
| `README.md` | This file - brief project description and navigation |
| `readMe.md` | Alternate README format (deprecated) |

---

## 🔗 Run the Project Online

Run the full pipeline directly on Google Colab:  
[Click here to open in Colab](https://colab.research.google.com/drive/1_VcG-HvtXihENWJ1fWx-U91AwFp6KmUR?usp=sharing)

---

## 🧠 Models Used

The following machine learning algorithms were tested and evaluated:
- CatBoost (main deployed model)
- Random Forest
- XGBoost
- LightGBM
- Extra Trees
- AdaBoost
- Neural Network
- TabNet
- QDA

---

## 📊 Goals

- Clean and merge Microsoft vulnerability data
- Perform deep feature engineering
- Train and compare multiple ML models
- Predict whether a vulnerability is likely to lead to a cyberattack
- Create a web UI using Gradio for user interaction

---

## 👨‍💻 Author

**Sahar Yaakov**  
Third-year Information Systems student  
Max Stern Yezreel Valley College  
GitHub: [ss331144](https://github.com/ss331144)

---
