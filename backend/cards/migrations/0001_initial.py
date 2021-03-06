# Generated by Django 3.1.14 on 2022-05-06 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.PositiveIntegerField(verbose_name='Артикул')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('discont_value', models.PositiveIntegerField(verbose_name='Цена со скидкой')),
                ('value', models.PositiveIntegerField(verbose_name='Полная стоимость')),
                ('brand', models.CharField(max_length=200, verbose_name='Бренд')),
                ('supplier', models.CharField(max_length=100, verbose_name='Поставщик')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Карточка товара',
                'verbose_name_plural': 'Карточки товаров',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.PositiveIntegerField(unique=True, verbose_name='Артикул')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Отслеживаемый артикул',
                'verbose_name_plural': 'Отслеживаемые артикулы',
                'ordering': ['date'],
            },
        ),
    ]
