from django.urls import include, path
from rest_framework import routers

from .views import CardViewSet, ProductViewSet, UserViewSet, get_parced_data

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('products', ProductViewSet)
router_api.register(
    r'^products/(?P<vendor_code>\d+)/cards',
    CardViewSet,
    basename='cards'
)
router_api.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router_api.urls)),
    path('parcing/', get_parced_data)
]
