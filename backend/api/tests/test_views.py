from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from cards.models import Product

User = get_user_model()


class ApiViewsTests(TestCase):
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
            user=ApiViewsTests.user
        )

    def setUp(self):
        """Создаем клиент гостя и зарегистрированного пользователя."""
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

    def test_create_product(self):
        """Post запрос создает запись в Pruduct."""
        product_count = Product.objects.count()
        data = {
            "vendor_code": 22223333
        }
        response = self.authorized_client.post(
            reverse(
                'api:product-list'
            ),
            data=data,
            format='json'
        )
        new_product = Product.objects.last()
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Product.objects.count(), product_count + 1)
        self.assertEqual(new_product.vendor_code, data['vendor_code'])
        self.assertEqual(new_product.user, ApiViewsTests.user)

    def test_delete_product(self):
        """Delete запрос удаляет запись из Product."""
        product_count = Product.objects.count()
        data = {
            "vendor_code": 22223333
        }
        response = self.authorized_client.delete(
            reverse(
                'api:product-detail',
                kwargs={'vendor_code': ApiViewsTests.product.vendor_code}
            ),
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Product.objects.count(), product_count - 1)

    def test_create_user(self):
        """Post запрос создает запись в User."""
        user_count = User.objects.count()
        data = {
            "username": 'niko2',
            "password": "niko2",
            "email": 'Elnikit2@rambler.ru'
        }
        response = self.authorized_client.post(
            reverse(
                'api:users-list'
            ),
            data=data,
            format='json'
        )
        new_user = User.objects.last()
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertEqual(new_user.email, data['email'])
        self.assertEqual(new_user.username, data['username'])
