import pytest
from http import HTTPStatus

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'urlname',
    ('api:categories', 'api:products')
)
def test_pages_availability_for_anonymous_user(api_client, urlname):
    """Операции по эндпоинтам категорий и продуктов может осуществлять любой пользователь."""
    url = reverse(urlname)
    response = api_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('api_client'), HTTPStatus.UNAUTHORIZED),
        (pytest.lazy_fixture('auth_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'urlname',
    ('api:cart', 'api:cart-items-list')
)
def test_cart_availability(parametrized_client, expected_status, urlname):
    """Доступ к корзине имеет только авторизированный пользователь."""
    url = reverse(urlname)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status

