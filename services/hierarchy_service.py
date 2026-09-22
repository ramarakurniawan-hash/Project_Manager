from services.task_service import find_task

def normalize_orders(tasks):
    parents = set(
        task.parent_id
        for task in tasks
    )

    for parent_id in parents:
        siblings = [
            task
            for task in tasks
            if task.parent_id == parent_id
        ]

        siblings.sort(
            key=lambda task: task.order
        )

        for index, task in enumerate(siblings):
            task.order = index

def indent_task(tasks, task_id):
    task = find_task(tasks, task_id)

    if task is None:
        return False
    
    current_parent_id = task.parent_id

    siblings = [
        sibling
        for sibling in tasks
        if sibling.parent_id == current_parent_id
    ]

    siblings.sort(
        key=lambda sibling: sibling.order
    )

    task_index = siblings.index(task)

    if task_index == 0:
        return False

    previous_sibling = siblings[task_index - 1]

    task.parent_id = previous_sibling.id

    new_siblings = [
        sibling
        for sibling in tasks
        if sibling.parent_id == previous_sibling.id
        and sibling.id != task.id
    ]

    task.order = len(new_siblings)

    normalize_orders(tasks)

    return True

def outdent_task(tasks, task_id):
    task = find_task(tasks, task_id)

    if task is None:
        return False

    if task.parent_id is None:
        return False

    parent = find_task(
        tasks,
        task.parent_id
    )

    if parent is None:
        return False

    new_parent_id = parent.parent_id

    siblings = [
        sibling
        for sibling in tasks
        if sibling.parent_id == new_parent_id
        and sibling.id != task.id
    ]

    siblings.sort(
        key=lambda sibling: sibling.order
    )

    parent_index = siblings.index(parent)

    task.parent_id = new_parent_id

    siblings.insert(
        parent_index + 1,
        task
    )

    for index, sibling in enumerate(siblings):
        sibling.order = index

    return True

def move_task_up(tasks, task_id):
    task = find_task(tasks, task_id)

    if task is None:
        return False

    siblings = [
        sibling
        for sibling in tasks
        if sibling.parent_id == task.parent_id
    ]

    siblings.sort(
        key=lambda sibling: sibling.order
    )

    task_index = siblings.index(task)

    if task_index == 0:
        return False

    previous_sibling = siblings[task_index - 1]

    task.order, previous_sibling.order = (
        previous_sibling.order,
        task.order
    )

    return True

def move_task_down(tasks, task_id):
    task = find_task(tasks, task_id)

    if task is None:
        return False

    siblings = [
        sibling
        for sibling in tasks
        if sibling.parent_id == task.parent_id
    ]

    siblings.sort(
        key=lambda sibling: sibling.order
    )

    task_index = siblings.index(task)

    if task_index == len(siblings) - 1:
        return False

    next_sibling = siblings[task_index + 1]

    task.order, next_sibling.order = (
        next_sibling.order,
        task.order
    )

    return True