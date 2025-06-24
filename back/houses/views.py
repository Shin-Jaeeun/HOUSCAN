import openai
import logging
from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from django.conf import settings
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FavoriteNotice, CompetitionRate, UserScore, RecruitNotice
from .serializers import (
    CompetitionRateSerializer,
    UserScoreSerializer,
    RecruitNoticeSerializer,
    FavoriteNoticeReadSerializer,
    FavoriteNoticeWriteSerializer,
    FavoriteNoticeFlatSerializer,
)


# ✅ 크롤링 실행용
import subprocess
from datetime import datetime, timedelta

# ✅ ViewSets


class CompetitionRateViewSet(viewsets.ModelViewSet):
    queryset = CompetitionRate.objects.all()
    serializer_class = CompetitionRateSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['region', 'year_month']
    ordering_fields = ['year_month', 'general_competition_rate']


class UserScoreViewSet(viewsets.ModelViewSet):
    queryset = UserScore.objects.all()
    serializer_class = UserScoreSerializer


# ✅ 연도/월/지역 기반 필터링용 API
@api_view(['GET'])
def filter_competition(request):
    region = request.GET.get('region')
    start = request.GET.get('start')  # 예: '2020-01'
    end = request.GET.get('end')      # 예: '2024-12'

    qs = CompetitionRate.objects.all()

    if region:
        qs = qs.filter(region=region)
    if start:
        qs = qs.filter(year_month__gte=start)
    if end:
        qs = qs.filter(year_month__lte=end)

    qs = qs.order_by('year_month')  # 정렬

    serializer = CompetitionRateSerializer(qs, many=True)
    return Response(serializer.data)


# ✅ 수동 크롤링 실행용 API (관리자만 POST 가능)
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def fetch_competition_data(request):
    subprocess.call(["python", "manage.py", "fetch_excel"])
    return Response({"message": "경쟁률 데이터를 크롤링했습니다."})

from openai import OpenAI
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RecommendView(APIView):
    def post(self, request):
        user_score = request.data.get('score')
        user_text = request.data.get('user_text')  # ✅ 수정!


        prompt = f"""
        사용자의 청약 가점은 {user_score}점입니다.
        {user_text if user_text else "찜한 공고는 없습니다."}
        사용자가 어떤 청약에 유리할지, 경쟁률을 고려해 전략을 요약해 주세요.
        """

        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o",  # 또는 gpt-4o-mini
                messages=[
                    {"role": "system", "content": "청약 전문가처럼 조언해 주세요."},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response.choices[0].message.content
            return Response({"result": answer})
        except Exception as e:
            print(f"❌ OpenAI 호출 실패: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RecruitNoticeListView(generics.ListAPIView):
    queryset = RecruitNotice.objects.all().order_by('-apply_start')
    serializer_class = RecruitNoticeSerializer

class RecruitNoticeDetailView(generics.RetrieveAPIView):
    queryset = RecruitNotice.objects.all()
    serializer_class = RecruitNoticeSerializer
    lookup_field = 'id'


class FavoriteNoticeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteNotice.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteNotice.objects.filter(user=self.request.user).select_related('notice')

    def get_serializer_class(self):
        # flat 형태 응답이 필요한 조건 (알림창 등)
        if self.request.query_params.get('flat') == 'true':
            return FavoriteNoticeFlatSerializer
        if self.request.method == 'GET':
            return FavoriteNoticeReadSerializer
        return FavoriteNoticeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


