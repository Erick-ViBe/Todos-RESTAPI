from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from tasks.models import Task

from tasks.serializers import TaskSerializer


TASKS_URL = reverse('tasks:task-list')


def detail_url(task_id):
    """Return task detail URL"""
    return reverse('tasks:task-detail', args=[task_id])


def change_done_url(task_id):
    """Return done state change URL"""
    return reverse('tasks:task-done-change', args=[task_id])


class PublicTasksAPITests(TestCase):
    """Test the publicly available tasks API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tasks"""
        res = self.client.get(TASKS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTasksAPITests(TestCase):
    """Test the authorized user tasks API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testusername',
            color='pink',
            password='testpassword'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tasks(self):
        """Test retrieving tasks"""
        Task.objects.create(author=self.user, content='Make dinner')
        Task.objects.create(author=self.user, content='Make video')

        res = self.client.get(TASKS_URL)

        tasks = Task.objects.all().order_by('-created_at')
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tasks_limited_to_user(self):
        """Test that tasks returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            username='usernametest',
            color='pink',
            password='testpassword'
        )
        Task.objects.create(author=user2, content='Todo for user 2')
        task = Task.objects.create(author=self.user, content='Make sandwich')

        res = self.client.get(TASKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['content'], task.content)

    def test_view_task_detail(self):
        """Test viewing a task detail"""
        task = Task.objects.create(author=self.user, content='Some content')

        url = detail_url(task.id)
        res = self.client.get(url)

        serializer = TaskSerializer(task)

        self.assertEqual(res.data, serializer.data)

    def test_create_task(self):
        """Test creating task"""
        payload = {
            'content': 'Some Content of a task'
        }

        res = self.client.post(TASKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(task, key))

    def test_partial_update_task(self):
        """Test updating a task with PATCH"""
        task = Task.objects.create(
            author=self.user,
            content='Some fun content'
        )

        payload = {
            'done': 1
        }

        url = detail_url(task.id)
        self.client.patch(url, payload)

        task.refresh_from_db()

        self.assertEqual(task.done, payload['done'])

    def test_full_update_task(self):
        """Test updating a task with PUT"""
        task = Task.objects.create(author=self.user, content='Some content')

        payload = {
            'content': 'Updated content',
            'done': 1
        }

        url = detail_url(task.id)
        self.client.put(url, payload)

        task.refresh_from_db()

        self.assertEqual(task.content, payload['content'])
        self.assertEqual(task.done, payload['done'])

    def test_delete_task(self):
        """Test deleting a task with DELETE"""
        task = Task.objects.create(
            author=self.user, content='Delete this task'
        )

        url = detail_url(task.id)
        self.client.delete(url)

        task_exists = Task.objects.filter(
            id=task.id
        ).exists()

        self.assertFalse(task_exists)

    def test_filter_finished_tasks(self):
        """Test returning task with done field equals true"""
        task1 = Task.objects.create(
            author=self.user,
            content='Finished task',
            done=True
        )
        task2 = Task.objects.create(
            author=self.user,
            content="Task"
        )

        res = self.client.get(
            TASKS_URL,
            {'done': 1}
        )

        serializer1 = TaskSerializer(task1)
        serializer2 = TaskSerializer(task2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_filter_not_finished_tasks(self):
        """Test returning task with done field equals false"""
        task1 = Task.objects.create(
            author=self.user,
            content='Finished task',
            done=True
        )
        task2 = Task.objects.create(
            author=self.user,
            content="Task"
        )

        res = self.client.get(
            TASKS_URL,
            {'done': 0}
        )

        serializer1 = TaskSerializer(task1)
        serializer2 = TaskSerializer(task2)

        self.assertNotIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_done_state_false_to_true(self):
        """Test done state change false to true successfully"""
        task = Task.objects.create(
            author=self.user,
            content='Some content'
        )

        url = change_done_url(task.id)
        self.client.post(url)

        task.refresh_from_db()

        self.assertEqual(task.done, True)

    def test_done_state_true_to_false(self):
        """Test done state change true to false successfully"""
        task = Task.objects.create(
            author=self.user,
            content='Some content',
            done=True
        )

        url = change_done_url(task.id)
        self.client.post(url)

        task.refresh_from_db()

        self.assertEqual(task.done, False)

    def test_done_state_change_only_limited_to_user(self):
        """Test only change done state for users tasks"""
        user2 = get_user_model().objects.create_user(
            username='usernametest',
            password='testpassword'
        )

        task = Task.objects.create(
            author=user2,
            content='Some content'
        )

        url = change_done_url(task.id)
        res = self.client.post(url)

        task.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(task.done, False)
