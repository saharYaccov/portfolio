#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd


# In[3]:


# load file
labels_df = pd.read_csv('/kaggle/input/fake-or-real-the-impostor-hunt/data/train.csv')

text_true = [] 
text_fake = []

# for any article in file
for i, row in labels_df.iterrows():
    article_id = row['id']  # לדוגמה: article_0000
    real_id = row['real_text_id']   # 1 או 2
    str_article_id = 'article_' + str(i).zfill(4)  # ==> 'article_0005'

    #the pathes pf  articales
    file1_path = f'/kaggle/input/fake-or-real-the-impostor-hunt/data/train/{str_article_id}/file_1.txt'
    file2_path = f'/kaggle/input/fake-or-real-the-impostor-hunt/data/train/{str_article_id}/file_2.txt'

    
    #read texts
    with open(file1_path, 'r', encoding='utf-8') as f1:
        text1 = f1.read()

    with open(file2_path, 'r', encoding='utf-8') as f2:
        text2 = f2.read()

    #save file by true or fake
    if real_id == 1:
        text_true.append(text1)
        text_fake.append(text2)
    else:
        text_true.append(text2)
        text_fake.append(text1)

    # 94 files exists
    if i == 94:
        break


# In[29]:


print(f"🟢 Real texts count: {len(text_true)}")
print(f"🔴 Fake texts count: {len(text_fake)}")

import re

def clean_and_split(text):
    #Return lowercase words from text without punctuation.
    return re.findall(r'\b\w+\b', text.lower())

zero_pair_text_in_file = []
min_len = min(len(text_true), len(text_fake))


for i in range(len(text_true)):
    true_words = clean_and_split(text_true[i])
    fake_words = clean_and_split(text_fake[i])
    both_words = [word for word in true_words if word in fake_words]
    if (len(both_words) == 0 ):
        zero_pair_text_in_file.append(i+1)
        print(f'🔎 Pair {i+1}: {len(both_words)}' )


if zero_pair_text_in_file:
    print(f"\n😶 No common words found in {len(zero_pair_text_in_file)} pairs: {zero_pair_text_in_file}")
else:
    print("\n🎉 All pairs have at least one common word!")


# In[32]:


df = pd.DataFrame({'True': text_true,'Fake': text_fake}) 


# In[33]:


df.head()


# In[39]:


from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(text):
    """
    Generates and displays a word cloud from the given text.

    Args:
        text (str): The input text to visualize.
    """
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("☁️ Word Cloud", fontsize=16)
    plt.show()

for num_df_file in [0,1]:
    if num_df_file == 0:
        print(f"🚀 {'-'*20} detect for True file {'-'*20}")
    else:
        print(f"🚨 {'-'*20} detect for Fake file {'-'*20}")
    for i in range(10):
        print(f'⏱️ file {i}')
        sample_text = df.iloc[i, num_df_file]  # שורה i, עמודה 0
        print(f"🌟 Word Cloud for row {i+1}")
        generate_wordcloud(sample_text)



# In[40]:


from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump, load
def create_vector_from_list(col_values):
    # create vector from texts
    vectorizer = TfidfVectorizer(stop_words='english')  # auto stop word
    X = vectorizer.fit_transform(col_values)
    X = X.toarray()
    dump(vectorizer, 'vectorizer.joblib')
    return X ,vectorizer,vectorizer.get_feature_names_out()
all_texts = list(text_true) + list(text_fake)  # כל הטקסטים ביחד
vectors_all, vectorizer_all, feature_names_all = create_vector_from_list(all_texts)
vectors_t = vectors_all[:len(text_true), :]
vectors_f = vectors_all[len(text_true):, :]


# In[158]:


print(len(vectorizer_all.get_feature_names_out()))


# In[79]:


len(vectors_t)


# In[41]:


df_all_txt = pd.DataFrame(vectors_all)
print(f"🧐 Total missing values (NaN) in dataframe: {df_all_txt.isnull().sum().sum()} ❌")


# In[163]:


