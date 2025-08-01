### **Running Process**:

# Here is the running process for the software:

1. **Initialization**:
   * Upon starting the program, the system initializes the database connection using the `sql` class and sets up necessary tables (if not already present).
   * Each user (Manager, Teacher, General Worker, or Student) logs into the system by providing credentials.
2. **Login**:
   * The user is prompted to choose from a set of roles:
     * **Manager**: Manages users (teachers, students, and workers), assigns tasks, creates reports, and schedules courses.
     * **General Worker**: Views and updates tasks assigned to them and reports issues.
     * **Student**: Views and registers for courses, manages their schedule, and checks available spots in courses.
   * Each user type is linked to specific functionality within the system.
3. **Interactive Menu**:
   * Once logged in, the user is presented with an interactive menu based on their role:
     * **Manager**: Options to add students, teachers, workers, courses, and manage queues.
     * **General Worker**: Options to view assigned tasks, update task status, or report issues.
     * **Student**: Options to view available courses and register for them.
   * The menu allows users to perform the actions they need based on their role, which are then executed through the relevant methods in the program.
4. **Database Operations**:
   * After the user interacts with the menu, corresponding database operations are triggered via the `sql` class (e.g., adding values to tables, updating columns, deleting rows).
   * All data changes are automatically saved in the database, maintaining data integrity.
5. **Exit**:
   * Once the user completes their tasks, they can choose to exit the system. The system disconnects from the database, ensuring that all changes are saved.


### solution

# The solution process is organized in the following steps:

1. **Database Connection**:
   * The system starts by connecting to the database using provided credentials (host, username, password, and database name). Once connected, it proceeds to the next step.
2. **Table Management**:
   * **Create Database**: If the database doesn’t exist, the system creates it.
   * **Create Tables**: If tables are missing, they are created based on the defined structure.
3. **Data Insertion**:
   * The system allows inserting data (e.g., students, teachers) directly into tables through an interactive menu, ensuring data is added efficiently.
4. **Data Update and Deletion**:
   * Users can update or delete data using unique identifiers (e.g., student or teacher ID). The system uses SQL queries to manage these operations.
5. **User Interaction**:
   * An interactive menu adapts to the user's role (manager, student, teacher, general worker), allowing them to perform specific actions suited to their needs.
6. **Data Persistence**:
   * All actions are automatically saved in the database, ensuring data integrity and real-time updates.
7. **Closing Connection**:
   * After all operations are complete, the system closes the database connection properly.
8. **Extensibility**:
   * The system can be extended to include new features (e.g., course scheduling, financial reports) by modifying or adding new functionalities.
