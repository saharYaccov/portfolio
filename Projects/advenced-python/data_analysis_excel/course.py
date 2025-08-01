import utils
import pandas as pd
class Course:

    def __init__(self):
        self.df = utils.read_sheet("Courses")
        self.file_name = "data.xlsx"  # שם הקובץ הקיים

        # לוודא שעבור הקובץ הנוכחי יש עמודת MinAge
        if "MinAge" not in self.df.columns:
            self.df["MinAge"] = None  # או 0 כברירת מחדל

    def add_course_class_overflow(self,course_name,capacity, teacher_id):
        if course_name in self.df["CourseName"].values:
            print(f"הקורס {course_name} כבר קיים במערכת!")
            return False

        # יצירת מזהה ייחודי לקורס
        course_id = "class overflow"

        # הוספת קורס לטבלה
        self.df = pd.concat([self.df, pd.DataFrame({
            "CourseID": [course_id],
            "CourseName": [course_name],
            "TeacherID": [teacher_id],
            "Capacity": [capacity],
            "RegisteredStudents": [0]
        })], ignore_index=True)

        print(f"הקורס {course_name} נוסף בהצלחה!")
        return True

    #
    # def add_course(self, course_id,course_name,capacity, teacher_id):
    #     if course_name in self.df["CourseName"].values:
    #         print(f"הקורס {course_name} כבר קיים במערכת!")
    #         return False
    #
    #     # הוספת קורס לטבלה
    #     new_course = pd.DataFrame({
    #         "CourseID": [course_id],
    #         "CourseName": [course_name],
    #         "TeacherID": [teacher_id],
    #         "Capacity": [capacity],
    #         "RegisteredStudents": [0]
    #     })
    #     # הוספת הסטודנט החדש ל-DataFrame
    #     self.df = pd.concat([self.df, new_course], ignore_index=True)
    #     # שמירת הנתונים לקובץ ה-Excel הקיים, מבלי למחוק את הנתונים הקיימים
    #     self.save_to_excel()
    #
    #     print(f"הקורס {course_name} נוסף בהצלחה!")
    #     return True


    def add_course(self, course_id, course_name, teacher_id,capacity,  min_age=None):
        if course_id in self.df["CourseID"].values:
            print(f"הקורס {course_name} כבר קיים במערכת!")
            return False

        # הוספת קורס לטבלה
        new_course = pd.DataFrame({
            "CourseID": [course_id],
            "CourseName": [course_name],
            "TeacherID": [teacher_id],
            "Capacity": [capacity],
            "RegisteredStudents": [0],
            "MinAge": [min_age if min_age is not None else 0]  # גיל מינימלי עם ברירת מחדל 0
        })

        # הוספת הקורס החדש ל-DataFrame
        self.df = pd.concat([self.df, new_course], ignore_index=True)

        # שמירת הנתונים לקובץ ה-Excel הקיים
        self.save_to_excel()

        print(f"הקורס {course_name} נוסף בהצלחה עם גיל מינימלי {min_age if min_age else 0}!")
        return True


    def save_to_excel(self):
        # שמירת הנתונים בקובץ ה-Excel הקיים "data.xlsx" מבלי למחוק נתונים קיימים
        with pd.ExcelWriter(self.file_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            self.df.to_excel(writer, sheet_name="Courses", index=False)
        print(f"הנתונים נשמרו בהצלחה בקובץ {self.file_name}.")


        # מתודה שמחזירה 2 רשימות, אחת עבור קורסים מלאים 2 עבור קורסים פנויים

    def get_courses_full_and_Unfull_lists(self):
        full_courses = []
        not_full_courses = []
        for idx in range(len(self.df)):
            if self.df.iloc[idx]["Capacity"] <= self.df.iloc[idx]["RegisteredStudents"]:
                # print(f'this course {self.df.iloc[idx]["CourseName"]} is full')
                full_courses.append(self.df.iloc[idx]["CourseName"])

            else:
                not_full_courses.append(self.df.iloc[idx]["CourseName"])
                # print(f'this course {self.df.iloc[idx]["CourseName"]} is available '
                #         f'and has { abs(self.df.iloc[idx]["RegisteredStudents"]-self.df.iloc[idx]["Capacity"]) } available places')
        return full_courses, not_full_courses

    def get_courses_is_in_available_places(self, course_name):
        condition = self.df["CourseName"] == course_name
        if not self.df.loc[condition, "RegisteredStudents"].empty:
            if self.df.loc[condition, "RegisteredStudents"].iloc[0] < self.df.loc[condition, "Capacity"].iloc[0]:
                self.df.loc[condition, "RegisteredStudents"] += 1
                return True
        return False



if __name__ == "__main__":
         # c = Course()
         # print ()

    # print(c.df.iloc[0])
    # print(c.df.iloc[0, 0])
    # print(c.df.iloc[0]["CourseID"])
    # print(c.get_courses_full_and_Unfull_lists())

    pass
