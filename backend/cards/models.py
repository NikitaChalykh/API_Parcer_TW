from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Article(models.Model):
    '''Модель артикулов для парсинга'''
    article_value = models.PositiveIntegerField(
        unique=True,
        verbose_name='Артикул'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
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
        return str(self.article_value)


class Card(models.Model):
    '''Модель карточек для артикулов'''
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='Модель артикула'
    )
    article_value = models.PositiveIntegerField(
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
