from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from store.models import Category, Product
from cart.models import Cart, CartItem
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer
from constants import MIN_QUANTITY_PRODUCT


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,) 


class ProductList(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('images')
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,) 


class CartList(generics.ListAPIView):

    def get_queryset(self):
        return self.request.user.cart.items
        
    def list(self, request):
        queryset = self.get_queryset()
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        product_id = serializer.validated_data['product'].id
        cart_item = self.request.user.cart.items.filter(product_id=product_id).first()
        if cart_item:
            cart_item.quantity = serializer.validated_data.get('quantity', MIN_QUANTITY_PRODUCT)
            cart_item.save()
            return Response({'message': 'Количество обновлено'})

        serializer.save(cart=self.request.user.cart)

