from rest_framework import generics, viewsets, permissions, mixins
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from store.models import Category, Product
from .serializers import (CategorySerializer,
                          ProductSerializer,
                          CartSerializer,
                          CartItemSerializer)
from constants import MIN_QUANTITY_PRODUCT


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,) 


class ProductList(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('images')
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,) 


class CartRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        return self.request.user.cart


class CartClearAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        request.user.cart.items.all().delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    # queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return self.request.user.cart.items.all()

    def perform_create(self, serializer):
        queryset = self.get_queryset()
        product_id = serializer.validated_data['product'].id
        cart_item = queryset.filter(product_id=product_id).first()
        if cart_item:
            cart_item.quantity = serializer.validated_data.get('quantity', MIN_QUANTITY_PRODUCT)
            cart_item.save()
            return Response({'message': 'Количество обновлено'})
        serializer.save(cart=self.request.user.cart)
