from typing import Dict, List

from typing_extensions import override

from AdvancedPythonProject.logic.Employee import Employee, Seniority
from AdvancedPythonProject.logic.Person import State
from AdvancedPythonProject.logic.Task import Task , TaskStatus

# הגדרת המחלקה General_Worker שמרשת מ-Employee
class General_Worker(Employee):

    def __init__(self, name, g_id, age, phone_number, status: State, salary, seniority: Seniority, tasks_list:List[Task]):
        """
        Initializes a General Worker object with the provided attributes.
        :param name: The name of the worker.
        :param id: The ID of the worker.
        :param age: The age of the worker.
        :param phone_number: The phone number of the worker.
        :param status: The status of the worker (must be an instance of State).
        :param salary: The salary of the worker (must be a positive number).
        :param seniority: The seniority level of the worker (must be an instance of Seniority).
        :param tasks_list: A dictionary where the keys are task names and the values are TaskStatus.
        """
        super().__init__(name, g_id, age, phone_number, status, salary, seniority)
        self.tasks_list = tasks_list  # Dictionary of tasks with task status as values

    ################################################################################################################################

    # Getter and Setter for tasks_list
    @property
    def tasks_list(self):
        return self._tasks_list

    @tasks_list.setter
    def tasks_list(self, tasks_list):
        """
        Validates that tasks_list is a dictionary where keys are strings and values are instances of TaskStatus.
        """
        self._tasks_list = tasks_list


    ################################################################################################################################
    def change_task_status_of_task(self,task_id, new_task_status):
        """
            Find the task by ID and change its status if it's in the worker's issue list.
            :param task_id: The ID of the task to be updated.
            :param new_status: The new status to be set for the task.
            """
        # בדוק אם המשימה נמצאת במערך הבעיות של העובד
        for task in self.tasks_list:
            if task.task_id == task_id:
                print(f"Task found: {task.description}")
                print(f"Before change: {task.status}")
                task.status = new_task_status
                print(f"After change: {task.status}")
                return True

        # אם המשימה לא נמצאה ברשימת הבעיות של העובד
        print(f"Task with ID {task_id} not found in your issue list.")
        return False
    def problem_report(self):
        """
        Report a general problem with the worker's tasks or operations.
        """
        problem_description = "There is a general issue with the tasks or operations of the worker. Further investigation is required."
        print(problem_description)

    def view_tasks(self):
        print("\nYour Tasks List:")
        for task in self.tasks_list:
            print(f"Task: {task.description}, Status: {task.status}")
    ################################################################################################################################

    # __str__ method
    def __str__(self):
        base_str = super().__str__()  # Call to the __str__ of the Employee class
        return f"{base_str}, Tasks: [{self.tasks_list.__str__()}]"

    # this method is for getting the tasks

    ################################################################################################################################

    def login(self):
        print('Hello, General Worker! Please choose an option:')
        while True:
            try:
                print("\n1. View Tasks List")
                print("2. Change Task Status")
                print("3. Report Problem")
                print("g. Start the greet method (polymorphism)")
                print("0. Exit")

                choice = input("Enter your choice : ")

                if choice == "1":
                    self.view_tasks()
                elif choice == "2":
                    task_id = input("Enter the task id: ")
                    input_status=-1
                    new_status = None
                    while input_status not in ['1', '2', '3']:
                        input_status = input("Enter the new task status: (1)-wait 2-(execution) (3)-complete  ")
                    if input_status==1 : new_status = TaskStatus.WAIT
                    elif input_status==2 : new_status = TaskStatus.EXECUTION
                    elif input_status==3 : new_status = TaskStatus.COMPLETE
                    self.change_task_status_of_task(task_id, new_status)

                elif choice == "3":
                    self.problem_report()
                elif choice == "0":
                    print("Logging out...")
                    break
                elif choice == 'g':
                    self.greet()
                else:
                    print("Invalid choice, please try again.")
            except Exception as e:
                print(f"Error: {e}")
                continue

    @override
    def greet(self):
        """
        A personalized greeting based on the worker's status.
        """
        print(f"Hello, {self.name}!")
        print(f"Welcome, General Worker. Your tasks are important, and you play a vital role in the operations.")
