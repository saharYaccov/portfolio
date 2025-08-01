"""
Machine Learning Pipeline for Classification with Missing Data Handling and Model Evaluation

This script provides functions to preprocess data, handle missing categorical values,
train decision tree models for imputation and classification,
and run multiple classifiers with evaluation and visualization.

Key functionalities:

1. fill_missing_categorical_values(df, strategy='most_frequent'):
   - Fills missing values in categorical columns using SimpleImputer.
   - Supports different strategies (default: most frequent value).

2. split_by_target_null(df, target):
   - Splits the DataFrame into two subsets: rows where the target is null and where it is not.
   - Enables separate handling of missing target values.

3. tree_model(df, df_null_target, target, name_fig):
   - Trains a decision tree classifier on the complete cases.
   - Predicts missing target values in the subset with null targets.
   - Displays and saves the decision tree visualization.
   - Returns the trained model, accuracy, and the DataFrame with predicted target values.

4. train_decision_tree_filled_data(df, target, new_data_for_predict):
   - Trains a decision tree classifier on the full dataset without missing values.
   - Evaluates accuracy, F1 score, and precision.
   - Visualizes and saves the decision tree.
   - Predicts the target for new input data.
   - Returns the trained model, accuracy, confusion matrix, predictions DataFrame, and a dictionary of model accuracies.

5. convert_to_datetime(df, column_name, separator='-'):
   - Converts a date column (string) to separate numeric Year, Month, and Day columns.
   - Automatically detects common date separators and handles conversion errors.

6. run_models_and_plot(df, target):
   - Encodes categorical features numerically.
   - Splits data into training and testing sets.
   - Trains and evaluates three classifiers: Random Forest, SVM, and Gradient Boosting.
   - Computes accuracy, F1 score, precision, and confusion matrices.
   - Visualizes confusion matrices and saves them.
   - Plots example decision trees from Random Forest.
   - Shows SVM decision boundaries for the first two features.
   - Saves all plots in the 'graphs' directory.

General notes:
- Uses sklearn for modeling and metrics.
- Visualization via matplotlib and seaborn.
- Saves models and plots to organized directories.
- Designed to handle datasets with categorical data and missing values efficiently.

"""
            


import os
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, f1_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer



max_d = 12
fontsize = 10

dict_best_model = {}
os.makedirs('decision trees', exist_ok=True)
os.makedirs('output data', exist_ok=True)
##############################################################################################################################################
##############################################################################################################################################
'''
ממלא ערכים חסרים בעמודות קטגוריאליות לפי אסטרטגיה מוגדרת.
משתמש ב-SimpleImputer להשלמת ערכים חסרים כגון None או NaN.


print(f'[parameters : max deeps = {max_d} , fontsize = {fontsize}]')
print('='*444)
'''
def fill_missing_categorical_values(df, strategy='most_frequent'):
    # המרת None ל-nan
    df = df.replace({None: np.nan})

    # יצירת SimpleImputer עבור עמודות קטגוריאליות
    imputer = SimpleImputer(strategy=strategy, fill_value='missing')

    # התאמת האימפוטר ל-DataFrame
    filled_array = imputer.fit_transform(df)
    df = pd.DataFrame(filled_array, columns=df.columns)


    # החזרת DataFrame ממולא
    return df


#decision_tree_model(filled_df, target)

##############################################################################################################################################
##############################################################################################################################################
'''
מחלק את הנתונים לשתי קבוצות: אחת עם ערכים חסרים בעמודת היעד ואחת בלי.
מאפשר טיפול נפרד בנתונים עם ובלי ערך יעד.
'''
def split_by_target_null(df,target):
    df_null_target = df[df[target].isnull()]
    df_not_null_target = df[df[target].notnull()]
    return df_null_target, df_not_null_target


