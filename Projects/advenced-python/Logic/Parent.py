from typing_extensions import override

from AdvancedPythonProject.logic.Student import Students, Registered_Status
from AdvancedPythonProject.logic.Course import Course
from AdvancedPythonProject.logic.Person import Person, State
from AdvancedPythonProject.logic.Payment import Payment

class Parent(Person):
    def __init__(self, name, p_id, age, phone_number, status: State,payment:Payment, childrenList: list):
        """
        Initializes a Parent object with the provided attributes.
        :param name: The name of the parent.
        :param id: The ID of the parent.
        :param age: The age of the parent.
        :param phone_number: The phone number of the parent.
        :param status: The status of the parent (must be an instance of State).
        :param childrenList: A list of children (instances of Person).
        """
        super().__init__(name, p_id, age, phone_number, status)
        self.childrenList = childrenList  # Assign the list of children
        self.payment = payment # Assign the payment

    ################################################################################################################################

    # Getter and Setter for childrenList
    @property
    def childrenList(self):
        return self._childrenList

    @childrenList.setter
    def childrenList(self, childrenList):
        """
        Validates that the childrenList is a list and each child is an instance of Person.
        """
        self._childrenList = childrenList

    @property
    def payment(self):
        return self._payment

    @payment.setter
    def payment(self, value):
        if not isinstance(value, Payment):
            raise ValueError("Payment must be an instance of Payment class.")
        self._payment = value

    ################################################################################################################################

    def register_child_to_course_if_course_not_full(self,course:Course,courseList,queueList , childName , child_id,age,phone_number,state):
        '''
        Registers a child to a course if the course is not full, or adds them to the waitlist if the course is full.
        :param course:
        :param courseList:
        :param queueList:
        :param childName:
        :param child_id:
        :param age:
        :param phone_number:
        :param state:
        :return:
        '''
        childName = childName.lower()
        student_child = Students(childName , child_id,age,phone_number,state,{},Registered_Status.REGISTERED)
        if childName not in self.childrenList:
            print(f'cant do that , you have not child name {childName}')
            return False
        if course in courseList:
            if len(course.student_list) < course.course_size:
                for course_in_list in courseList:
                    if course == course_in_list:
                        course_in_list.student_list.append(student_child)
                        print(f"Child {childName} has been registered to course {course.name}.")
                        return True
            else:
                for queue in queueList:
                    if course == queue.course:
                        queue.add_student_to_waitlist(student_child)
                        print(f"Child {childName} has been added to waitlist for course {course.name}.")
                        return True
                queueList.append(course)
                queueList[-1].add_student_to_waitlist(student_child)



    def show_child_info(self,childName,course_list):
        childName = childName.lower()
        for course in course_list:
            course_name = course.name
            for student in course.student_list:
                if student.name.lower() == childName:
                    print(f"Child {student.name} is in course {course_name}.")
                    print(student.__str__())
                    return True

    def show_place_in_queue(self,childName ,queueList):
        childName = childName.lower()
        found = False  # Flag to check if the child is found in any queue
        for queue in queueList:
            if queue.course_of_queue.name.lower() == childName:  # Check if course matches child name
                # Loop through waitlist and find the child's position
                for idx, student in enumerate(queue.waitlist):
                    if student.name.lower() == childName:
                        print(
                            f"Child {student.name} is at position {idx + 1} in the queue for course {queue.course.name}.")
                        found = True
                        break  # Exit the loop once the child is found
                if found:
                    break  # Exit the outer loop once the child is found in any queue

        if not found:
            print(f"Child {childName} is not found in any queue.")

    def payment_report(self):
        print(self.payment.create_pay_report())

    #################################################################################################################################
    # __str__ method
    def __str__(self):
        base_str = super().__str__()  # Call to the __str__ of the Person class
        children_names =self.childrenList.__str__()
        return f"{base_str}, Children: {children_names}"

    def login(self, courseList, queueList):
        """
        Interactive menu for the parent to choose actions.
        :param courseList: List of available courses.
        :param queueList: List of courses with waitlists.
        """
        while True:
            print("\n=== Parent Menu ===")
            print("1. Register a child to a course (if not full)")
            print("2. Show child info")
            print("3. Show child's place in queue")
            print("4. View payment report")
            print("g. Start the greet method (polymorphism)")
            print("0. Exit")

            try:
                choice = (input("Choose an option : "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")
                continue

            if choice == '1':
                # Register a child to a course
                course_name = input("Enter the course name: ")
                child_name = input("Enter your child's name: ")
                child_id = input("Enter your child's ID: ")
                age = int(input("Enter your child's age: "))
                phone_number = input("Enter your child's phone number: ")
                state = State.state_student

                # Find the course by name
                course = next((c for c in courseList if c.name.lower() == course_name.lower()), None)
                if course is None:
                    print(f"Course {course_name} not found.")
                    continue
                else:
                    self.register_child_to_course_if_course_not_full(course, courseList, queueList, child_name, child_id,
                                                                 age, phone_number, state)


            elif choice == "2":
                # Show child info
                child_name = input("Enter your child's name: ")
                self.show_child_info(child_name, courseList)

            elif choice == "3":
                # Show child's place in queue
                child_name = input("Enter your child's name: ")
                self.show_place_in_queue(child_name, queueList)

            elif choice == "4":
                # View payment report
                self.payment_report()
            elif choice == 'g':
                self.greet()

            elif choice == "0":
                # Exit
                print("Exiting menu. Goodbye!")
                break

            else:
                print("Invalid choice. Please choose a valid option.")


    @override
    def greet(self):
        """
        A personalized greeting for the Parent.
        Displays details of the parent, including name, ID, age, phone number, status,
        children, and payment information.
        """
        greeting = f"Hello, my name is {self.name}. " \
                   f"My ID is {self.id}, I am {self.age} years old, and my phone number is {self.phone_number}. " \
                   f"My status is {self.status}. " \
                   f"children {self.childrenList} "\
                   f"My payment details are as follows: {self.payment.create_pay_report()}"
        print(greeting)
        return greeting
