import pandas as pd
from sqlalchemy import create_engine, text , inspect
import warnings


warnings.filterwarnings("ignore")


import pyautogui as pg
# If the tables already exist:
# Using 'if_exists="replace"' in df.to_sql will drop the existing table and recreate it with new data.
# This means every time you run the function with the same table name, the old table is completely replaced.
#




schema_name='Sahar_project_sql'
def get_engine(schema_name='Sahar_project_sql', user='root', password='9192939495', host='localhost', port='3306'):
    """
    מחזירה אובייקט engine לפי פרטי חיבור שהוזנו.
    אם schema_name לא מוגדר, תוחזר התחברות רק לשרת ללא בסיס נתונים.
    """
    if schema_name:
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{schema_name}"
    else:
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/"
    return create_engine(connection_string, echo=False)

def clean_column_name(col_name):
    # מסירים רווחים, תווי שורה, נקודות, מחליפים בנקודתיים או תחתונות
    return col_name.replace('\n', '_').replace(' ', '_').replace('.', 'POINT').strip()

def save_excel_to_mysql(path,table_name ,schema_name=schema_name, password='9192939495' , user='root'):
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

def get_preimr_code_by_table_name(table_name, schema_name=schema_name, user='root', password='9192939495',printing = False):
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



def drop_col_by_primery(table_name, primery_kay={'ID': 1}, schema_name=schema_name,printing = False, user='root', password='9192939495'):
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


def set_pk(table_name ,schema_name=schema_name, pk_name='ID', user='root', password='9192939495'):
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


if __name__ == "__main__":
    try:
        # my data
        new_col = ['MS25-001', '5000001', 'Denial of Service', 'Security Update for Windows Defender', 'Windows 10 Version 2004 for x64-based Systems', '5000001', 'Windows Defender', 'Denial of Service', 'Important', 'MS25-001[5000001]', 'No', 'CVE-2025-0001', '2025', '5', '20', 'Important', '16']
        schema_name = 'Sahar_project_sql'
        table_name = 'Microsoft_Security'
        pk_name = 'ID'
        p_sahar = '/Users/shryqb/PycharmProjects/new_project_original/file_1/data/Merged_Bulletin_Data.xlsx'
        #remove_pk_and_column(table_name=table_name,schema_name=schema_name)


        save_excel_to_mysql(path=p_sahar, schema_name=schema_name, table_name=table_name)
        set_pk(table_name=table_name ,pk_name=pk_name ,schema_name=schema_name )

        #בודק אם המסד קיים
        exists = is_exist_schema(schema_name=schema_name)
        print('Schema exist : '+str(exists))
        i=1



    except Exception as e:
        print(e)