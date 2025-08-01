import analyzer
import course
import students
import waitlist
import teacher
import pandas as pd


def main():
    # יצירת אובייקטים עבור כל מערכת
    analyzer_obj = analyzer.Analyzer()
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
            preferred_course = input("\nהכנס שם קורס להערכת התאמת מורה: ").strip()
            if analyzer.is_teacher_qualified_for_course(preferred_course):
                print(f"המורה מוסמך לקורס {preferred_course}")
            else:
                print(f"המורה לא מוסמך לקורס {preferred_course}")

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



if __name__ == "__main__":
    main()
