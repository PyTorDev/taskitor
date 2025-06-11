from task import Task
from storage import load_tasks, save_tasks
from datetime import datetime


def add_task(description):
    tasks = load_tasks()
    if not tasks:
        id = 1
    else:
        id = max([t.id for t in tasks]) + 1

    new_task = Task(id, description)

    tasks.append(new_task)
    save_tasks(tasks)

    print(f"Task added successfully (ID: {id})")

def delete_task(id: int):
    tasks = load_tasks()
    task_to_rid = None

    for t in tasks:
        if t.id == id:
            task_to_rid = t

    if task_to_rid:
        tasks.remove(task_to_rid)
        save_tasks(tasks)
        print(f"Task with ID: {id} deleted successfully")
    else:
        print(f"Task with ID: {id} not found")

def update_task(id: int, description: str):
    tasks = load_tasks()
    task_to_update = None

    for t in tasks:
        if t.id == id:
            task_to_update = t

    if task_to_update:
        task_to_update.description = description
        task_to_update.updated_at = datetime.now().isoformat()
        save_tasks(tasks)
        print(f"Task with ID: {id} updated successfully")
    else:
        print(f"Task with ID: {id} not found")

def change_status(id: int, status: str):
    if status in [Task.STATUS_TODO, Task.STATUS_IN_PROGRESS, Task.STATUS_DONE]:

        tasks = load_tasks()
        task_to_update = None

        for t in tasks:
            if t.id == id:
                task_to_update = t

        if task_to_update:
            task_to_update.status = status
            task_to_update.updated_at = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task with ID: {id} marked as {status} successfully")
        else:
            print(f"Task with ID: {id} not found")

    else:
        print(f"Invalid status: {status}. Valid statuses are: To Do, In Progress, Done")

def list_tasks(status:str = None):
    tasks = load_tasks()

    if status and status not in [Task.STATUS_TODO, Task.STATUS_IN_PROGRESS, Task.STATUS_DONE]:
        print(f"Invalid status: {status}. Valid statuses are: To Do, In Progress, Done")
        return

    if status:
        tasks = [t for t in tasks if t.status == status]
        print(f"Tasks with status '{status}':")
    else:
        print("All tasks:")

    if not tasks:
        print("No tasks found.")
        return

    for t in tasks:
        print(f"[{t.id}] {t.description} — {t.status}")