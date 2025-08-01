### ***System Overview***

* The system operates interactively, maintaining a simple and efficient user experience. When the user opens the system, they are presented with a main menu containing several options that lead to different system functions. Each action chosen from the menu is executed by transferring the user to the appropriate function. For example, if the user selects the option to "Add Course," they are directed to a function implemented through the Manager class that allows them to input data about the new course. Any actions performed, such as adding students or teachers to the course, will be updated in the database using the methods in the SQL class. Each process of adding, updating, or deleting is carried out through SQL queries in the database.
* Additionally, the system allows administrators to generate reports, update worker tasks, and assign tasks or teachers to courses. Each of these actions is executed through the Manager class, which provides the capability to add students, parents, teachers, and general workers, assign tasks, and manage the teacher scheduling process. When a manager or a general worker, such as one from the General\_Worker class, accesses the system, they can view tasks assigned to them or change the status of tasks through an interactive menu within the General\_Worker class. Any status changes to tasks are updated in the database and displayed in the task list. Workers can also report issues or update their progress by interacting with the system, and all actions are recorded.
* Moreover, any student who accesses the system can browse available courses, register for courses, and manage their schedule. Any action the student performs, such as registering for a course or updating their personal details, is executed through the Student class, and their data is saved in the database. When a student chooses to register for a course, the system checks if there is space in the course and whether they meet the course requirements. The QueueWait class manages queues in case there is a need to register students for courses with limited capacity, allowing the system to track students waiting for a spot. The manager can then schedule them in the course as soon as space becomes available.
* Finally, all data updates, course creation, and the addition of workers and students to the system, as well as task management, are carried out while ensuring data integrity in the database through the methods in the SQL class. Every action of adding information or updating is automatically saved, and the system is always connected to the database, executing all requests smoothly. In case of login requirements, the user will select the appropriate option from the main menu, and then the system will perform all necessary actions while maintaining user data and the relationships between different entities in the system. Each of the menu options links the user to the corresponding functions, which perform the actions automatically and are connected to the database.

# 

Course Department, Employee Department, General Worker Department, and Manager Department Documentation

## Course Department

The `Course` class embodies an academic course, comprising essential properties including the course name, unique ID, a list of students, and the maximum allowable student capacity. The design emphasizes data integrity through property-based getters and setters.

### Key Properties:

- **name (str)**: Represents the name of the course and requires a string of at least three characters.
- **course_id (int)**: A unique identifier for the course, ensuring it is a positive integer.
- **student_list (list)**: Holds the registered students, mandated to be a list type for structural consistency.
- **course_size (int)**: Defines the maximum student capacity, necessitating that it must be greater than one.

### Key Methods:

- **check_add_student_and_full_course_size()**: This placeholder method is responsible for assessing whether a new student can be added to the course, considering its size constraints.
- **__str__()**: Provides a string representation that includes the course name, ID, and names of enrolled students.

---

## Employee Department

The `Employee` class serves to track individual employee details, including personal data, salary, employment status, and seniority level. This class derives from the foundational `Person` class.

### Key Properties:

- **salary (float/int)**: Specifies a positive salary amount for the employee.
- **seniority (Seniority Enum)**: Designates the employee's seniority level, subject to validation against the defined `Seniority` Enum.

### Key Methods:

- **__str__()**: Outputs a string representation encompassing salary and seniority details of the employee.

---

## General Worker Department

The `General Worker` class extends the `Employee` class, representing individuals who perform general tasks. This class includes a framework for managing task lists and their statuses.

### Key Properties:

- **tasks_list (List[Task])**: Maintains a list of tasks assigned to the general worker.

### Key Methods:

- **login()**: A placeholder method intended for worker login functionality.
- **change_task_status_of_task(task, new_task_status)**: Refines the status of a designated task if it is present in the list.
- **problem_report()**: A placeholder for capturing problem reports encountered by the worker.
- **__str__()**: Generates a string representation of the general worker, including their tasks.

---

## Manager Department