print(df_all_txt.head(2))
# שיטה 1: הדפסת מספר העמודות
print(len(df_all_txt.columns))

# שיטה 2: הדפסת הצורה (מספר שורות, מספר עמודות)
print(df_all_txt.shape)  # התוצאה: (rows, columns)


# In[42]:


df_all_txt.describe()


# In[44]:


df_vec_t_f = df_all_txt
print(f"🔎 Total missing values (NaN) in dataframe: {df_vec_t_f.isnull().sum().sum()} ❌")


df_vectors_t_mean = pd.DataFrame(np.mean(vectors_t, axis=1), columns=['mean_vector_t'])
df_vectors_t_std = pd.DataFrame(np.std(vectors_t, axis=1), columns=['std_vector_t'])
df_vectors_f_mean = pd.DataFrame(np.mean(vectors_f, axis=1), columns=['mean_vector_f'])
df_vectors_f_std = pd.DataFrame(np.std(vectors_t, axis=1), columns=['std_vector_f'])

df_true = pd.DataFrame({
    'mean_vector': df_vectors_t_mean['mean_vector_t'],
    'std_vector': df_vectors_t_std['std_vector_t'],
    'label': 'true'
})

df_fake = pd.DataFrame({
    'mean_vector': df_vectors_f_mean['mean_vector_f'],
    'std_vector': df_vectors_f_std['std_vector_f'],
    'label': 'fake'
})

df_vec_t_f_mean = pd.concat([df_true, df_fake], axis=0).reset_index(drop=True)


print(f"🧐 Total missing values (NaN) in dataframe mean: {df_vec_t_f.isnull().sum().sum()} ❌")
print(df_vec_t_f_mean.iloc[[20,25,34, 40, 102,112,122, 129]])


# In[156]:


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2, n_init=10, random_state=42)
kmeans.fit(df_all_txt)
df_vec_t_f['cluster'] = kmeans.labels_

print(df_vec_t_f.shape)


# In[157]:


print("Number of iterations run:", kmeans.n_iter_)
print("Number of clusters:", kmeans.n_clusters)
print("Random state:", kmeans.random_state)


import matplotlib.pyplot as plt

def plot_clusters(df, kmeans, normalize=True):
    """
    Plot the clustered data points in 2D with cluster centers.
    
    Args:
        df (pd.DataFrame): Original DataFrame of features.
        kmeans: Fitted KMeans model.
        normalize (bool): Whether the data was normalized (to plot in scaled space).
    """
    if normalize:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X = scaler.fit_transform(df)
    else:
        X = df.values

    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    plt.figure(figsize=(8,6))
    scatter = plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.6)
    plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=200, label='Centers')

    plt.title('KMeans Clusters')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.show()

# שימוש לדוגמה:
plot_clusters(new_df, k_mean_model_1)


