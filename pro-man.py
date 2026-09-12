from datetime import date
import tkinter as tk
from tkinter import ttk, simpledialog
import json

class Task:
    def __init__(self, name, start_date, end_date, status):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.duration = (end_date - start_date).days + 1
        self.status = status

def print_task(task):
    print("Task:", task.name)
    print("Start:", task.start_date)
    print("End:", task.end_date)
    print("Duration:", task.duration, "days")
    print("Status:", task.status)
    print()

def add_task(tasks):
    new_task_name = input("Enter a task name: ")
    new_task_start = input("Enter start date (YYYY-MM-DD): ")
    new_task_end = input("Enter end date (YYYY-MM-DD): ")

    new_task_start = date.fromisoformat(new_task_start)
    new_task_end = date.fromisoformat(new_task_end)

    while True:
        new_task_status = input("Enter the status (Done/In Progress/Not Started): ")
        if new_task_status in ["Done", "In Progress", "Not Started"]:
            break
        else:
            print("Invalid status. Please try again.")

    if new_task_status == "Done":
        print("Task is completed!")
    elif new_task_status == "In Progress":
        print("Task is currently being worked on.")
    else:
        print("Task has not started yet.")

    new_task = Task(
        new_task_name,
        new_task_start,
        new_task_end,
        new_task_status
    )

    tasks.append(new_task)

    return new_task

def find_task(tasks, task_name):
    for task in tasks:
        if task.name == task_name:
            return task

    return None

def update_task(tasks, task_name, new_status):
    task = find_task(tasks, task_name)

    if task is None:
        print("Task not found.")
        return
        
    task.status = new_status

    print("Task updated!")

def delete_task(tasks, task_name):
    task = find_task(tasks, task_name)

    if task is None:
        print("Task not found.")
        return

    tasks.remove(task)
    
    print("Task deleted!")

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
        
        if task:
            print("Selected Task:", task.name)
            print("Status:", task.status)

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

        status_window = tk.Toplevel(window)
        status_window.title("Update Status")
        status_window.geometry("300x150")

        status_label = tk.Label(
            status_window,
            text="Select new status:"
        )
        status_label.pack(pady=10)

        status_dropdown = ttk.Combobox(
            status_window,
            values=["Done", "In Progress", "Not Started"],
            state="readonly"
        )
        status_dropdown.pack()

        status_dropdown.set(item["values"][4])

        def confirm_status_update():
            new_status = status_dropdown.get()

            update_task(
                tasks,
                task_name,
                new_status
            )

            save_tasks(tasks)

            refresh_table()
            status_window.destroy()

        update_button = tk.Button(
            status_window,
            text="Update",
            command=confirm_status_update
        )

        update_button.pack(pady=15)

def delete_selected_task():
    selected_item = table.selection()

    if selected_item:
        item = table.item(selected_item[0])
        task_name = item["values"][0]

        delete_task(tasks, task_name)

        save_tasks(tasks)

        refresh_table()

def add_task_window():
    task_window = tk.Toplevel(window)
    task_window.title("Add Task")
    task_window.geometry("350x250")

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
    status_dropdown.pack()

    status_dropdown.set("Not Started")

    def save_new_task():
        new_task_name = task_entry.get()
        new_task_start = date.fromisoformat(start_entry.get())
        new_task_end = date.fromisoformat(end_entry.get())
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
    text="Update Status",
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