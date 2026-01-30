from rest_framework import serializers

from store.models import Category, Subcategory, Product, ProductImage
from cart.models import Cart, CartItem


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'image', 'subcategories')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'size')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)
    category = serializers.CharField(
        source='subcategory.category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'slug', 'category', 'subcategory', 'price', 'images')


class CartItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'quantity не может быть отрицательным!')
        return value


class CartItemUpdateSerializer(CartItemCreateSerializer):

    class Meta:
        model = CartItem
        fields = ('quantity',)


class ProductCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price']


class CartItemReadSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('total_quantity', 'total_price', 'items')
