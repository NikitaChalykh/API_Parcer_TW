from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from cards.models import Card, Product

User = get_user_model()


class PostURLTests(TestCase):
    """Создаем тестовую модель артикула продукта и
    тестовую модель пользователя."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='niko',
            password='niko',
            email='Elnikit@rambler.ru'
        )
        cls.product = Product.objects.create(
            vendor_code=11112222,
            user=PostURLTests.user
        )
        cls.card = Card.objects.create(
            vendor_code=11112222,
            product=PostURLTests.product,
            user=PostURLTests.user,
            name='iphone',
            discont_value='112',
            value='90',
            brand='apple',
            supplier='apple'
        )

    def setUp(self):
        """Создаем клиент гостя и зарегистрированного пользователя."""
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        djoser_jwt_create_url = '/api/auth/jwt/create/'
        token_response = self.authorized_client.post(
            djoser_jwt_create_url,
            {'username': 'niko', 'password': 'niko'},
            format='json'
        )
        self.assertTrue('access' in token_response.data)
        token = token_response.data['access']
        self.authorized_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(token)
        )

    def test_urls_response_guest(self):
        """Проверяем статус страниц для гостя."""
        url_status = {
            reverse('api:users-me'): HTTPStatus.UNAUTHORIZED,
            reverse('api:product-list'): HTTPStatus.UNAUTHORIZED,
            reverse(
                'api:product-detail',
                kwargs={'vendor_code': PostURLTests.product.vendor_code}
            ): HTTPStatus.UNAUTHORIZED,
            (
                '/api/products/{}/cards/'.format(
                    PostURLTests.product.vendor_code
                )
            ): HTTPStatus.UNAUTHORIZED
        }
        for url, status_code in url_status.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_urls_response_auth(self):
        """Проверяем статус страниц для аутентифицированного пользователя."""
        url_status = {
            reverse('api:users-me'): HTTPStatus.OK,
            reverse('api:product-list'): HTTPStatus.OK,
            reverse(
                'api:product-detail',
                kwargs={'vendor_code': PostURLTests.product.vendor_code}
            ): HTTPStatus.OK,
            (
                '/api/products/{}/cards/'.format(
                    PostURLTests.product.vendor_code
                )
            ): HTTPStatus.OK
        }
        for url, status_code in url_status.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, status_code)
