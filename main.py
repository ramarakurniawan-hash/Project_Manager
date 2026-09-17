import uuid
from datetime import date, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json

class Task:
    def __init__(
        self,
        name,
        start_date,
        end_date,
        status,
        parent_id=None,
        order=0
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.parent_id = parent_id
        self.order = order

    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1

def find_task(tasks, task_id):
    for task in tasks:
        if task.id == task_id:
            return task

    return None

def validate_dates(start_date, end_date):
    if start_date > end_date:
        return False
    
    return True

def calculate_end_date(start_date, duration):
    return start_date + timedelta(days=duration - 1)

def update_task(tasks, task_id, new_name, new_start, new_end, new_status):
    task = find_task(tasks, task_id)

    if task is None:
        return False

    if not validate_dates(new_start, new_end):
        messagebox.showerror(
            "Invalid Date Range",
            "End date cannot be earlier than start date."
        )
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

def save_tasks(tasks):
    task_data = []

    for task in tasks:
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

tasks = load_tasks()
active_editor = None

def get_hierarchy(tasks):
    ordered_tasks = []

    def add_children(parent_id):
        children =[
            task
            for task in tasks
            if task.parent_id == parent_id
        ]

        children.sort(
            key=lambda task: task.order
        )

        for task in children:
            ordered_tasks.append(task)
            add_children(task.id)

    add_children(None)

    return ordered_tasks

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

    new_siblings =[
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

    if task_index == len(siblings) -1:
        return False

    next_sibling = siblings[task_index + 1]

    task.order, next_sibling.order = (
        next_sibling.order,
        task.order
    )

    return True

def indent_selected_task():
    selected_item = table.selection()

    if not selected_item:
        return

    task_id = selected_item[0]

    changed = indent_task(
        tasks,
        task_id
    )

    if changed:
        save_tasks(tasks)
        refresh_table()

def outdent_selected_task():
    selected_item = table.selection()

    if not selected_item:
        return

    task_id = selected_item[0]

    changed = outdent_task(
        tasks,
        task_id
    )

    if changed:
        save_tasks(tasks)
        refresh_table()

def move_selected_task_up():
    selected_item = table.selection()

    if not selected_item:
        return

    task_id = selected_item[0]

    changed = move_task_up(
        tasks,
        task_id
    )

    if changed:
        save_tasks(tasks)
        refresh_table()

def move_selected_task_down():
    selected_item = table.selection()

    if not selected_item:
        return

    task_id = selected_item[0]

    changed = move_task_down(
        tasks,
        task_id
    )

    if changed:
        save_tasks(tasks)
        refresh_table()

def close_editor():
    global active_editor

    if active_editor is not None:
        editor = active_editor["editor"]
        finish = active_editor["finish"]

        if not editor.winfo_exists():
            active_editor = None
            return

        if finish():
            active_editor = None

def cancel_editor():
    global active_editor
    if active_editor is not None:
        active_editor["editor"].destroy()
        active_editor = None

def handle_click_away(event):
    print("CLICK:", event.widget)

    if active_editor is not None:
        close_editor()

def refresh_table():
    selected_item = table.selection()
    selected_id = selected_item[0] if selected_item else None

    open_states = {}

    def collect_open_states(parent=""):
        for item in table.get_children(parent):
            open_states[item] = table.item(item, "open")
            collect_open_states(item)

    collect_open_states()

    for item in table.get_children():
        table.delete(item)

    ordered_tasks = get_hierarchy(tasks)

    for task in ordered_tasks:
        parent = task.parent_id if task.parent_id else ""

        table.insert(
            parent,
            "end",
            iid=task.id,
            text=task.name,
            values=(
                task.start_date,
                task.end_date,
                task.duration,
                task.status
            ),
            open=open_states.get(task.id, True),
            tags=("row_even" if len(table.get_children(parent)) % 2 ==0 else "row_odd",)
        )

    if selected_id and table.exists(selected_id):
        table.selection_set(selected_id)
        table.focus(selected_id)

def edit_task_name(event):
    global active_editor

    row_id = table.identify_row(event.y)
    column = table.identify_column(event.x)

    if not row_id or column != "#0":
        return

    close_editor()

    x, y, width, height = table.bbox(row_id, column)

    current_value = table.item(
        row_id,
        "text"
    )

    editor = tk.Entry(table)

    editor.insert(
        0,
        current_value
    )

    editor.select_range(
        0,
        tk.END
    )

    editor.place(
        x=x,
        y=y,
        width=width,
        height=height
    )

    editor.focus()

    def finish_edit(event=None):
        global active_editor

        new_name = editor.get().strip()

        task_id = row_id

        task = find_task(tasks, task_id)

        if task:
            task.name = new_name
            save_tasks(tasks)

            active_editor = None

            editor.destroy()
            refresh_table()

            return True

        return False

    active_editor = {
        "editor": editor,
        "finish": finish_edit
    }

    editor.bind(
        "<Return>",
        finish_edit
    )

    editor.bind(
        "<Escape>",
        lambda event: cancel_editor()
    )

def edit_task_start_date(event):
    global active_editor

    row_id = table.identify_row(event.y)
    column = table.identify_column(event.x)

    if not row_id or column != "#1":
        return

    close_editor()

    x, y, width, height = table.bbox(row_id, column)

    current_value = table.item(
        row_id,
        "values"
    )[0]

    editor = DateEntry(
        table,
        date_pattern="yyyy-mm-dd"
    )

    editor.set_date(current_value)

    editor.place(
        x=x,
        y=y,
        width=width,
        height=height
    )

    editor.focus()
    editor.drop_down()

    def finish_edit(event=None):
        global active_editor

        new_start = editor.get_date()

        task_id = row_id

        task = find_task(tasks, task_id)

        if not task:
            return False


        if not validate_dates(new_start, task.end_date):
            messagebox.showerror(
                "Invalid Date Range",
                "Start date cannot be later than end date."
            )
            editor.focus()
            editor.after(
                10,
                editor.drop_down
            )
            return False

        task.start_date = new_start
        save_tasks(tasks)

        active_editor = None

        editor.destroy()
        refresh_table()

        return True

    active_editor = {
        "editor": editor,
        "finish": finish_edit
    }

    editor.bind(
        "<Return>",
        finish_edit
    )

    editor.bind(
        "<<DateEntrySelected>>",
        lambda event: editor.after(10, finish_edit)
    )

    editor.bind(
        "<Escape>",
        lambda event: cancel_editor()
    )

def edit_task_end_date(event):
    global active_editor
    row_id = table.identify_row(event.y)
    column = table.identify_column(event.x)

    if not row_id or column != "#2":
        return

    close_editor()

    x, y, width, height = table.bbox(row_id, column)

    current_value = table.item(
        row_id,
        "values"
    )[1]

    editor = DateEntry(
        table,
        date_pattern="yyyy-mm-dd"
    )

    editor.set_date(current_value)

    editor.place(
        x=x,
        y=y,
        width=width,
        height=height,
    )

    editor.focus()
    editor.drop_down()

    def finish_edit(event=None):
        global active_editor
        new_end = editor.get_date()

        task_id = row_id
        task = find_task(tasks, task_id)

        if not task:
            return False

        if not validate_dates(task.start_date, new_end):
            messagebox.showerror(
                "Invalid Date Range",
                "End date cannot be earlier than start date."
            )
            editor.focus()
            editor.after(
                10,
                editor.drop_down
            )
            return False

        task.end_date = new_end
        save_tasks(tasks)

        active_editor = None

        editor.destroy()
        refresh_table()

        return True

    active_editor = {
        "editor": editor,
        "finish": finish_edit
    }

    editor.bind(
        "<Return>",
        finish_edit
    )

    editor.bind(
        "<<DateEntrySelected>>",
        finish_edit
    )

    editor.bind(
        "<Escape>",
        lambda event: cancel_editor()
    )

def edit_task_duration(event):
    global active_editor

    row_id = table.identify_row(event.y)
    column = table.identify_column(event.x)

    if not row_id or column != "#3":
        return

    close_editor()

    x, y, width, height = table.bbox(row_id, column)

    current_value = table.item(
        row_id,
        "values"
    )[2]

    editor = tk.Entry(table)

    editor.insert(
        0,
        current_value
    )

    editor.select_range(
        0,
        tk.END
    )

    editor.place(
        x=x,
        y=y,
        width=width,
        height=height
    )

    editor.focus()

    def finish_edit(event=None):
        global active_editor
        value = editor.get().strip()

        try:
            new_duration = int(value)
        except ValueError:
            messagebox.showerror(
                "Invalid Duration",
                "Duration must be a whole number of days."
            )
            editor.focus()
            editor.select_range(0, tk.END)
            return False
        
        if new_duration < 1:
            messagebox.showerror(
                "Invalid Duration",
                "Duration must be at least 1 day."
            )
            editor.focus()
            editor.select_range(0, tk.END)
            return False

        task_id = row_id
        task = find_task(tasks, task_id)

        if not task:
            return False

        new_end = calculate_end_date(
            task.start_date,
            new_duration
        )

        task.end_date = new_end

        save_tasks(tasks)

        active_editor = None

        editor.destroy()
        refresh_table()

    active_editor = {
        "editor": editor,
        "finish": finish_edit
    }

    editor.bind(
        "<Return>",
        finish_edit
    )

    editor.bind(
        "<Escape>",
        lambda event: cancel_editor()
    )

def edit_task_status(event):
    global active_editor

    row_id = table.identify_row(event.y)
    column = table.identify_column(event.x)

    if not row_id or column != "#4":
        return

    close_editor()

    x, y, width, height = table.bbox(row_id, column)

    current_value = table.item(
        row_id,
        "values"
    )[3]

    editor = ttk.Combobox(
        table,
        values=["Done", "In Progress", "Not Started"],
        state="readonly"
    )

    editor.set(current_value)

    editor.place(
        x=x,
        y=y,
        width=width,
        height=height
    )

    editor.focus()
    editor.tk.call("ttk::combobox::Post", editor)

    def finish_edit(event=None):
        global active_editor
        
        new_status = editor.get()

        task_id = row_id

        task = find_task(tasks, task_id)

        if task:
            task.status = new_status
            save_tasks(tasks)

            active_editor = None

            editor.destroy()
            refresh_table()

            return True

        return False

    active_editor = {
        "editor": editor,
        "finish": finish_edit
    }

    editor.bind(
        "<Return>",
        finish_edit
    )

    editor.bind(
        "<Escape>",
        lambda event: cancel_editor()
    )

def edit_cell(event):
    column = table.identify_column(event.x)

    if column == "#0":
        element = table.identify_element(event.x, event.y)

        if "indicator" in element:
            return
        
        edit_task_name(event)

    elif column == "#1":
        edit_task_start_date(event)

    elif column == "#2":
        edit_task_end_date(event)

    elif column == "#3":
        edit_task_duration(event)

    elif column == "#4":
        edit_task_status(event)

    return "break"

def update_selected_task():
    selected_item = table.selection()

    if selected_item:
        item = table.item(selected_item[0])
        task_id = selected_item[0]

        edit_window = tk.Toplevel(window)
        edit_window.title("Update Task")

        edit_window.transient(window)
        edit_window.grab_set()

        name_label = tk.Label(
            edit_window,
            text="Task Name:"
        )
        name_label.pack(pady=5)

        name_entry = tk.Entry(
            edit_window
        )
        name_entry.pack(pady=5)
        name_entry.insert(
            0,
            item["text"][0]
        )

        start_label = tk.Label(
            edit_window,
            text="Start Date:"
        )
        start_label.pack(pady=5)

        start_entry = DateEntry(
            edit_window,
            date_pattern="yyyy-mm-dd"
        )
        start_entry.pack(pady=5)

        start_entry.set_date(item["values"][0])

        end_label = tk.Label(
            edit_window,
            text="End Date:"
        )
        end_label.pack(pady=5)

        end_entry = DateEntry(
            edit_window,
            date_pattern="yyyy-mm-dd"
        )
        end_entry.pack(pady=5)

        end_entry.set_date(item["values"][1])

        status_label = tk.Label(
            edit_window,
            text="Select new status:"
        )
        status_label.pack(pady=10)

        status_dropdown = ttk.Combobox(
            edit_window,
            values=["Done", "In Progress", "Not Started"],
            state="readonly"
        )
        status_dropdown.pack(padx=10)

        status_dropdown.set(item["values"][3])

        def confirm_task_update():
            new_name = name_entry.get()

            try:
                new_start = date.fromisoformat(start_entry.get())
                new_end = date.fromisoformat(end_entry.get())
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Please enter dates in the format YYYY-MM-DD."
                )
                return

            new_status = status_dropdown.get()

            updated = update_task(
                tasks,
                task_id,
                new_name,
                new_start,
                new_end,
                new_status
            )

            if not updated:
                return

            save_tasks(tasks)

            refresh_table()
            edit_window.destroy()

        update_button = tk.Button(
            edit_window,
            text="Update",
            command=confirm_task_update
        )

        update_button.pack(pady=15)

def delete_selected_task():
    selected_item = table.selection()

    if selected_item:
        item = table.item(selected_item[0])
        task_id = selected_item[0]
        task_name = item["text"]

        confirm = messagebox.askyesno(
            "Delete Task",
            f"Are you sure you want to delete the task '{task_name}'?"
        )

        if confirm:
            delete_task(tasks, task_id)
            save_tasks(tasks)
            refresh_table()

def add_task_window():
    task_window = tk.Toplevel(window)

    task_window.title("Add Task")

    task_window.transient(window)
    task_window.grab_set()

    task_label = tk.Label(
        task_window,
        text="Task Name:"
    )
    task_label.pack(pady=5)

    task_entry = tk.Entry(
        task_window
    )
    task_entry.pack(pady=5)

    start_label = tk.Label(
        task_window,
        text="Start Date:"
    )
    start_label.pack(pady=5)

    start_entry = DateEntry(
        task_window,
        date_pattern="yyyy-mm-dd"
    )
    start_entry.pack()

    end_label = tk.Label(
        task_window,
        text="End Date:"
    )
    end_label.pack(pady=5)

    end_entry = DateEntry(
        task_window,
        date_pattern="yyyy-mm-dd"
    )
    end_entry.pack()

    status_label = tk.Label(
        task_window,
        text="Status:"
    )
    status_label.pack(pady=5)

    status_dropdown = ttk.Combobox(
        task_window,
        values=["Done", "In Progress", "Not Started"],
        state="readonly"
    )
    status_dropdown.pack(padx=5)

    status_dropdown.set("Not Started")

    def save_new_task():
        new_task_name = task_entry.get()
        
        try:
            new_task_start = date.fromisoformat(start_entry.get())
            new_task_end = date.fromisoformat(end_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please enter dates in the format YYYY-MM-DD."
            )
            return        

        if not validate_dates(new_task_start, new_task_end):
            messagebox.showerror(
                "Invalid Date Range",
                "End date cannot be earlier than start date."
            )
            return

        new_task_status = status_dropdown.get() 

        new_task = Task(
            new_task_name,
            new_task_start,
            new_task_end,
            new_task_status
        )

        tasks.append(new_task)

        save_tasks(tasks)

        refresh_table()
        task_window.destroy()

    add_task_button = tk.Button(
        task_window,
        text="Add",
        command=save_new_task
    )

    add_task_button.pack(pady=10)

window = tk.Tk()

window.title("Pro-Man")
window.geometry("800x400")

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    rowheight=28,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold")
)

