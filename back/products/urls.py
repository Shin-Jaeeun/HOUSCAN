from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinancialProductViewSet, FavoriteProductViewSet, GroupedDepositProductView

router = DefaultRouter()
router.register('products', FinancialProductViewSet)
router.register('favorites', FavoriteProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('grouped/', GroupedDepositProductView.as_view()), 
]
