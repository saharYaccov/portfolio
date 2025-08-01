https://huggingface.co/spaces/sahar-yaccov/Microsoft-Attack
# 🛡️ Microsoft Attack Prediction App – Hugging Face Space

A machine learning web application that predicts cybersecurity attack events using real-world Microsoft security data, based on over 23,000 records and 43 features.

🔗 **Live Demo**: [Microsoft-Attack on Hugging Face Spaces](https://huggingface.co/spaces/sahar-yaccov/Microsoft-Attack)

---

## 📊 Project Overview

This app is the final project for the **Information Systems B.Sc.** program at **Max Stern Yezreel Valley College**, developed by **Sahar Yaakov**.

The project uses real Microsoft vulnerability reports and attack event records to train several machine learning models and forecast potential threats. The interface allows users to explore how specific features affect predictions and interact with different model results.

---

## 🚀 Features

- ✅ Uses real Microsoft security update data (~23K rows)
- 🤖 Multiple ML models: CatBoost, LightGBM, Random Forest, etc.
- 🧪 Model selection and evaluation using Optuna
- 📉 Prediction interface for user input
- 📈 Visual dashboard and results plots
- 🌐 Deployed on Hugging Face Spaces using **Gradio**

---

## 🧠 Models Used

- CatBoostClassifier
- LightGBMClassifier
- RandomForestClassifier
- ExtraTreesClassifier
- AdaBoostClassifier
- Neural Networks (MLP)
- TabNet
- QDA

All models were trained and evaluated using a consistent pipeline and were compared based on prediction accuracy, distance from ground truth, and robustness.

---

## 🛠️ Tech Stack

- **Python**
- **scikit-learn**, **Optuna**, **CatBoost**, **LightGBM**, **XGBoost**, **TabNet**
- **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**
- **Gradio** for web UI
- **Hugging Face Spaces** for deployment

---

## 📁 Directory Structure

