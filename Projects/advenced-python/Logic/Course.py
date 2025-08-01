#from Teacher import Teacher
from AdvancedPythonProject.AdvancedPythonProject.try_2.Queue_wait import Queue_wait


class Course:
    def __init__(self, name: str, course_id: str,course_size:int, student_list: list):
        """
        Initializes a Course object with the provided attributes.
        :param name: The name of the course.
        :param course_id: The unique ID of the course.
        :param student_list: A list of students enrolled in the course.
        """
        self.name = name
        self.course_id = course_id
        self.student_list = student_list  # List of students enrolled in the course
        self._course_size = course_size  # The maximum number of students allowed in the course

    ################################################################################################################################

    # Getter and Setter for name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if len(name) > 1:
            self._name = name
        else:
            raise ValueError("Course name must be a string with more than 2 characters.")

    ################################################################################################################################

    # Getter and Setter for course_id
    @property
    def course_id(self):
        return self._course_id

    @course_id.setter
    def course_id(self, course_id):
        if  len(course_id) == 9:
            self._course_id = course_id
        else:
            raise ValueError("Course ID must be a positive integer.")
    ################################################################################################################################

    # Getter and Setter for student_list
    @property
    def student_list(self):
        return self._student_list

    @student_list.setter
    def student_list(self, student_list):
        self._student_list = student_list

    ################################################################################################################################
    @property
    def course_size(self):
        return self._course_size

    @course_size.setter
    def course_size(self, course_size):

        if course_size>1:
            self._course_size = course_size
        else:
            raise ValueError("Course size must be an integer and bigger than 1.")

    ################################################################################################################################
    def check_add_student_and_full_course_size(self, Student, queue_wait_list):
        # אם יש מקום בקורס, הוסף את התלמיד
        if len(self.student_list) < self._course_size:
            if Student not in self.student_list:  # בדוק שהתלמיד לא קיים כבר ברשימה
                self.student_list.append(Student)
                print(f'Student {Student.name} added to the course {self.name}')
            else:
                print(f'Student {Student.name} is already enrolled in the course {self.name}')
        else:
            # אם הקורס מלא, בדוק אם יש מקום ברשימת ההמתנה
            for queue_ in queue_wait_list:
                if isinstance(queue_, Queue_wait) and queue_.course_of_queue == self.name:
                    # אם יש רשימת המתנה לקורס הזה, הוסף את התלמיד לרשימה
                    queue_.queue.append(Student)
                    print(f'Student {Student.name} added to the queue for course {self.name}')
                    break
            else:
                # אם לא מצאנו רשימת המתנה מתאימה, צור אחת חדשה
                new_queue = Queue_wait(course_of_queue=self.name)
                new_queue.queue.append(Student)
                queue_wait_list.append(new_queue)
                print(f'Student {Student.name} added to a new queue for course {self.name}')

    # __str__ method
    ################################################################################################################################
    def __str__(self):
        student_names = ', '.join([student.name for student in self.student_list])  # Assuming student objects have a 'name' attribute
        return f"Course(Name: {self.name}, ID: {self.course_id}, Students: {student_names})"
