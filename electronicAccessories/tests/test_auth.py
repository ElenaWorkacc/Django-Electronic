from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client


class AuthorizationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_authorization_success(self):
        response = self.client.post(reverse('auth'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('laptop_index'))

