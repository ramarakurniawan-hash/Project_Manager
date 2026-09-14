from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox
import json

class Task:
    def __init__(self, name, start_date, end_date, status):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1

def find_task(tasks, task_name):
    for task in tasks:
        if task.name == task_name:
            return task

    return None

def validate_dates(start_date, end_date):
    if start_date > end_date:
        return False
    
    return True

def update_task(tasks, task_name, new_name, new_start, new_end, new_status):
    task = find_task(tasks, task_name)

    if task is None:
        print("Task not found.")
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

def delete_task(tasks, task_name):
    task = find_task(tasks, task_name)

    if task is None:
        print("Task not found.")
        return

    tasks.remove(task)

def save_tasks(tasks):
    task_data = []

    for task in tasks:
        task_data.append({
            "name": task.name,
            "start_date": task.start_date.isoformat(),
            "end_date": task.end_date.isoformat(),
            "status": task.status   
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
            task["status"]
        )
        tasks.append(new_task)

    return tasks

tasks = load_tasks()

def select_task(event):
    selected_item = table.selection()

    if selected_item:
        item = table.item(selected_item[0])
        task_name = item["values"][0]

        task = find_task(tasks, task_name)

def refresh_table():
    for item in table.get_children():
        table.delete(item)

    for task in tasks:
        table.insert(
            "",
            "end",
            values=(
                task.name,
                task.start_date,
                task.end_date,
                task.duration,
                task.status
            )
        )

def update_selected_task():
    selected_item = table.selection()

    if selected_item:
        item = table.item(selected_item[0])
        task_name = item["values"][0]

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
            item["values"][0]
        )

        start_label = tk.Label(
            edit_window,
            text="Start Date:"
        )
        start_label.pack(pady=5)

        start_entry = tk.Entry(
            edit_window
        )
        start_entry.pack(pady=5)

        start_entry.insert(
            0,
            item["values"][1]
        )

        end_label = tk.Label(
            edit_window,
            text="End Date:"
        )
        end_label.pack(pady=5)

        end_entry = tk.Entry(
            edit_window
        )
        end_entry.pack(pady=5)

        end_entry.insert(
            0,
            item["values"][2]
        )

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

        status_dropdown.set(item["values"][4])

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
                task_name,
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
        task_name = item["values"][0]

        confirm = messagebox.askyesno(
            "Delete Task",
            f"Are you sure you want to delete the task '{task_name}'?"
        )

        if confirm:
            delete_task(tasks, task_name)
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

    start_entry = tk.Entry(
        task_window
    )
    start_entry.pack()

    end_label = tk.Label(
        task_window,
        text="End Date:"
    )
    end_label.pack(pady=5)

    end_entry = tk.Entry(
        task_window
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

table = ttk.Treeview(
    window,
    columns=("Task", "Start", "End", "Duration", "Status"),
    show="headings"
)

table.bind("<<TreeviewSelect>>", select_task)

table.heading("Task", text="Task")
table.heading("Start", text="Start")
table.heading("End", text="End")
table.heading("Duration", text="Duration")
table.heading("Status", text="Status")

table.column("Task", width=200, stretch=True)
table.column("Start", width=120, stretch=True)
table.column("End", width=120, stretch=True)
table.column("Duration", width=100, stretch=True)
table.column("Status", width=150, stretch=True)

table.pack(fill="both", expand=True)

update_button = tk.Button(
    window,
    text="Update Task",
    command=update_selected_task
)

update_button.pack()

add_button = tk.Button(
    window,
    text="Add Task",
    command=add_task_window
)

add_button.pack()

delete_button = tk.Button(
    window,
    text="Delete Task",
    command=delete_selected_task
)

delete_button.pack()

save_button = tk.Button(
    window,
    text="Save",
    command=lambda: save_tasks(tasks)
)

save_button.pack()

for task in tasks:
    table.insert(
        "",
        "end",
        values=(
            task.name,
            task.start_date,
            task.end_date,
            task.duration,
            task.status
        )
    )
    
window.mainloop()
