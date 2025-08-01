import pymysql
from sqlalchemy import create_engine
import json

class sql:
    def __init__(self, host='localhost', user='root', password='newpassword'):
        self.host = host # my host
        self.user = user # my username
        self.password = password # my password
        self.connection = None # my connection , stay none - when create db , it changed
        self.cursor = None # my cursor , stay none - when create db , it changed
        self.table_name = None # my table name , stay none - when create db , it changed
        self.db_name = None # my db name , stay none - when create db , it changed


    def connect_my_db(self, db=None):

        """תחבר למסד הנתונים"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=db # when db is none in first time because we need create it
            )
            self.cursor = self.connection.cursor() # cursor variable in constructor
            self.db_name = db # db variable in constructor
            if(db!=None):
                print(f'------>>>data base name : {db} connected successfully<<------')
        except pymysql.MySQLError as e:
            print(f"==================Error connecting to MySQL: {e}")
            self.connection = None

    def create_db(self, db):
        """צור את מסד הנתונים"""
        try:
            self.connect_my_db() # connect without db
            query = f"CREATE DATABASE IF NOT EXISTS {db}" #create db
            #print(f"||Running query: ||\n{query}")  # הדפסת השאילתא
            self.cursor.execute(query)  # running query
            self.connection.commit()  # confirm connection and query connection

            print(f'------>>>data base name : {db} created successfully<<------')
            self.connect_my_db(db)  # connect with db after created
        except pymysql.MySQLError as e:
            print(f"================Error creating database: {e}")
        finally:
            if self.connection:
                self.connection.close() # close connection

    def create_table(self, table_name, def_col):
        """צור טבלה בתוך מסד הנתונים"""

        if isinstance(def_col, str):
            try:
                self.connect_my_db(self.db_name)    #connect with db

                self.table_name = table_name  # save table name

                query = f"CREATE TABLE IF NOT EXISTS {table_name} ({def_col})" # table create query
                #print(f"||Running query: ||\n{query}")  # הדפסת השאילתא
                self.cursor.execute(query)  # יצירת הטבלה
                self.connection.commit()  # אישור השאילתא
                print(f"------>>Table {table_name} created successfully.<<------")
            except pymysql.MySQLError as e:
                print(f"==============Error creating table: {e}")
        else:
            print(f'~~~~~def_col must be a string like: "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), age INT"')


    def add_value_to_table(self, table_name, df_vals, col_names):
        """הוסף רשומה חדשה לטבלה, מתאימה גם עבור DataFrame"""
        try:
            # יצירת מחרוזת של שמות העמודות
            columns = ', '.join(col_names) # create string of column name

            # לולאה על כל שורה ב-DataFrame
            for _, row in df_vals.iterrows(): # over by any row in dataFrame
                values = []
                for val in row:
                    # אם הערך None, נכניס ערך SQL מתאים (NULL)
                    if val is None or val == '':  # גם מיתרים ריקים יהפכו ל-NULL
                        values.append('NULL')
                    else:
                        values.append(f"'{str(val)}'")  # אכילת הערך כטקסט ועטיפתו במרכאות

                # יצירת מחרוזת ערכים
                values_str = ', '.join(values) # create string values from list

                # יצירת שאילתת SQL
                insert_query = f'INSERT IGNORE INTO {table_name} ({columns}) VALUES ({values_str})' # the query of insert

                # הדפסת השאילתה כדי לוודא שהיא נכונה
                #print(f"Executing query: {insert_query}")

                # ביצוע השאילתה
                self.cursor.execute(insert_query) # use query

            # Commit על מנת להחיל את השינויים
            self.cursor.connection.commit()

            print(f"Records added to {table_name} successfully.")
        except pymysql.MySQLError as e:
            print(f"Error adding record: {e}")

    def update_col_by_id(self , table_name ,  col_name_update , col_name_where , update_val , id ):
        #not working
        try:
            self.connect_my_db(self.db_name)

            update_query = f"UPDATE {table_name} SET {col_name_update} = '{update_val}' WHERE {col_name_where} = {id}"
            self.cursor.execute(update_query)
            self.connection.commit()
            print(f"Rows affected: {self.cursor.rowcount}")
            print(f"UPDATED FOR ID {id}: \n{col_name_update} updated to {update_val} for ID : {id}  in {table_name} successfully.")

        except pymysql.MySQLError as e:
            print(f"Error updating status: {e}")

    def del_col_by_id(self , table_name  , col_name_where  , id ):
        #not working
        try:
            self.connect_my_db(self.db_name)

            update_query = f"DELETE FROM {table_name} WHERE {col_name_where} = {id}"
            self.cursor.execute(update_query)
            self.connection.commit()
            print(f"Rows affected: {self.cursor.rowcount}")
            print(f'deleted id : {id} from tabla name : {table_name} successfully')

        except pymysql.MySQLError as e:
            print(f"Error updating status: {e}")




    def add_df_to_table(self, table_name, df_vals):
        """הוסף ערכים מ-DataFrame לטבלה"""
        try:
            # יצירת מחרוזת של שמות העמודות
            columns = ', '.join(df_vals.columns)  # create string of column names

            # לולאה על כל שורה ב-DataFrame
            for _, row in df_vals.iterrows():  # iterate over each row
                values = []
                for col, val in row.items():  # iterate through column and value
                    # אם הערך None, נכניס ערך SQL מתאים (NULL)
                    if val is None or val == '':  # also empty strings will be NULL
                        values.append('NULL')
                    elif isinstance(val, list):  # אם הערך הוא רשימה
                        # הפוך רשימה למחרוזת מופרדת בפסיקים
                        values.append(f"'{','.join(map(str, val))}'")
                    elif isinstance(val, dict):  # אם הערך הוא מילון
                        # הפוך מילון למחרוזת JSON
                        values.append(f"'{json.dumps(val)}'")
                    else:
                        values.append(f"'{str(val)}'")  # wrap value in quotes for SQL compatibility

                # יצירת מחרוזת ערכים
                values_str = ', '.join(values)  # create string of values from list

                # יצירת שאילתת SQL
                insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({values_str})'  # insert query

                # ביצוע השאילתא
                self.cursor.execute(insert_query)

            # Commit to apply changes
            self.connection.commit()
            print(f"Records added to {table_name} successfully.")
        except pymysql.MySQLError as e:
            print(f"Error in {table_name}\n adding records from DataFrame: {e}")


def main(tableName , df_vals , table_col_name):
    SQL_OBJ = sql(password="newpassword") # creare modlet sql
    SQL_OBJ.create_db('my_database_for_my_project')  # create db with name
    print("     ±±±")
    SQL_OBJ.create_table(tableName, table_col_name ) # create table with name and column names -- look how
    # הוסף ערכים לטבלה
    SQL_OBJ.add_value_to_table(tableName ,df_vals , df_vals.columns) # add values in dataframe -- look how

    if (tableName == 'teachers'):
        SQL_OBJ.update_col_by_id(table_name=tableName , col_name_update='Expertise',col_name_where='TeacherID' , update_val=str('Math') ,id=[1])
    print('-'*180)














'''
import pandas as pd
path = r'/Users/shryqb/PycharmProjects/AdvancedPythonProject/Sql_Con/learning_center_project_data.xlsx'
data_students = pd.read_excel(path, sheet_name='Students')
df_course = pd.read_excel(path, sheet_name='Courses')
df_waitList = pd.read_excel(path, sheet_name='Waitlist')
df_teachers = pd.read_excel(path, sheet_name='Teachers')

df_students = pd.DataFrame(data_students)
df_course = pd.DataFrame(df_course)
df_waitList = pd.DataFrame(df_waitList)
df_teachers = pd.DataFrame(df_teachers)


# יצירת טבלאות במסד נתונים והוספת נתונים
student_table_columns = "StudentID INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(100),Age INT,ParentEmail VARCHAR(100),PreferredCourse VARCHAR(100)"
main(tableName="students", df_vals=df_students, table_col_name=student_table_columns)

course_table_columns = "CourseID INT AUTO_INCREMENT PRIMARY KEY,CourseName VARCHAR(100),TeacherId INT,Capacity INT,RegisteredStudents INT"
main("courses", df_course, course_table_columns)

waitlist_table_columns = "WaitlistID INT AUTO_INCREMENT PRIMARY KEY,CourseID INT,StudentID INT,RequestDate DATE"
main("waitlists", df_waitList, waitlist_table_columns)

teacher_table_columns = "TeacherID INT AUTO_INCREMENT PRIMARY KEY,Name VARCHAR(100),Expertise VARCHAR(100)"
main("teachers", df_teachers, teacher_table_columns)




'''