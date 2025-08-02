# Fake or Real: The Impostor Hunt

A machine learning project to classify articles as fake or real using various text analysis techniques and models.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Require Package](#Require Package)
- [Models](#models)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This project aims to distinguish between fake and real articles using text analysis and machine learning models. The project leverages various techniques such as TF-IDF vectorization, clustering, and classification algorithms to achieve this goal.

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

## Require Package
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=0.24.0
matplotlib>=3.4.0
wordcloud>=1.8.0
joblib>=1.0.0
xgboost>=1.4.0
lightgbm>=3.2.0
tensorflow>=2.6.0
optuna>=2.10.0
kagglehub>=0.1.0


## RandomForest
XGBoost
LightGBM
ExtraTrees
Neural Networks

## Results
The results of the classification models are evaluated based on accuracy and other performance metrics. The best model and its parameters are saved for future use.
ModelAccuracyRandomForest0.95XGBoost0.94LightGBM0.96ExtraTrees0.93Neural Network0.92

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
Contact



For any questions or feedback, please contact:
Sahar Yaccov
[Contact via Email](mailto:saharyaccov@gmail.com)
