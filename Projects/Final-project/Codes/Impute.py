import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import confusion_matrix,accuracy_score,f1_score,precision_score

max_d = 12
fontsize = 3

dict_best_model = {}
os.makedirs('decision trees', exist_ok=True)
os.makedirs('output data', exist_ok=True)
##############################################################################################################################################
##############################################################################################################################################
'''
ממלא ערכים חסרים בעמודות קטגוריאליות לפי אסטרטגיה מוגדרת.
משתמש ב-SimpleImputer להשלמת ערכים חסרים כגון None או NaN.
'''

print(f'[parameters : max deeps = {max_d} , fontsize = {fontsize}]')
print('='*444)
#🍻
def fill_missing_categorical_values(df, strategy='most_frequent'):
    # המרת None ל-nan
    df = df.replace({None: np.nan})

    # יצירת SimpleImputer עבור עמודות קטגוריאליות
    imputer = SimpleImputer(strategy=strategy, fill_value='missing')

    # התאמת האימפוטר ל-DataFrame
    filled_array = imputer.fit_transform(df)
    df = pd.DataFrame(filled_array, columns=df.columns)

    columns = df.columns
    # הצגת ערכי המילוי שנבחרו
    for col, fill_value in zip(columns, imputer.statistics_):
        print(f"column {col} filled by :  {fill_value}")
    # החזרת DataFrame ממולא
    return df


#decision_tree_model(filled_df, target)

##############################################################################################################################################
##############################################################################################################################################
#🍻
'''
מחלק את הנתונים לשתי קבוצות: אחת עם ערכים חסרים בעמודת היעד ואחת בלי.
מאפשר טיפול נפרד בנתונים עם ובלי ערך יעד.
'''
def split_by_target_null(df):
    df_null_target = df[df[target].isnull()]
    df_not_null_target = df[df[target].notnull()]
    return df_null_target, df_not_null_target


##############################################################################################################################################
##############################################################################################################################################
'''
מאמן מודל עץ החלטה לחיזוי ערכים חסרים בעמודת היעד.
מציג מטריצת בלבול, דיוק המודל, ותרשים עץ החלטה.
'''
#🍻
def tree_model(df,df_null, target,name):
    df_not_target = df.drop(columns=[target])
    df_null_not_target = df_null.drop(columns=[target]) # this df has null in target

    df_combined = pd.concat([df_not_target, df_null_not_target])
    df_combined_dummies = pd.get_dummies(df_combined)

    df1_dummies = df_combined_dummies.iloc[:len(df)]
    df2_dummies_ob = df_combined_dummies.iloc[len(df):]

    X = df1_dummies
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    print(f'Confusion Matrix:\n{cm}')

    accuracy = accuracy_score(y_test, y_pred)
    #predict for df_null
    df_2_predict = model.predict(df2_dummies_ob)

    df_null.loc[:, target] = df_2_predict

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
    plt.savefig(os.path.join('decision trees',f'tree of {name} for predict missing target.png'))

    dict_best_model['decision tree model missing data'] = accuracy
    return model, accuracy , df_null

##############################################################################################################################################
##############################################################################################################################################
#🍻
'''
מאמן מודל עץ החלטה על הנתונים המלאים ומחשב דיוק.
חוזה ערכים לנתונים חדשים ומציג תרשים עץ החלטה.
הנתונים המלאים ללא ערכים חסרים
'''
def train_decision_tree_filled_data(df, target ,new_data):
    # המרת משתנים קטגוריאליים לדמי

    # חיתוך הנתונים בין תכונות (X) ליעד (y)
    X = df.drop(columns=[target])  # כל העמודות חוץ מהיעד
    y = df[target]  # העמודה שמייצגת את היעד

    X = pd.get_dummies(X, drop_first=True) #dummies fichers
    print(f'--------- shape of dummy : {X.shape}')
    #pd.concat([X,y]).to_csv(os.path.join('output data' , 'dummies values frame.csv'))
    #print('---------- saved dummies values frame successfully')
    # חיתוך הנתונים לסט אימון וסט מבחן
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # יצירת המודל
    model = DecisionTreeClassifier(random_state=42)

    # אימון המודל
    model.fit(X_train, y_train)

    # חיזוי על סט המבחן
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print(f'Confusion Matrix for full dataFrame : \n{cm}')


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

    try:
      # המרת התצפית החדשה לדמיות
      new_data_dummies = pd.get_dummies(new_data)
      # מוודאים שהתצפית החדשה כוללת את כל העמודות של X מהמודל, וממלאים ערכים חסרים ב-0
      new_data_dummies = new_data_dummies.reindex(columns=X.columns, fill_value=0)
      # חיזוי עם המודל
      new_prediction = model.predict(new_data_dummies)
      # הדפסת התוצאה
      #print(f'Predicted value for the new data: {new_prediction}')
      dict_best_model['decision tree model filled all data'] = accuracy
    except Exception as e:
      print(e)


    print(f'evulate model : dicision tree model - acc {accuracy} , f1 {f1} , precision {precision}')
    return model, accuracy , new_prediction



