#!/usr/bin/env python
# coding: utf-8

# In[99]:


get_ipython().system('pip install rdkit-pypi')

#important : 
# need to download it from link
# https://www.kaggle.com/datasets/jainam213/rdkit-wheels?utm_source=chatgpt.com
# !!

get_ipython().system('pip install /kaggle/input/rdkit-library/rdkit-2025.3.3-cp311-cp311-manylinux_2_28_x86_64.whl')

import numpy as np
import pandas as pd
import os


# In[100]:


import os
print(os.listdir('/kaggle/input/rdkit-library/'))


# In[101]:


modules_to_check = [
    "Chem",
    "DataStructs",
    "RDLogger",
    "Geometry",
    "Chem.AllChem",
    "Chem.Draw"
]

for mod_name in modules_to_check:
    try:
        module = __import__("rdkit." + mod_name, fromlist=["*"])
        print(f"✅ RDKit.{mod_name} is installed and ready to use!")
    except ImportError:
        print(f"❌ RDKit.{mod_name} is NOT installed or not available.")


# In[102]:


df_train_dataset_1 = pd.DataFrame(pd.read_csv('/kaggle/input/neurips-open-polymer-prediction-2025/train_supplement/dataset1.csv'))
df_train_dataset_2 = pd.DataFrame(pd.read_csv('/kaggle/input/neurips-open-polymer-prediction-2025/train_supplement/dataset2.csv'))
df_train_dataset_3 = pd.DataFrame(pd.read_csv('/kaggle/input/neurips-open-polymer-prediction-2025/train_supplement/dataset3.csv'))
df_train_dataset_4 = pd.DataFrame(pd.read_csv('/kaggle/input/neurips-open-polymer-prediction-2025/train_supplement/dataset4.csv'))

df_test = pd.DataFrame(pd.read_csv('/kaggle/input/neurips-open-polymer-prediction-2025/test.csv'))
df_train = pd.DataFrame(pd.read_csv('/kaggle/input/neurips-open-polymer-prediction-2025/train.csv'))


# In[103]:


df_train.head()


# In[104]:


df_test.head()


# In[105]:


df_train_dataset_1.head()


# In[106]:


df_train_dataset_2.head()


# In[107]:


df_train_dataset_3.head()


# In[108]:


df_train_dataset_4.head()


# In[109]:


import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid", palette="muted", font_scale=1.2)

print(f'Null in train : /n{df_train.isnull().sum()}')
print('-'*40)
print(f'describe train :/n{df_train.describe()}')
print('-'*40)


# In[110]:


plt.figure(figsize=(10, 5))
plt.scatter(df_train['id'], df_train['FFV'], c=df_train['FFV'], cmap='viridis', alpha=0.7)
plt.title('Scatter: FFV by ID')
plt.xlabel('ID')
plt.ylabel('FFV')
plt.colorbar(label='FFV Value')
plt.show()


# In[111]:


df_train['FFV_bin'] = pd.cut(df_train['FFV'], bins=5)

# גרף עמודות
plt.figure(figsize=(8, 5))
sns.barplot(x=df_train['FFV_bin'], y=df_train['FFV'], palette='Set2')
plt.title('Bar Plot: Avg FFV by FFV Range')
plt.xlabel('FFV Range')
plt.ylabel('Average FFV')
plt.xticks(rotation=45)
plt.show()


# In[112]:


df_tc_notnull = df_train[df_train['Tc'].notna()]
plt.figure(figsize=(15, 5))
sns.barplot(x='SMILES', y='Tc', data=df_tc_notnull[:60], palette='coolwarm')
plt.title('Bar Plot: Tc by ID (First 40 entries with Tc)')
plt.xlabel('SMILES')
plt.ylabel('Tc')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# In[113]:


con_data = df_train.merge(df_train_dataset_1, on='SMILES', how='outer') \
                   .merge(df_train_dataset_2, on='SMILES', how='outer') \
                   .merge(df_train_dataset_3, on='SMILES', how='outer') \
                   .merge(df_train_dataset_4, on='SMILES', how='outer')
print(con_data.shape)
print(con_data.isnull().sum())


# In[114]:


if('Tg_y' in con_data.columns):
    con_data.drop('Tg_y', axis=1, inplace=True)
    print('Tg_y deleted')
if('Tg_x' in con_data.columns):
    con_data.drop('Tg_x', axis=1, inplace=True)
    print('Tg_x deleted')


# In[115]:


con_data = con_data.dropna(subset=['id'])
con_data.shape


