import unittest
from datetime import datetime, timedelta
from main import Task, prioritize_tasks

class TestDeadlineTracker(unittest.TestCase):
    def test_task_time_remaining(self):
        # Test time remaining calculation
        future_date = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
        task = Task("Test Task", future_date, 1)
        remaining = task.time_remaining()
        self.assertTrue(3500 < remaining < 3700)  # Around 1 hour in seconds

    def test_prioritize_tasks(self):
        # Test prioritization
        task1 = Task("Urgent", (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"), 1)
        task2 = Task("Later", (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"), 2)
        tasks = [task2, task1]
        prioritized = prioritize_tasks(tasks)
        self.assertEqual(prioritized[0].name, "Urgent")  # Urgent task should come first

if __name__ == "__main__":
    unittest.main()