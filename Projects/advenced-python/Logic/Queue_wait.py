from AdvancedPythonProject.logic.Course import Course

class Queue_wait():
    def __init__(self, queue: list, course_of_queue, id: str):
        self._id = id  # מזהה ייחודי
        self._queue = queue  # שימוש במשתנה פנימי
        self._course_of_queue = course_of_queue  # קורס משויך לתור

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        '''
        check id equal to 9 digit

        '''
        if len(id) ==9:
            self._id = id
        else:
            raise ValueError("ID must be a positive integer.")

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, queue):
        '''
        Updates the queue.
        '''
        self._queue = queue  # עדכון המשתנה הפנימי

    @property
    def course_of_queue(self):
        return self._course_of_queue

    @course_of_queue.setter
    def course_of_queue(self, course_of_queue):
        if isinstance(course_of_queue, Course):
            self._course_of_queue = course_of_queue  # עדכון משתנה פנימי
        else:
            raise ValueError("Course must be an instance of Course class.")

    def __str__(self):
        return f'Queue [id : {self.id} , course : {self.course_of_queue.name} , number of student in list : {len(self.queue)} ]'
