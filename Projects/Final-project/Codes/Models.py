import os
import random

import numpy as np
import pandas as pd
from catboost import Pool, CatBoostClassifier, CatBoostRegressor
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, mean_squared_error, mean_absolute_error, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import seaborn as sns
import sympy
import sympy as sp
import math



x = sympy.Symbol('x')
# פונקציית רגרסיה עם NumPy
def reg_accuracy_by_numpy(acc_dict,deg=2):
    global x
    x_vals = np.array(list(acc_dict.keys()))
    y_vals = np.array(list(acc_dict.values()))
    coeffs = np.polyfit(x_vals, y_vals, deg=deg)
    fx = sum(coef * x**i for i, coef in enumerate(reversed(coeffs)))

    return fx
def draw_fx(fx, acc_dict,  num_points=100 , title = None , path_save_fig=None):
    x_range = (0, max(acc_dict.keys()))
    x = sp.Symbol('x')
    fx_numeric = sp.lambdify(x, fx, modules=['numpy'])

    # טווח ערכים לציר X
    x_vals = np.linspace(x_range[0], x_range[1], num_points)
    y_vals = fx_numeric(x_vals)

    # המרת dict לרשימות
    dict_x = list(acc_dict.keys())
    dict_y = list(acc_dict.values())

    # ציור
    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label=f"y = {sp.simplify(fx)}", color='blue')  # קו רגרסיה
    plt.scatter(dict_x, dict_y, color='red', label='Original Data')  # נקודות הנתונים המקוריים

    plt.axhline(0, color='black', linewidth=0.5)  # ציר X
    plt.axvline(0, color='black', linewidth=0.5)  # ציר Y
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Linear Regression + Original Data ,"+str(title))
    plt.grid(True)
    plt.legend()
    if path_save_fig is not None:
        plt.savefig(os.path.join(path_save_fig,f'Linear Regression + Original Data ,{title}.png'))
    plt.show()










# CatBoost
print('-'*20+'🐱CatBoost Model Information '+'-'*20)
current_F = ['Impact','Title','Severity.1','Supersedes','Reboot','CVEs','Affected Component','Component KB','Severity']
df_process = pd.read_excel('/Users/shryqb/PycharmProjects/new_project_original/file_1/output data/3 - Original alldata filled with target.xlsx')
currect_frame = df_process[current_F]
df_0 = currect_frame.copy()

test = 0.443251
i=156
D=6
features = ['Impact',
            'Title',
            'Severity.1',
             'Supersedes',
             'Reboot',
             'CVEs',
             'Affected Component',
             'Component KB']
os.makedirs('Reports/CatBoost', exist_ok=True)
def train_catboost_(df: pd.DataFrame,iterations : int , features: list, target: str, cat_features: list = None,
                   task: str = "classification" , test = 0.2 , Depth = 6 , LR=0.1):

    """
    פונקציה לאימון מודל CatBoost והערכתו במדדים שונים בהתאם לסוג המשימה.
    :param df: DataFrame עם הנתונים
    :param features: רשימת שמות העמודות של הפיצ'רים
    :param target: שם עמודת המטרה
    :param cat_features: רשימת שמות של משתנים קטגוריים (אופציונלי)
    :param task: סוג המשימה - "classification" או "regression"
    :param tree_idx: מספר העץ לציור
    :return: המודל המאומן, המטריקות, וסט האימון
    """
    X = df.drop(columns=target)
    y = df[target]

    # זיהוי משתנים קטגוריים אם לא סופקו
    if cat_features is None:
        cat_features = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # המרת משתנים קטגוריים לקטגוריה
    for col in cat_features:
        X[col] = X[col].astype('category')

    num_features = [col for col in features if col not in cat_features]
    print(num_features)
    scaler = MinMaxScaler()
    X[num_features] = scaler.fit_transform(X[num_features])


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= test, random_state=42)

    # The `Pool` class in CatBoost is a special way to give data to the model.
    # It helps CatBoost know which columns are categorical (not numbers).
    # It also makes training faster and uses less memory.
    train_pool = Pool(X_train, label=y_train, cat_features=cat_features)
    test_pool = Pool(X_test, label=y_test, cat_features=cat_features)

    if task == "classification":
        model = CatBoostClassifier(iterations=iterations, learning_rate=LR, depth=Depth, verbose=100,thread_count = -1)
    elif task == "regression":
        model = CatBoostRegressor(iterations=iterations, learning_rate=LR, depth=Depth, verbose=0)
    else:
        raise ValueError("Task must be either 'classification' or 'regression'")

    # אימון המודל
    model.fit(train_pool)

    # חיזוי על סט הבדיקה
    y_pred = model.predict(X_test)

    # מדדים לפי סוג המשימה
    if task == "classification":
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')



        metrics = {"Accuracy": accuracy, "F1 Score": f1, "Precision": precision, "Recall": recall}
    else:
        rmse = mean_squared_error(y_test, y_pred, squared=False)  # RMSE
        mae = mean_absolute_error(y_test, y_pred)

        print(f"RMSE: {rmse:.4f}")
        print(f"MAE: {mae:.4f}")

        metrics = {"RMSE": rmse, "MAE": mae}

    # הצגת כמות העצים במודל
    print(f"Number of trees in model: {model.tree_count_}")

    return model, metrics, X_train