The `Manager` class denotes an administrative role, inheriting from the `Employee` class. It is tasked with overseeing general workers, teachers, courses, tasks, and financial operations.

### Key Properties:

- **worker_list (List[General_Worker])**: A compilation of general workers under the manager’s supervision.
- **teacher_list (List[Teacher])**: Holds teachers managed by the manager.

### Key Methods:

- **create_report_income_outcome(year, income, outcome)**: Produces a financial report delineating income and expenditures for a specific year.
- **assign_task_to_general_employee(n_general_employee, task)**: Responsible for appointing tasks to specific general workers.
- **create_general_employee(general_employee, general_employee_list)**: Facilitates the addition of new general employees, ensuring no duplicates are introduced.
- **create_teacher(teacher, teacher_list)**: Similar to the above, it enables the addition of teachers while preventing duplication in the roster.

This documentation collectively outlines the structure and functionalities of the courses, employee roles, general workers, and managerial responsibilities within an academic administrative framework. Each class is defined with clear properties and methods to maintain order and efficiency.

## System Functionality Overview

The system provides a comprehensive structure to enhance the management of educational courses, students, parents, and payment tracking. It enables various administrative actions that facilitate the efficient assignment of educators, enrollment processes, and payment reporting, while maintaining clear data integrity.

### Key Functionalities

- **assign_teacher_to_course(teacher, course)**: This function is crucial for assigning an educator to a specific course, ensuring that qualified individuals are linked with the appropriate subjects they will be teaching.
- **create_student(student, student_list)**: With the ability to add new students, this function checks for duplicate entries, thereby maintaining the uniqueness of each student within the system.
- **create_parent(parent, parent_list)**: Similar to student creation, this function allows for adding new parents while preventing duplication, ensuring that each parent is represented only once in the system.
- **create_course(course, course_list)**: This function enables the addition of new courses, also with checks to circumvent duplication, which is essential for efficient course management.
- **manage_queue(queue_list)**: This functionality oversees waiting lists for courses, allowing students to be organized according to their admission into classes where space may be limited.
- **login(...)**: It provides a menu interface for various administrative actions, facilitating ease of access to different functionalities within the system.

### Department Insights

#### Parent Department

The `Parent` class plays a pivotal role by capturing details about parents who interact with the system. It is derived from a more general `Person` class and includes:

- **childrenList (List[Person])**: This property holds a list of the parent's children under their supervision.
- **Payment (Payment)**: This integrates a payment object that details the parent's financial transactions.

Methods offered by this class include:

- **Login()**: A gateway for parents to access the system.
- **register_child_to_course_if_course_not_full(...)**: Allows a parent to enroll their child in a course or alternatively place them on a waiting list if the course is full.
- **show_child_info(childName, course_list)**: It displays pertinent information regarding the child and their enrolled courses.
- **show_place_in_queue(childName, queueList)**: This method reveals a child’s position in the queue for limited courses.
- **payment_report()**: Summarizes the parent's payment history and transactions.

#### Payment Department

Within the payment domain, the `Payment` class encapsulates financial data relevant to parent transactions:

- **Income (float)** and **Outcome (float)** track financial inflows and outflows respectively.

Core methods include:

- **create_pay_report()**: This generates a detailed payment report including metrics like income, expenses, net profit, and ROI.
- **__str__()**: Provides a descriptive string representation of the payment object, outlining revenue and expenses.

#### Person Department

The `Person` class establishes a framework for storing individual-level information:

- It holds critical identity attributes such as **name**, **id**, **age**, and **phone_number**.
- **status (State)** indicates the individual’s current role or standing within the system.

Methods such as **__str__()** and **__eq__()** facilitate descriptions of identity and comparisons based on unique identifiers.

#### Queue Wait Department

The `Queue_wait` class manages student queuing for courses, efficiently coordinating student placements:

- **id (int)** serves as a unique identifier for each queue, ensuring streamlined management of student positions and associated courses.

This structured approach across departments allows for effective educational management and satisfactory parent and student engagement with the institution's services.
The provided documentation outlines several classes and their corresponding properties and methods within an educational system.

