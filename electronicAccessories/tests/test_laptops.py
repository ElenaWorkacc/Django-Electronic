from django.test import TestCase, Client
from django.urls import reverse
from electronicAccessories.models import Electronic


class ElectronicTestCase(TestCase):
    def setUp(self):
        # Создаем несколько объектов модели Electronic
        self.laptop1 = Electronic.objects.create(
            title='Laptop1', description='Description1', price=1000, diagonal='14.4', SSD_Volume=256)
        self.laptop2 = Electronic.objects.create(
            title='Laptop2', description='Description2', price=2000, diagonal='15.2', SSD_Volume=512)

    def test_laptop_detail_view(self):
        # Создаем экземпляр клиента
        client = Client()

        # Получаем URL для первого ноутбука
        url = reverse('one_laptop', args=[str(self.laptop1.id)])

        # Отправляем GET-запрос на URL
        response = client.get(url)

        # Проверяем, что ответ содержит ожидаемый текст
        self.assertContains(response, 'Laptop1')
        self.assertContains(response, 'Description1')
        self.assertContains(response, '1000')

    def test_laptop_delete_view(self):
        # Создаем экземпляр клиента
        client = Client()

        # Получаем URL для удаления первого ноутбука
        url = reverse('laptop_delete', args=[str(self.laptop1.id)])

        # Отправляем GET-запрос на URL
        response = client.get(url)

        # Проверяем, что ответ содержит ожидаемый текст
        self.assertContains(response, 'Вы действительно хотите удалить товар?')

        # Отправляем POST-запрос на URL для подтверждения удаления
        response = client.post(url)

        # Проверяем, что объект модели был удален
        with self.assertRaises(Electronic.DoesNotExist):
            Electronic.objects.get(pk=self.laptop1.id)
