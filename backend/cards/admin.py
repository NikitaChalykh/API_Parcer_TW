from django.contrib import admin

from .models import Card, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'vendor_code',
        'user',
        'date'
    )
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class CardAdmin(admin.ModelAdmin):
    list_display = (
        'vendor_code',
        'name',
        'user',
        'discont_value',
        'value',
        'brand',
        'supplier',
        'date'
    )
    list_filter = ('user', 'vendor_code')
    empty_value_display = '-пусто-'


admin.site.register(Product, ProductAdmin)
admin.site.register(Card, CardAdmin)
