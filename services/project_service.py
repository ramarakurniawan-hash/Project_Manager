def get_tasks(project):
    return [
        row.content
        for row in project.rows
        if not row.is_blank
    ]

def get_ordered_rows(project):
    return project.rows

def find_row(project, task_id):
    for row in project.rows:
        if not row.is_blank and row.content.id == task_id:
            return row

    return None

def delete_row(project, task_id):
    for row in project.rows:
        if not row.is_blank and row.content.id == task_id:
            project.rows.remove(row)
            return True

    return False
