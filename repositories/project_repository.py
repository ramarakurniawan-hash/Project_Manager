import json
from datetime import date

from models.project import Project
from models.row import Row
from models.task import Task

def save_project(project):
    project_data = {
        "id": project.id,
        "name": project.name,
        "owner_id": project.owner_id,
        "rows": []
    }

    for row in project.rows:
        if row.is_blank:
            project_data["rows"].append({
                "type": "blank"
            })
        else:
            task = row.content

            project_data["rows"].append({
                "type": "task",
                "id": task.id,
                "name": task.name,
                "start_date": task.start_date.isoformat(),
                "end_date": task.end_date.isoformat(),
                "status": task.status,
                "parent_id": task.parent_id,
                "order": task.order
            })

    with open("project.json", "w") as file:
        json.dump(project_data, file, indent=4)

def load_project():
    with open("project.json", "r") as file:
        project_data = json.load(file)

    project = Project(
        project_data["name"],
        project_data["owner_id"]
    )

    project.id = project_data["id"]

    for row_data in project_data["rows"]:
        if row_data["type"] == "task":
            task = Task(
                row_data["name"],
                date.fromisoformat(row_data["start_date"]),
                date.fromisoformat(row_data["end_date"]),
                row_data["status"],
                parent_id=row_data.get("parent_id"),
                order=row_data.get("order", 0)
            )

            task.id = row_data["id"]

            row = Row(task)

            project.rows.append(row)

        elif row_data["type"] == "blank":
            row = Row()
            project.rows.append(row)

    return project