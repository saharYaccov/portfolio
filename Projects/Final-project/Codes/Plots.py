import os
from itertools import combinations
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats
import warnings

from wordcloud import WordCloud

warnings.filterwarnings("ignore")


excel_path = '/Users/shryqb/PycharmProjects/new_project_original/file_1/data/Merged_Bulletin_Data.xlsx'
df = pd.read_excel(excel_path)


# 3D PLOT
def encode_columns(df):
    """
    ממירה עמודות קטגוריאליות בדאטה פריים למספרים.

    df: דאטה פריים (DataFrame)
    מחזירה את הדאטה פריים עם עמודות מקודדות.
    """
    df_encoded = df.copy()  # יצירת עותק של הדאטה פריים
    encoders = {}
    encoding_map = {}
    words_encode = {}

    # קידוד עמודות קטגוריאליות
    for col in df_encoded.select_dtypes(include=['object']).columns:
        encoder = LabelEncoder()
        df_encoded[col] = encoder.fit_transform(df_encoded[col])
        encoders[col] = encoder

        # יצירת מילון מיפוי ייחודי לערכים בעמודה זו
        mapping = {label: int(i) for i, label in enumerate(encoder.classes_)}
        encoding_map[col] = mapping
        help_encode = []
        for val, code in mapping.items():
            help_encode.append(f"  '{val}'  ⇒  {code}")
        words_encode[col]=(help_encode)


    print("✅ קודדו עמודות קטגוריאליות.")
    return df_encoded, encoder ,words_encode


def generate_all_3d_plots(df):
    os.makedirs('plot_active', exist_ok=True)
    """
    מייצרת גרפים תלת-מימדיים עבור כל שילוב של שלוש עמודות מתוך דאטה פריים.

    df: דאטה פריים (DataFrame) המכיל את הנתונים.
    """
    # קידוד העמודות לפני יצירת הגרפים
    df_encoded, encoders ,words_encode  = encode_columns(df)

    # בדיקה אם יש לפחות 3 עמודות
    if len(df_encoded.columns) < 3:
        raise ValueError("יש צורך ביותר מ-2 עמודות בדאטה פריים עבור גרף תלת-מימדי.")

    # יצירת כל השילובים האפשריים של 3 עמודות
    col_combinations = combinations(df_encoded.columns, 3)

    for k,val in words_encode.items():
      print(f'encode for {k} : ')
      for i in val:
        print(i)
    # עבור כל שילוב עמודות
    for col1, col2, col3 in col_combinations:
        try:
            # יצירת גרף תלת-מימדי
            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_subplot(111, projection='3d')

            # נתונים עבור כל אחת מהעמודות
            x = df_encoded[col1]
            y = df_encoded[col2]
            z = df_encoded[col3]

            # הצגת הנתונים בגרף תלת-מימדי
            ax.scatter(x, y, z, c=z, cmap='hot')

            # כותרות לצירים
            ax.set_xlabel(f'{col1},  - x label')
            ax.set_ylabel(f'{col2},  - y label')
            ax.set_zlabel(f'{col3},  - z label' )

            # שמירת הגרף בתיקייה
            #plt.savefig(os.path.join('plot_active', f'{col1}_{col2}_{col3}.png'))
            #plt.close()  # סוגר את הגרף כדי למנוע הצגת גרפים מרובים

            print(f"✅ גרף תלת-מימדי עבור {col1}, {col2}, {col3} נוצר בהצלחה.")
            plt.savefig(os.path.join('plot_active', f'{col1}_{col2}_{col3}.png'))
            plt.show()

        except Exception as e:
            print(f"⚠️ לא ניתן ליצור גרף עבור {col1}, {col2}, {col3}. שגיאה: {e}")
            continue  # ממשיך לשילוב הבא אם יש שגיאה



# קריאה לגרפים תלת-מימדיים עבור כל שילוב של 3 עמודות
generate_all_3d_plots(df[['Severity' , 'Severity.1', 'Reboot']])


#Chi Squered Plots

def plot_chi_square_bar(results_df, top_n=10):
    """
    מצייר גרף עמודות של ערכי חי-בריבוע עבור המשתנים עם הקשרים החזקים ביותר

    Args:
        results_df (pd.DataFrame): DataFrame עם Feature_1, Feature_2 וערכי Chi2
        top_n (int): מספר הצמדים החזקים ביותר להציג

    Returns:
        None
    """
    # מיון לפי הערך הגבוה ביותר של Chi2
    sorted_results = results_df.sort_values(by="Chi2", ascending=False).head(top_n)

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=sorted_results,
        x="Chi2",
        y="Feature_1" + " - " + sorted_results["Feature_2"],
        hue="Feature_1" + " - " + sorted_results["Feature_2"],  # Assign y to hue
        palette="coolwarm",
        legend=False  # Disable the legend
    )

    plt.xlabel("Chi-Square Value")
    plt.ylabel("Feature Pairs")
    plt.title(f"Top {top_n} Strongest Chi-Square Associations")
    plt.show()

