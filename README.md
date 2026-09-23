# Pro-Man

A lightweight project management tool built with Python and Tkinter.

## About

Pro-Man is a personal learning project inspired by project management
tools such as Smartsheet and Excel.

I am building this application to strengthen my practical programming
skills while applying concepts from my experience in project and
payment-system implementation.

The project is being developed incrementally, starting with a simple
task tracker and gradually expanding toward a more complete project
management application with features such as task hierarchy, Gantt
charts, dashboards, and persistent project data.

## Current Features

* Task management

  * Add new tasks
  * Update existing tasks
  * Delete tasks
  * View tasks in a table

* Task information

  * Task name
  * Start date
  * End date
  * Automatically calculated duration
  * Task status:

    * Not Started
    * In Progress
    * Done

* Inline table editing

  * Double-click a task name to edit it directly
  * Double-click a start date to edit it
  * Double-click an end date to edit it
  * Double-click duration to change the task duration
  * Double-click status to select a new status
  * Press Enter to save an edit
  * Click away from the editor to save
  * Press Escape to cancel

* Date handling

  * Calendar-based date selection
  * Prevents an end date from being earlier than the start date
  * Prevents a start date from being later than the end date
  * Automatically recalculates task duration when dates change
  * Changing duration automatically recalculates the end date

* Data persistence

  * Project data is saved to `project.json`
  * Changes are automatically saved
  * Tasks retain a unique ID between sessions
  * Project rows can contain either tasks or blank rows
  * Project and row structure is preserved between sessions

* GUI

  * Tkinter-based desktop interface
  * Editable task table
  * Row numbering
  * Add Task dialog
  * Update Task dialog
  * Delete confirmation
  * Ribbon-style task and hierarchy controls

## Technologies

* Python
* Tkinter / ttk
* tkcalendar
* JSON
* Git / GitHub

## Current Status

Work in progress.

The current version is a functional desktop prototype undergoing
structural refactoring.

The data model has been expanded from a simple task list into a project
and row-based structure. Current development is focused on completing
the hierarchy implementation and improving the underlying architecture
before moving on to row manipulation and further UI improvements.

## Planned Features

### Version 0.4

* [ ] Rebuild task hierarchy around the new project/row structure
* [ ] Task indentation
* [ ] Task outdentation
* [ ] Task reordering
* [ ] Preserve hierarchy and row order during save/load
* [ ] Complete removal of the legacy task-order structure

### Version 0.5

* [ ] Add Row functionality
* [ ] Insert rows above/below existing rows
* [ ] Blank row editing
* [ ] Improve row numbering and table alignment
* [ ] General UI cleanup and usability improvements

### Version 1.0

* [ ] Web-based version
* [ ] Web-based project table
* [ ] Task hierarchy
* [ ] Task dependencies
* [ ] Gantt chart
* [ ] Dashboard / project overview
* [ ] Excel export
* [ ] SQLite database
* [ ] Multi-user/team functionality

## Completed

* [x] Task creation, updating, and deletion
* [x] Task status management
* [x] Date validation
* [x] JSON data persistence
* [x] Inline task editing
* [x] Inline duration editing
* [x] Persistent task IDs
* [x] Project / Row / Task data model
* [x] Project-based save/load
* [x] Automatic project persistence after changes

## Why I Built This

I wanted to learn programming by building something directly related
to my professional experience rather than following isolated coding
exercises.

The long-term goal is to develop a practical project management tool
while learning software development concepts such as data modeling,
persistence, user interfaces, databases, and eventually web
application development.

The project is also intended to serve as a practical learning exercise
in gradually moving from a desktop prototype toward a web application.
