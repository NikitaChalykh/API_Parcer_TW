import logging

from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from cards.models import Card, Product, User

from .filters import CardFilterBackend
from .serializers import CardSerializer, ProductSerializer, UserSerializer
from .utils import get_card, get_supplier

logger = logging.getLogger(__name__)


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


@api_view(['POST'])
def get_parced_data(request):
    products = Product.objects.select_related('user').filter(user=request.user)
    try:
        for product in products:
            new_cart = get_card(product.vendor_code)
            supplier = get_supplier(product.vendor_code)
            Card.objects.create(
                **new_cart,
                user=request.user,
                product=product,
                supplier=supplier
            )
    except Exception as error:
        logger.error(f'Сбой при парсинге артикулов: {error}')
        return Response(
            'Карточки не созданы',
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        'Созданы карточки для отслеживаемых артикулов',
        status=status.HTTP_201_CREATED
    )
