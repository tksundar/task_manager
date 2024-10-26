import os
import pickle
import sys
from os import path

# Write to a binary file. We choose the binary format because it is best suited for nested
# data structures
user_file = 'users.pkl'
task_file = 'tasks.pkl'


# Read from file
def deserialize(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


# write to file
def serialize(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def display_tasks(tasks):
    col = []
    if tasks is None:
        return col
    for task in tasks:
        col.append({'name': task.task_name, 'completed': task.completed})
    print('Available Tasks ', col)


class User:

    def __init__(self, name, email, password):
        """email will also serve as the username"""
        self.name = name
        self.email = email
        self.password = password

    def authenticate(self, email, password):
        return self.email == email and self.password == password

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        # Strictly, we just need to compare the emails. I am comparing all variables
        # for the purpose of testing
        return self.email == other.email and self.name == other.name and self.password == other.password


class Task:
    def __init__(self, name, completed=False):
        self.task_name = name
        self.completed = completed

    def mark_complete(self):
        self.completed = True

    def is_completed(self):
        return self.completed

    # def __eq__(self, other):
    #     if not isinstance(other,Task):
    #         return False
    #     return other.task_name == self.task_name


def _contains(stored_tasks, task):
    contains = False
    for t in stored_tasks:
        if t.task_name == task.task_name:
            contains = True
    return contains


class TaskManager:
    def __init__(self):
        if path.exists(task_file):
            self.tasks = deserialize(task_file)
        else:
            self.tasks = dict()
        if path.exists(user_file):
            self.users = deserialize(user_file)
        else:
            self.users = dict()

    def show_users(self):
        return self.users.values()

    def authenticate(self, email, password):
        if email in self.users.keys():
            return self.users.get(email).authenticate(email,password)
        return False

    def register(self, new_user):
        values = self.users.values()
        if new_user in values:
            print('User exists.Please login with credentials')
            return False
        else:
            self.users.update({new_user.email: new_user})
            serialize(self.users, user_file)
            print('User %s registered successfully' % new_user.name)
            return True

    def show_tasks(self, email):
        # keys = self.users.keys()
        # if email in keys:
        display_tasks(self.tasks.get(email))
        return True

    def add_task(self, email, task):
        added = False
        stored_tasks = self.tasks.get(email)
        if stored_tasks is None:
            stored_tasks = set()
            stored_tasks.add(task)
            print("Task %s successfully added " % task.task_name)
        elif not _contains(stored_tasks, task):
            stored_tasks.add(task)
            print("Task %s successfully added " % task.task_name)
        else:
            print('task already present')
        self.tasks.update({email: stored_tasks})
        serialize(self.tasks, task_file)
        added = True
        display_tasks(stored_tasks)
        return added

    def process_delete(self,email, tasks_for_user):
        self.tasks.update({email: tasks_for_user})
        serialize(self.tasks, task_file)
        print('Task(s) deleted')
        display_tasks(tasks_for_user)

    def delete_task(self, email, task, delete_all=False):
        tasks_for_user = self.tasks.get(email)
        for t in tasks_for_user:
            if not delete_all:
                if task.task_name == t.task_name:
                    tasks_for_user.remove(t)
                    self.process_delete(tasks_for_user)
                    return True
            else:
                tasks_for_user.clear()
                self.process_delete(email,tasks_for_user)
                return True

    def mark(self,email, t):
        t.mark_complete()
        print('\nTask %s marked complete ' % t.task_name)
        serialize(self.tasks, task_file)
        self.show_tasks(email)
        return True

    def mark_task_completed(self, email, task, mark_all=False):
        done = False
        for t in self.tasks.get(email):
            if not mark_all:
                if t.task_name == task.task_name:
                    done = self.mark(email,t)
            else:
                done = self.mark(email,t)

        return done
class Main:
    def get_email_pwd(self):
        email_id = input("email id: ")
        pwd = input("password: ")
        return email_id, pwd


    def login(self,manager: TaskManager):
        os.system('cls')
        print('\n\nTask Manager Login...\n')
        (email_id, pwd) = self.get_email_pwd()
        status = manager.authenticate(email_id,pwd)
        return status, email_id


    def register(self,manager: TaskManager):
        print('\n\n Task Manager Registration...\n')
        name = input("Name: ")
        (email_id, pwd) = self.get_email_pwd()
        print(name, email_id, pwd)
        status = manager.register(User(name, email_id, pwd))
        return status, email_id


    def add_task(self,manager: TaskManager, email):
        self.show_tasks(manager, email)
        try:
            task = input("Enter task to add(enter \'a' to abort): ")
            manager.add_task(email, Task(task))
        except ValueError:
            self.show_menu(manager, email), email


    def show_tasks(self,manager: TaskManager, email):
        manager.show_tasks(email)


    def delete_task(self,manager: TaskManager, email):
        self.show_tasks(manager, email)
        task = input("Enter task to delete(enter \'a' to abort,\'all\' to delete all): ")
        if task == 'a':
            self.show_menu(manager, email)
        elif task == 'all':
            manager.delete_task(email, Task(task), True)
        else:
            manager.delete_task(email, Task(task))


    def mark_complete(self,manager: TaskManager, email):
        self.show_tasks(manager, email)
        task = input("Enter task to mark(enter \'a' to abort, \'all\' to mark all as completed): ")
        if task == 'a':
            self.show_menu(manager, email)
        elif task == 'all':
            manager.mark_task_completed(email, Task(task), True)
        else:
            manager.mark_task_completed(email, Task(task))


    def show_menu(self,manager: TaskManager, email):
        menu = ['Add Task', 'View Tasks', 'Delete Task', 'Mark Task completed', 'Exit']
        print('*******************************************************************')
        print("Now you can add tasks, delete tasks and mark tasks as completed   *  ")
        print("You can also see your tasks and their status                      *")
        print("********************************************************************")
        print()
        should_run = True

        while should_run:
            print("Enter the number of the action you want to perform.")
            print()
            for i, v in enumerate(menu):
                print("%d. %s " % (i + 1, v))
            try:
                choice = int(input())
            except ValueError:
                choice = 5
            if choice == 1:
                self.add_task(manager, email)
            elif choice == 2:
                self.show_tasks(manager, email)
            elif choice == 3:
                self.delete_task(manager, email)
            elif choice == 4:
                self.mark_complete(manager, email)
            else:
                print('exiting...')
                should_run = False

    def start(self):
        welcome = '\n\n\nWelcome to TasK Manager, your one stop app for managing daily tasks'
        login_prompt = "\nType 1 to login, 2 to register\n"
        options = ['Login', 'Register', 'Quit']
        inputs = ['Name', 'email id', 'Password']
        manager = TaskManager()
        print('           ', welcome)
        print(login_prompt)
        for i, v in enumerate(options):
            print("%d. %s" % (i + 1, v))

        try:
            choice = int(input())
            if choice == 1:
                (status, email) = self.login(manager)
                if status:
                    self.show_menu(manager, email)
                else:
                    print('\nYou are not registered...')
                    (status, email) = self.register(manager)
                    if status:
                        self.show_menu(manager, email)
            elif choice == 2:
                (status, email) = self.register(manager)
                if status:
                    self.show_menu(manager, email)
                else:
                    sys.exit(0)
        except ValueError:
            sys.exit(0)


if __name__ == '__main__':

    Main().start()