from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    '''Модель артикулов для парсинга'''
    vendor_code = models.PositiveIntegerField(
        unique=True,
        verbose_name='Артикул'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Пользователь'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = "Отслеживаемый артикул"
        verbose_name_plural = "Отслеживаемые артикулы"
        ordering = ['date']

    def __str__(self):
        return str(self.vendor_code)


class Card(models.Model):
    '''Модель карточек для артикулов'''
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='Продукт'
    )
    vendor_code = models.PositiveIntegerField(
        verbose_name='Артикул'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='Пользователь'
    )
    discont_value = models.PositiveIntegerField(
        verbose_name='Цена со скидкой'
    )
    value = models.PositiveIntegerField(
        verbose_name='Полная стоимость'
    )
    brand = models.CharField(
        max_length=200,
        verbose_name='Бренд'
    )
    supplier = models.CharField(
        max_length=100,
        verbose_name='Поставщик'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = "Карточка товара"
        verbose_name_plural = "Карточки товаров"
        ordering = ['date']

    def __str__(self):
        return self.name
