from django.test import TestCase
from django.urls import reverse
from ..forms import Form_registration


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.url = reverse('registr')

    def test_user_registration_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'electronicAccessories/auth/registr.html')
        self.assertIsInstance(response.context['form'], Form_registration)
