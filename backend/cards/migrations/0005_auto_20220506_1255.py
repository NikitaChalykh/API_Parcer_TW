# Generated by Django 3.1.14 on 2022-05-06 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_auto_20220506_1254'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['date'], 'verbose_name': 'Отслеживаемый артикул', 'verbose_name_plural': 'Отслеживаемые артикулы'},
        ),
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['date'], 'verbose_name': 'Карточка товара', 'verbose_name_plural': 'Карточки товаров'},
        ),
    ]