##############################################################################################################################################
##############################################################################################################################################
'''
מאמן מודל עץ החלטה לחיזוי ערכים חסרים בעמודת היעד.
מציג מטריצת בלבול, דיוק המודל, ותרשים עץ החלטה.
'''
def tree_model(df,df_null_target, target,name_fig):
    df_not_target = df.drop(columns=[target])
    df_null_not_target = df_null_target.drop(columns=[target]) # this df has null in target

    df_combined = pd.concat([df_not_target, df_null_not_target])
    df_combined_dummies = pd.get_dummies(df_combined)

    df1_dummies = df_combined_dummies.iloc[:len(df)]
    df2_dummies_ob = df_combined_dummies.iloc[len(df):]

    X = df1_dummies
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    print(f'Confusion Matrix:\n{cm}')

    accuracy = accuracy_score(y_test, y_pred)
    #predict for df_null
    df_2_predict = model.predict(df2_dummies_ob)

    df_null_target.loc[:, target] = df_2_predict

    print(f'predict :\n {df_2_predict}')

    # הגבלת שמות הפיצ'רים ל-20 תווים
    max_length = 20
    truncated_feature_names = [name[:max_length] for name in X.columns]

    plt.figure(figsize=(12, 8))
    plot_tree(
        model,  # מודל העץ עצמו
        filled=True,  # צבע את המלבן בהתאם למחלקה (True=צבע מלא, False=לא)
        feature_names=truncated_feature_names,  # שמות הפיצ'רים (עמודות) ששימשו לאימון המודל
        class_names=model.classes_.astype(str),  # שמות המחלקות בתוויות (במקרה הזה המרתן למחרוזות)
        rounded=True,  # עיגול הפינות של המלבן (True=עיגול פינות, False=פינות חדות)
        max_depth=max_d,  # העמק (max_depth) של העץ, כלומר עד איזו רמה לעומק לצייר את העץ
        fontsize=fontsize,  # גודל הגופן של הטקסט בעץ
        precision=2,  # רמת דיוק של ציון המידע בתוך המלבן (כמו אחוזים)
        proportion=True,  # האם להציג את הערכים היחסיים של כל מחלקה (True=מינונים יחסיים)
        label='all',  # לציין אם להציג את כל התוויות בכל צומת (אפשר גם 'root', 'none', 'all')
    )

    plt.title("Decision Tree Model")
    #plt.show()
    plt.savefig(os.path.join('decision trees',f'tree of {name_fig}.png'))

    dict_best_model['decision tree model missing data'] = accuracy
    return model, accuracy , df_null_target

