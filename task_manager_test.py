import unittest

from task_manager import TaskManager, Task


class TaskManagerTest(unittest.TestCase):


    def test_add_task(self):
        email = 'sundar@abc.com'
        password = '123'
        manager = TaskManager()
        self.assertTrue(manager.add_task(email,Task("task1")))
        self.assertTrue(manager.add_task(email,Task("task2")))
    #
    # def test_view_task(self):
    #     self.assertTrue(manager.show_tasks(email))
    #
    # def test_mark_task_completed(self):
    #     self.assertTrue(manager.mark_task_completed(email,'task1'))
    #
    # def test_delete_task(self):
    #     self.assertTrue(manager.delete_task(email,'task1'))






