from django.contrib import admin

from .models import Article, Card


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'article',
        'user',
        'date'
    )
    list_filter = ('article', 'user')
    empty_value_display = '-пусто-'


class CardAdmin(admin.ModelAdmin):
    list_display = (
        'article',
        'name',
        'user',
        'discont_value',
        'value',
        'brand',
        'date'
    )
    list_filter = ('article', 'user')
    empty_value_display = '-пусто-'


admin.site.register(Article, ArticleAdmin)
admin.site.register(Card, CardAdmin)
