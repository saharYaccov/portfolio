# Fake or Real: The Impostor Hunt

A machine learning project to classify articles as fake or real using various text analysis techniques and models.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Kaggle notebook](#Kaggle-notebook)
- [Require Package](#Require-Package)
- [Models](#models)
- [Results](#results)
- [Images](#Image)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This project aims to distinguish between fake and real articles using text analysis and machine learning models. The project leverages various techniques such as TF-IDF vectorization, clustering, and classification algorithms to achieve this goal.

[LeaderBoard : 0.319 ](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/leaderboard)

## Features

- Text preprocessing and cleaning
- TF-IDF vectorization
- Word cloud generation
- Clustering using KMeans
- Classification using RandomForest, XGBoost, LightGBM, ExtraTrees, and Neural Networks
- Hyperparameter tuning with Optuna
- Evaluation and visualization of results

## Installation

To get started with this project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/fake-or-real-the-impostor-hunt.git
cd fake-or-real-the-impostor-hunt
pip install -r requirements.txt
```
## Usage

Data Preparation: Ensure your data is in the correct format and placed in the appropriate directories.
Text Preprocessing: Run the text preprocessing scripts to clean and prepare the text data.
Feature Extraction: Use TF-IDF vectorization to convert text data into numerical features.
Model Training: Train the machine learning models using the provided scripts.
Evaluation: Evaluate the models and visualize the results.

## Data
The dataset used in this project consists of articles labeled as fake or real. The data is preprocessed and vectorized using TF-IDF.
ColumnDescriptionidUnique identifier for each articlereal_text_idIdentifier for the real text in the article pairtextThe content of the article
Models
The project uses several machine learning models for classification:

## Kaggle-notebook
[Kaggle Notebook](https://www.kaggle.com/code/saharhaimyaccov/notebookcc02f1c748)
## Require-Package

| Library and Version | Description |
|---------------------|-------------|
| numpy>=1.21.0 | Fundamental package for scientific computing with Python, providing support for arrays and matrices. |
| pandas>=1.3.0 | Data manipulation and analysis library offering data structures and operations for manipulating numerical tables and time series. |
| scikit-learn>=0.24.0 | Machine learning library for Python, featuring various classification, regression, and clustering algorithms. |
| matplotlib>=3.4.0 | Comprehensive library for creating static, animated, and interactive visualizations in Python. |
| wordcloud>=1.8.0 | Library for generating word clouds, visual representations of text data. |
| joblib>=1.0.0 | Library for running Python functions as pipeline jobs, useful for parallelizing computations. |
| xgboost>=1.4.0 | Optimized distributed gradient boosting library, designed to be highly efficient, flexible, and portable. |
| lightgbm>=3.2.0 | Fast, distributed, high-performance gradient boosting framework based on decision tree algorithms. |
| tensorflow>=2.6.0 | Open-source platform for machine learning, providing a comprehensive ecosystem of tools, libraries, and community resources. |
| optuna>=2.10.0 | Hyperparameter optimization framework to automate hyperparameter search. |
| kagglehub>=0.1.0 | Library for interacting with Kaggle datasets and competitions directly from Python. |




## RandomForest
XGBoost
LightGBM
ExtraTrees
Neural Networks

## Results
The results of the classification models are evaluated based on accuracy and other performance metrics. The best model and its parameters are saved for future use.
ModelAccuracyRandomForest0.95XGBoost0.94LightGBM0.96ExtraTrees0.93Neural Network0.92

## Image

### Data
![data](https://github.com/user-attachments/assets/776996e3-1aab-473c-b329-ec22bfb617c3)

### word cloud TRUE article 1 
![word cloud true article 1](https://github.com/user-attachments/assets/8108583f-74d6-49cf-9e04-2c090be9376a)

### word cloud FAKE article 1 
![word cloud fake article 1](https://github.com/user-attachments/assets/a88c6c05-34b7-4f04-931b-16512a79127f)

### KPI vectores
![KPI vectors](https://github.com/user-attachments/assets/7a7d5fcc-520f-4726-aab9-74c39d5b477d)

###Optuna model
![Optuna model](https://github.com/user-attachments/assets/0670d72c-6738-4900-8a47-4182ae950456)


## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
Contact



For any questions or feedback, please contact:
Sahar Yaccov
[Contact via Email](mailto:saharyaccov@gmail.com)
