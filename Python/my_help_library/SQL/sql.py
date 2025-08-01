"""
MySQL Database Utilities with SQLAlchemy and Pandas

This module provides helper functions to manage MySQL databases and tables,
including reading Excel files into tables, managing primary keys, deleting rows by primary key,
and retrieving metadata and data from tables.

Functions:

- get_engine(schema_name, user, password, host, port):
    Returns a SQLAlchemy engine connected to the specified MySQL schema.

- save_excel_to_mysql(path, table_name, schema_name, user, password):
    Loads an Excel file or DataFrame into a MySQL table.
    Creates the database schema if it doesn't exist.
    Replaces the table if it already exists.

- get_preimr_code_by_table_name(table_name, schema_name, user, password, printing):
    Retrieves column names and primary key columns of a specified table.

- drop_col_by_primery(table_name, primery_kay, schema_name, printing, user, password):
    Deletes a row from the table identified by the primary key dictionary.

- set_pk(table_name, schema_name, pk_name, user, password):
    Adds a new AUTO_INCREMENT primary key column to a table if none exists.

- get_col_info(table_name, col_name, schema_name, user, password):
    Retrieves column-level statistics such as data type, null count, unique values, and basic numeric stats.

- get_row_info(table_name, id_value, id_column, schema_name):
    Retrieves a row from a table by primary key value.

- is_exist_schema(schema_name, user, password):
    Checks if a database schema exists on the MySQL server.

- is_exist_table(schema_name, table_name):
    Checks if a table exists within a given schema.

- add_row_by_pk(schema_name, table_name, pk_columns, column_add):
    Inserts a new row into a table if a row with the same primary key does not already exist.

- clean_column_name(col_name):
    Cleans column names by replacing spaces with underscores and dots with 'POINT'.

- get_col_types(table_name, schema_name):
    Returns a dictionary with column names as keys and their MySQL types as values.

Usage:
- Typical usage involves creating the engine, loading Excel data, managing primary keys,
  and querying or modifying table data programmatically.

Dependencies:
- pandas
- sqlalchemy
- pymysql
- pyautogui (imported but not used in code snippet)
"""


import pandas as pd
from sqlalchemy import create_engine, text , inspect


import pyautogui as pg
# If the tables already exist:
# Using 'if_exists="replace"' in df.to_sql will drop the existing table and recreate it with new data.
# This means every time you run the function with the same table name, the old table is completely replaced.
#

from sqlalchemy import create_engine



def get_engine(schema_name='project_database', user='root', password='9192939495', host='localhost', port='3306'):
    """
    מחזירה אובייקט engine לפי פרטי חיבור שהוזנו.
    אם schema_name לא מוגדר, תוחזר התחברות רק לשרת ללא בסיס נתונים.
    """
    if schema_name:
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema_name}"
    else:
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/"
    return create_engine(connection_string, echo=False)

def save_excel_to_mysql(path,table_name ,schema_name='project_database', password='9192939495' , user='root'):
    print(f".... 🛠️ Creating schema '{schema_name}' in table '{table_name}' for user '{user}' 👤✅")

    schema_name = schema_name
    table_name = table_name
    mysql_user = user
    mysql_password = password
    mysql_host = 'localhost'
    mysql_port = '3306'

    # קריאת הקובץ
    try:
        excel_path = path
        df = pd.read_excel(excel_path)
        print(f"✅ Excel file loaded successfully from: {excel_path}")
    except Exception as e:
        print("ERROR : cant read - ", e)
        df=path
        print('💮your path is instance of dataframe .')

        pass

    # החלפת רווחים בנקודתיים ושינויים בשמות העמודות
    def clean_column_name(col_name):
        return col_name.replace(' ', '_').replace('.', 'POINT')

    df.rename(columns=clean_column_name, inplace=True)

    # יצירת חיבור למנוע MySQL דרך SQLAlchemy
    connection_string = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/"
    engine = create_engine(connection_string, echo=False)

    # יצירת הסכימה (Database) אם לא קיימת
    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{schema_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))
            print(f"🍻 database - {schema_name} created . ")
    except Exception as e:
        print("ERROR : cant create database - ", e)
        return

    # מחברים מחדש עם הסכימה (database) כדי לכתוב את הטבלה
    connection_string_db = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{schema_name}"
    engine_db = create_engine(connection_string_db, echo=False)

    # שמירת הנתונים לטבלה - אם הטבלה קיימת, מוחקים ומחליפים (replace)
    try:
        df.to_sql(name=table_name, con=engine_db, if_exists='replace', index=False)
        print(f"✅ Table '{table_name}' was successfully saved in schema '{schema_name}'. 💾🎉")
    except Exception as e:
        print("שגיאה בשמירת הטבלה:", e)