def chi_square_test(df, target_feature=None):
    """
    מחשבת חי בריבוע לכל זוג משתנים קטגוריאליים ב-DataFrame.

    Args:
        df (pd.DataFrame): מסגרת נתונים עם משתנים קטגוריאליים.
        target_feature (str, optional): משתנה יעד לבדיקה מול כל השאר (אם לא הוגדר, ייבדקו כל הצמדים האפשריים).

    Returns:
        pd.DataFrame: תוצאות מבחן חי בריבוע לכל זוג עמודות.
    """
    # סינון משתנים קטגוריאליים בלבד
    cat_columns = df.select_dtypes(include=['object', 'category']).columns
    results = []

    # אם הוגדר משתנה יעד, בודקים רק מולו
    if target_feature and target_feature in cat_columns:
        columns_to_check = [col for col in cat_columns if col != target_feature]
        pairs = [(target_feature, col) for col in columns_to_check]
    else:
        # בדיקת כל הצמדים האפשריים
        pairs = [(col1, col2) for i, col1 in enumerate(cat_columns) for col2 in cat_columns[i + 1:]]

    # חישוב חי בריבוע לכל צמד משתנים
    for col1, col2 in pairs:
        contingency_table = pd.crosstab(df[col1], df[col2])  # טבלת שכיחות
        chi2, p, dof, expected = stats.chi2_contingency(contingency_table)  # חישוב חי בריבוע
        results.append({'Feature_1': col1, 'Feature_2': col2, 'Chi2': chi2, 'p-value': p})

    return pd.DataFrame(results)


df_res=chi_square_test(df,'Severity')
print('chi test result : ')
print(df_res)
#df_res.to_csv('chi Squered values.csv')
try:
  plot_chi_square_bar(df_res)
except Exception as e:
  print(e)


# Box Plot
def box_plots(df: pd.DataFrame, target: str):
    """
    מבצע מבחן ANOVA לכל משתנה מספרי ב-df מול משתנה מטרה קטגורי ומציג גרף boxplot + barplot.

    :param df: DataFrame עם משתנים מספריים וקטגוריים.
    :param target: שם המשתנה הקטגורי (משתנה המטרה).
    """

    # בדיקה שהמשתנה המטרה קיים
    if target not in df.columns:
        raise ValueError(f"המשתנה {target} לא נמצא ב-DataFrame")

    # בדיקה שהמשתנה המטרה הוא קטגורי
    if df[target].dtype not in ['object', 'category']:
        raise ValueError("משתנה המטרה חייב להיות קטגורי")

    numeric_cols = df.select_dtypes(include=['number']).columns  # מזהה משתנים מספריים
    results = {}

    for col in numeric_cols:
        unique_values = df[target].nunique()
        if unique_values < 2:
            print(f"Skipping {col}: המשתנה המטרה מכיל רק קטגוריה אחת")
            continue

        groups = [df[col][df[target] == cat].dropna() for cat in df[target].unique()]
        stat, p_value = stats.f_oneway(*groups)
        results[col] = {'F-Statistic': stat, 'p-value': p_value}

        # יצירת גרף Boxplot
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df[target], y=df[col])
        plt.title(f'Boxplot of {col} by {target}')
        plt.xlabel(target)
        plt.ylabel(col)
        plt.xticks(rotation=45)
        plt.show()
box_plots(df=df,target='Severity')


# Pair Wise Plot


def plot_pairwise_relationships(df, target):
    """
    This function creates a pairplot to visualize pairwise relationships between numeric columns,
    encoding the target column if it's categorical.

    Args:
        df (pd.DataFrame): Input dataframe.
        target (str): Name of the target column to encode.
    """
    df_copy = df.copy()

    # Encode target column if categorical
    if df_copy[target].dtype == 'object' or str(df_copy[target].dtype).startswith('category'):
        le = LabelEncoder()
        df_copy[target] = le.fit_transform(df_copy[target])
        print(f"✅ Encoded target column '{target}' with mapping: {dict(zip(le.classes_, le.transform(le.classes_)))}")

    # Select numeric columns only
    numeric_df = df_copy.select_dtypes(include=['number'])

    # Create pairplot
    sns.pairplot(numeric_df)
    plt.suptitle('Pairwise Relationships', y=0.96)
    plt.tight_layout()

    # Save the plot in the existing directory

    plt.show()
    plt.close()


plot_pairwise_relationships(df, 'Severity')

