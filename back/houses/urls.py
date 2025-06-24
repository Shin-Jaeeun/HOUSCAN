from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FavoriteNoticeViewSet,
    CompetitionRateViewSet,
    UserScoreViewSet,
    filter_competition,
    fetch_competition_data,
    RecommendView,
    RecruitNoticeListView,
    RecruitNoticeDetailView,
)

router = DefaultRouter()
router.register('favorites', FavoriteNoticeViewSet)
router.register('competition', CompetitionRateViewSet)
router.register('score', UserScoreViewSet)

urlpatterns = [
    path('houselist/', RecruitNoticeListView.as_view()),         # 공고 리스트
    path('houselist/<int:id>/', RecruitNoticeDetailView.as_view()),  # 공고 상세
    # 기존 라우터 및 API들
    path('competition/filter/', filter_competition),
    path('competition/fetch/', fetch_competition_data),
    path('recommend/', RecommendView.as_view()),
    path('ai/', RecommendView.as_view()),
    path('', include(router.urls)),
]