def get_preimr_code_by_table_name(table_name, schema_name='project_database', user='root', password='9192939495',printing = False):
    try:
        engine = get_engine(schema_name=schema_name, user=user, password=password)
        inspector = inspect(engine)

        # כל העמודות
        columns = inspector.get_columns(table_name)
        col_names = [col['name'] for col in columns]

        # המפתח הראשי (אם קיים)
        pk_info = inspector.get_pk_constraint(table_name)
        pk_columns = pk_info.get('constrained_columns', [])
        if printing:
            print(f"📌 Columns in table '{table_name}': {col_names}")
            print(f"🔑 Primary key(s): {pk_columns}")

        return {'columns': col_names, 'pk': pk_columns}

    except Exception as e:
        print("⚠️ Error getting primary key or columns:", e)
        return None



def drop_col_by_primery(table_name, primery_kay={'ID': 1}, schema_name='project_database',printing = False, user='root', password='9192939495'):
    engine = get_engine(schema_name=schema_name, user=user, password=password)
    dels = None
    pk = get_preimr_code_by_table_name(table_name=table_name,schema_name=schema_name)
    if len(pk['pk'])==0 :
        return False
    try:
        col_name, val = list(primery_kay.items())[0]
        with engine.begin() as conn:  # 'begin' פותח טרנזקציה עם commit אוטומטי בסיום
            delete_stmt = text(f"DELETE FROM `{table_name}` WHERE `{col_name}` = :val")
            result = conn.execute(delete_stmt, {"val": val})
            if result.rowcount==1:
                dels=True
            elif result.rowcount==0:
                dels = False
            if printing:
                print(f"🗑️ Deleted {result.rowcount} row(s) from '{table_name}' where {col_name}={val}")
        return  dels
    except Exception as e:
        print("⚠️ Error deleting by primary key:", e)


def set_pk(table_name ,schema_name='project_database', pk_name='ID', user='root', password='9192939495'):
    try:
        engine = get_engine(schema_name=schema_name, user=user, password=password)
        with engine.connect() as conn:
            inspector = inspect(engine)


            dict_primary = get_preimr_code_by_table_name(table_name=table_name, schema_name=schema_name)
            current_pks = dict_primary['pk']


            if current_pks:
                print(f"✅ Table '{table_name}' already has a primary key defined: {current_pks} – no action taken.")
                return

            # חיפוש שם עמודה ייחודי להוספה, לדוגמה set_id_pk1, set_id_pk2 ...
            existing_columns = [col['name'] for col in inspector.get_columns(table_name)]
            new_col_name = pk_name
            while new_col_name in existing_columns:
                new_col_name = pk_name

            # הוספת עמודה חדשה מסוג INT AUTO_INCREMENT NOT NULL
            conn.execute(text(f"""
                ALTER TABLE `{table_name}`
                ADD COLUMN `{new_col_name}` INT NOT NULL AUTO_INCREMENT UNIQUE
            """))

            # הגדרת העמודה החדשה כמפתח ראשי
            conn.execute(text(f"""
                ALTER TABLE `{table_name}`
                ADD PRIMARY KEY (`{new_col_name}`)
            """))

            print(f"✅ Added new primary key '{new_col_name}' to table '{table_name}'")

    except Exception as e:
        print(f"❌ Error setting primary key: {e}")

