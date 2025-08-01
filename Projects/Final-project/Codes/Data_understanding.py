# -----------------------------------------
# 🧮 ספריות עיבוד נתונים וסטטיסטיקה
# -----------------------------------------
import os

import pandas as pd  # ניהול וניתוח טבלאות

# -----------------------------------------
# 📊 ספריות ויזואליזציה וגרפים
# -----------------------------------------

import matplotlib.pyplot as plt  # גרפים ותרשימים דו-ממדיים
import seaborn as sns  # גרפים סטטיסטיים מעוצבים

# -----------------------------------------
# 📉 יצירת דוח פרופילינג לדאטה
# -----------------------------------------

from ydata_profiling import ProfileReport  # דוח אוטומטי לניתוח נתונים


excel_path = '/Users/shryqb/PycharmProjects/new_project_original/file_1/data/Merged_Bulletin_Data.xlsx'
df = pd.read_excel(excel_path)
# קריאת קבצי ה-Testing ו-Training
df_all = df.copy()
print(f'columns names :  {df.columns}')
# הצגת המידות של המטריצות
print("=======================================================================================================================")
print(f"Training Set Shape: {df_all.shape}\n")

# הצגת סוגי הנתונים של כל עמודה ב-DataFrame
print("=======================================================================================================================")
print("DataTypes of the dataset:\n")
print(df_all.info(), "\n")


# זיהוי עמודות חסרות
print("=======================================================================================================================")
missing_columns = df_all.isna().sum()
print("Missing columns and count of NaN values:\n", missing_columns[missing_columns > 0], "\n")

# בדיקת דופליקציות בסט
print("=======================================================================================================================")
duplicates = df_all.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}\n")

# הצגת ערכים בעמודות נומריות וקטגוריאליות
print("=======================================================================================================================")
print("Distribution of values in numeric & categorical columns:\n")
print(df_all.describe(include='all'), "\n")


# בדיקת ערכים בעמודה 'Severity'
print("=======================================================================================================================")
sns.boxplot(x=df_all['Severity'].dropna())
plt.title('Incident Grade Distribution')
plt.grid()
plt.show()

# המרת עמודות תאריך לפורמט datetime
print("=======================================================================================================================")
if 'Date Posted' in df_all.columns:
    df_all['Date Posted'] = pd.to_datetime(df_all['Date Posted'], errors='coerce')

# חישוב מטריצת קורלציה עבור הנתונים
print("=======================================================================================================================")
df_numeric = df_all.select_dtypes(include=['number'])
correlation_matrix = df_numeric.corr()
sns.heatmap(correlation_matrix.round(3), annot=True, cbar=True, cmap="coolwarm", annot_kws={"size": 6})
plt.title('Correlation Matrix')
plt.grid()
plt.tight_layout()
plt.show()

# בדיקה אם יש תאריכים עתידיים בעמודת Timestamp
print("=======================================================================================================================")
min_timestamp = df_all['Date Posted'].min()
max_timestamp = df_all['Date Posted'].max()
print(f"Date Posted range: {min_timestamp} to {max_timestamp}\n")


# בדיקת ערכים ייחודיים
print("=======================================================================================================================")
print("Number of unique values:\n")
print(df_all.nunique(), "\n")

# גרף חום תרמוגרפי עבור ערכים חסרים
print("=======================================================================================================================")
sns.heatmap(df_all.isnull(), cbar=True, cmap='viridis')
plt.title('Missing Values')
plt.ylabel('Count')
plt.xlabel('Category Name')
plt.grid()
plt.tight_layout()
plt.show()

# המרת משתנים קטגוריאליים לנומריים אם יש
print("=======================================================================================================================")
if 'Category' in df_all.columns:
    df_all['Category'] = df_all['Category'].astype('category').cat.codes

# חישוב מטריצת הקורלציה אחרי המרה לנומרי
print("=======================================================================================================================")
correlation_matrix = df_all.select_dtypes(include=['number']).corr()
sns.heatmap(correlation_matrix, annot=True, cbar=True, cmap="coolwarm", annot_kws={"size": 6})
plt.title('Correlation Heatmap')
plt.grid()
plt.tight_layout()
plt.show()

def create_html_report(df):
    html_dir='Html_Report'
    os.makedirs(html_dir, exist_ok=True) # Changed from os.mkdir to os.makedirs for robustness
    profile = ProfileReport(df , title="Profile Report for the Data",explorative=True , progress_bar=True)
    file_path = os.path.join(html_dir, "Profile data.html")
    # Save the report to the specified file path
    profile.to_file(file_path)

    print(f"✅ HTML report saved successfully at: {file_path}")

create_html_report(df)
print("=======================================================================================================================")
print(f'data feature types:')
print(df.dtypes)
