from rest_framework import viewsets, mixins

from cards.models import Article, Card
from .serializers import ArticleSerializer, CardSerializer
from .filters import CardFilterBackend


class ArticleViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Article.objects.select_related('user').all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        new_queryset = self.queryset.filter(user=self.request.user)
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