### Queue Class

The **Queue** class manages a list of students waiting for a specific course, referred to as `course_of_queue`. It features:

- **Properties**:
  - `queue`: A list detailing the students waiting to enroll.
  - `course_of_queue`: Links to the course tied to the queue.
- **Methods**:
  - `id`: Getter/Setter to manage the queue ID.
  - `queue`: Getter/Setter for updating the list of students.
  - `course_of_queue`: Getter/Setter for the associated course updates.
  - `__str__()`: Provides a string representation, summarizing the queue's details.

### Students Department

The **Students** department extends the capabilities of the **Person** department. This class manages student-specific information including grades and registration status.

- **Properties**:
  - `grade_course`: A dictionary that connects course IDs to the respective grades received by the student.
  - `registered`: Indicates the current enrollment status of the student.
- **Methods**:
  - `grade_course`: Getter/Setter for updating the student's grades.
  - `registered`: Getter/Setter for managing registration status.
  - `login()`: Welcomes the student and prompts for sign-in.
  - `show_grade(list_courses)`: Displays grades for a specified list of courses.
  - `show_place_in_queue(queueList)`: Indicates the student's position within the queue for various courses.
  - `__str__()`: Offers a string layout that describes the student, inclusive of personal details and grades.

### Task Department

The **Task** class encapsulates information regarding tasks within the system, characterized by an ID, description, and current status.

- **Properties**:
  - `task_id`: A positive integer for identifying the task.
  - `description`: A string that explains the task.
  - `status`: Represents the current status of the task as defined by an enumerated type.
- **Methods**:
  - `task_status`: Getter/Setter for adjusting a task's status.
  - `task_id`: Getter/Setter for modifying the task's ID.
  - `description`: Getter/Setter for altering the task's description.

### Teacher Department

The **Teacher** class, derived from the **Employee** class, encapsulates information regarding teachers who can supervise courses and manage student interactions.

- **Properties**:
  - `course_list`: Catalog of courses taught by the teacher.
  - `student_list`: Enumeration of students under the teacher’s guidance.
  - `salary`: A float indicating the teacher’s payment, which must be a positive value.
  - `seniority`: Represents the teacher's level of experience.
- **Methods**:
  - `course_list`: Getter/Setter for the courses the teacher instructs.
  - `student_list`: Getter/Setter for the roster of students under the teacher’s tutelage.
  - `login()`: A placeholder method for teacher sign-in functionality.
  - `show_student_in_course()`: Displays students assigned to the teacher’s lessons.
  - `assign_student_to_course(student)`: Enrolls a student in the teacher's courses.
  - `assign_grade_to_student(student, grade, course)`: Records a student's grade for a designated course.
  - `problem_report()`: A placeholder for logging issues related to the teacher’s responsibilities.

Through these classes and their respective properties and methods, the system establishes a comprehensive framework for managing educational tasks, student information, queuing processes, and teacher responsibilities.


**Classes Overview**

