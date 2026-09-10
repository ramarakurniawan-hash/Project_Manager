from datetime import date
import tkinter as tk
from tkinter import ttk

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

tasks = [
    Task(
        "Requirement Gathering",
        date(2026, 9, 10),
        date(2026, 9, 15),
        "Done"
    ),

    Task(
        "Development",
        date(2026, 9, 16),
        date(2026, 9, 30),
        "In Progress"
    )
]

print("Number of tasks:", len(tasks))
print()

for task in tasks:
    print_task(task)

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

# new_task = add_task(tasks)

# update_task(tasks, "Development")

# delete_task(tasks, "Development")

print()
print("Updated number of tasks:", len(tasks))
print()

for task in tasks:
    print_task(task)

def select_task(event):
    selected_item = table.selection()

    if selected_item:
        item = table.item(selected_item[0])
        task_name = item["values"][0]

        task = find_task(tasks, task_name)
        
        if task:
            print("Selected Task:", task.name)
            print("Status:", task.status)

def update_selected_task():
    selected_item = table.selection()

    if selected_item:
        item = table.item(selected_item[0])
        task_name = item["values"][0]

        print("Update selected task:", task_name)

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