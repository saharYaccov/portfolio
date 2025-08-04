## NeurIPS - Open Polymer Prediction 2025

A machine learning project to predict fundamental polymer properties from chemical structures using advanced models and feature engineering.

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Kaggle Notebook](#kaggle-notebook)
- [Required Packages](#required-packages)
- [Models](#models)
- [Images](#Images)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Introduction

This project aims to predict key physical and chemical properties of polymers, accelerating sustainable materials research. The dataset contains polymer chemical structures represented as SMILES strings, along with target properties derived from molecular simulations.

[LeaderBoard : 0.319](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/leaderboard)
---

## Features

- Chemical structure preprocessing and feature extraction (e.g., SMILES vectorization)  
- Regression modeling using various machine learning algorithms  
- Hyperparameter tuning with Optuna  
- Performance evaluation using weighted Mean Absolute Error (wMAE)  
- Visualization of results and feature importance

---

## Installation

Clone the repository and install dependencies:

``bash
git clone https://github.com/yourusername/open-polymer-prediction.git
cd open-polymer-prediction
pip install -r requirements.txt
``

## Usage
Prepare and preprocess the polymer data.

Extract features from SMILES strings.

Train regression models with the provided scripts.

Evaluate performance and generate submission files.

## Data
The dataset includes:

## Column	Description
id	Unique polymer identifier
smiles	Polymer chemical structure (SMILES string)
Tg	Glass transition temperature
FFV	Fractional free volume
Tc	Thermal conductivity
Density	Polymer density
Rg	Radius of gyration

## Kaggle Notebook
You can find the main notebook for this competition here.

## Required Packages

| Library    | Version / Notes                              | Description                                   |Link                                                    |
|------------|---------------------------------------------|-----------------------------------------------|---------------------------------------------------------|
| rdkit-pypi | Install via pip or download wheel from link | Computational chemistry library for molecule analysis and cheminformatics | [rdkit-pypi](https://www.kaggle.com/datasets/jainam213/rdkit-wheels?utm_source=chatgpt.com)|
| numpy      | No specific version here, commonly >=1.21.0 | Numerical computing with arrays and matrices  |                                                          |
| pandas     | No specific version here, commonly >=1.3.0  | Data manipulation and analysis with tables    |                                                          |
| os         | Built-in Python module                       | Operating system interfaces and file management |                                                        |

---
[rdkit-pypi](https://www.kaggle.com/datasets/jainam213/rdkit-wheels?utm_source=chatgpt.com)

## Installing RDKit on Kaggle

```bash
!pip install rdkit-pypi

# Important:
# You need to download the wheel file from:
# https://www.kaggle.com/datasets/jainam213/rdkit-wheels?utm_source=chatgpt.com
# !!

!pip install /kaggle/input/rdkit-library/rdkit-2025.3.3-cp311-cp311-manylinux_2_28_x86_64.whl
```
## Images

### Data
![Data](https://github.com/user-attachments/assets/879c242e-3c60-4ab1-9c12-81dd0b2eca9e)

### Scatter
![Scatter](https://github.com/user-attachments/assets/fb5c1efa-c663-4e15-aa1b-eeebe71f26f1)

### TC by ID (Bar)
![TC by ID](https://github.com/user-attachments/assets/9c004cff-5ad5-4725-862a-4b94edbfa5bd)

### Models Comparison
![Models](https://github.com/user-attachments/assets/95a3fe27-710c-4643-b42d-11729d12ef53)

### Scatter & KMeans of 2 Targets
![Scatter & KMeans](https://github.com/user-attachments/assets/3f6d82b9-7cdb-46ee-a286-c7f33aabf730)

### Prediction Model - SVR
![Prediction model SVR](https://github.com/user-attachments/assets/59603810-ee99-4e66-9f13-2042de7e05bc)

## Models
RandomForest

XGBoost

LightGBM

ExtraTrees

Neural Networks

## Results
Model	Validation Score (wMAE)
RandomForest	0.95
XGBoost	0.94
LightGBM	0.96
ExtraTrees	0.93
Neural Network	0.92

## Contributing
Contributions are welcome! Please fork the repo, create a branch, and open a pull request with your changes. Follow the project's coding style and include tests where appropriate.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or feedback, contact:
Sahar Yaccov
[Email](saharyaccov@gmail.com)

NeurIPS Open Polymer Prediction 2025 - University of Notre Dame

אם תרצה שאעזור לייצר את קובץ ה־requirements.txt או כל קוד אחר לפרויקט, תגיד!
