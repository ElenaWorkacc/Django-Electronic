# Generated by Django 4.1.7 on 2023-05-05 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('electronicAccessories', '0003_alter_electronic_options_alter_electronic_ssd_volume_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electronic',
            name='price',
            field=models.FloatField(default=15000, verbose_name='Цена'),
        ),
    ]