# Correlation Plot
def plot_correlation_matrix_with_all_columns(df,target):
    """
    This function generates a heatmap of the correlation matrix for all columns in the dataframe.
    Non-numeric columns are encoded numerically before calculating the correlation matrix.

    Args:
        df (pd.DataFrame): Input dataframe.
    """
    # Copy the dataframe to avoid modifying the original
    df_encoded = df.copy()

    # Convert non-numeric columns to numeric using category encoding
    for col in df_encoded.select_dtypes(exclude='number').columns:
        df_encoded[col] = df_encoded[col].astype('category').cat.codes

    # Calculate and plot the correlation matrix
    plt.figure(figsize=(10, 8))
    correlation_matrix = df_encoded.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix (with Encoded Non-Numeric Columns)')
    plt.show()
    plt.close()
    print("✅ Correlation matrix plot saved successfully.")
    return correlation_matrix[target]
plot_correlation_matrix_with_all_columns(df,'Severity')

#Word Cloud Plot

def create_wordcloud_for_target(df, target_column):
    # ודא שהעמודה קיימת ב-DataFrame
    if target_column not in df.columns:
        print(f"עמודה {target_column} לא קיימת ב-DataFrame.")
        return

    # המרת הערכים בעמודה לטקסט
    text = ' '.join(df[target_column].dropna().astype(str))

    # יצירת מפת מילים
    wordcloud = WordCloud(width=800, height=400, background_color='white',colormap='coolwarm').generate(text)

    # הצגת המפה
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"word cloud for feature - {target_column}", fontsize=30)  # 🔵 הוספת כותרת
    plt.tight_layout(pad=0)  # אופציונלי: להקטין רווחים מסביב
    plt.show()
    print(f'🎯 cloud for {target_column} completed !')
    # שמירה לקובץ

nums = 0
create_wordcloud_for_target(df, 'Severity')
for i in df.columns:
  nums+=1
  if nums==10 :
    break
  try:
    create_wordcloud_for_target(df, i)
  except Exception as e:
    print(e)

# Dashboard X Plots
c = ['Date\nPosted', 'Bulletin\nId', 'Bulletin KB', 'Severity', 'Impact',
       'Title', 'Affected Product', 'Component KB', 'Affected Component',
       'Impact.1', 'Severity.1', 'Supersedes', 'Reboot', 'CVEs', 'Date Posted',
       'Bulletin Id']

df_fig = df.copy()
df_fig = df_fig.dropna(how='all')

dates = list(df_fig['Date\nPosted'])
severity = df_fig['Severity'].astype(str).tolist()
reboot = df_fig['Reboot'].astype(str).tolist()
impact = list(df_fig['Impact'])
encoder = LabelEncoder()
severity_encode = encoder.fit_transform(df_fig['Severity'])

print(df.dtypes)


#!pip install plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

c = ['Date\nPosted', 'Bulletin\nId', 'Bulletin KB', 'Severity', 'Impact',
       'Title', 'Affected Product', 'Component KB', 'Affected Component',
       'Impact.1', 'Severity.1', 'Supersedes', 'Reboot', 'CVEs', 'Date Posted',
       'Bulletin Id']


# יצירת פיגר עם 2 שורות ו-2 עמודות
fig = make_subplots(
    rows=2, cols=2,
    specs=[[ {"type": "scatter","colspan":2},None],
           [{"type": "bar"}, {"type": "pie"}]],
    subplot_titles=['time by severity' ,'scatter of impact','pie of reboot'],
)


# תרשים Scatter
fig.add_trace(go.Scatter(
    x=dates, y=severity,
    mode='lines+markers', name='Severity by Dates',
    marker=dict(color='black'),
    line=dict(color='skyblue'),
), row=1, col=1)

# תרשים Bar
impact_counts = df['Impact'].value_counts().sort_index()

fig.add_trace(go.Bar(
    x=impact_counts.index,                   # שמות הקטגוריות
    y=impact_counts.values,                  # מספר מופעים
    text=[f"{val}" for val in impact_counts.values],  # טקסט מעל כל עמודה
    textposition='outside',
    textfont=dict(
        size=10,
        color='black'
    ),
    marker=dict(
        color='yellow',
        line=dict(color='black', width=1)
    ),
    opacity=0.9,
    name='count of Impact'
), row=2, col=1)
# ספירה של ערכים בעמודת 'reboot'

rc = df['Reboot'].value_counts().sort_index()

# תרשים עוגה (Pie)
fig.add_trace(go.Pie(
    labels=rc.index,             # ערכים ייחודיים ממוינים
    values=rc.values,            # מספר מופעים לכל אחד
    marker=dict(colors=['blue', 'red', 'green']),
    textinfo='label+percent',    # הצגת תווית ואחוזים
    hoverinfo='label+value'      # מה שמוצג ב-hover
), row=2, col=2)


# עדכון עיצוב כללי
fig.update_layout(
    height=850,
    title_text="Security Microsoft Graphs",
    uniformtext_minsize=5,
    uniformtext_mode='hide'
)

os.makedirs('DashBoards',exist_ok=True)
fig.write_html("DashBoards/security_graphs.html")

fig.show()

