# Generated by Django 3.1.14 on 2022-05-06 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20220506_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='cards.product', verbose_name='Продукт'),
        ),
    ]
