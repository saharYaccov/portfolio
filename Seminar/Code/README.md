
# Text Processing and Clustering Analysis

This project involves loading data, processing text, and performing clustering analysis on text data. The script uses libraries such as `pandas`, `numpy`, `sklearn`, and `nltk` to process and analyze text data from CSV files.

## Features

- **Data Loading**: Load data from CSV files.
- **Text Vectorization**: Convert text data into vectors using TF-IDF.
- **Text Cleaning**: Remove stopwords from text data.
- **Clustering**: Use K-Means clustering to group similar text data.
- **Evaluation**: Evaluate clustering results using metrics like Silhouette Score, SSE, and others.
- **Visualization**: Visualize clustering results and metrics using `matplotlib` and `seaborn`.

## Dependencies

- pandas
- numpy
- matplotlib
- sklearn
- nltk
- seaborn

## Installation

Ensure you have Python installed on your system. You can install the required libraries using pip:

```bash
pip install pandas numpy matplotlib scikit-learn nltk seaborn
Usage


Load Data: Use the load_data function to load data from a CSV file.


Text Processing: Use the clear_stopWord function to remove stopwords from text data.


Vectorization: Use the create_vector_from_list function to convert text data into vectors.


Clustering: Use the kMean_model function to perform K-Means clustering on the vectorized text data.


Evaluation: Use the evaluate_clustering function to evaluate the clustering results.


Visualization: Use matplotlib and seaborn to visualize the clustering results and metrics.


Example
 Copyimport numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns

# Download stopwords
nltk.download('stopwords')

def load_data(path):
    data = pd.read_csv(path)
    return data

def create_vector_from_list(col_values):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(col_values)
    return X.toarray()

def clear_stopWord(col_val):
    stop_words = set(stopwords.words('english'))
    filtered_text = [word for word in col_val if word not in stop_words]
    return " ".join(filtered_text)

# Example usage
data = load_data('path_to_your_csv_file.csv')
text_col = 'reviews.title'
rating_col = 'reviews.rating'

df = data[[rating_col, text_col]].dropna(subset=[text_col])
df = df[df[rating_col] <= 3]

cur_col_title = df[text_col]
cur_col_rating = df[rating_col]

# Process text data
processed_text = [clear_stopWord(text.split()) for text in cur_col_title]
vectors = create_vector_from_list(processed_text)

# Perform clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(vectors)

# Evaluate clustering
sse = kmeans.inertia_
silhouette_avg = silhouette_score(vectors, kmeans.labels_)
db_index = davies_bouldin_score(vectors, kmeans.labels_)
ch_index = calinski_harabasz_score(vectors, kmeans.labels_)

print(f"SSE: {sse}")
print(f"Silhouette Score: {silhouette_avg}")
print(f"Davies-Bouldin Index: {db_index}")
print(f"Calinski-Harabasz Index: {ch_index}")

# Visualize clustering results
plt.scatter(vectors[:, 0], vectors[:, 1], c=kmeans.labels_, cmap='viridis')
plt.title('Clustering Results')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
Code Explanation
Data Loading
The load_data function loads data from a CSV file into a pandas DataFrame.
 Copydef load_data(path):
    data = pd.read_csv(path)
    return data
Text Processing
The clear_stopWord function removes stopwords from text data.
 Copydef clear_stopWord(col_val):
    stop_words = set(stopwords.words('english'))
    filtered_text = [word for word in col_val if word not in stop_words]
    return " ".join(filtered_text)
Vectorization
The create_vector_from_list function converts text data into vectors using TF-IDF.
 Copydef create_vector_from_list(col_values):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(col_values)
    return X.toarray()
Clustering
The kMean_model function performs K-Means clustering on the vectorized text data.
 Copydef kMean_model(n_class, new_ob, RandState):
    kmeans = KMeans(n_clusters=n_class, random_state=RandState)
    kmeans.fit(new_ob)
    sse = kmeans.inertia_
    silhouette_avg = silhouette_score(new_ob, kmeans.labels_)
    return kmeans, sse, silhouette_avg
Evaluation
The evaluate_clustering function evaluates the clustering results using metrics like Silhouette Score, SSE, and others.
 Copydef evaluate_clustering(X, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    sse = kmeans.inertia_
    silhouette_avg = silhouette_score(X, kmeans.labels_)
    db_index = davies_bouldin_score(X, kmeans.labels_)
    ch_index = calinski_harabasz_score(X, kmeans.labels_)
    return sse, silhouette_avg, db_index, ch_index
Visualization
The script uses matplotlib and seaborn to visualize the clustering results and metrics.
 Copyimport matplotlib.pyplot as plt
import seaborn as sns

# Visualize clustering results
plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap='viridis')
plt.title('Clustering Results')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

# Visualize metrics
sns.heatmap(sse_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
plt.xlabel('Clusters')
plt.ylabel('SSE')
plt.title('Heatmap of SSE for Different Number of Clusters')
plt.show()
Notes

Ensure all dependencies are installed before running the script.
The script can be extended to include additional text processing and clustering techniques.
The script uses sklearn for clustering and evaluation, which requires a significant amount of computational resources.

 CopyThis `README.md` provides an overview of the script, its main functions, usage instructions, and an example of how to run the script. You can copy this content into a `README.md` file in your project directory.