# In[117]:


from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem,Lipinski, rdMolDescriptors
from rdkit.Chem import Draw
from IPython.display import display
import pubchempy as pcp


# In[118]:


from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, rdMolDescriptors, Draw
import pandas as pd

def calc_features(smiles: str) -> dict:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return {
        "SMILES": smiles,
        "origin": mol,  # אם לא נדרש – אפשר למחוק
        "MolWt": Descriptors.MolWt(mol),
        "NumAromaticRings": Lipinski.NumAromaticRings(mol),
        "NumRings": rdMolDescriptors.CalcNumRings(mol),
        "FractionCSP3": Descriptors.FractionCSP3(mol),
        "NumRotatableBonds": Lipinski.NumRotatableBonds(mol),
        "TPSA": Descriptors.TPSA(mol),
        "HBA": Lipinski.NumHAcceptors(mol),
        "HBD": Lipinski.NumHDonors(mol),
        "BalabanJ": Descriptors.BalabanJ(mol),
        "MolLogP": Descriptors.MolLogP(mol),
    }

# איסוף התכונות
mols = []
for i in range(df_train.shape[0]):  # או כל תחום אחר שתרצה
    smiles = df_train["SMILES"][i]
    mol_dict = calc_features(smiles)
    if mol_dict is not None:
        mols.append(mol_dict)

# הפיכה ל-DataFrame
df_features_train = pd.DataFrame(mols)

# הסרת העמודה origin אם לא דרושה בטבלה
df_features = df_features_train.drop(columns=["origin"])

# הצגה
display(df_features)
print(df_features.shape)
print(df_train.shape)


# In[119]:


mol_test = []
for i in range (df_test.shape[0]):
    smiles = df_train["SMILES"][i]
    mol_dict = calc_features(smiles)
    if mol_dict is not None:
        mol_test.append(mol_dict)
# הפיכה ל-DataFrame
df_features_test = pd.DataFrame(mol_test)

# הסרת העמודה origin אם לא דרושה בטבלה
df_train_process = df_features_test.drop(columns=["origin"])

# הצגה
display(df_train_process)
print(df_train_process.shape)
print(df_test.shape)


# In[120]:


list_target = ['Tg','FFV','Tc','Density','Rg'] 
_df_train_ = df_train.drop(columns=['FFV_bin'])
_df_train_1 = pd.merge(_df_train_, df_features, on='SMILES')
_df_train_1


# In[121]:


print(f'null : {_df_train_1.isnull().sum()}')


# In[122]:


list_target = ['Tg', 'FFV', 'Tc', 'Density', 'Rg']

# מילונים לשמירת זוגות DataFrame
X_dict = {}
Y_dict = {}

for target in list_target:
    # בחר שורות שבהן העמודה target לא ריקה
    df_x = _df_train_1[_df_train_1[target].notnull()].copy()
    # בחר שורות שבהן העמודה target ריקה
    df_y = _df_train_1[_df_train_1[target].isnull()].copy()

    # עמודות מטרות להוציא (כל העמודות חוץ מהעמודה target)
    cols_to_drop = [col for col in list_target if col != target]

    # מחיקת העמודות שאינן העמודה target
    df_x.drop(columns=cols_to_drop, inplace=True)
    df_y.drop(columns=cols_to_drop, inplace=True)
    
    df_x.drop(columns='id', inplace=True)
    df_y.drop(columns='id', inplace=True)

    df_x.drop(columns='SMILES', inplace=True)
    df_y.drop(columns='SMILES', inplace=True)

    # שמירת התוצאות במילונים
    X_dict[f"{target}"] = df_x
    Y_dict[f"{target}"] = df_y

# דוגמה להדפסת הצורה של Tg_x ו-Tg_y
for i in list_target:
    print(i)
    print(X_dict[f'{i}'].shape)
    print(Y_dict[f'{i}'].shape)


# In[123]:


print(X_dict['Tg'].head)


# In[124]:


from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def train_linear_regression(df, target_col, test_size=0.3, random_state=42):
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    predict = model.predict(X_test_scaled)

    return model, predict, scaler

def train_random_forest(df, target_col, test_size=0.3, random_state=42):
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestRegressor(random_state=random_state)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)

    return model, y_pred, scaler

def train_gradient_boosting(df, target_col, test_size=0.3, random_state=42):
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = GradientBoostingRegressor(random_state=random_state)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)

    return model, y_pred, scaler

def train_svr(df, target_col, test_size=0.3, random_state=42):
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = SVR()
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)

    return model, y_pred, scaler 




