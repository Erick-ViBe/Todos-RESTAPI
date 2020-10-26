from django.test import TestCase
from django.contrib.auth import get_user_model

from tasks.models import Task


def sample_user(username='test@gmail.com', password='testpassword'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):

    def test_task_str(self):
        """Test the task string representation"""
        task = Task.objects.create(
            author=sample_user(),
            content='Make tea',
        )

        self.assertEqual(str(task), task.content)