##############################################################################################################################################
##############################################################################################################################################
'''
מאמן מודל עץ החלטה על הנתונים המלאים ומחשב דיוק.
חוזה ערכים לנתונים חדשים ומציג תרשים עץ החלטה.
הנתונים המלאים ללא ערכים חסרים
'''
def train_decision_tree_filled_data(df, target ,new_data_for_predict):
    # המרת משתנים קטגוריאליים לדמי

    # חיתוך הנתונים בין תכונות (X) ליעד (y)
    X = df.drop(columns=[target])  # כל העמודות חוץ מהיעד
    y = df[target]  # העמודה שמייצגת את היעד

    X = pd.get_dummies(X, drop_first=True) #dummies fichers
    #print(f'--------- shape of dummy : {X.shape}')
    #pd.concat([X,y]).to_csv(os.path.join('output data' , 'dummies values frame.csv'))
    #print('---------- saved dummies values frame successfully')
    # חיתוך הנתונים לסט אימון וסט מבחן
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    # יצירת המודל
    model = DecisionTreeClassifier(random_state=42)

    # אימון המודל
    model.fit(X_train, y_train)

    # חיזוי על סט המבחן
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    #print(f'Confusion Matrix for full dataFrame : \n{cm}')


    # חישוב הדיוק
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    precision = precision_score(y_test, y_pred, average='weighted')


    # הגבלת שמות הפיצ'רים ל-20 תווים
    max_length = 20
    truncated_feature_names = [name[:max_length] for name in X.columns]

    # הצגת עץ החלטה
    plt.figure(figsize=(12, 8))
    plot_tree(
        model,  # מודל העץ עצמו
        filled=True,  # צבע את המלבן בהתאם למחלקה (True=צבע מלא, False=לא)
        feature_names=truncated_feature_names,  # שמות הפיצ'רים (עמודות) ששימשו לאימון המודל
        class_names=model.classes_.astype(str),  # שמות המחלקות בתוויות (במקרה הזה המרתן למחרוזות)
        rounded=True,  # עיגול הפינות של המלבן (True=עיגול פינות, False=פינות חדות)
        max_depth=max_d,  # העמק (max_depth) של העץ, כלומר עד איזו רמה לעומק לצייר את העץ
        fontsize=fontsize,  # גודל הגופן של הטקסט בעץ
        precision=2,  # רמת דיוק של ציון המידע בתוך המלבן (כמו אחוזים)
        proportion=True,  # האם להציג את הערכים היחסיים של כל מחלקה (True=מינונים יחסיים)
        label='all',  # לציין אם להציג את כל התוויות בכל צומת (אפשר גם 'root', 'none', 'all')
    )
    plt.title("Decision Tree Model")
    plt.savefig(os.path.join('decision trees',f'decision_tree_{target} - full dataFrame.png'))  # לשמור את העץ כקובץ תמונה

    # המרת התצפית החדשה לדמיות
    new_data_dummies = pd.get_dummies(new_data_for_predict)
    # מוודאים שהתצפית החדשה כוללת את כל העמודות של X מהמודל, וממלאים ערכים חסרים ב-0
    new_data_dummies = new_data_dummies.reindex(columns=X.columns, fill_value=0)
    # חיזוי עם המודל
    new_prediction = model.predict(new_data_dummies)
    # הדפסת התוצאה
    #print(f'Predicted value for the new data: {new_prediction}')
    dict_best_model['decision tree model filled all data'] = accuracy
    #print(f'evulate model : dicision tree model - acc {accuracy} , f1 {f1} , precision {precision}')
    return model, accuracy ,cm, pd.DataFrame(new_prediction , columns=[target]) , dict_best_model



##############################################################################################################################################
##############################################################################################################################################
'''
ממיר עמודת תאריך לפורמט מספרי עם יום, חודש ושנה.  
מזהה מפריד תאריך אוטומטית ומטפל בשגיאות המרה.
'''
def convert_to_datetime(df, column_name, separator='-'):
    df[column_name] = df[column_name].astype(str)
    if df[column_name].str.contains(r'\.', regex=True).any():
        separator = '.'
    elif df[column_name].str.contains(r'\\', regex=True).any():
        separator = '\\'
    else:
        separator = '-'
    try:
        # מפרידים את התאריך לחלקים (יום, חודש, שנה)
        df[['Year', 'Month', 'Day']] = df[column_name].str.split(separator, expand=True)

        # הופכים את העמודות לנתונים מספריים (אם הם לא כבר ככה)
        df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
        df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

        # מוחקים את עמודת התאריך המקורית
        df = df.drop(columns=[column_name])

    except Exception as e:
        print(f"Error occurred while converting date: {e}")
    return df


