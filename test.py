import unittest
from io import StringIO
from contextlib import redirect_stdout
from commands import add_task, delete_task, update_task, change_status, list_tasks
import storage
from storage import load_tasks, save_tasks
from task import Task

class TestTaskCommands(unittest.TestCase):
    def setUp(self):
        storage.FILE_PATH = "test_tasks.json"
        save_tasks([])
    
    def test_add_task(self):
        add_task("Test task")
        tasks = load_tasks()
        self.assertIsInstance(tasks[0], Task)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Test task")

    def test_update_task(self):
        add_task("Test task")
        tasks = load_tasks()
        task_id = tasks[0].id

        update_task(task_id, "Updated task")

        tasks = load_tasks()
        self.assertIsInstance(tasks[0], Task)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Updated task")
        self.assertNotEqual(tasks[0].created_at, tasks[0].updated_at)

    def test_delete_task(self):
        add_task("Test task")
        tasks = load_tasks()
        task_id = tasks[0].id

        delete_task(task_id)
        tasks = load_tasks()
        self.assertEqual(len(tasks), 0)
        self.assertNotIn(task_id, [t.id for t in tasks])

    def test_change_status(self):
        add_task("Test task")
        tasks = load_tasks()
        task_id = tasks[0].id

        change_status(task_id, Task.STATUS_IN_PROGRESS)

        tasks = load_tasks()
        self.assertEqual(tasks[0].status, Task.STATUS_IN_PROGRESS)

        old_updated_at = tasks[0].updated_at
        change_status(task_id, Task.STATUS_DONE)
        tasks = load_tasks()
        self.assertEqual(tasks[0].status, Task.STATUS_DONE)
        self.assertNotEqual(tasks[0].updated_at, old_updated_at)


class TestListTasks(unittest.TestCase):
    def setUp(self):
        save_tasks([])  # Limpia el archivo antes de cada test

    def test_list_all_tasks(self):
        add_task("Tarea A")
        add_task("Tarea B")

        f = StringIO()
        with redirect_stdout(f):
            list_tasks()
        output = f.getvalue()

        self.assertIn("All tasks:", output)
        self.assertIn("Tarea A", output)
        self.assertIn("Tarea B", output)

    def test_list_tasks_by_status(self):
        add_task("Tarea A")
        tasks = save_tasks  # reload to get real ID
        tasks = load_tasks()
        change_status(tasks[0].id, Task.STATUS_DONE)

        f = StringIO()
        with redirect_stdout(f):
            list_tasks(Task.STATUS_DONE)
        output = f.getvalue()

        self.assertIn("Tasks with status 'Done'", output)
        self.assertIn("Tarea A", output)

    def test_list_tasks_empty(self):
        f = StringIO()
        with redirect_stdout(f):
            list_tasks()
        output = f.getvalue()

        self.assertIn("No tasks found.", output)

    def test_invalid_status(self):
        f = StringIO()
        with redirect_stdout(f):
            list_tasks("Banana")
        output = f.getvalue()

        self.assertIn("Invalid status", output)