def plot_feature_importance(model, features):
    feature_importance = model.get_feature_importance()


    if len(feature_importance) != len(features):
        print(f"Warning: Model has {len(feature_importance)} features but features list has {len(features)}")
        features = model.feature_names_  # קבלת שמות הפיצ'רים מהמודל ישירות

    sorted_idx = np.argsort(feature_importance) # מיון הפיצ׳רים

    #הוצאת גרף bar
    plt.figure(figsize=(10, 6))
    plt.barh([features[i] for i in sorted_idx], feature_importance[sorted_idx])
    plt.xlabel("Feature Importance")
    plt.title("CatBoost Feature Importance")
    plt.show()



lr=0.13834061227219888
print(f'lr - {lr}')
catMod, metrics , x_train = train_catboost_(df_0, iterations=i, features=features, target='Severity', task="classification",
                                        test=test, Depth=D, LR=lr)
pd.DataFrame(metrics,index=[0]).to_csv(os.path.join('Reports/CatBoost', 'catboost Report.csv'), index=False)
print(f'🐱 metrics : {metrics}')
print(f'best lr ={lr}')

plot_feature_importance(catMod, features)
catMod.save_model("my_catboost_model.cbm")
'''
how to load model -

from catboost import CatBoostClassifier

loaded_model = CatBoostClassifier()
loaded_model.load_model("my_catboost_model.cbm")

'''

# extre tree
from sklearn.metrics import classification_report
from sklearn.ensemble import ExtraTreesClassifier
print('-'*20+'🎄Extra Tree Model Information '+'-'*20)
os.makedirs('Reports/Extra_tree', exist_ok=True)
def run_extra_trees_model(df, target_column , T=0.2, N=400, D=10):
    df_encoded = df.copy()

    # הסרת כל העמודות מסוג תאריך
    datetime_cols = df_encoded.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns
    df_encoded.drop(columns=datetime_cols, inplace=True)

    # One-Hot Encoding לכל התכונות הקטגוריאליות למעט עמודת המטרה
    df_encoded = pd.get_dummies(df_encoded, columns=[col for col in df_encoded.columns if col != target_column and df_encoded[col].dtype == 'object'])

    # קידוד עמודת המטרה (אם היא קטגוריאלית)
    le = None
    if df[target_column].dtype == 'object':
        le = LabelEncoder()
        df_encoded[target_column] = le.fit_transform(df[target_column])
        class_names = le.classes_
    else:
        class_names = sorted(df[target_column].unique().astype(str))

    X = df_encoded.drop(columns=[target_column])
    y = df_encoded[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=T, random_state=42)

    model = ExtraTreesClassifier(
        n_estimators=N,
        max_depth=D,
        min_samples_split=4,
        min_samples_leaf=2,
        max_features='sqrt',
        bootstrap=False,
        n_jobs=-1,
        random_state=42,
        verbose=100
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print("✅ Extra Trees Results:")
    print("Accuracy:", acc)

    report_dict = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose()
    report_df['accuracy'] = acc

    report_df.to_csv("Reports/Extra_tree/extra_trees_report.csv", index=True)
    print("📄 Classification Report saved to: extra_trees_report.csv")
    print(report_df)

    return model, acc

accu = {}
accMax = 0
testMax = 0
best_D = 0
mon=0
for D in range(5, 10, 2):
  t = random.uniform(0.1, 0.2)
  model, acc = run_extra_trees_model(df=df_0, target_column='Severity', T=t, N=300, D=D)
  accu[mon]=acc
  if acc > accMax:
      accMax = acc
      testMax = t
      best_D = D
  mon+=1

fx = reg_accuracy_by_numpy(acc_dict=accu, deg=3)
print(f'Accuracy: {accMax} | test size: {testMax} | max depth: {best_D}')

draw_fx(fx,acc_dict=accu , title='Extra Tree Model',path_save_fig='/Users/shryqb/PycharmProjects/new_project_original/file_1/Reports/Extra_tree'
                                                                  '')

# Light GBM

import lightgbm as lgb

print('-'*20+'🔆🌈Light GBM Model Information '+'-'*20)
os.makedirs('Reports/lightGBM', exist_ok=True)

def run_lightgbm_model(df , T=3):
    # המרת עמודת המטרה לערכים מספריים
    target = df['Severity']

    # הסרת עמודת המטרה
    df_features = df.drop('Severity', axis=1)

    # זיהוי משתנים קטגוריאליים
    categorical_cols = df_features.select_dtypes(include=['object']).columns.tolist()

    # המרת כל המשתנים הקטגוריאליים לקטגוריות (LightGBM תומך בזה באופן טבעי)
    for column in categorical_cols:
        df_features[column] = df_features[column].astype('category')

    # פיצול הנתונים לסט אימון וסט בדיקה
    X_train, X_test, y_train, y_test = train_test_split(df_features, target, test_size=0.3, random_state=42)

    # יצירת המודל
    model = lgb.LGBMClassifier(
        n_estimators=300,
        learning_rate=0.01,
        max_depth=T,
        num_leaves=20,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.05,
        reg_lambda=0.1,
        random_state=42,
        n_jobs=-1
    )

    # אימון המודל
    model.fit( X_train, y_train,
    categorical_feature=categorical_cols,

    )

    # חיזוי על סט הבדיקה
    y_pred = model.predict(X_test)

    # חישוב הדיוק ודוח הסיווג
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose()

    # תוצאות
    print("דיוק (Accuracy):", accuracy)
    print("\nדוח סיווג:\n", report_df)
    print("\nמטריצת בלבול:\n", conf_matrix)



    # הצגת מטריצת בלבול בתמונה
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Critical', 'Important', 'Low', 'Moderate'],
                yticklabels=['Critical', 'Important', 'Low', 'Moderate'])
    plt.title("Confusion Matrix")
    plt.xlabel("Prediction")
    plt.ylabel("True Label")
    plt.show()
    print(report_df)


    return model , accuracy,report_df


