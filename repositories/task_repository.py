import json
from datetime import date
from models.task import Task

def save_tasks(tasks):
    task_data = []

    for task in (tasks):
        task_data.append({
            "id": task.id,
            "name": task.name,
            "start_date": task.start_date.isoformat(),
            "end_date": task.end_date.isoformat(),
            "status": task.status,
            "parent_id": task.parent_id,
            "order": task.order
        })

    with open("tasks.json", "w") as file:
        json.dump(task_data, file, indent=4)

def load_tasks():
    with open("tasks.json", "r") as file:
        task_data = json.load(file)

    tasks = []

    for task in task_data:
        new_task = Task(
            task["name"],
            date.fromisoformat(task["start_date"]),
            date.fromisoformat(task["end_date"]),
            task["status"],
            parent_id=task.get("parent_id"),
            order=task.get("order", 0)
        )

        new_task.id = task["id"]

        tasks.append(new_task)

    return tasks