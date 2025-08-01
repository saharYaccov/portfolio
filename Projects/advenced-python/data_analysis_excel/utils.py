import pandas as pd


def read_sheet(_sheet_name) :
    excel_path = "data.xlsx"
    try:
        if not _sheet_name or not isinstance(_sheet_name, str):
            raise ValueError("שם הגיליון לא יכול להיות מחרוזת ריקה")
        return pd.read_excel(excel_path, sheet_name=_sheet_name)
    except ValueError as e:
        raise ValueError(f"הגליון {_sheet_name}' לא קיים בקובץ .") from e

def list_sheets_in_excel(excel_path):
    # טוען את קובץ האקסל
    try:
        xls = pd.ExcelFile(excel_path)
        # מדפיס את רשימת הגיליונות
        print(f"רשימת הגיליונות בקובץ {excel_path}:")
        print(xls.sheet_names)
    except Exception as e:
        print(f"שגיאה בטעינת הקובץ: {e}")

# קריאה לפונקציה עם נתיב הקובץ
excel_path = "data.xlsx"
list_sheets_in_excel(excel_path)
