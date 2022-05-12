import logging

from celery import shared_task

from cards.models import Card, Product

from .utils import get_card, get_supplier

logger = logging.getLogger(__name__)


@shared_task
def get_data():
    products = Product.objects.select_related('user').all()
    try:
        for product in products:
            new_cart = get_card(product.vendor_code)
            supplier = get_supplier(product.vendor_code)
            Card.objects.create(
                **new_cart,
                user=product.user,
                product=product,
                supplier=supplier
            )
        logger.info('Карточки товаров сохранены успешно')
    except Exception as error:
        logger.error(f'Сбой при парсинге артикулов: {error}')
