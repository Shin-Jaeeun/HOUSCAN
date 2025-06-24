from django.db import models
from accounts.models import User


class UserScore(models.Model):
    """사용자가 입력한 청약 가점 계산 요소를 저장하는 테이블"""
    homeless_years = models.PositiveIntegerField()  # 무주택 기간 (년)
    num_dependents = models.PositiveIntegerField()  # 부양가족 수
    subscription_years = models.PositiveIntegerField()  # 청약통장 가입기간 (년)
    total_score = models.PositiveIntegerField()  # 계산된 총 가점

    def __str__(self):
        return f'가점 {self.total_score}점 (무주택 {self.homeless_years}년, 부양 {self.num_dependents}명)'


class RecruitNotice(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    apply_start = models.DateField()
    apply_end = models.DateField()
    detail_url = models.URLField(unique=True)
    image_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    scale = models.CharField(max_length=50, blank=True, null=True)
    notice_url = models.URLField(blank=True, null=True)
    winner_announcement_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"[{self.category}] {self.title}"

class FavoriteNotice(models.Model):
    """사용자가 찜한 청약 공고를 저장하는 테이블 (User ↔ SubscriptionNotice 중간 테이블)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_notices')
    notice = models.ForeignKey(RecruitNotice, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'notice')

    def __str__(self):
        return f'{self.user.email} - {self.notice.title}'


class CompetitionRate(models.Model):
    year_month = models.CharField(max_length=10)           # 연월
    region = models.CharField(max_length=20)               # 시도

    special_supply_units = models.IntegerField(null=True, blank=True)        # 특별공급 공급세대수
    special_applications = models.IntegerField(null=True, blank=True)       # 특별공급 접수건수
    special_competition_rate = models.FloatField(null=True, blank=True)     # 특별공급 경쟁률

    general_supply_units = models.IntegerField(null=True, blank=True)       # 일반공급 공급세대수
    general_applications = models.IntegerField(null=True, blank=True)       # 일반공급 접수건수
    general_competition_rate = models.FloatField(null=True, blank=True)     # 일반공급 경쟁률

    def __str__(self):
        return f"{self.year_month} {self.region}"


