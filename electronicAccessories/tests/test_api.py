from rest_framework.test import APITestCase
from django.urls import reverse
from electronicAccessories.models import Electronic
from electronicAccessories.serializers import ElectronicSerilizer
from rest_framework import status

class ElectronicApiTestCase(APITestCase):
    def test_get_list(self):
        laptop_1 = Electronic.objects.create(title='Ноутбук HP', price=48900, diagonal=15.5, SSD_Volume=512)
        laptop_2 = Electronic.objects.create(title='Ноутбук Lenovo', price=56700, diagonal=14.8, SSD_Volume=256)

        response = self.client.get(reverse('laptops_api_list'))

        serial_data = ElectronicSerilizer([laptop_1, laptop_2], many=True).data
        serial_data = {'laptops_list': serial_data}

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serial_data, response.data)

class ElectronicAPITest(APITestCase):
    def setUp(self):
        self.laptop1 = Electronic.objects.create(
            title='Asus', price=1000, diagonal=14.7, SSD_Volume=256, exist=True
        )
        self.laptop2 = Electronic.objects.create(
            title='Lenovo', price=800, diagonal=14.7, SSD_Volume=256, exist=False
        )

    def test_get_laptop(self):
        url = reverse('laptops_api_one', kwargs={'pk': self.laptop1.pk})
        response = self.client.get(url)
        laptop1 = Electronic.objects.get(pk=self.laptop1.pk)
        serializer = ElectronicSerilizer(laptop1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_laptop(self):
        url = reverse('laptops_api_one', kwargs={'pk': self.laptop1.pk})
        data = {
            'title': 'Asus Laptop',
            'price': 1200,
            'diagonal': '14.7',
            'SSD_Volume': 512,
            'exist': False
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        laptop1 = Electronic.objects.get(pk=self.laptop1.pk)
        serializer = ElectronicSerilizer(laptop1)
        self.assertEqual(serializer.data['title'], data['title'])
        self.assertEqual(serializer.data['price'], data['price'])
        self.assertEqual(serializer.data['exist'], data['exist'])

    def test_delete_laptop(self):
        url = reverse('laptops_api_one', kwargs={'pk': self.laptop1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
