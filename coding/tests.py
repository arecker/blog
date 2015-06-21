from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.conf import settings
from .models import Project
import os



class ProjectAPITests(APITestCase):
    fixutres = [
        os.path.join(settings.BASE_DIR, 'coding', 'fixtures', 'projects.json')
    ]


    def setUp(self):
        self.client = APIClient()


    def test_list(self):
        response = self.client.get('/api/projects/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Project.objects.all().count())


    def test_forbidden_post(self):
        response = self.client.post('/api/projects/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_forbidden_delete(self):
        response = self.client.delete('/api/projects/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_forbidden_put(self):
        response = self.client.put('/api/projects/1/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


