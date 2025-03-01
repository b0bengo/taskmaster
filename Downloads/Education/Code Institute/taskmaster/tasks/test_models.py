from django.test import TestCase
from tasks.models import Task, Category
from django.core.exceptions import ValidationError

class TaskModelTest(TestCase):

    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.category = Category.objects.create(name="Work")
        self.task = Task.objects.create(
            title="Test Task",
            due_date="2025-12-31",
            completed=False,
            category=self.category
        )

    def test_task_creation(self):
        # Test task creation
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.due_date, "2025-12-31")
        self.assertEqual(self.task.completed, False)
        self.assertEqual(self.task.category, self.category)
        pass

    def test_task_str(self):
        # Test the string representation of the task
        self.assertEqual(str(self.task), "Test Task")
        pass

    def test_task_due_date(self):
        # Test the due date of the task
        self.assertEqual(self.task.due_date, "2025-12-31")
        pass

    def test_task_completed(self):
        # Test the completed status of the task
        self.assertEqual(self.task.completed, False)
        pass

    def test_task_category(self):
        # Test the category of the task
        self.assertEqual(self.task.category, self.category)
        self.assertEqual(self.category.name, "Work")
        self.assertEqual(str(self.category), "Work")
        self.assertEqual(self.category.__str__(), "Work")
        pass

    # generate a unit test that checks for an error if the title is longer than 100 characters
    def test_task_title_length(self):
        # Test the title length of the task
        self.task.title = "a" * 201  # Title longer than 200 characters
        with self.assertRaises(ValidationError):
            self.task.full_clean()  # This will trigger model validation
        pass