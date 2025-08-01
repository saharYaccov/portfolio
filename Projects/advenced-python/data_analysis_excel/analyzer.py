import pandas as pd
import course
import students
import waitlist
import teacher
from datetime import datetime
class Analyzer:
    def __init__(self):
        self._courses = course.Course()
        self._students = students.Students()
        self._waitlist = waitlist.Waitlist()
        self._teacher = teacher.Teacher()
        self.file_name = "data.xlsx"


# איחוד בן הטבלאות סטודנטים, תור וקורסים
    def marge_sheets_course_and_waitlist_and_students(self):
        merge_tables_step1 = pd.merge(self._courses.df, self._waitlist.df, on = "CourseID")
        merge_tables =pd.merge(merge_tables_step1, self._students.df, on = "StudentID")
        return merge_tables

# נשתמש במילון על מנת להחזיר את רשימת הסטודנטים ברשימת ההמתנה לקורס
    def get_waiting_students_for_full_courses(self):
        full_courses, _ = self._courses.get_courses_full_and_Unfull_lists()
        marge_table = self.marge_sheets_course_and_waitlist_and_students()
        student_waitlist = dict()
        # מעבר על כל הקורסים המלאים
        for course_name in full_courses:
            course_data = marge_table[marge_table["CourseName"] == course_name]
            # הוספת סטודנטים למילון אם הם ברשימת המתנה
            for _, row in course_data.iterrows():
                # רק אם הסטודנט נמצא ברשימת המתנה לקורס
                student_id = row["StudentID"]
                student_name = row["Name"]
                student_waitlist[student_id] = student_name
        return student_waitlist

    def register_student_to_course(self, student_id, course_id, course_name):
        merged_table = self.marge_sheets_course_and_students()  # ממזג את הנתונים
        condition = merged_table["CourseName"] == course_name  # איתור שורה המתאימה לקורס

        if not merged_table.loc[condition].empty:
            course_row = merged_table.loc[condition].iloc[0]  # לוקח את השורה הראשונה

            if course_row["RegisteredStudents"] < course_row["Capacity"]:
                # יש מקום בקורס → נרשום את הסטודנט
                self._courses.df.loc[condition, "RegisteredStudents"] += 1
                print(f"הסטודנט {student_id} נרשם בהצלחה לקורס {course_name}!")
            else:
                # הקורס מלא → נוסיף לרשימת המתנה ונעדכן תאריך
                request_date = datetime.today().strftime('%Y-%m-%d')  # תאריך כניסה להמתנה
                new_waitlist_entry = pd.DataFrame({
                    "StudentID": [student_id],
                    "CourseID": [course_id],
                    "RequestDate": [request_date]
                })
                # הוספת הסטודנט לרשימת המתנה
                self._waitlist.df = pd.concat([self._waitlist.df, new_waitlist_entry], ignore_index=True)
                print(f"הקורס {course_name} מלא. הסטודנט {student_id} נוסף לרשימת המתנה בתאריך {request_date}.")

                # עדכון הרשימה לקובץ Excel
                self._waitlist.df.save_to_excel()

            # שמירת הנתונים בקובץ DATA
            self._courses.df.save_to_excel()

        else:
            print(f"קורס {course_name} לא נמצא במערכת.")

    def save_to_excel(self):
        # שמירת הנתונים בקובץ ה-Excel הקיים "data.xlsx"
        with pd.ExcelWriter(self.file_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            # שמירה של רשימת המתנה לקובץ
            self._waitlist.df.to_excel(writer, sheet_name="Waitlist", index=False)
            # שמירה של הקורסים לקובץ
            self._courses.df.to_excel(writer, sheet_name="Courses", index=False)
            print(f"הנתונים נשמרו בהצלחה בקובץ {self.file_name}.")

    def get_min_age_for_course(self):
        # קריאה לטבלת הקורסים עם רשימת ההמתנה והסטודנטים
        courses_list = self._courses.df
        # בדיקה האם עמודת "MinAge" קיימת בטבלה
        if "MinAge" not in self._courses.df.columns:
            print("️ שגיאה: עמודת MinAge לא נמצאה בטבלה המאוחדת.")
            return {}

        # המרת עמודת "MinAge" לערכים מספריים (אם יש ערכים חסרים - נמלא ב-0)
        courses_list["MinAge"] = pd.to_numeric(courses_list["MinAge"], errors='coerce').fillna(0).astype(int)

        # קיבוץ לפי קורס ומציאת הגיל המינימלי עבור כל קורס
        min_age_per_course = courses_list.groupby("CourseName")["MinAge"].min()

        # החזרת התוצאה כמילון: שם קורס => גיל מינימלי
        return min_age_per_course.to_dict()

    def marge_sheets_course_and_Teachers(self):
        merge_tables_tc = pd.merge(self._teacher.df, self._courses.df, on="TeacherID")
        return merge_tables_tc

    def is_teacher_qualified_for_course(self, course_name):
        # ממזג את הטבלאות קורסים ומורים
        merge_tables_tc = self.marge_sheets_course_and_Teachers()

        # מציאת המורה המתאים לקורס על פי ההתמחות
        qualified_teachers = merge_tables_tc[
            merge_tables_tc["Expertise"].str.contains(course_name, case=False, na=False)]

        if not qualified_teachers.empty:
            # לוקח את המורה הראשון שיכול ללמד את הקורס
            teacher_id = qualified_teachers.iloc[0]["TeacherID"]

            # עדכון טבלת Courses כך שהמורה ישובץ לקורס
            condition = self._courses.df["CourseName"] == course_name
            self._courses.df.loc[condition, "TeacherID"] = teacher_id

            # שמירת הנתונים חזרה לקובץ DATA
            self._courses.save_to_excel()

            print(f"המורה עם מזהה {teacher_id} שובץ בהצלחה לקורס {course_name}!")
            return True
        else:
            print(f"אין מורה מוסמך לקורס {course_name}")
            return False

    def add_student_to_course(self):
        _, not_full_courses = self._courses.get_courses_full_and_Unfull_lists()
        course_characteristics = self.get_min_age_for_course()
        added_students = {}
        not_added_students = {}

        for _, student in self._students.df.iterrows():
            student_id = student["StudentID"]
            student_name = student["Name"]
            preferred_course = student["PreferredCourse"]
            age = student["Age"]

            assigned = False  # דגל לפיו נוודא אם הסטודנט שובץ לקורס
            rejection_reason = []  # רשימת סיבות דחייה

            # בדיקת הקורס המועדף
            if preferred_course in course_characteristics:
                min_age = course_characteristics[preferred_course]
                if age < min_age :
                    rejection_reason.append("גיל נמוך מדי לקורס המועדף")
                elif preferred_course not in not_full_courses:
                    rejection_reason.append("אין מקום בקורס המועדף")
                elif not self._courses.get_courses_is_in_available_places(preferred_course):
                    rejection_reason.append("אין מקום פנוי בקורס המועדף")
                elif not self.is_teacher_qualified_for_course(preferred_course):
                    rejection_reason.append("מורה לא מוסמך לקורס המועדף")
                else:
                    if age >= min_age :
                        # אם כל התנאים מתקיימים, הוסף את הסטודנט לקורס המועדף
                        added_students[student_id] = [student_name, preferred_course]
                        assigned = True

            # אם לא הוקצה קורס מועדף, חיפוש קורס חלופי
            if not assigned:
                for course, min_age in course_characteristics.items():
                    if age < min_age:
                        continue  # גיל נמוך מדי לקורס זה
                    if course not in not_full_courses:
                        continue  # הקורס מלא
                    if not self._courses.get_courses_is_in_available_places(course):
                        continue  # אין מקום בקורס זה
                    if not self.is_teacher_qualified_for_course(course):
                        continue  # מורה לא מוסמך לקורס זה

                    # מצאנו קורס מתאים, משבצים את הסטודנט
                    added_students[student_id] = [student_name, course]
                    assigned = True
                    break

            # אם לא נמצא שיבוץ בכלל, הסטודנט ללא הקצאה לקורס
            if not assigned:
                if not rejection_reason:
                    rejection_reason.append("לא נמצאה התאמה לקורס כלשהו")
                not_added_students[student_id] = [student_name, preferred_course, ", ".join(rejection_reason)]

        return added_students, not_added_students

    def open_class_overflow(self, not_added_students):
        class_overflow = dict()

        # בדיקת מספר הסטודנטים שלא שובצו
        if len(not_added_students) >= 30:
            print("\nיש יותר מ-30 תלמידים שלא שובצו לקורסים. יש לפתוח קורס חירום.")
            print("עלות פתיחת קורס החירום: 500$")

            # הפקת מזהי סטודנטים מרשימת not_added_students
            not_added_ids = list(not_added_students.keys())

            # סינון הסטודנטים על פי מזהה ייחודי (StudentID)
            emergency_students = self._students.df[self._students.df["StudentID"].isin(not_added_ids)]

            for _, student in emergency_students.iterrows():
                student_id = student["StudentID"]
                student_name = student["Name"]
                class_overflow[student_id] = [student_name, "קורס חירום"]

        return class_overflow

    def save_report_to_excel(self, added_students, not_added_students, class_overflow):
        # גיליון 1: תלמידים ששובצו לקורסים
        if added_students:
            added_students_df = pd.DataFrame(
                [
                    {"StudentID": student_id, "Name": details[0], "AssignedCourse": details[1]}
                    for student_id, details in added_students.items()
                ]
            )
        else:
            added_students_df = pd.DataFrame()

        # גיליון 2: תלמידים שלא שובצו וסיבת הדחייה
        if not_added_students:
            not_added_students_df = pd.DataFrame(
                [
                    {
                        "StudentID": student_id,
                        "Name": details[0],
                        "PreferredCourse": details[1],
                        "RejectionReason": details[2],
                    }
                    for student_id, details in not_added_students.items()
                ]
            )
        else:
            not_added_students_df = pd.DataFrame()

        # גיליון 3: קורסים חדשים שנפתחו (קורסי חירום)
        if class_overflow:
            class_overflow_df = pd.DataFrame(
                [
                    {"StudentID": student_id, "Name": details[0], "NewCourse": details[1]}
                    for student_id, details in class_overflow.items()
                ]
            )
        else:
            class_overflow_df = pd.DataFrame()

        # כתיבת הנתונים לקובץ Excel עם שלושה גיליונות
        try:
            with pd.ExcelWriter("Course_Assignment_Report.xlsx", engine="xlsxwriter") as writer:
                # גיליון 1: תלמידים ששובצו לקורסים
                added_students_df.to_excel(writer, sheet_name="Assigned Students", index=False)

                # גיליון 2: תלמידים שלא שובצו וסיבת הדחייה
                not_added_students_df.to_excel(writer, sheet_name="Not Assigned Students", index=False)

                # גיליון 3: פרטים על קורסים חדשים שנפתחו
                class_overflow_df.to_excel(writer, sheet_name="New Courses", index=False)

            print("הדוח נשמר בהצלחה כקובץ Excel: Course_Assignment_Report.xlsx")
        except Exception as e:
            print(f"שגיאה בשמירת הקובץ: {e}")

if __name__ == "__main__":
        analyzer = Analyzer()
        courses_obj = course.Course()
        students_obj = students.Students()
        waitlist_obj = waitlist.Waitlist()
        teacher_obj = teacher.Teacher()
        added_students = {}  # ניהול משתנים לקבצים
        not_added_students = {}
        print("----- מערכת ניתוח נתונים -----")
        while True:
            pd.read_excel("data.xlsx")
            print(
                "\nבחר פעולה: \n"
                "(1) רשימת סטודנטים הממתינים לקורסים מלאים\n"
                "(2) גיל מינימלי לכל קורס\n"
                "(3) התאמת מורה לקורס\n"
                "(4) הוספת סטודנטים לקורסים\n"
                "(5) שמירה לקובץ Excel\n"
                "(6) רשימת קורסים פנויים \n"
                "(7) הוספת סטודנט חדש \n"
                "(8) הוספת קורס חדש \n"
                "(9) הוספת מרצה חדש \n"
                "(10) יציאה מהמערכת \n"
            )

            # קלט עבור בחירת פעולה
            choice = input("הכנס מספר פעולה: ").strip()

            # טיפול בבחירות
            if choice == "1":
                print("\n--- סטודנטים ברשימת המתנה לקורסים ---")
                waiting_students = analyzer.get_waiting_students_for_full_courses()
                if waiting_students:
                    print(waiting_students)
                else:
                    print("אין סטודנטים ברשימת המתנה לקורסים מלאים.")
                #     # for student_id, student_name in waiting_students.items():
                #     #     print(f"סטודנט {student_name} (ID: {student_id}) ברשימת המתנה")


            elif choice == "2":
                print("\n--- גיל מינימלי לכל קורס ---")
                min_ages = analyzer.get_min_age_for_course()
                if min_ages:
                    for course_name, min_age in min_ages.items():
                        print(f"קורס {course_name}: גיל מינימלי {min_age}")
                else:
                    print("אין מידע על גיל מינימלי לקורסים.")


            elif choice == "3":
                course_name = input("\nהכנס את שם המקצוע אותו המורה רוצה ללמד : ").strip()
                if analyzer.is_teacher_qualified_for_course(course_name):
                    print(f"המורה מוסמך לקורס {course_name}")
                else:
                    print(f"המורה לא מוסמך לקורס {course_name}")

            elif choice == "4":
                print("\n--- הוספת סטודנטים לקורסים ---")
                added_students, not_added_students = analyzer.add_student_to_course()

                # הצגת שיבוצים לסטודנטים שהתקבלו לקורסים
                print("\nסטודנטים שהתקבלו לקורסים:")
                print(added_students)

                # הצגת סטודנטים שלא התקבלו לקורסים
                print("\nסטודנטים שלא התקבלו לקורסים :")
                print(not_added_students)

                class_overflow = analyzer.open_class_overflow(not_added_students)
                print(class_overflow)

            elif choice == "5":
                print("\n--- שמירת נתונים לקובץ Excel ---")
                try:
                    added_students, not_added_students = analyzer.add_student_to_course()
                    # ודא שהמשתנים לא ריקים לפני השמירה
                    if not added_students or not not_added_students:
                        print("עליך להריץ קודם את האפשרות להוספת סטודנטים לקורסים (אפשרות 4).")
                    else:
                        class_overflow = analyzer.open_class_overflow(not_added_students)
                        analyzer.save_report_to_excel(added_students, not_added_students, class_overflow)
                except Exception as e:
                    print(f"שגיאה בשמירת הקובץ: {e}")

            elif choice == "6":

                print ("רשימת הקורסים הפנויים")
                _ , course_not_full =courses_obj.get_courses_full_and_Unfull_lists()
                print(course_not_full)


            elif choice == "7":
                print ("הוספת סטודנט חדש")
                student_id = input("\nהכנס מספר מזהה סטודנט: ")
                student_name = input("הכנס שם סטודנט:\n ")
                age = int(input("הכנס גיל: \n"))
                parent_email = input("הכנס מייל של אחד ההורים: ")
                perferre_course = input("הכנס קורס מועדף: ")
                if students_obj.add_student(student_id, student_name,age ,parent_email,perferre_course):
                    print(f"\nהסטודנט {student_name} נוסף בהצלחה!")

            elif choice == "8":
                print("הוספת קורס חדש")
                course_id = input("\nהכנס מספר מזהה קורס: ")
                course_name = input("הכנס שם קורס :\n ")
                teacher_id = int(input("הכנס מספר מזהה מרצה : \n"))
                capacity = int(input("הכנס כמות סטודנטים מקסימלים לקורס : \n"))
                min_age = int(input("הכנס את הגיל המינימלי לקורס : \n"))
                if courses_obj.add_course(course_id, course_name, teacher_id, capacity,min_age):
                    print(f"\nהקורס {course_name} נוסף בהצלחה!")

            elif choice == "9":
                print("הוספת מרצה חדש")
                teacher_id = input("\nהכנס מספר מזהה עבור מרצה : ")
                teacher_name = input("שם המרצה :\n ")
                Experitse = input("הכנס את התמחות המרצה : \n")
                if teacher_obj.add_teacher(teacher_id, teacher_name, Experitse):
                    print(f"\nהמרצה {teacher_name} נוסף בהצלחה!")

            elif choice == "10":
                break
            else:
                print("\nבחירה לא חוקית. נסה שוב.")


