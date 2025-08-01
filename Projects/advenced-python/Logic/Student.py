from typing import Dict
from AdvancedPythonProject.logic.Course import Course
from AdvancedPythonProject.logic.Person import Person, State
from enum import Enum

class Registered_Status(Enum):
    REGISTERED = "registered"
    UNREGISTERED = "unregistered"

class Students(Person):
    def __init__(self, name, s_id, age, phone_number, status: State, grade_course: Dict[int, int], registered: Registered_Status):
        """
        Initializes a Student object with the provided attributes.
        :param name: The name of the student.
        :param id: The ID of the student.
        :param age: The age of the student.
        :param phone_number: The phone number of the student.
        :param status: The status of the student (must be an instance of State).
        :param grade_course: A dictionary mapping courses to grades.
        :param registered: The registration status of the student (must be an instance of Registered_Status).
        """
        super().__init__(name, s_id, age, phone_number, status)
        self.grade_course = grade_course  # Dictionary of courses and corresponding grades
        self.registered = registered  # Registered status

    ################################################################################################################################

    # Getter and Setter for grade_course
    @property
    def grade_course(self):
        return self._grade_course

    @grade_course.setter
    def grade_course(self, grade_course):
        """
        Validates that grade_course is a dictionary where the keys are instances of Course
        and the values are integers or floats (grades).
        """
        if all(isinstance(course_id, int) and isinstance(grade, (int, float)) for course_id, grade in grade_course.items()):
            self._grade_course = grade_course
        else:
            raise ValueError("grade_course must be a dictionary where the keys are instances of Course and the values are numbers (int or float).")

    ################################################################################################################################

    # Getter and Setter for registered
    @property
    def registered(self):
        return self._registered

    @registered.setter
    def registered(self, register):
        """
        Validates that registered is an instance of Registered_Status.
        """
        if isinstance(register, Registered_Status):
            self._registered = register
        else:
            raise ValueError("registered must be an instance of Registered_Status.")
#פולימורפיזם!!!!!!!!!!!!!!!!
    ################################################################################################################################

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        """
        Validates and sets the age for Student (between 18 and 40).
        """
        if 18 <= age <= 40:
            self._age = age
        else:
            raise ValueError("Age for student must be between 18 and 40.")

    ################################################################################################################################
    def login(self,queue_all_):
        while True:
            try:
                print("\n")
                print('=' * 188)
                print("--- * Student manu * ---")
                print("1. Show Grades")
                print("2. Show Place in Queue")
                print("g. Start the greet method (polymorphism)")
                print("0. Exit")

                choice = input("Enter your choice: ")

                if choice == '1':
                    # תבקש את רשימת הקורסים ותעביר אותם למתודת show_grade
                    list_courses = self.grade_course
                    self.show_grade(list_courses)
                elif choice == '2':
                    # תבקש את רשימת התורים ותעביר אותם למתודת show_place_in_queue
                    queue_list =  queue_all_
                    self.show_place_in_queue(queue_list)
                elif choice == 'g':
                    self.greet()
                elif choice == '0':
                    print("Exiting...")
                    break  # יוצא מהלולאה אם נבחרה אופציה זו
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error in login: {e}")
                continue
        pass

    def show_grade(self,list_courses):
        #print(f'grade of {self.name} [course_id,grade] - {self._grade_course.__str__()}')
        for key,val in self._grade_course.items():
            for course in list_courses:
                if course._course_id == key:
                    print(f'Student {self.name} grade in course {course.name} is {val}')
        return self.grade_course
    def show_place_in_queue(self,queueList):
        mon = 0
        for queue_ in queueList:
            for stu in queue_.queue:
                try:
                    if stu.name == self.name:
                        print(f"Student {self.name} is at position {queue_.queue.index(stu) + 1} found in queue of {queue_.course_of_queue.name}")
                        mon+=1

                except Exception as e:
                    #print(f"Error in show_place_in_queue: {e}")
                    continue
        if mon==0:
            print(f"Student {self.name} not found in queue of {queue_.course_of_queue.name}")
            return False
        else:
            return True



    ################################################################################################################################

    # __str__ method
    def __str__(self):
        base_str = super().__str__()  # Call to the __str__ of the Person class
        grade_course_str = ', '.join(f"{course}: {grade}" for course, grade in self.grade_course.items())  # Format course and grade pairs
        return f"{base_str}, Courses and Grades: [{grade_course_str}], Registration Status: {self.registered.value}"

    def greet(self):
        """
        A personalized greeting for the Student.
        Displays details of the student, including name, ID, age, phone number, status,
        courses with grades, and registration status.
        """
        courses_info = ', '.join(f"{course_id}: {grade}" for course_id, grade in self.grade_course.items())
        greeting = f"Hello, my name is {self.name}. I am {self.age} years old, and my ID is {self.id}. " \
                   f"My phone number is {self.phone_number}. My status is {self.status}. " \
                   f"I am registered in the following courses with grades: {courses_info}. " \
                   f"My current registration status is {self.registered.value}."
        print(greeting)
        return greeting
