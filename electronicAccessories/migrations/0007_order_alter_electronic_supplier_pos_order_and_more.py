# Generated by Django 4.1.7 on 2023-05-08 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('electronicAccessories', '0006_supplier_electronic_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('date_finish', models.DateTimeField(null=True, verbose_name='Дата окончания заказа')),
                ('price', models.FloatField(null=True, verbose_name='Стоимость заказа')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес доставки ноутбука')),
                ('status', models.CharField(choices=[(1, 'создан'), (2, 'отменен'), (3, 'согласован'), (4, 'в пути'), (5, 'завершен')], max_length=200, verbose_name='Состояние заказа')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['date_create'],
            },
        ),
        migrations.AlterField(
            model_name='electronic',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='electronicAccessories.supplier', verbose_name='Поставщик'),
        ),
        migrations.CreateModel(
            name='Pos_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_laptop', models.IntegerField(verbose_name='Количество ноутбуков')),
                ('price', models.FloatField(verbose_name='Общая стоимость ноутбуков')),
                ('laptop', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='electronicAccessories.electronic', verbose_name='Ноутбук')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='electronicAccessories.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Позиция',
                'verbose_name_plural': 'Позиции',
                'ordering': ['laptop', 'order', 'price'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='laptops',
            field=models.ManyToManyField(through='electronicAccessories.Pos_order', to='electronicAccessories.electronic'),
        ),
    ]