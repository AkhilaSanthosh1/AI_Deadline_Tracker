from datetime import datetime
import time
import json
from plyer import notification

class Task:
    def __init__(self, name, deadline, priority, milestones=None):
        self.name = name
        self.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        self.priority = priority
        self.milestones = milestones if milestones else []
        self.completed = False
        self.milestone_status = {m: False for m in self.milestones}

    def time_remaining(self):
        return (self.deadline - datetime.now()).total_seconds()

    def check_milestones(self):
        for milestone, done in self.milestone_status.items():
            if not done:
                time_left = self.time_remaining()
                if time_left <= 86400:
                    return f"Reminder: Complete milestone '{milestone}' for {self.name}"
        return None

def prioritize_tasks(tasks):
    # TODO: Replace with real AI model (e.g., LLaMA 3.2) via API in the future
    workload = sum(1 for task in tasks if task.time_remaining() <= 86400 and not task.completed)
    for task in tasks:
        if workload > 3:
            task.priority = max(1, task.priority - 1)
    return sorted(tasks, key=lambda x: (x.time_remaining(), x.priority))

def check_deadlines(tasks):
    for task in tasks:
        if not task.completed:
            remaining = task.time_remaining()
            if remaining <= 3600:
                notification.notify(
                    title=f"Reminder: {task.name}",
                    message=f"Deadline approaching! Due at {task.deadline.strftime('%Y-%m-%d %H:%M')}",
                    timeout=10
                )
            milestone_reminder = task.check_milestones()
            if milestone_reminder:
                notification.notify(
                    title=f"Milestone Alert: {task.name}",
                    message=milestone_reminder,
                    timeout=10
                )

def add_task_interactively():
    name = input("Enter task name: ")
    deadline = input("Enter deadline (YYYY-MM-DD HH:MM, e.g., 2025-03-06 10:00): ")
    priority = int(input("Enter priority (1=high, 2=medium, 3=low): "))
    milestones = input("Enter milestones (comma-separated, e.g., Draft,Review) or press Enter for none: ")
    milestones = [m.strip() for m in milestones.split(",")] if milestones else []
    return Task(name, deadline, priority, milestones)

def save_tasks(tasks, filename="tasks.json"):
    task_data = [
        {
            "name": t.name,
            "deadline": t.deadline.strftime("%Y-%m-%d %H:%M"),
            "priority": t.priority,
            "milestones": t.milestones,
            "completed": t.completed,
            "milestone_status": t.milestone_status
        } for t in tasks
    ]
    with open(filename, "w") as f:
        json.dump(task_data, f)

def load_tasks(filename="tasks.json"):
    try:
        with open(filename, "r") as f:
            task_data = json.load(f)
            return [
                Task(t["name"], t["deadline"], t["priority"], t["milestones"])
                for t in task_data
            ]
    except FileNotFoundError:
        return []

def main():
    tasks = load_tasks()
    print("Starting AI Deadline Tracker...")
    print("Add tasks (type 'done' when finished)")
    
    while True:
        user_input = input("Add a task? (yes/done): ").lower()
        if user_input == "done":
            break
        elif user_input == "yes":
            tasks.append(add_task_interactively())
    
    while True:
        prioritized_tasks = prioritize_tasks(tasks)
        print("\nPrioritized Tasks:")
        for i, task in enumerate(prioritized_tasks, 1):
            print(f"{i}. {task.name} - Due: {task.deadline} - Priority: {task.priority}")
        check_deadlines(tasks)
        save_tasks(tasks)
        time.sleep(30)

if __name__ == "__main__":
    main()