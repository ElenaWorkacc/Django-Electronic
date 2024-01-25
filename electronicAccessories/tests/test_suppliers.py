from django.test import TestCase
from django.urls import reverse
from ..models import Supplier

class SupplierListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание объектов поставщиков для тестирования
        number_of_suppliers = 5
        for supplier_id in range(number_of_suppliers):
            Supplier.objects.create(
                title=f'Поставщик{supplier_id}',
                representative_firstname=f'Имя{supplier_id}',
                representative_lastname=f'Фамилия{supplier_id}',
                representative_patronymic=f'Отчество{supplier_id}',
                exist=True
            )

    def test_view_url_accessible_by_name(self):
        # Тестирование доступности страницы со списком поставщиков по имени url
        response = self.client.get(reverse('list_supplier'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Тестирование правильности использования шаблона для страницы со списком поставщиков
        response = self.client.get(reverse('list_supplier'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'electronicAccessories/supplier/supplier_list.html')

    def test_extra_context(self):
        # Тестирование дополнительного контекста на странице списка поставщиков
        response = self.client.get(reverse('list_supplier'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['name'], 'Список поставщиков')
