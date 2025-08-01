import pandas as pd
import utils

class Students:
    def __init__(self):
        # קריאה לקובץ Excel (המשתמש בקובץ שנקרא "DATA")
        self.df = utils.read_sheet("Students")  # קריאה לגיליון "Students" בקובץ DATA
        self.file_name = "data.xlsx"  # שם הקובץ הקיים

    def add_student(self, student_id, student_name, age, parent_email,preferred_course):
        # בודקים אם הסטודנט כבר קיים
        if student_id in self.df["StudentID"].values:
            print(f"הסטודנט {student_name} כבר קיים במערכת!")
            return False

        # הוספת סטודנט חדש
        new_student = pd.DataFrame({
            "StudentID": [student_id],
            "Name": [student_name],
            "Age": [age],
            "ParentEmail" : [parent_email],
            "PreferredCourse": [preferred_course],
        })

        # הוספת הסטודנט החדש ל-DataFrame
        self.df = pd.concat([self.df, new_student], ignore_index=True)

        # שמירת הנתונים לקובץ ה-Excel הקיים, מבלי למחוק את הנתונים הקיימים
        self.save_to_excel()

        print(f"הסטודנט {student_name} נוסף בהצלחה!")
        return True

    def save_to_excel(self):
        # שמירת הנתונים בקובץ ה-Excel הקיים "data.xlsx" מבלי למחוק נתונים קיימים
        with pd.ExcelWriter(self.file_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            self.df.to_excel(writer, sheet_name="Students", index=False)
        print(f"הנתונים נשמרו בהצלחה בקובץ {self.file_name}.")


if __name__ == "__main__":
    # יצירת מופע של Students והוספת סטודנט
    s = Students()
    s.add_student("12345", "יוסי כהן", 25, "מתכנת Python")
