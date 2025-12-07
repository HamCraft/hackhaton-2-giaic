import json
import os
from datetime import datetime
from typing import List, Optional

# ----------------------------
# Task Model
# ----------------------------
class Task:
    def __init__(self, id: int, title: str, description: str = "",
                 priority: str = "medium", tags: List[str] = None,
                 due_date: Optional[str] = None, completed: bool = False,
                 created_at: str = None):

        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.tags = tags or []
        self.due_date = due_date  # Format: "YYYY-MM-DD"
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert task to dictionary for JSON
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "tags": self.tags,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at
        }

    # Recreate a Task instance from dictionary
    @staticmethod
    def from_dict(data):
        return Task(**data)


# ----------------------------
# Todo Manager
# ----------------------------
class TodoManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()

    # Load tasks from JSON
    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task) for task in data]
        else:
            self.tasks = []

    # Save tasks to JSON
    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    # Generate new task ID
    def generate_id(self):
        return max([task.id for task in self.tasks], default=0) + 1

    # Add a new task
    def add_task(self):
        title = input("Enter task title: ")
        description = input("Enter task description: ")

        priority = input("Priority (low/medium/high): ").lower()
        if priority not in ["low", "medium", "high"]:
            priority = "medium"

        tags = input("Tags (comma separated): ").lower().split(",")

        due_date = input("Due date (YYYY-MM-DD or blank): ")
        if due_date.strip() == "":
            due_date = None

        new_task = Task(
            id=self.generate_id(),
            title=title,
            description=description,
            priority=priority,
            tags=[t.strip() for t in tags if t.strip()],
            due_date=due_date
        )

        self.tasks.append(new_task)
        self.save_tasks()
        print("Task added successfully!")

    # Delete a task
    def delete_task(self):
        task_id = int(input("Enter task ID to delete: "))
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
        print("Task deleted.")

    # Update task
    def update_task(self):
        task_id = int(input("Enter task ID to update: "))
        task = self.find_task(task_id)

        if not task:
            print("Task not found.")
            return

        print("Leave blank to keep current value.")

        title = input(f"New title (current: {task.title}): ")
        description = input(f"New description (current: {task.description}): ")

        priority = input(f"Priority (low/medium/high) (current: {task.priority}): ").lower()

        tags = input(f"Tags comma separated (current: {task.tags}): ")
        due_date = input(f"Due date YYYY-MM-DD (current: {task.due_date}): ")

        if title:
            task.title = title
        if description:
            task.description = description

        if priority in ["low", "medium", "high"]:
            task.priority = priority

        if tags.strip():
            task.tags = [t.strip() for t in tags.split(",")]

        if due_date.strip():
            task.due_date = due_date

        self.save_tasks()
        print("Task updated.")

    # Mark complete / incomplete
    def toggle_complete(self):
        task_id = int(input("Enter task ID to toggle completion: "))
        task = self.find_task(task_id)

        if not task:
            print("Task not found.")
            return

        task.completed = not task.completed
        self.save_tasks()
        print("Task status changed.")

    # Find task by ID
    def find_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    # View tasks
    def view_tasks(self):
        if not self.tasks:
            print("\nNo tasks found.\n")
            return

        print("\n-------- TASK LIST --------")
        for task in self.tasks:
            status = "✔ Completed" if task.completed else "❌ Not Completed"
            print(f"""
ID: {task.id}
Title: {task.title}
Description: {task.description}
Priority: {task.priority}
Tags: {task.tags}
Due Date: {task.due_date}
Created At: {task.created_at}
Status: {status}
------------------------------
""")

    # Search tasks by keyword
    def search_tasks(self):
        keyword = input("Enter keyword: ").lower()
        results = [t for t in self.tasks if keyword in t.title.lower() or keyword in t.description.lower()]

        if not results:
            print("No matching tasks.")
            return

        print("\nSearch Results:")
        for t in results:
            print(f"- {t.id} | {t.title}")

    # Filter by priority or completion
    def filter_tasks(self):
        print("""
1. Filter by completed
2. Filter by not completed
3. Filter by priority
""")
        choice = input("Choose option: ")

        if choice == "1":
            filtered = [t for t in self.tasks if t.completed]
        elif choice == "2":
            filtered = [t for t in self.tasks if not t.completed]
        elif choice == "3":
            p = input("Enter priority (low/medium/high): ")
            filtered = [t for t in self.tasks if t.priority == p]
        else:
            print("Invalid choice.")
            return

        for t in filtered:
            print(f"- {t.id} | {t.title} | {t.priority}")

    # Sort tasks
    def sort_tasks(self):
        print("""
1. Sort by priority
2. Sort alphabetically
3. Sort by creation date
""")

        choice = input("Choose sort option: ")

        if choice == "1":
            self.tasks.sort(key=lambda x: ["low", "medium", "high"].index(x.priority))
        elif choice == "2":
            self.tasks.sort(key=lambda x: x.title.lower())
        elif choice == "3":
            self.tasks.sort(key=lambda x: x.created_at)
        else:
            print("Invalid choice.")
            return

        self.save_tasks()
        print("Tasks sorted.")


# ----------------------------
# Console Menu
# ----------------------------
def main():
    manager = TodoManager()

    while True:
        print("""
========== TODO APP ==========
1. Add Task
2. Delete Task
3. Update Task
4. View Tasks
5. Mark Complete/Incomplete
6. Search Tasks
7. Filter Tasks
8. Sort Tasks
9. Exit
""")

        choice = input("Choose an option: ")

        if choice == "1":
            manager.add_task()
        elif choice == "2":
            manager.delete_task()
        elif choice == "3":
            manager.update_task()
        elif choice == "4":
            manager.view_tasks()
        elif choice == "5":
            manager.toggle_complete()
        elif choice == "6":
            manager.search_tasks()
        elif choice == "7":
            manager.filter_tasks()
        elif choice == "8":
            manager.sort_tasks()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
