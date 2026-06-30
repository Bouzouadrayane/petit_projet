from django.test import TestCase
from rest_framework.test import APIClient
from mongoengine import connect, disconnect
from .models import Task


class TaskAPITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        disconnect()
        connect('tododb-test', host='mongomock://localhost')

    def setUp(self):
        Task.objects.delete()
        self.client = APIClient()

    # 1. Créer une tâche → 201
    def test_create_task(self):
        response = self.client.post('/api/tasks/', {'title': 'Apprendre k8s'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Apprendre k8s')
        self.assertFalse(response.data['done'])
        self.assertIn('id', response.data)

    # 2. Créer sans title → 400
    def test_create_task_missing_title(self):
        response = self.client.post('/api/tasks/', {}, format='json')
        self.assertEqual(response.status_code, 400)

    # 3. Lister les tâches → 200 + liste non vide
    def test_list_tasks(self):
        Task(title='Task 1').save()
        Task(title='Task 2').save()
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    # 4. Récupérer une tâche par id → 200
    def test_get_task(self):
        task = Task(title='Ma tâche').save()
        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Ma tâche')

    # 5. Modifier une tâche → 200 + done=True
    def test_update_task(self):
        task = Task(title='A faire').save()
        response = self.client.put(f'/api/tasks/{task.id}/', {'done': True}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['done'])

    # 6. Supprimer une tâche → 204
    def test_delete_task(self):
        task = Task(title='A supprimer').save()
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 0)

    # 7. Récupérer une tâche inexistante → 404
    def test_get_task_not_found(self):
        response = self.client.get('/api/tasks/000000000000000000000000/')
        self.assertEqual(response.status_code, 404)