# In[125]:


list_target


# In[126]:


models = []
scalers = []
list_pred = []



for i in list_target:
    model_lr,predict_lr,scaler_lr = train_linear_regression(X_dict[i],i)
    
    model_rf,predict_rf,scaler_rf= train_random_forest(X_dict[i], i)
    
    
    model_gb,predict_gb,scaler_gb= train_gradient_boosting(X_dict[i],i)
    
    
    model_svr,predict_svr,scaler_svr= train_svr(X_dict[i], i)

    print("="*50)
    print(f"📈 Linear Regression - מספר תחזיות: {len(predict_lr)} 📊")
    print(f"🌲 Random Forest - מספר תחזיות: {len(predict_rf)} 🌳")
    print(f"🚀 Gradient Boosting - מספר תחזיות: {len(predict_gb)} ⚡")
    print(f"🎯 SVR (Support Vector Regression) - מספר תחזיות: {len(predict_svr)} 🤖")
    print("="*50)

    list_pred.append(({
        
            'linear_regression': predict_lr,
            'random_forest': predict_rf,
            'gradient_boosting': predict_gb,
            'svr': predict_svr
        
    }))
    models.append(({
        
            'linear_regression': model_lr,
            'random_forest': model_rf,
            'gradient_boosting': model_gb,
            'svr': model_svr
        
    }))
    scalers.append(({
        
            'linear_regression': scaler_lr,
            'random_forest': scaler_rf,
            'gradient_boosting': scaler_gb,
            'svr': scaler_svr
        
    }))


# In[127]:


try:
    df_1 = pd.DataFrame({k: list_pred[0][k] for k in list(list_pred[0].keys())[0:4]})
    df_2 = pd.DataFrame({k: list_pred[1][k] for k in list(list_pred[1].keys())[0:4]})
    df_3 = pd.DataFrame({k: list_pred[2][k] for k in list(list_pred[2].keys())[0:4]})
    df_4 = pd.DataFrame({k: list_pred[3][k] for k in list(list_pred[3].keys())[0:4]})
    df_5 = pd.DataFrame({k: list_pred[4][k] for k in list(list_pred[4].keys())[0:4]})
except Exception as e:
    df_1 = pd.DataFrame({k: list_pred[0][k] for k in list(list_pred[0].keys())[0:3]})
    df_2 = pd.DataFrame({k: list_pred[1][k] for k in list(list_pred[1].keys())[0:3]})
    df_3 = pd.DataFrame({k: list_pred[2][k] for k in list(list_pred[2].keys())[0:3]})
    df_4 = pd.DataFrame({k: list_pred[3][k] for k in list(list_pred[3].keys())[0:3]})
    df_5 = pd.DataFrame({k: list_pred[4][k] for k in list(list_pred[4].keys())[0:3]})


# In[128]:


df_1.describe()


# In[129]:


df_2.describe()


# In[130]:


df_3.describe()


# In[131]:


df_4.describe()


# In[132]:


df_5.describe()


# In[133]:


#list_target = ['Tg', 'FFV', 'Tc', 'Density', 'Rg']
df_final_pred = df_features_train.copy()
df_final_pred_lr = df_features_train.copy()
df_final_pred_rf = df_features_train.copy()
df_final_pred_gb = df_features_train.copy()


pdFrameForPred = pd.DataFrame(df_features_train.drop(columns=['SMILES']))
pdFrameForPred = pd.DataFrame(pdFrameForPred.drop(columns=['origin']))


# In[134]:


pdFrameForPred.head()


# In[135]:


list_target = ['Tg', 'FFV', 'Tc', 'Density', 'Rg']
# יוצרים מטריצת פיצ'רים עבור ניבוי
X_pred = pdFrameForPred

# מבצעים ניבוי על כל הדוגמאות

for i,name in enumerate(list_target):    
    df_final_pred[f'{name}_prediction'] = models[i]['svr'].predict(scalers[0]['svr'].fit_transform(X_pred))
    df_final_pred_lr[f'{name}_prediction'] = models[i]['linear_regression'].predict(scalers[0]['svr'].fit_transform(X_pred))
    df_final_pred_rf[f'{name}_prediction'] = models[i]['random_forest'].predict(scalers[0]['svr'].fit_transform(X_pred))
    df_final_pred_gb[f'{name}_prediction'] = models[i]['gradient_boosting'].predict(scalers[0]['svr'].fit_transform(X_pred))



# In[136]:


pdFrameForPred.describe()


