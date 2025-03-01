from django.test import TestCase
from django.urls import reverse
from tasks.models import Task, Category

class TaskViewsTest(TestCase):

    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.category = Category.objects.create(name="Work")
        self.task = Task.objects.create(
            title="Test Task",
            due_date="2025-12-31",
            completed=False,
            category=self.category
        )

    def test_home_view_get(self):
        # Test the home view with a GET request
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertContains(response, 'Test Task')
        self.assertContains(response, '2025-12-31')
        self.assertContains(response, 'Work')
        self.assertContains(response, 'Add Task')
        self.assertContains(response, 'To-Do')
        self.assertContains(response, 'Done')

    def test_home_view_post_valid(self):
        # Test the home view with a valid POST request
        response = self.client.post(reverse('home'), {
            'title': 'New Task',
            'due_date': '2025-12-31',
            'completed': False,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertEqual(Task.objects.count(), 2)  # Ensure a new task is created
        self.assertEqual(Task.objects.last().title, 'New Task')  # Check the title of the new task
        self.assertEqual(Task.objects.last().due_date, '2025-12-31')  # Check the due date of the new task
        self.assertEqual(Task.objects.last().completed, False)  # Check the completed status of the new task
        self.assertEqual(Task.objects.last().category, self.category)  # Check the category of the new task

    def test_home_view_post_invalid(self):
        # Test the home view with an invalid POST request
        response = self.client.post(reverse('home'), {
            'title': '',  # Invalid data: empty title
            'due_date': '2025-12-31',
            'completed': False,
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 200)  # Should not redirect
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertEqual(Task.objects.count(), 1)  # Ensure no new task is created
