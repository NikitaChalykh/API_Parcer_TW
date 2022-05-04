from django.urls import include, path
from rest_framework import routers

from .views import ArticleViewSet, CardViewSet

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('articles', ArticleViewSet)
router_api.register('cards', CardViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_api.urls))
]
