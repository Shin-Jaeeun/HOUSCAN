from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import FinancialProduct, FavoriteProduct
from .serializers import FinancialProductSerializer, FavoriteProductSerializer

class FinancialProductViewSet(viewsets.ModelViewSet):
    queryset = FinancialProduct.objects.all()
    serializer_class = FinancialProductSerializer


class FavoriteProductViewSet(viewsets.ModelViewSet):
    queryset = FavoriteProduct.objects.all()  # ✅ 이 줄이 꼭 필요!
    serializer_class = FavoriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("자신의 찜만 삭제할 수 있습니다.")
        instance.delete()

class GroupedDepositProductView(APIView):
    def get(self, request):
        products = FinancialProduct.objects.all()
        grouped = {}

        for p in products:
            key = (p.institution, p.name)
            if key not in grouped:
                grouped[key] = {
                    "bank": p.institution,
                    "product_name": p.name,
                    "rates": {}
                }
            grouped[key]["rates"][str(p.option_saving_period)] = p.option_base_rate

        return Response(list(grouped.values()))