##############################################################################################################################################
##############################################################################################################################################
'''
מאמנת שלושה מודלים (Random Forest, SVM, Gradient Boosting), מחשבת את דיוקם, מציגה מטריצות בלבול ומייצרת גרפים:

ממירה עמודות קטגוריאליות למספרים בעזרת LabelEncoder.
מחלקת נתונים לסטי אימון ומבחן.
מאמנת כל מודל ובודקת דיוק, False Positives ו-False Negatives.
מציגה מטריצות בלבול עם seaborn.heatmap ושומרת אותן בתיקיית graphs.
מציירת עצים נבחרים עבור Random Forest.
מציגה את גבול ההחלטה עבור SVM.
האם יש לך שאלות או שאתה רוצה לשפר משהו בפונקציה?

'''
def run_models_and_plot(df, target):
    os.makedirs('graphs')

    # חיתוך הנתונים בין תכונות (X) ליעד (y)
    X = df.drop(columns=[target])
    y = df[target]

    # זיהוי עמודות לא מספריות (קטגוריות)
    non_numeric_columns = X.select_dtypes(include=['object']).columns

    # המרת עמודות לא מספריות לערכים מספריים
    for col in non_numeric_columns:
        if X[col].dtype == 'object':  # אם מדובר בקטגוריה
            le = LabelEncoder()  # או אפשר להשתמש ב-OneHotEncoder אם יש הרבה קטגוריות שונות
            X[col] = le.fit_transform(X[col])

    # חיתוך הנתונים לסט אימון וסט מבחן
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    # המרת y_pred (התחזיות) לערכים מספריים אם יש בהם טקסט
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    models = {
        'Random Forest': RandomForestClassifier(random_state=42),
        'SVM': SVC(random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42)
    }


    for model_name, model in models.items():
        # אימון המודל
        model.fit(X_train, y_train_encoded)

        # חיזוי על סט המבחן
        y_pred_encoded = model.predict(X_test)

        # חישוב הדיוק
        accuracy = accuracy_score(y_test_encoded, y_pred_encoded)
        f1 = f1_score(y_test_encoded, y_pred_encoded, average='weighted')
        precision = precision_score(y_test_encoded, y_pred_encoded, average='weighted')

        print(f"----------- {model_name} accuracy: {accuracy}")
        print(f"*********** {model_name} F1 Score: {f1}")
        print(f"$$$$$$$$$$$ {model_name} Precision: {precision}")

        # יצירת מטריצת בלבול
        cm = confusion_matrix(y_test_encoded, y_pred_encoded)
        print(f"Confusion Matrix for {model_name}:\n{cm}")

        # חישוב שגיאות (False Positive ו-False Negative)
        FP = cm[0][1]  # False Positive (שגיאה של סוג ראשון)
        FN = cm[1][0]  # False Negative (שגיאה של סוג שני)
        print(f"{model_name} - False Positive: {FP}")
        print(f"{model_name} - False Negative: {FN}")

        # הצגת ביצועים - מטריצת בלבול
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_ )
        plt.title(f'Confusion Matrix for {model_name}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.savefig(os.path.join('graphs',f'{model_name}_confusion_matrix.png'))
        #plt.savefig(f'{model_name}_confusion_matrix.png')
        plt.close()



        # הצגת גרף עבור Random Forest ו-Gradient Boosting (מגוון עצי החלטה)
        if model_name == 'Random Forest':

            # הגבלת שמות הפיצ'רים ל-20 תווים
            max_length = None
            truncated_feature_names = [name[:max_length] for name in X.columns]

            plt.figure(figsize=(12, 8))
            for i, tree_in_forest in enumerate(model.estimators_[:3]):  # הצגת 3 עצים ראשונים מתוך היער
                plt.subplot(1, 3, i + 1)
                plot_tree(tree_in_forest, filled=True, feature_names=truncated_feature_names, class_names=model.classes_.astype(str),
                          rounded=True,max_depth=max_d , fontsize=fontsize)
                plt.title(f"Tree {i + 1} in Random Forest")
            plt.savefig(os.path.join('graphs',f'{model_name}_decision_trees.png'))
            dict_best_model['random forest model'] = accuracy
            #plt.savefig(f'{model_name}_decision_trees.png')

            plt.close()
        # הצגת גרף עבור SVM
        elif model_name == 'SVM':
            plt.figure(figsize=(8, 6))
            plt.scatter(X_test.iloc[:, 0], X_test.iloc[:, 1], c=y_pred_encoded, cmap='coolwarm', edgecolors='k', s=50)
            plt.title('SVM Decision Boundary')
            plt.xlabel(X.columns[0])
            plt.ylabel(X.columns[1])
            plt.savefig(os.path.join('graphs', f'{model_name}_svm_boundary.png'))
            #plt.savefig(f'{model_name}_svm_boundary.png')
            dict_best_model['SVN model'] = accuracy
            plt.close()

