from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