import pandas as pd

def get_col_info(table_name, col_name, schema_name='project_database', user='root', password='9192939495'):
    try:
        engine = get_engine(schema_name=schema_name, user=user, password=password)
        with engine.connect() as conn:
            df = pd.read_sql_table(table_name, con=engine)

        if col_name not in df.columns:
            raise ValueError(f"Column '{col_name}' not found in table '{table_name}'.")

        col_data = df[col_name]

        stats = {
            "Data Type": str(col_data.dtype),
            "Number of Nulls": col_data.isnull().sum(),
            "Number of Unique Values": col_data.nunique()
        }

        # עמודות מספריות – הוספת סטטיסטיקות
        if pd.api.types.is_numeric_dtype(col_data):
            desc = col_data.describe()
            stats.update({
                "Count": desc.get("count", None),
                "Mean": desc.get("mean", None),
                "Standard Deviation": desc.get("std", None),
                "Minimum": desc.get("min", None),
                "25th Percentile": desc.get("25%", None),
                "50th Percentile (Median)": desc.get("50%", None),
                "75th Percentile": desc.get("75%", None),
                "Maximum": desc.get("max", None)
            })
        else:
            # קטגורית – הצגת עד 10 ערכים ייחודיים
            unique_vals = col_data.dropna().unique()[:3]
            stats["Top 10 Unique Values"] = list(unique_vals)

        # הפיכת הסטטיסטיקה לסדרה
        stats_series = pd.Series(stats, name=col_name)


        return stats_series, col_data

    except Exception as e:
        print("⚠️ Error getting column info:", e)
        return None


def get_row_info(table_name, id_value, id_column='ID', schema_name='project_database'):
    try:
        engine = get_engine(schema_name=schema_name)
        with engine.connect() as conn:
            df = pd.read_sql_table(table_name, con=engine)

        if id_column not in df.columns:
            raise ValueError(f"⚠️ Column '{id_column}' not found in table '{table_name}'.")

        # איתור השורה לפי הערך ב-id_column
        row = df[df[id_column] == id_value]

        if row.empty:
            raise ValueError(f"⚠️ Row with {id_column} = {id_value} not found in table '{table_name}'.")

        # ניקח רק את השורה הראשונה אם יש יותר מאחת עם אותו ID

        return row
    except Exception as e:
        print("⚠️ Error getting row info:", e)
        return None
def is_exist_schema(schema_name,user='root', password='9192939495'):
    try:
        # התחברות לשרת MySQL ללא סכימה מסוימת
        #engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}')
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES;"))
            databases = [row[0] for row in result]

        if schema_name in databases:
            return True
        else:
            raise False

    except Exception as e:
        raise Exception(f"שגיאה בבדיקת הסכימה: {e}")
def is_exist_table(schema_name,table_name):
    try:
        # התחברות לשרת MySQL ללא סכימה מסוימת
        # בודק אם הטבלה קיימת
        engine = get_engine()
        query = """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = :schema_name
                  AND table_name = :table_name
                LIMIT 1;
            """
        with engine.connect() as conn:
            result = conn.execute(text(query), {
                'schema_name': schema_name,
                'table_name': table_name
            })
            count = result.scalar()
            return count > 0

    except Exception as e:
        raise Exception(f"שגיאה בבדיקת הסכימה: {e}")