* The `Course` class represents a course in the system, with attributes such as `course_id`, `course_name`, `teacher`, `students`, `capacity`, and `registered_students`. It includes the method `__str__`, which displays the course details as text.
* The `Employee` class represents an employee in the system, with attributes such as `salary` and `seniority`. The `greet` method is abstract and returns a personalized greeting, implemented by subclasses. The `__str__` method displays employee details.
* The `General_Worker` class is a subclass of `Employee`, representing a general worker. It includes the attribute `tasks_list`, which holds assigned tasks for the worker. The `greet` method is polymorphic, providing personalized greetings. The `update_task_status`, `view_tasks`, and `report_problem` methods handle task management and problem reporting. The `login` method offers an interactive menu for task actions and issue reporting.
* The `Manager` class, a subclass of `Employee`, represents a manager in the system. It includes attributes like `worker_list` (supervised workers) and `teacher_list` (managed teachers). Methods such as `greet`, `create_report`, and `assign_task` are used for employee and task management. The `add_teacher`, `add_student`, `add_parent`, `add_general_worker`, and `add_course` methods manage various system entities. Additional methods like `manage_queue`, `schedule_teacher`, and `login` allow for further system operations.
* The `Parent` class represents a parent in the system, with attributes `parent_id`, `name`, and `email`. The `__str__` method displays the parent’s details as text.
* The `Payment` class represents a payment, with attributes `payment_id`, `amount`, and `payment_date`. The `__str__` method displays the payment details as text.
* The `Person` class represents a person, with attributes `name` and `email`. The `__str__` method displays the person’s details as text.
* The `QueueWait` class represents a queue of people waiting for a course spot. Attributes include `waitlist_id`, `course_id`, `student_id`, and `request_date`. The `__str__` method displays queue details as text.
* The `Student` class represents a student, with attributes like `student_id`, `name`, `age`, and `preferred_course`. The `__str__` method displays the student’s details as text.
* The `Task` class represents a task in the system, with attributes `task_id`, `description`, and `status`. The `__str__` method displays the task details as text.
* The `Teacher` class represents a teacher, with attributes `teacher_id`, `name`, and `expertise`. The `__str__` method displays the teacher’s details as text.
* The `sql` class manages database connections and interactions. Attributes include `host`, `user`, `password`, `connection`, and `cursor`. Methods such as `connect_my_db`, `create_db`, and `create_table` perform database operations. Other methods like `add_value_to_table`, `update_col_by_id`, and `del_col_by_id` manage data within tables.
* The system allows for interactive user processes where tasks are performed via dynamic menus. Polymorphism in the `greet` method provides personalized greetings for employees based on roles. All data management is conducted in a MySQL database, ensuring efficient handling of information.

---

### **Main Class Overview**

* The `A_main` class handles the system’s interactive menu and function execution. The `login` method displays the menu and performs actions based on user choices.
* The `Main` class serves as the core of the system, linking all other classes together. The `main` method opens the interface and performs system management tasks.

---

### **SQL Class Overview**

* The `sql` class is responsible for managing connections and operations with a database (MySQL). It includes the following variables:
  * `host`, `user`, `password`: Database connection details.
  * `connection`: The connection to the database.
  * `cursor`: A tool for executing SQL queries.
  * `table_name`, `db_name`: Table and database names.
* Methods:
  * `connect_my_db`: Establishes a connection to the database using the provided details.
  * `create_db`: Creates a new database.
  * `create_table`: Creates a new table in the database.
  * `add_value_to_table`: Inserts values into a table.
  * `update_col_by_id`: Updates a column value in a table by ID.
  * `del_col_by_id`: Deletes a record from the table by ID.
  * `add_df_to_table`: Inserts data from a DataFrame into the database.
* Usage:
  1. Create an object from the `sql` class and define the connection details (host, user, password).
  2. Use the methods to connect to the database, create tables, and update/delete data as needed.
  3. The methods provide simple interaction with the database through standard SQL queries.


### another axplain by Sql Area


```
-----------  *another explain by sql class* ------
*   Brief Summary of the `sql` Class

**  Structure:
    - The `sql` class is responsible for managing connections and operations with a database (MySQL).
    - It includes the following variables:
    - `host`, `user`, `password`: Database connection details.
    - `connection`: The connection to the database.
    - `cursor`: A tool for executing SQL queries.
    - `table_name`, `db_name`: Table and database names.

**  Methods:
    -connect_my_db`**: Establishes a connection to the database using the provided details.
    -create_db`**: Creates a new database.
    -create_table`**: Creates a new table in the database.
    -add_value_to_table`**: Inserts values into a table.
    -update_col_by_id`**: Updates a column value in a table by ID.
    -del_col_by_id`**: Deletes a record from the table by ID.
    -add_df_to_table`**: Inserts data from a DataFrame into the database.

** Usage:
    1. Create an object from the `sql` class and define the connection details (host, user, password).
        2. Use the methods to connect to the database, create tables, and update/delete data as needed.
            3. The methods provide simple interaction with the database through standard SQL queries.

The class allows for easy interaction with a database and performs actions in an organized and accessible manner.
```
