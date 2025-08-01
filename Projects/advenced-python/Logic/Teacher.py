from AdvancedPythonProject.logic.Employee import Employee, Seniority
from AdvancedPythonProject.logic.Person import State

class Teacher(Employee):
    def __init__(self, name, t_id, age, phone_number, status: State, salary, seniority: Seniority, course_list: list, student_list: list):
        """
        Initializes a Teacher object with the provided attributes.
        :param name: The name of the teacher.
        :param id: The ID of the teacher.
        :param age: The age of the teacher.
        :param phone_number: The phone number of the teacher.
        :param status: The status of the teacher (must be an instance of State).
        :param salary: The salary of the teacher (must be a positive number).
        :param seniority: The seniority level of the teacher (must be an instance of Seniority).
        :param course_list: A list of courses taught by the teacher.
        :param student_list: A list of students taught by the teacher.
        """
        super().__init__(name, t_id, age, phone_number, status, salary, seniority)
        self.course_list = course_list  # List of courses
        self.student_list = student_list  # List of students

    ################################################################################################################################

    # Getter and Setter for course_list
    @property
    def course_list(self):
        return self._course_list

    @course_list.setter
    def course_list(self, course_list):
        """
        Validates that course_list is a list of strings (course names).
        """

        self._course_list = course_list


    ################################################################################################################################

    # Getter and Setter for student_list
    @property
    def student_list(self):
        return self._student_list

    @student_list.setter
    def student_list(self, student_list):
        """
        Validates that student_list is a list.
        """

        self._student_list = student_list


    ################################################################################################################################
    def show_student_in_course(self):
        for i in self._student_list:
            print(i.__str__())
        pass
    def assign_student_to_course(self,student):
        if student not in self._student_list:
            self._student_list.append(student)
            print(f"Student {student.name} assigned to courses of teacher {self.name}")
        else:
            print(f"Student {student.name} already assigned to courses of teacher {self.name}")

    def assign_grade_to_student(self, student, grade, course):
        if student not in self._student_list:
            print(f"Student {student.name} not found in the list of students assigned to teacher {self.name}")
            return False
        elif course not in self._course_list:
            print(f"Course {course} not found in the list of courses assigned to teacher {self.name}")
            return False
        else:
            if course.course_id not in student.grade_course:
                student.grade_course[
                    course.course_id] = grade  # If course_id not in grade_course, add it with the grade
            else:
                student.grade_course[course.course_id].append(grade)  # If course_id exists, append the grade
            print(f"Grade {grade} assigned to student {student.name} in course {course.name}")
            return True

    def problem_report(self):
        """
        Report a general problem with a specific course.
        :param course_name: The name of the course to report the issue for.
        """
        # דוח בעיה כללי
        problem_description = f"There is an issue . The issue needs to be reviewed and resolved as soon as possible."
        print(problem_description)
    ################################################################################################################################

    # __str__ method

    # __str__ method
    def __str__(self):
        base_str = super().__str__()  # Call to the __str__ of the Employee class
        return f'{base_str} , {self.course_list.__str__()} , {self.student_list.__str__()}'


#################################################################################################################################
    def login(self, courseList):
        """
        Interactive menu for the teacher to choose actions.
        :param courseList: List of available courses.
        """
        while True:
            print("\n=== Teacher Menu ===")
            print("1. Show students in courses")
            print("2. Assign a student to a course")
            print("3. Assign a grade to a student")
            print("4. Report an issue")
            print("g. Start the greet method (polymorphism)")
            print("0. Exit")

            try:
                choice = (input("Choose an option : "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")
                continue

            if choice == "1":
                # Show students in the teacher's courses
                self.show_student_in_course()

            elif choice == "2":
                # Assign a student to a course
                student_name = input("Enter student's name: ")
                student = next((s for s in self._student_list if s.name.lower() == student_name.lower()), None)
                if not student:
                    print(f"Student {student_name} not found.")
                    continue
                else:
                    self.assign_student_to_course(student)

            elif choice == "3":
                # Assign a grade to a student in a specific course
                student_name = input("Enter student's name: ")
                student = next((s for s in self._student_list if s.name.lower() == student_name.lower()), None)
                if not student:
                    print(f"Student {student_name} not found.")
                    continue

                course_name = input("Enter the course name: ")
                course = next((c for c in courseList if c.name.lower() == course_name.lower()), None)
                if not course:
                    print(f"Course {course_name} not found.")
                    continue

                grade = input(f"Enter grade for {student_name} in {course_name}: ")
                self.assign_grade_to_student(student, grade, course)

            elif choice == "4":
                # Report an issue
                self.problem_report()

            elif choice == 'g':
                self.greet()
            elif choice == "0":
                # Exit
                print("Exiting menu. Goodbye!")
                break

            else:
                print("Invalid choice. Please choose a valid option.")


#################################################################################################################################def greet(self):
    def greet(self):
        """
        Greet the teacher with a personalized message based on their details.
        """
        print(f"Hello, Professor {self.name}!")
        print(f"Your ID is {self.id} ")
        print(f"Your current salary is {self.salary} and you have {self.seniority.value} seniority.")

