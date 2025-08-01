from enum import Enum


# הגדרת ה-Enum עבור סטטוס משימה
class TaskStatus(Enum):
    WAIT = "wait"
    EXECUTION = "execution"
    COMPLETE = "complete"


class Task():
    def __init__(self, task_id, description, status):
        self.task_id = task_id
        self.description = description
        self.status = status

    @property
    def task_status(self):
        return self.status

    @task_status.setter
    def task_status(self, new_status):
        if isinstance(new_status, TaskStatus):
            self.status = new_status
        else:
            raise ValueError('Invalid status. Must be either completed, in_progress or not_started')

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, new_id):
        if  len(new_id) == 9:
            self._task_id = new_id
        else:
            raise ValueError('Task ID must be a positive integer')

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        if  len(new_description)>2:
            self._description = new_description
        else:
            raise ValueError('Description must be a non-empty string')
################################################################################################################################


    def __str__(self):
        return f'Task ID: {self.task_id}, Description: {self.description}, Status: {self.status}'