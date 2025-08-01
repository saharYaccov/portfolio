import random
import pandas as pd
import utils
class Teacher:
    def __init__(self):
        self.df = utils.read_sheet("Teachers")
        self.file_name = "data.xlsx"  # שם הקובץ הקיים

    def get_random_teacher_id(self):
        # בחירת מורה אקראי מתוך ה-DataFrame של המורים
        if not self.df.empty:
            teacher_id = random.choice(self.df["TeacherID"].tolist())
            return teacher_id
        else:
            raise ValueError("לא נמצאו מורים פנויים במערכת.")

    def add_teacher(self, teacher_id, teacher_name,experitse):
        # בודקים אם המרצה כבר קיים
        if teacher_id in self.df["TeacherID"].values:
            print(f"מרצה {teacher_name} כבר קיים במערכת!")
            return False

        # הוספת מרצה חדש
        new_teacher = pd.DataFrame({
            "TeacherID": [teacher_id],
            "Name": [teacher_name],
            "Expertise": [experitse],
        })

        # הוספת המרצה החדש ל-DataFrame
        self.df = pd.concat([self.df, new_teacher], ignore_index=True)

        # שמירת הנתונים לקובץ ה-Excel הקיים, מבלי למחוק את הנתונים הקיימים
        self.save_to_excel()

        print(f"המרצה {teacher_name} נוסף בהצלחה!")
        return True

    def save_to_excel(self):
        # שמירת הנתונים בקובץ ה-Excel הקיים "data.xlsx" מבלי למחוק נתונים קיימים
        with pd.ExcelWriter(self.file_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            self.df.to_excel(writer, sheet_name="Teachers", index=False)
        print(f"הנתונים נשמרו בהצלחה בקובץ {self.file_name}.")


if __name__ == "__main__":
    pass