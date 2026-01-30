from django.contrib.auth import get_user_model
from django.db import models

from store.models import Product
from constants import MIN_QUANTITY_PRODUCT


User = get_user_model()


class Cart(models.Model):
    """Модель для хранения корзины пользователя."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Корзина')

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    class Meta:
        verbose_name = 'Корзина пользователя'
        ordering = ('user',)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    """Модель для хранения товаров в корзине пользователя."""

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина пользователя')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт')
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=MIN_QUANTITY_PRODUCT)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'Товары пользователя'
        ordering = ('cart', 'product')
        unique_together = ('cart', 'product')
