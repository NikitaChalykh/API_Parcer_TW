import json

import requests
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from cards.models import Card, Product, User

from .filters import CardFilterBackend
from .serializers import CardSerializer, ProductSerializer, UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Product.objects.select_related('user').all()
    serializer_class = ProductSerializer
    lookup_field = 'vendor_code'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        new_queryset = self.queryset.filter(
            user=self.request.user
        )
        return new_queryset


class CardViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Card.objects.select_related(
        'user',
        'product',
        'product__user'
    ).all()
    serializer_class = CardSerializer
    filter_backends = (CardFilterBackend,)

    def get_queryset(self):
        vendor_code = self.kwargs.get("vendor_code")
        product = get_object_or_404(
            Product,
            vendor_code=vendor_code
        )
        new_queryset = self.queryset.filter(
            product=product
        )
        return new_queryset


def get_meta_tag(data, symbol):
    '''Функция для обработки данных из мета-тегов'''
    data = str(data)
    new_data_dict = []
    for i in range(15, len(data) + 1):
        if data[i] != symbol:
            new_data_dict.append(data[i])
        else:
            break
    return ''.join(new_data_dict)


def get_tag_for_value(data):
    '''Функция для обработки числовых данных из тегов'''
    data = str(data)
    new_data_dict = []
    for symbol in data:
        try:
            int(symbol)
            new_data_dict.append(symbol)
        except ValueError:
            continue
    return int(''.join(new_data_dict)) * 100


def get_card(vendor_code):
    '''Функция для получения данных с сайта по артикулу'''
    url = 'https://www.wildberries.ru/catalog/{}/detail.aspx'.format(
        vendor_code
    )
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    vendor_code_quote = soup.find('span', id="productNmId")
    brand_quote = soup.find('meta', itemprop="brand")
    name_quote = soup.find('meta', itemprop="name")
    discont_value_quote = soup.find('span', class_="price-block__final-price")
    value_quote = soup.find(
        'del', class_="price-block__old-price j-final-saving"
    )
    return {
        'vendor_code': int(vendor_code_quote.text),
        'brand': get_meta_tag(brand_quote, '"'),
        'name': get_meta_tag(name_quote, ','),
        'discont_value': get_tag_for_value(discont_value_quote.text),
        'value': get_tag_for_value(value_quote.text)
    }


def get_supplier(vendor_code):
    data = requests.get(
        'https://wbx-content-v2.wbstatic.net/sellers/{}.json'.format(
            vendor_code
        )
    ).text
    supplier = json.loads(data)['supplierName']
    return supplier


@api_view(['POST'])
def get_parced_data(request):
    products = Product.objects.select_related('user').filter(user=request.user)
    for product in products:
        new_cart = get_card(product.vendor_code)
        supplier = get_supplier(product.vendor_code)
        Card.objects.create(
            **new_cart,
            user=request.user,
            product=product,
            supplier=supplier
        )
    return Response(
        'Созданы карточки для отслеживаемых артикулов',
        status=status.HTTP_201_CREATED
    )
