def get_tasks(project):
    return [
        row.content
        for row in project.rows
        if not row.is_blank
    ]

def get_ordered_rows(project):
    return project.rows