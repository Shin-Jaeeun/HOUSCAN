from rest_framework import serializers
from .models import FinancialProduct, FavoriteProduct

class FinancialProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProduct
        fields = [
            'id',
            'name',
            'institution',
            'option_base_rate',
            'option_max_rate',
            'option_saving_period',
            'preferred_type',
        ]


class FavoriteProductSerializer(serializers.ModelSerializer):
    # 👇 POST 요청에서 product ID 받기
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=FinancialProduct.objects.all(),
        source='product',
        write_only=True
    )

    # 👇 응답에서는 product 전체 정보 반환
    product = FinancialProductSerializer(read_only=True)

    class Meta:
        model = FavoriteProduct
        fields = ['id', 'product', 'product_id', 'user', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']
        if FavoriteProduct.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("이미 찜한 상품입니다.")
        return data