style.layout(
    "Grid.Treeview",
    [
        (
            "Treeview.treearea",
            {
                "sticky": "nswe"
            }
        )
    ]
)

style.configure(
    "Grid.Treeview",
    rowheight=28,
    font=("Segoe UI", 10)
)

table = ttk.Treeview(
    window,
    columns=("Start", "End", "Duration", "Status"),
    show="tree headings",
    style="Grid.Treeview"
)

table.heading("#0", text="Task")
table.heading("Start", text="Start")
table.heading("End", text="End")
table.heading("Duration", text="Duration")
table.heading("Status", text="Status")

table.column(
    "#0",
    width=260,
    minwidth=180,
    stretch=True
)

table.column(
    "Start",
    width=110,
    minwidth=100,
    anchor="center",
    stretch=True
)

table.column(
    "End",
    width=110,
    minwidth=100,
    anchor="center",
    stretch=True
)

table.column(
    "Duration",
    width=90,
    minwidth=80,
    anchor="center",
    stretch=True
)

table.column(
    "Status",
    width=130,
    minwidth=110,
    anchor="center",
    stretch=True
)

table.tag_configure(
    "row_even",
    background="#f7f7f7"
)

table.tag_configure(
    "row_odd",
    background="#ffffff"
)


ribbon = tk.Frame(window)

