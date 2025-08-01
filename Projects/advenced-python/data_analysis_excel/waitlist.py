import utils
import pandas as pd

class Waitlist:
    def __init__(self):
        self.df = utils.read_sheet("Waitlist")


    def add_to_waitlist(self, student_id, course_name):
        if ((self.df["StudentID"] == student_id) & (self.df["CourseName"] == course_name)).any():
            print(f"הסטודנט {student_id} כבר ממתין לקורס {course_name}!")
            return False

        self.df = pd.concat([self.df, pd.DataFrame({
            "StudentID": [student_id],
            "CourseName": [course_name]
        })], ignore_index=True)

        print(f"הסטודנט {student_id} נוסף לרשימת ההמתנה לקורס {course_name}!")
        return True

    def get_waiting_students_for_course(self, course_name):
        return self.df[self.df["CourseName"] == course_name]["StudentID"].tolist()

    def remove_from_waitlist(self, student_id, course_name):
        self.df = self.df[~((self.df["StudentID"] == student_id) & (self.df["CourseName"] == course_name))]
        print(f"הסטודנט {student_id} הוסר מרשימת ההמתנה לקורס {course_name}!")






if __name__ == "__main__":
    pass