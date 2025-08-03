# NeurIPS - Open Polymer Prediction 2025

Predicting polymer properties with machine learning to accelerate sustainable materials research.

---

## Overview

Polymers are essential building blocks in many fields such as medicine, electronics, and sustainability. This competition challenges participants to predict five key physical and chemical properties of polymers based solely on their chemical structure represented as SMILES strings.

The dataset provided is one of the largest open-source polymer datasets ever, enabling breakthroughs in sustainable materials research.

---

## Challenge Description

Your task is to build models that accurately predict the following polymer properties:

- **Density**  
- **Glass Transition Temperature (Tg)**  
- **Thermal Conductivity (Tc)**  
- **Radius of Gyration (Rg)**  
- **Fractional Free Volume (FFV)**  

The ground truth values are averaged from multiple molecular dynamics simulation runs.

---

## Evaluation Metric

The competition uses a **weighted Mean Absolute Error (wMAE)** across the five properties, calculated as:

\[
\text{wMAE} = \frac{1}{|P|} \sum_{p \in P} \sum_{t \in T} w_t \cdot |y_{p,t} - \hat{y}_{p,t}|
\]

where:  
- \(P\) = set of polymers  
- \(T\) = set of property types  
- \(y_{p,t}\) = true value of property \(t\) for polymer \(p\)  
- \(\hat{y}_{p,t}\) = predicted value  
- \(w_t\) = weight for property \(t\) (based on data distribution and range)

The weights normalize the impact of each property, ensuring fair contribution regardless of scale or rarity.

---

## Submission File Format

Submit a CSV file named `submission.csv` with the following format:

