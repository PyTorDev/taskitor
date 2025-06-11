import unittest
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch
import sys
import os
from taskitor.commands import add_task, delete_task, update_task, change_status, list_tasks, normalize_status
from taskitor.main import main
import taskitor.storage as storage
from taskitor.storage import load_tasks, save_tasks
from taskitor.task import Task

class TestTaskCommands(unittest.TestCase):
    def setUp(self):
        storage.FILE_PATH = "test_tasks.json"
        save_tasks([])

    def tearDown(self):
        if os.path.exists(storage.FILE_PATH):
            os.remove(storage.FILE_PATH)
    
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
        tasks = load_tasks()
        change_status(tasks[0].id, Task.STATUS_DONE)

        f = StringIO()
        with redirect_stdout(f):
            list_tasks(Task.STATUS_DONE)
        output = f.getvalue()

        self.assertIn("Tasks with status 'done'", output)
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


class TestNormalizeStatus(unittest.TestCase):
    def test_spaces_to_hyphen(self):
        self.assertEqual(normalize_status("To Do"), Task.STATUS_TODO)
        self.assertEqual(normalize_status("In Progress"), Task.STATUS_IN_PROGRESS)

    def test_case_insensitive(self):
        self.assertEqual(normalize_status("DONE"), Task.STATUS_DONE)
        self.assertEqual(normalize_status("in-progress"), Task.STATUS_IN_PROGRESS)

    def test_invalid(self):
        self.assertIsNone(normalize_status("banana"))


class TestCommandCaseInsensitive(unittest.TestCase):
    def setUp(self):
        storage.FILE_PATH = "test_tasks.json"
        save_tasks([])

    def tearDown(self):
        if os.path.exists(storage.FILE_PATH):
            os.remove(storage.FILE_PATH)

    def run_main(self, argv):
        with patch.object(sys, "argv", argv):
            f = StringIO()
            with redirect_stdout(f):
                main()
            return f.getvalue()

    def test_add_uppercase_command(self):
        self.run_main(["taskitor", "ADD", "cli"])
        tasks = load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "cli")

    def test_status_mixed_case(self):
        add_task("task")
        tasks = load_tasks()
        self.run_main(["taskitor", "STATUS", str(tasks[0].id), "In ProgrESS"])
        tasks = load_tasks()
        self.assertEqual(tasks[0].status, Task.STATUS_IN_PROGRESS)

