from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import CategoryList, ProductList, CartRetrieveAPIView, CartClearAPIView, CartItemViewSet


router = DefaultRouter() 
router.register(r'cart/items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('products/', ProductList.as_view()),
    path('cart/', CartRetrieveAPIView.as_view()),
    path('cart/clear/', CartClearAPIView.as_view()),
    path('', include(router.urls)),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
