from django.test import TestCase

from todo.main.models import YourTask


class ModelsTestCase(TestCase):
    def test_tasks_title(self):
        tasks = YourTask.objects.create(title="Create a test")
        tasks.save()
        self.assertEqual(tasks.title, tasks.__str__())
