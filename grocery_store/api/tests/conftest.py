import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from store.models import Category, Subcategory, Product


User = get_user_model()


@pytest.fixture
def api_client():
    """Анонимный API клиент."""
    return APIClient()


@pytest.fixture
def auth_client(api_client, django_user_model):
    """Авторизованный пользователь."""
    user = django_user_model.objects.create_user(username='user', password='pass')
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    api_client.user = user
    return api_client


@pytest.fixture
def product(db):
    """Тестовый продукт."""
    category = Category.objects.create(
        name='Категория',
        slug='category'
    )
    subcategory = Subcategory.objects.create(
        name='Подкатегория',
        slug='subcategory',
        category=category
    )
    product = Product.objects.create(
        name='Продукт',
        slug='product',
        price='100',
        subcategory=subcategory
    )
    return product


@pytest.fixture
def form_data(product):
    """Тестовые данные для CartItem."""
    return {
        'product': product.id,
        'quantity': 10
    } 
