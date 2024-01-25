from django.db import models
from django.urls import reverse, reverse_lazy

class Electronic(models.Model):
    title = models.CharField(
        default='Ноутбук',
        max_length=150,
        verbose_name='Наименование',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    photo = models.ImageField(
        upload_to='image/%Y/%m/%d',
        verbose_name='Фото'
    )
    price = models.FloatField(
        default=10000,
        verbose_name='Цена'
    )
    diagonal = models.FloatField(verbose_name='Диагональ')
    SSD_Volume = models.IntegerField(verbose_name='Объем SSD')
    date_create = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    date_update = models.DateField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    exist = models.BooleanField(
        default=True,
        verbose_name='Наличие'
    )

    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT, null=True, verbose_name='Поставщик')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'
        ordering = ['title']


# ID - автоматическое создание Django
# title - наименование товара
# description - описание
# photo - фото
# price - цена
# processor - тип процессора
# diagonal - диагональ
# SSD volume - объем SSD
# exist (логическое существование)

class Supplier(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование поставщика')
    representative_firstname = models.CharField(max_length=150, verbose_name='Имя представителя поставщика')
    representative_lastname = models.CharField(max_length=150, verbose_name='Фамилия представителя поставщика')
    representative_patronymic = models.CharField(max_length=150, verbose_name='Отчество представителя поставщика')
    exist = models.BooleanField(default=True, verbose_name='Сотрудничество')

    def get_absolute_url(self):
        return reverse('info_supplier_view', kwargs={'supplier_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['title']

class Order(models.Model):
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания заказа'
    )
    date_finish = models.DateTimeField(
        null=True,
        verbose_name='Дата окончания заказа',
        blank=True
    )
    price = models.FloatField(
        null=True,
        verbose_name='Стоимость заказа'
    )
    address = models.CharField(
        max_length=200,
        verbose_name='Адрес доставки ноутбука'
    )
    status = models.CharField(
        max_length=200,
        verbose_name='Состояние заказа',
        choices=[
            ('1', 'создан'),
            ('2', 'отменен'),
            ('3', 'согласован'),
            ('4', 'в пути'),
            ('5', 'завершен')
        ])

    laptops = models.ManyToManyField(Electronic, through='Pos_order')

    def __str__(self):
        return f"{self.date_create} {self.status} {self.price}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['date_create']

class Pos_order(models.Model):
    laptop = models.ForeignKey(
        Electronic, on_delete=models.PROTECT,
        verbose_name='Ноутбук'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        verbose_name='Заказ'
    )
    count_laptop = models.IntegerField(verbose_name='Количество ноутбуков')
    price = models.FloatField(verbose_name='Общая стоимость ноутбуков')

    def __str__(self):
        return self.laptop.title + ' ' + self.order.address + ' ' + self.order.status

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'
        ordering = ['laptop', 'order', 'price']

class Invoice(models.Model):

    date_printout = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания чека')
    address_printout = models.CharField(max_length=200, verbose_name='Адрес создания чека')
    terminal = models.CharField(max_length=20, verbose_name='Код терминала')
    order = models.OneToOneField(Order, on_delete=models.PROTECT, primary_key=True, verbose_name='Заказ')

    def __str__(self):
        return str(self.date_printout) + ' ' + self.terminal

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
        ordering = ['terminal', 'date_printout']