ribbon.pack(
    fill="x"
)


file_group = tk.LabelFrame(
    ribbon,
    text="File"
)

file_group.pack(
    side="left"
)

task_group = tk.LabelFrame(
    ribbon,
    text="Task"
)

task_group.pack(
    side="left"
)

hierarchy_group = tk.LabelFrame(
    ribbon,
    text="Hierarchy"
)

hierarchy_group.pack(
    side="left"
)


save_button = tk.Button(
    file_group,
    text="Save",
    command=lambda: save_tasks(tasks)
)

save_button.pack(
    side="left"
)

add_button = tk.Button(
    task_group,
    text="Add Task",
    command=add_task_window
)

add_button.pack(
    side="left"
)

update_button = tk.Button(
    task_group,
    text="Update Task",
    command=update_selected_task
)

update_button.pack(
    side="left"
)

delete_button = tk.Button(
    task_group,
    text="Delete Task",
    command=delete_selected_task
)

delete_button.pack(
    side="left"
)


outdent_button = tk.Button(
    hierarchy_group,
    text="Outdent",
    command=outdent_selected_task
)

outdent_button.pack(
    side="left"
)

indent_button = tk.Button(
    hierarchy_group,
    text="Indent",
    command=indent_selected_task
)

indent_button.pack(
    side="left"
)

move_up_button = tk.Button(
    hierarchy_group,
    text="Move Up",
    command=move_selected_task_up
)

move_up_button.pack(
    side="left"
)

move_down_button = tk.Button(
    hierarchy_group,
    text="Move Down",
    command=move_selected_task_down
)

move_down_button.pack(
    side="left"
)

table.pack(fill="both", expand=True)

table.bind("<Double-1>", edit_cell)
table.bind("<Button-1>", handle_click_away)

refresh_table()
    
window.mainloop()