##############################################################################################################################################
##############################################################################################################################################
#🍻
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


#### running
####
df = pd.read_csv('/Users/shryqb/PycharmProjects/new_project_original/file_1/data/Merged_Bulletin_Data.csv')

data_csv = df.copy()
last_row = data_csv.iloc[-1:]  # שכפול השורה האחרונה של ה-DataFrame
data_csv = pd.concat([data_csv, last_row], ignore_index=True)  # הוספת השורה המשוכפלת כנתון חדש

data_csv.at[data_csv.index[-1], 'Severity'] = np.nan  # שינוי הערך בעמודת 'Severity' בשורה האחרונה ל-NaN

print(f'null in last row : \n{data_csv.iloc[-1]["Severity"]}')  # הדפסת הערך של 'Severity' בשורה האחרונה


features =  [
    "Date Posted", "Bulletin Id", "Bulletin KB",  "Impact", "Title",
    "Affected Product", "Component KB", "Affected Component", "Impact.1",
    "Severity.1", "Supersedes", "Reboot", "CVEs"
]

target = 'Severity' # מטרה
target_row = data_csv[target]# קבלת המטרה

data = data_csv[features] # קבלת הפיצרים מהנתונים

df_features = pd.DataFrame(data) # דאטהםריים של פיצרים
df_features = convert_to_datetime(df_features, 'Date Posted') # הפרדת התאריך מפורמט תאריך כי הוא לא עובד

df_target = pd.DataFrame(target_row , columns = [target]) # דאטהפריים של מטרה
null_target = df_target.isnull().sum() # בדיקה כמה נאלים יש במטרה
print(f'null in target row : \n{null_target}') #הדפסת נאלים של מטרה
print(f'null in all data before impute : \n{data_csv.isnull().sum()}') #הדפסת נאלים של מטרה
print('-'*222)

filled_df = fill_missing_categorical_values(df_features)# מילוי ערכים חסרים בעמודות קטגוריאליות

filled_df.to_excel(os.path.join('output data' , '1 - Data filled in featurs.xlsx'), index=False) # שמירה' ), index=False) # שמירה)

full_df_concat = pd.concat([filled_df, df_target] , axis=1) # חיבור הנתונים המלאים של מטרה ופיצרים
full_df_concat.to_excel(os.path.join('output data' , r'2 - All data filled with target.xlsx'), index=False) # שמירה

print (f'null value in full df :\n{full_df_concat.isnull().sum()}') # בדיקה אם יש נאלים בפריים החדש המלא
print('='*222)

#🧠 Using Fill Algorithm for missing data
if (null_target > 0).all():
    # פיצול הנתונים לשורות עם ובלי ערכים חסרים בעמודת היעד
    null_target_row, not_null_target_row = split_by_target_null(full_df_concat)
    null_target_row.to_csv(os.path.join('output data','divide dataframe null in severity.csv'))
    # אימון מודל עץ החלטה על הנתונים המלאים והשערת הערכים החסרים
    model, accuracy, null_target_row = tree_model(not_null_target_row, null_target_row, target, 'Severity')
    print('the accuracy of first model with part of df not null (tree model) : ')  # הדפסת הודעה על ביצועי המודל הראשון
    print(f'accuracy : {accuracy}')  # הדפסת דיוק המודל
    full_df_all = pd.concat([not_null_target_row, null_target_row], ignore_index=True)  # שילוב חזרה של הנתונים עם ובלי הערכים החסרים לאחר מילוי
else:
    print("No null values in target row, training model on full data.")  # הודעה אם אין ערכים חסרים בעמודת היעד
    full_df_all = full_df_concat  # שימוש בכל הנתונים ללא צורך בפיצול

print('='*222)  # הדפסת קו מפריד באורך 222 תווים
full_df_all.to_excel(os.path.join('output data' , r'3 - Original alldata filled with target.xlsx'), index=False) # שמירה