def add_row_by_pk(schema_name, table_name, pk_columns, column_add):
    engine = get_engine(schema_name=schema_name)

    # נקי את שמות המפתחות במילון column_add
    clean_column_add = {clean_column_name(k): v for k, v in column_add.items()}

    # בדיקת קיום שורה עם ערכי מפתח ראשי
    where_conditions = []
    where_params = {}

    for key in pk_columns:
        clean_key = clean_column_name(key)
        if clean_key not in clean_column_add:
            print(f"❌ Missing PK column '{clean_key}' in column_add!")
            return
        where_conditions.append(f"`{clean_key}` = :{clean_key}")
        where_params[clean_key] = clean_column_add[clean_key]

    where_clause = " AND ".join(where_conditions)
    check_sql = f"SELECT COUNT(*) FROM `{table_name}` WHERE {where_clause};"

    try:
        with engine.connect() as conn:
            count = conn.execute(text(check_sql), where_params).scalar()
            if count > 0:
                print(f"⚠️ Row with PK {where_params} already exists. No insert done.")
                return

        # הכנת INSERT
        cols = list(clean_column_add.keys())
        cols_str = ", ".join([f"`{col}`" for col in cols])
        placeholders = ", ".join([f":{col}" for col in cols])
        insert_sql = f"INSERT INTO `{table_name}` ({cols_str}) VALUES ({placeholders});"

        with engine.begin() as conn:
            conn.execute(text(insert_sql), clean_column_add)
            print(f"✅ Row inserted into `{table_name}` successfully.")

    except Exception as e:
        print(f"❌ Error: {e}")

def clean_column_name(col_name):
    return col_name.replace(' ', '_').replace('.', 'POINT')
def get_col_types(table_name,schema_name = 'project_database'):
    try:
        engine = get_engine()
        full_table_name = f"`{schema_name}`.`{table_name}`" if schema_name else f"`{table_name}`"

        query = text(f"SHOW COLUMNS FROM {full_table_name};")

        with engine.connect() as conn:
            result = conn.execute(query)
            columns_info = result.fetchall()

        # columns_info: [(Field, Type, Null, Key, Default, Extra), ...]
        col_types = {row[0]: row[1] for row in columns_info}
        return col_types

    except Exception as e:
        raise Exception(f"שגיאה בקבלת סוגי עמודות: {e}")


if __name__ == "__main__":
    try:
        # iman data
        table_namei = 'iman_table'
        schema_namei = 'Iman_project_sql'
        p_iman='/Users/shryqb/PycharmProjects/PythonProject/some_running/iman_project/Final Data.xlsx'
        save_excel_to_mysql(path=p_iman,schema_name=schema_namei,table_name=table_namei)
        dict_iman_key = get_preimr_code_by_table_name(table_name=table_namei,schema_name=schema_namei)
        if len(dict_iman_key['pk'])==0:
            set_pk(schema_name=schema_namei,table_name=table_namei)
        delsi = drop_col_by_primery(table_name=table_namei ,schema_name=schema_namei)
        print(delsi)

        '''
        # my data
        new_col = ['MS25-001', '5000001', 'Denial of Service', 'Security Update for Windows Defender', 'Windows 10 Version 2004 for x64-based Systems', '5000001', 'Windows Defender', 'Denial of Service', 'Important', 'MS25-001[5000001]', 'No', 'CVE-2025-0001', '2025', '5', '20', 'Important', '16']
        schema_name = 'Sahar_project_sql'
        table_name = 'Microsoft_Security'
        pk_name = 'ID'
        p_sahar = '/Users/shryqb/PycharmProjects/new_project_original/final_code/AA_cleaned_data/Original all not null with target.xlsx'
        #remove_pk_and_column(table_name=table_name,schema_name=schema_name)
        save_excel_to_mysql(path=p_sahar, schema_name=schema_name, table_name=table_name)
        set_pk(table_name=table_name ,pk_name=pk_name ,schema_name=schema_name )
        i=1
        dels = drop_col_by_primery(table_name=table_name,primery_kay={pk_name : i},schema_name=schema_name)
        print(dels)
        #dict_primary = get_preimr_code_by_table_name(table_name=table_name,schema_name=schema_name)
        #print(dict_primary)
        '''
    except Exception as e:
        print(e)
