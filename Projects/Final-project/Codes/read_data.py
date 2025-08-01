# -----------------------------------------
# 🧮 ספריות עיבוד נתונים וסטטיסטיקה
# -----------------------------------------
import os  # עבודה עם מערכת קבצים
import pandas as pd  # ניהול וניתוח טבלאות




os.makedirs('data', exist_ok=True)
Files = ['/Users/shryqb/PycharmProjects/new_project_original/file_1/Original_Data/Bulletin Search (2001 - 2008).xlsx',
         '/Users/shryqb/PycharmProjects/new_project_original/file_1/Original_Data/Bulletin Search (2008 - 2017).xlsx']  # רשימה של קבצי האימון
Data_Frame = pd.concat([pd.read_excel(file) for file in Files], ignore_index=True)    # מיזוג קבצי האימון לדאטה סט אחד

# אכיפת סדר על ידי חידוש אינדקסים
Data_Frame = Data_Frame.reset_index(drop=True)

save_dir = 'data'
excel_path = os.path.join(save_dir, 'Merged_Bulletin_Data.xlsx')
csv_path = os.path.join(save_dir, 'Merged_Bulletin_Data.csv')

# שמירת הדאטה למבנה אקסל
with pd.ExcelWriter(excel_path) as writer:
    Data_Frame.to_excel(writer, index=False, sheet_name='All Data')
Data_Frame.to_csv(csv_path, index=False)

df = pd.read_excel(excel_path)
print(df.head(4))