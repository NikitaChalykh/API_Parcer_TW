# Generated by Django 3.1.14 on 2022-05-05 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20220504_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='link',
        ),
    ]
