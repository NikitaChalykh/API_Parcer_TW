from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
import requests

from cards.models import Article, Card, User

from .filters import CardFilterBackend
from .serializers import ArticleSerializer, CardSerializer, UserSerializer


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


class ArticleViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Article.objects.select_related('user').all()
    serializer_class = ArticleSerializer
    lookup_field = 'article_value'

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
        'article',
        'article__user'
    ).all()
    serializer_class = CardSerializer
    filter_backends = (CardFilterBackend,)

    def get_queryset(self):
        article = self.kwargs.get("article")
        article = get_object_or_404(
            Article,
            article_value=article
        )
        new_queryset = self.queryset.filter(
            article=article
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


def get_card(article):
    '''Функция для получения данных с сайта по артикулу'''
    url = 'https://www.wildberries.ru/catalog/' + (
        str(article) + '/detail.aspx'
    )
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_quote = soup.find('span', id="productNmId")
    brand_quote = soup.find('meta', itemprop="brand")
    name_quote = soup.find('meta', itemprop="name")
    discont_value_quote = soup.find('span', class_="price-block__final-price")
    value_quote = soup.find(
        'del', class_="price-block__old-price j-final-saving"
    )
    return {
        'article_value': int(article_quote.text),
        'brand': get_meta_tag(brand_quote, '"'),
        'name': get_meta_tag(name_quote, ','),
        'discont_value': get_tag_for_value(discont_value_quote.text),
        'value': get_tag_for_value(value_quote.text)
    }


@api_view(['POST'])
def get_parced_data(request):
    articles = Article.objects.select_related('user').filter(user=request.user)
    for article in articles:
        new_cart = get_card(article.article_value)
        Card.objects.create(
            **new_cart, user=request.user, article=article
        )
    return Response(
        'Созданы карточки для отслеживаемых артикулов',
        status=status.HTTP_201_CREATED
    )