M, Acc ,report= run_lightgbm_model(df_0 , T=15)
report.to_csv(os.path.join('Reports/lightGBM', 'lightGBM.csv'), index=True)
print(f'depth = 15 , accuracy = {Acc}')

import xgboost as xgb
print('-'*20+'🚀XG boost Model Information '+'-'*20)
os.makedirs('Reports/XGboost', exist_ok=True)
def train_xgboost(df, target_column , T=0.2 , D =2, LR=0.1):
    # מחלק את הנתונים למשתנים (X) ועמודת מטרה (y)
    # הסרת כל עמודות datetime באופן אוטומטי
    X = df.drop(columns=[target_column])
    X = X.select_dtypes(exclude=['datetime64[ns]'])

    y = df[target_column]

    # המרת עמודת המטרה (y) למספרים באמצעות LabelEncoder
    target_encoder = LabelEncoder()
    y_encoded = target_encoder.fit_transform(y)

    # המרת משתנים קטגוריאליים במאפיינים (X) למספרים
    le = LabelEncoder()
    for col in X.select_dtypes(include=['object']).columns:
        X[col] = le.fit_transform(X[col])

    # מחלק את הנתונים לאימון ובדיקת המודל
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=T, random_state=42)

    # יצירת מודל XGBoost
    model = xgb.XGBClassifier(
        objective='multi:softprob',
        eval_metric='mlogloss',
        n_estimators=300,
        max_depth=D,
        learning_rate=LR,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=1,
        reg_alpha=1,
        reg_lambda=1,
        random_state=42,
        use_label_encoder=False
    )

    # אימון המודל
    model.fit(X_train, y_train)

    # חיזוי על קבוצת הבדיקה
    y_pred = model.predict(X_test)

    # חישוב דיוק המודל
    accuracy = accuracy_score(y_test, y_pred)
    #print(f'Accuracy: {accuracy}')

    # הערכת המודל
    #evulate_modle(model, y_test, y_pred, target_encoder)

    # יצירת דוח
    #report = create_report(df, y_test, y_pred, target_encoder)

    return model , accuracy



accuracy_for_reg = {}
acc_ = {}
# דוגמה לשימוש
# df - הנתונים שלך
# target_column - שם עמודת המטרה
mon=0
for i in range(5,12):
    mon+=1
    LR = random.uniform(0.1,5)
    TestSplit = random.uniform(0.1,0.3)
    model , acc = train_xgboost(df=df_0, target_column='Severity' , T=TestSplit , D=i,LR=LR)
    print(f'T = {TestSplit} , LR = {LR} , depth = {i} , Accuracy = {acc}')
    acc_[mon] = {"accuracy": acc, "T": TestSplit, "depth": i, "LR": LR}
    accuracy_for_reg[mon] = acc


pd.DataFrame(acc_).to_csv(os.path.join('Reports/XGboost','xgBoost report.csv'),index=True)
# מציאת התוצאה הטובה ביותר
best_key = max(acc_, key=lambda k: acc_[k]['accuracy'])
best_result = acc_[best_key]

print(f"\n🔥 התוצאה הטובה ביותר:")
print(f"Index: {best_key}")
print(f"Accuracy: {best_result['accuracy']}")
print(f"TestSplit (T): {best_result['T']}")
print(f"Max Depth: {best_result['depth']}")
print(f"Learning Rate: {best_result['LR']}")


fx=reg_accuracy_by_numpy(acc_dict=accuracy_for_reg,deg=4)
draw_fx(fx=fx,acc_dict=accuracy_for_reg , title='XGBoost Model',path_save_fig='/Users/shryqb/PycharmProjects/new_project_original/file_1/Reports/XGboost')
