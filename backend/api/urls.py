from django.urls import include, path
from rest_framework import routers

from .views import ArticleViewSet, CardViewSet, UserViewSet, get_parced_data

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('articles', ArticleViewSet)
router_api.register(
    r'^articles/(?P<article>\d+)/cards',
    CardViewSet
)
router_api.register('users', UserViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_api.urls)),
    path('parcing/', get_parced_data)
]
