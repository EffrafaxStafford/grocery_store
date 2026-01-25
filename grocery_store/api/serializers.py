from rest_framework import serializers

from store.models import Category, Subcategory, Product, ProductImage
from cart.models import Cart, CartItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'image')