# In[137]:


df_final_pred.filter(like='prediction')


# In[138]:


df_final_pred.filter(like='prediction').describe()


# In[139]:


df_final_pred_lr.filter(like='prediction')


# In[140]:


df_final_pred_rf.filter(like='prediction')


# In[141]:


df_final_pred_gb.filter(like='prediction')


# In[142]:


import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import AgglomerativeClustering

def create_hierarchical_clustered_scatterplot(df, x, y, n_clusters=3, show_fit_line=True):
    # סינון רק שני העמודות
    data = df[[x, y]].dropna()

    # קלאסטרינג היררכי
    clustering = AgglomerativeClustering(n_clusters=n_clusters)
    data['cluster'] = clustering.fit_predict(data[[x, y]])

    # ציור Scatter עם הצבעה לפי אשכול
    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=data, x=x, y=y, hue='cluster', palette='Set1', s=60)

    if show_fit_line:
        # מוסיפים קו רגרסיה לכל אשכול
        for cluster_id in range(n_clusters):
            cluster_data = data[data['cluster'] == cluster_id]
            if len(cluster_data) >= 2:
                coeffs = np.polyfit(cluster_data[x], cluster_data[y], deg=1)
                poly_line = np.poly1d(coeffs)
                xs = np.linspace(cluster_data[x].min(), cluster_data[x].max(), 100)
                ys = poly_line(xs)
                plt.plot(xs, ys, label=f'Fit Cluster {cluster_id}', linestyle='--')

    plt.title(f'Hierarchical Clustering: {x} vs {y}')
    plt.legend()
    plt.tight_layout()
    plt.show()


# In[143]:


m = 0
for i in df_final_pred.filter(like='prediction').columns:
    for j in df_final_pred.filter(like='prediction').columns:
        m+=1
        if i != j:  # אם לא רוצים זוגות זהים
            create_hierarchical_clustered_scatterplot(df_final_pred, i, j)
        if i=='TC_prediction' and j=='Density_prediction':
            print(f'🎨 🌠 - {m} Scatter + hierarchical Clustering + poly1d Plots ')
            break
        
            


# In[144]:


'''
id,Tg,FFV,Tc,Density,Rg
   2112371,0.0,0.0,0.0,0.0,0.0
   2021324,0.0,0.0,0.0,0.0,0.0
   343242,0.0,0.0,0.0,0.0,0.0
'''


# In[145]:


list_target = ['Tg', 'FFV', 'Tc', 'Density', 'Rg']
# יוצרים מטריצת פיצ'רים עבור ניבוי
df_t_pred = df_features_train.copy()
df_t_pred_lr = df_features_train.copy()
df_t_pred_rf = df_features_train.copy()
df_t_pred_gb = df_features_train.copy()

X_t_pred = df_train_process.drop(columns=['SMILES'])
predictionS = [X_t_pred.copy() for _ in range(len(list_target))]

# ניבוי לפי המודלים
for i, name in enumerate(list_target):    
    predictionS[i][f'{name}_prediction_svr'] = models[i]['svr'].predict(scalers[i]['svr'].fit_transform(X_t_pred))
    predictionS[i][f'{name}_prediction_lr'] = models[i]['linear_regression'].predict(scalers[i]['linear_regression'].fit_transform(X_t_pred))
    predictionS[i][f'{name}_prediction_rf'] = models[i]['random_forest'].predict(scalers[i]['random_forest'].fit_transform(X_t_pred))
    predictionS[i][f'{name}_prediction_gb'] = models[i]['gradient_boosting'].predict(scalers[i]['gradient_boosting'].fit_transform(X_t_pred))


# In[146]:


predictionS[0]


# In[147]:


for i in range(len(predictionS)):
    predictionS[i] = predictionS[i].iloc[:, -4:]


# In[148]:


predictionS[0].describe()


# In[149]:


predictionS[1].describe()


# In[150]:


predictionS[2].describe()


# In[151]:


predictionS[3].describe()


# In[152]:


predictionS[4].describe()


# In[153]:


for i in range(5):
    predictionS[i]['id'] = df_test['id']
predictionS[0]


# In[154]:


dictFinal = {}
dictFinal['id'] = df_test['id']
for i,target in enumerate(list_target):
    dictFinal[target]=predictionS[i][f'{target}_prediction_svr']


# In[155]:


dictFinal


# In[156]:


submission = pd.DataFrame(dictFinal)
submission.to_csv('submission.csv',index=False)

submission


# In[ ]:




