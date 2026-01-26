from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryList, ProductList, CartList, CartItemViewSet


router = DefaultRouter() 
router.register('cart/items', CartItemViewSet)

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('products/', ProductList.as_view()),
    path('cart/', CartList.as_view()),
    path('', include(router.urls)),
]
