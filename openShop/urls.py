from django.urls import path, include
from rest_framework import routers
from openShop.views import (
    CategoryViewSet, SellerViewSet, ProductViewSet, 
    ReviewViewSet, OrderViewSet, OrderItemViewSet, StockHistoryViewSet
)

router = routers.SimpleRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('sellers', SellerViewSet, basename='seller')
router.register('', ProductViewSet, basename='product')
router.register('reviews', ReviewViewSet, basename='review')
router.register('orders', OrderViewSet, basename='order')
router.register('order-items', OrderItemViewSet, basename='orderitem')
router.register('stock-history', StockHistoryViewSet, basename='stockhistory')

urlpatterns = [
    path('', include(router.urls)),
]