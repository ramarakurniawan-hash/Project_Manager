# Pro-Man

A lightweight project management tool built with Python and Tkinter.

## About

Pro-Man is a personal learning project inspired by project management
tools such as Smartsheet and Excel.

I am building this application to strengthen my practical programming
skills while applying concepts from my experience in project and
payment-system implementation.

The project is being developed incrementally, starting with a simple
task tracker and gradually expanding toward features such as Gantt
charts, dashboards, and persistent project data.

## Current Features

- Task management
  - Add new tasks
  - Update existing tasks
  - Delete tasks
  - View all tasks in a table

- Task information
  - Task name
  - Start date
  - End date
  - Automatically calculated duration
  - Task status:
    - Not Started
    - In Progress
    - Done

- Inline table editing
  - Double-click a task name to edit it directly
  - Double-click a start date to edit it
  - Double-click an end date to edit it
  - Double-click a status to select a new status
  - Press Enter to save an edit
  - Click away from the editor to save
  - Press Escape to cancel

- Date handling
  - Calendar-based date selection
  - Prevents an end date from being earlier than the start date
  - Prevents a start date from being later than the end date
  - Automatically recalculates task duration when dates change

- Data persistence
  - Tasks are saved to tasks.json
  - Tasks are automatically saved when changes are made
  - Tasks retain a unique ID between sessions

- GUI
  - Tkinter-based desktop interface
  - Editable task table
  - Add Task dialog
  - Update Task dialog
  - Delete confirmation

## Technologies

- Python
- Tkinter
- JSON
- Git / GitHub

## Current Status

 Work in progress

The current version is a functional prototype. Development is focused
on improving task editing, project visualization, and usability.

## Planned Features

- [x] Task creation, updating, and deletion
- [x] Task status management
- [x] Date validation
- [x] JSON data persistence
- [x] Inline task editing
- [x] Persistent task IDs
- [ ] Gantt chart
- [ ] Task dependencies
- [ ] Task hierarchy / indentation
- [ ] Task reordering
- [ ] Dashboard / project overview
- [ ] Excel export
- [ ] SQLite database
- [ ] Web-based version
- [ ] Multi-user/team functionality

## Why I Built This

I wanted to learn programming by building something directly related
to my professional experience rather than following isolated coding
exercises.

The long-term goal is to develop a practical project management tool
while learning software development concepts such as data modeling,
persistence, user interfaces, databases, and eventually web
application development.
