from django.test import TestCase
from tasks.forms import TaskForm
from tasks.models import Category, Task

class TaskFormTest(TestCase):

    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.category = Category.objects.create(name="Work")

    def test_task_form_valid(self):
        # Test the TaskForm with valid data
        form_data = {
            'title': 'New Task',
            'due_date': '2025-12-31',
            'category': self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.title, 'New Task')
        self.assertEqual(task.due_date, '2025-12-31')
        self.assertEqual(task.category, self.category)

    def test_task_form_invalid(self):
        # Test the TaskForm with invalid data
        form_data = {
            'title': '',  # Invalid data: empty title
            'due_date': '2025-12-31',
            'category': self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['This field is required.'])
