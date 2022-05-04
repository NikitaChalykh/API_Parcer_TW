from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Article(models.Model):
    article = models.PositiveIntegerField(
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

    def __str__(self):
        return self.user


class Card(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='Артикул'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='Пользователь'
    )
    value = models.PositiveIntegerField(
        verbose_name='Цена'
    )
    discont_value = models.PositiveIntegerField(
        verbose_name='Цена со скидкой'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания статьи'
    )
    brand = models.CharField(
        verbose_name='Бренд',
        max_length=200
    )
    supplier = models.CharField(
        verbose_name='Поставщик',
        max_length=200
    )

    class Meta:
        verbose_name = "Карточка товара"
        verbose_name_plural = "Карточки товаров"

    def __str__(self):
        return self.article
