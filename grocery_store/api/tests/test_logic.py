import pytest
from http import HTTPStatus

from django.urls import reverse

from cart.models import CartItem


def test_user_can_create_item(auth_client, form_data):
    """Пользователь может добавить товар в корзину."""
    # добавляем товар в корзину
    url = reverse('api:cart-items-list')
    response = auth_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.CREATED
    assert CartItem.objects.count() == 1
    # проверяем товар в корзине
    item = CartItem.objects.first()
    assert item.product.id == form_data['product']
    assert item.quantity == form_data['quantity']
    assert item.cart == auth_client.user.cart


def test_user_can_clear_cart(auth_client, product, form_data):
    """Пользователь может полностью очистить корзину."""
    # добавляем товар в корзину
    url = reverse('api:cart-items-list')
    auth_client.post(url, form_data)
    assert CartItem.objects.count() == 1
    # очищаем корзину
    clear_url = reverse('api:cart-clear')
    response = auth_client.post(clear_url)
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert CartItem.objects.count() == 0
