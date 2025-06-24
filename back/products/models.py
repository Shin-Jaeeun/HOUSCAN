from django.db import models
from accounts.models import User

class FinancialProduct(models.Model):
    name = models.CharField(max_length=100)  # 상품명
    institution = models.CharField(max_length=100)  # 금융회사명
    join_method = models.CharField(max_length=50, blank=True, null=True)  # 가입 방법
    maturity_interest_rate = models.FloatField(null=True, blank=True)  # 만기 후 이자율
    preferential_condition = models.TextField(blank=True, null=True)  # 우대 조건
    join_limit = models.CharField(max_length=100, blank=True, null=True)  # 가입 제한 조건
    join_target = models.CharField(max_length=100, blank=True, null=True)  # 가입 대상
    max_limit = models.CharField(max_length=100, blank=True, null=True)  # 최대 가입 한도
    notice = models.TextField(blank=True, null=True)  # 유의사항

    # 옵션 정보
    option_interest_type = models.CharField(max_length=50, blank=True, null=True)  # 고정/변동
    option_payment_type = models.CharField(max_length=50, blank=True, null=True)  # 자유/정기 등
    option_saving_period = models.CharField(max_length=50, blank=True, null=True)  # 저축 기간
    option_base_rate = models.FloatField(null=True, blank=True)  # 기본 금리
    option_max_rate = models.FloatField(null=True, blank=True)  # 최고 우대 금리

    max_monthly_payment = models.IntegerField()  # 월별 납입 가능 최대 금액

    # 사용자 추천 관련 필드
    goal_asset = models.IntegerField()  # 목표 자산
    target_date = models.DateField()  # 목표 도달 시점
    preferred_type = models.CharField(max_length=50)  # 예금/적금 등

    def __str__(self):
        return f'{self.name} - {self.institution}'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_products')
    product = models.ForeignKey(FinancialProduct, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.email} - {self.product.name}'
