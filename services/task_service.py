from datetime import timedelta

def find_task(tasks, task_id):
    for task in tasks:
        if task.id == task_id:
            return task

    return None

def validate_dates(start_date, end_date):
    return start_date <= end_date

def calculate_end_date(start_date, duration):
    return start_date + timedelta(days=duration - 1)

def update_task(
    tasks,
    task_id,
    new_name,
    new_start,
    new_end,
    new_status
):
    task = find_task(tasks, task_id)

    if task is None:
        return False

    if not validate_dates(new_start, new_end):
        return False

    task.name = new_name
    task.start_date = new_start
    task.end_date = new_end
    task.status = new_status

    return True

def delete_task(tasks, task_id):
    task = find_task(tasks, task_id)

    if task is None:
        return

    tasks.remove(task)