# In[98]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_and_evaluate_random_forest(X, y, test_size=0.2, random_state=42):
    """
    מאמן מודל RandomForestClassifier ומחזיר את דיוק המודל על קבוצת הבדיקה

    פרמטרים:
    - X: numpy array או DataFrame של מאפיינים
    - y: numpy array או סדרה של תוויות (מספריות)
    - test_size: חלק הנתונים שישמש לבדיקה (ברירת מחדל 0.2)
    - random_state: מספר לזרע אקראי (ברירת מחדל 42)

    מחזיר:
    - accuracy: דיוק המודל על קבוצת הבדיקה (float)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

from xgboost import XGBClassifier

def train_xgboost(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=random_state)
    model.fit(X_train, y_train)
    return accuracy_score(y_test, model.predict(X_test))

from lightgbm import LGBMClassifier

def train_lightgbm(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    model = LGBMClassifier(random_state=random_state)
    model.fit(X_train, y_train)
    return accuracy_score(y_test, model.predict(X_test))

from sklearn.ensemble import ExtraTreesClassifier

def train_extra_trees(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    model = ExtraTreesClassifier(n_estimators=100, random_state=random_state)
    model.fit(X_train, y_train)
    return accuracy_score(y_test, model.predict(X_test))

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

def train_neural_net(X, y, test_size=0.2, random_state=42, epochs=20, batch_size=32):
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

    model = Sequential([
        Dense(64, activation='relu', input_shape=(X.shape[1],)),
        Dense(32, activation='tanh'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    return accuracy_score(y_test, y_pred)




# In[99]:


from sklearn.preprocessing import LabelEncoder
X = df_vec_t_f_mean.drop(columns = 'label')
y = df_vec_t_f_mean['label']
# יצירת מקודד והמרה
le = LabelEncoder()
y_encoded = le.fit_transform(y)

accuracy = train_lightgbm(X, y_encoded)
print(f"🎯 Cross-validated Accuracy: {accuracy:.4f}")


# In[100]:


import numpy as np
import pandas as pd
from scipy.stats import entropy


def sigmoid_entropy_like(arr):
    s = np.sum(arr)
    # חישוב סיגמואיד: 1 / (1 + e^(-s))
    return 1 / (1 + np.exp(-s))


# חישוב אנטרופיה לכל שורה במטריצה (ווקטורים טקסט אמיתיים)
entropies_t = np.array([sigmoid_entropy_like(row) for row in vectors_t])

df_vectors_t_stats = pd.DataFrame({
    'mean_vector': np.mean(vectors_t, axis=1),
    'std_vector': np.std(vectors_t, axis=1),
    'var_vector': np.var(vectors_t, axis=1),
    'median_vector': np.median(vectors_t, axis=1),
    'entropy_vector': entropies_t,
    'label': 'true'
})

# חישוב אנטרופיה לכל שורה במטריצה (ווקטורים טקסט מזויפים)
entropies_f = np.array([sigmoid_entropy_like(row) for row in vectors_f])

df_vectors_f_stats = pd.DataFrame({
    'mean_vector': np.mean(vectors_f, axis=1),
    'std_vector': np.std(vectors_f, axis=1),
    'var_vector': np.var(vectors_f, axis=1),
    'median_vector': np.median(vectors_f, axis=1),
    'entropy_vector': entropies_f,
    'label': 'fake'
})

# איחוד טבלאות True ו-Fake
df_stats = pd.concat([df_vectors_t_stats, df_vectors_f_stats], axis=0).reset_index(drop=True)

print(df_stats.head())


# In[101]:


from itertools import combinations

metrics = [
    'mean_vector',    # ממוצע
    'std_vector',     # סטיית תקן
    'median_vector',  # חציון
    'var_vector',     # שונות
    'entropy_vector'
]
label_col = 'label'

all_combinations = []

for r in range(1, len(metrics)+1):  # 1 עד כל המדדים
    combs = list(combinations(metrics, r))
    for comb in combs:
        cols = list(comb) + [label_col]
        df_subset = df_stats[cols]
        all_combinations.append((comb, df_subset))

for i in all_combinations:
    print(i[0])


# In[102]:


df_stats


# In[103]:


# הגדרת הפונקציות לכל מודל
model_funcs = {
    'RandomForest': train_and_evaluate_random_forest,
    'XGBoost': train_xgboost,
    'LightGBM': train_lightgbm,
    'ExtraTrees': train_extra_trees,
    'NeuralNetwork':train_neural_net,
}

# מאגר התוצאות הסופי
overall_results = {}

# בחירת פיצ'רים
selected_features = ['mean_vector'	,'std_vector'	,'var_vector',	'median_vector'	,'entropy_vector']  # תוכל להוסיף: 'vector_variance', וכו'

# הכנת X ו-y
X = df_stats[selected_features]
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df_stats['label'])  # עכשיו y יהיה [0, 1]

# הרצת כל מודל פעם אחת בלבד
for model_name, func in model_funcs.items():
    print(f"\n🚀 Evaluating model: {model_name}")
    
    # הרצת המודל
    accuracy = func(X, y)  # הפונקציה שלך מחזירה את הדיוק (float)

    # שמירת תוצאה
    overall_results[model_name] = {
        'accuracy': accuracy,
        'features': selected_features
    }

    print(f"✅ Model: {model_name} | Accuracy: {accuracy:.4f}")

# סיכום כולל
print("\n🎯 Summary of Results:")
for model_name, result in overall_results.items():
    print(f"{model_name}: Accuracy = {result['accuracy']:.4f} using features {result['features']}")


# In[104]:


def get_df_for_combination(all_combinations, target_comb):
    for comb_columns, df_subset in all_combinations:
        if comb_columns == target_comb:
            return df_subset
    return None

target_features = ('mean_vector'	,'std_vector'	,	'median_vector','var_vector','entropy_vector'	) # תוכל להוסיף: 'vector_variance', וכו'
df_target = get_df_for_combination(all_combinations, target_features)

df_target


# In[96]:


get_ipython().system('pip install optuna')


# In[106]:


import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import numpy as np

def optimize_random_forest_with_optuna(X, y, n_trials=30):
    """
    אופטימיזציית RandomForest בעזרת Optuna – על כל הדאטה (בלי ולידציה חיצונית).

    פרמטרים:
    - X: מאפיינים
    - y: תוויות
    - n_trials: מספר ניסיונות (חיפושי פרמטרים)

    מחזיר:
    - best_model: המודל עם הפרמטרים הטובים ביותר
    - best_params: הפרמטרים
    - best_score: הדיוק הממוצע
    """

    def objective(trial):
        # הצעות פרמטרים
        n_estimators = trial.suggest_int("n_estimators", 100, 300)
        max_depth = trial.suggest_int("max_depth", 5, 11)
        max_features = trial.suggest_categorical("max_features", ["sqrt", "log2", None])

        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            max_features=max_features,
            random_state=42,
            n_jobs=-1
        )

        # דיוק על כל הדאטה (אפשר להחליף ל-cross_val_score)
        model.fit(X, y)
        preds = model.predict(X)
        acc = accuracy_score(y, preds)
        return acc  # דיוק גבוה יותר = טוב יותר

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)

    best_params = study.best_params
    best_score = study.best_value

    # אימון המודל הסופי עם הפרמטרים הטובים ביותר
    best_model = RandomForestClassifier(**best_params, random_state=42, n_jobs=-1)
    best_model.fit(X, y)

    return best_model, best_params, best_score


# In[107]:


# יצירת X ו-y (נניח שכבר שטחת וקטורים)


# הרצת Optuna
best_model, best_params, best_acc = optimize_random_forest_with_optuna(X, y, n_trials=40)

print("🏆 Best RandomForest Model:")
print(f"Params: {best_params}")
print(f"Accuracy: {best_acc:.4f}")


# In[114]:


from pprint import pprint
pprint(best_model.get_params())
print('-'*70)
import numpy as np
print(f"Most used feature index: {np.argmax(best_model.feature_importances_)}")
print('-'*70)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(range(len(best_model.feature_importances_)), best_model.feature_importances_)
plt.title("Feature Importances")
plt.xlabel("Feature Index")
plt.ylabel("Importance")
plt.show()
import joblib
joblib.dump(best_model, "best_random_forest_model.pkl")


# In[115]:


import os

folder_path = '/kaggle/input/fake-or-real-the-impostor-hunt/data/test'
lab = {}

for root, dirs, files in os.walk(folder_path):
    # שולף את שם התקיה מתוך הנתיב (התקיה הנוכחית)
    folder_name = os.path.basename(root)
    
    for filename in files:
        file_path = os.path.join(root, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # אם המפתח קיים, מוסיף לרשימה, אחרת יוצר רשימה חדשה
        if folder_name not in lab:
            lab[folder_name] = []
        lab[folder_name].append(content)


# In[125]:


import numpy as np
import pandas as pd

# שם המאמר לבדיקה
article_id = 'article_0000'

# תכונות שנבחרו עבור המודל
target_features = selected_features

# הדפסת מספר הטקסטים במאמר
num_texts = len(lab[article_id])
print(f"Number of texts in {article_id}: {num_texts}")

# שליפת שני הטקסטים הראשונים
text1 = lab[article_id][0]
text2 = lab[article_id][1]

# יצירת וקטורים מהטקסטים
vector1, _, _ = create_vector_from_list([text1])
vector2, _, _ = create_vector_from_list([text2])

# התאמת מבנה חד-ממדי
vec1 = vector1 if len(vector1.shape) == 1 else vector1[0]
vec2 = vector2 if len(vector2.shape) == 1 else vector2[0]

# חישוב תכונות לטקסט הראשון
features1 = {
    'mean_vector': np.mean(vec1),
    'std_vector': np.std(vec1),
    'median_vector': np.median(vec1),
    'var_vector': np.var(vec1),
    'entropy_vector': sigmoid_entropy_like(vec1)
}

# חישוב תכונות לטקסט השני
features2 = {
    'mean_vector': np.mean(vec2),
    'std_vector': np.std(vec2),
    'median_vector': np.median(vec2),
    'var_vector': np.var(vec2),
    'entropy_vector': sigmoid_entropy_like(vec2)
}

# יצירת טבלאות נתונים
df1 = pd.DataFrame([features1])
df2 = pd.DataFrame([features2])

# חיזוי עבור טקסט ראשון
prob1 = best_model.predict_proba(df1[target_features])[0][1]
pred1 = int(prob1 > 0.5)

# חיזוי עבור טקסט שני
prob2 = best_model.predict_proba(df2[target_features])[0][1]
pred2 = int(prob2 > 0.5)

# הדפסת תוצאות
print(f"\nText 1: Prediction probability: {prob1:.4f} | Binary prediction: {pred1}")
print(f"Text 2: Prediction probability: {prob2:.4f} | Binary prediction: {pred2}")


# In[159]:


print(len(vectorizer_all.get_feature_names_out()))


# In[160]:


from joblib import load
import numpy as np
from sklearn.base import ClusterMixin

def predict_and_distance(text: str, vectorizer: str, model: ClusterMixin) -> tuple[int, float]:
    """
    Predict cluster and compute Euclidean distance from cluster center for a given text.

    Args:
        text (str): Input text to classify.
        vectorizer_path (str): Path to saved vectorizer (.joblib).
        model (ClusterMixin): Pre-trained clustering model (e.g., KMeans).

    Returns:
        tuple[int, float]: (predicted_cluster, distance_to_cluster_center)
    """

    vec = vectorizer.transform([text])

    cluster = model.predict(vec)[0]
    center = model.cluster_centers_[cluster]
    distance = np.linalg.norm(vec.toarray() - center)

    return cluster, distance

# טעינת המודל פעם אחת מחוץ לפונקציה (למשל בתחילת הסקריפט)
# from joblib import load
# k_mean_model_1 = load('kmeans_model.joblib')

# שימוש
cluster_id, dist = predict_and_distance(text1, vectorizer_all, k_mean_model_1)

print(f"Cluster: {cluster_id}")
print(f"Distance from center: {dist:.4f}")


# In[156]:


results = []

# רשימת הפיצ'רים שהמודל הוכשר עליהם
features = target_features
#target_features = ('mean_vector'	,'std_vector'	,	'median_vector','var_vector','entropy_vector'	) # תוכל להוסיף: 'vector_variance', וכו'
for article_id, texts in lab.items():
    for idx, text in enumerate(texts):
        try:
            # יצירת הוקטור מהטקסט
            vector, _, _ = create_vector_from_list([text])

            # וקטור חד-ממדי (אם יש מימד נוסף, נבחר את השורה הראשונה)
            vec = vector if len(vector.shape) == 1 else vector[0]



            # יצירת DataFrame עם כל המדדים
            row_df = pd.DataFrame([{
                'article_id': article_id,
                'file_index': idx + 1,
                'mean_vector': np.mean(vec),
                'std_vector': np.std(vec),
                'median_vector': np.median(vec),
                'var_vector': np.var(vec),
                'entropy_vector': sigmoid_entropy_like(vec)
                
            }])

            # בודקים שהעמודות שהמודל מצפה להן אכן קיימות ובאותו סדר
            X_to_predict = row_df[features]

            # חיזוי הסתברותי וקבלת תוצאה בינארית
            prob = best_model.predict_proba(X_to_predict)[0][1]
            binary_pred = int(prob > 0.5)

        except Exception as e:
            print(f"Error processing article {article_id}, file_index {idx + 1}: {e}")

            # במקרה של שגיאה - סיווג 0 ומילוי ערכים חסרים
            binary_pred = 0
            prob = 0.0

            row_df = pd.DataFrame([{
                'article_id': article_id,
                'file_index': idx + 1,
                'mean_vector':0,
                'std_vector': 0,
                'median_vector':0,
                'var_vector': 0,
                'entropy_vector':0
                
            }])
            X_to_predict = row_df[features]

        # הוספת עמודות התוצאה ל-DataFrame
        row_df['prediction'] = binary_pred
        row_df['probability'] = prob

        # שמירת התוצאה לרשימה
        results.append(row_df)

# חיבור כל התוצאות ל-DataFrame אחד
final_results_df = pd.concat(results, ignore_index=True)


# In[157]:


final_results_df ['index_column'] = range(len(final_results_df ))
df_predictions =final_results_df 
df_predictions['probability'].unique


# In[158]:


df_predictions.to_csv('prediction.csv')


# In[160]:


import pandas as pd

# נניח ש-df_predictions קיים ויש בו עמודת 'probability'

# קודם מוסיפים עמודת index_column אם לא קיימת
df_predictions['index_column'] = range(len(df_predictions))

# יוצרים עמודה שמזהה את הזוג - כלומר כל שני אינדקסים שייכים לאותו זוג
df_predictions['pair_id'] = df_predictions['index_column'] // 2

# עכשיו עבור כל זוג בוחרים את השורה עם ה-probability הגבוה ביותר
idx_max_prob = df_predictions.groupby('pair_id')['probability'].idxmax()

# יוצרים דאטהפריים חדש עם השורות האלו
df_best_predictions = df_predictions.loc[idx_max_prob].reset_index(drop=True)

# אם רוצים, אפשר גם למחוק את העמודה 'pair_id' ו'index_column' כדי לנקות
df_best_predictions = df_best_predictions.drop(columns=['pair_id', 'index_column'])

df_best_predictions


# In[166]:


df_best_predictions[['article_id','prediction']]


# In[172]:


# נניח שיש לך בעמודה 'article_id' את מזהה המאמר
# נחלץ את התחזית המקסימלית לכל article_id
df_unique = final_results_df.groupby('article_id')['prediction'].max().reset_index()

# צור עמודת id רצה
df_unique['id'] = range(0, len(df_unique) )

# בחר עמודות לשמירה
df_to_save = df_unique[['id', 'prediction']]

print(df_to_save)
df_to_save.to_csv('predictions.csv', index=False)


# In[97]:


results = []


for article_id, texts in lab.items():
    for idx, text in enumerate(texts):
        try:
            vector, _, _ = create_vector_from_list([text])
            vec = vector if len(vector.shape) == 1 else vector[0]

            X_to_predict = vec

            # חיזוי קלאסטר עם k_mean_model_1
            cluster_label = k_mean_model_1.predict(X_to_predict)[0]

            # חישוב מרחק למרכז הקלאסטר
            distances = k_mean_model_1.transform(X_to_predict)
            distance_to_center = distances[0][cluster_label]

            # אפשר להוסיף פה גם חיזוי הסתברותי אם יש, אבל ב-KMeans אין.
            # לכן נוסיף רק את התווית והמרחק.

        except Exception as e:
            print(f"Error processing article {article_id}, file_index {idx + 1}: {e}")

            cluster_label = -1  # או ערך שמתאים ל"שגיאה"
            distance_to_center = np.nan

            X_to_predict = vec

        row_df['cluster'] = cluster_label
        row_df['distance_to_center'] = distance_to_center

        results.append(row_df)

final_results_df = pd.concat(results, ignore_index=True)

