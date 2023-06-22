from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from git_branch.models import *

class LevelsApiTest(APITestCase):
    def setUp(self):
        Levels.objects.create(title_level='Level 1', description='Description 1')

    def test_get_levels(self):
        url = reverse('levels')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 0)
        self.assertEqual(response.data['message'], 'Список уровней')
        self.assertEqual(response.data['levels'][0]['title_level'], 'Level 1')

    def test_get_levels_no_data(self):
        Levels.objects.all().delete()
        url = reverse('levels')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], -1)
        self.assertEqual(response.data['message'], 'Нет данных о уровнях')
        self.assertEqual(len(response.data['levels']), 0)


class TaskApiTest(APITestCase):
    def setUp(self):
        level = Levels.objects.create(title_level='Level 1', description='Description 1')
        Task.objects.create(level=level, solve=True)

    def test_get_tasks(self):
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 0)
        self.assertEqual(response.data['message'], 'Список всех задач')
        self.assertEqual(response.data['tasks'][0]['solve'], True)

    def test_get_tasks_no_data(self):
        Task.objects.all().delete()
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], -1)
        self.assertEqual(response.data['message'], 'Нет данных о задачах')
        self.assertEqual(len(response.data['tasks']), 0)

class LevelsModelTest(TestCase):
    def setUp(self):
        Levels.objects.create(title_level='Level 1', description='Description 1')

    def test_title_level(self):
        level = Levels.objects.get(title_level='Level 1')
        self.assertEqual(level.title_level, 'Level 1')

    def test_description(self):
        level = Levels.objects.get(title_level='Level 1')
        self.assertEqual(level.description, 'Description 1')


class TaskModelTest(TestCase):
    def setUp(self):
        level = Levels.objects.create(title_level='Level 1', description='Description 1')
        Task.objects.create(level=level, solve=True)

    def test_level(self):
        task = Task.objects.get(solve=True)
        self.assertEqual(task.level.title_level, 'Level 1')

    def test_solve(self):
        task = Task.objects.get(solve=True)
        self.assertTrue(task.solve)


class InfoModelTest(TestCase):
    def setUp(self):
        level = Levels.objects.create(title_level='Level 1', description='Description 1')
        task = Task.objects.create(level=level, solve=True)
        Info.objects.create(title='Info 1', task=task)

    def test_title(self):
        info = Info.objects.get(title='Info 1')
        self.assertEqual(info.title, 'Info 1')

    def test_task(self):
        info = Info.objects.get(title='Info 1')
        self.assertEqual(info.task.solve, True)


class InfoDetailModelTest(TestCase):
    def setUp(self):
        level = Levels.objects.create(title_level='Level 1', description='Description 1')
        task = Task.objects.create(level=level, solve=True)
        info = Info.objects.create(title='Info 1', task=task)
        InfoDetail.objects.create(info=info, content='Content 1')

    def test_info(self):
        info_detail = InfoDetail.objects.get(content='Content 1')
        self.assertEqual(info_detail.info.title, 'Info 1')

    def test_content(self):
        info_detail = InfoDetail.objects.get(content='Content 1')
        self.assertEqual(info_detail.content, 'Content 1')