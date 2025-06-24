from rest_framework import serializers
from .models import RecruitNotice, FavoriteNotice, CompetitionRate, UserScore



class CompetitionRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionRate
        fields = '__all__'


class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = '__all__'
        extra_kwargs = {
            'total_score': {'read_only': True}  # ✅ 사용자 입력 X, 자동 계산됨
        }

    def create(self, validated_data):
        # ✅ 자동 계산 로직
        homeless_years = validated_data.get('homeless_years', 0)
        num_dependents = validated_data.get('num_dependents', 0)
        subscription_years = validated_data.get('subscription_years', 0)

        homeless_score = min(homeless_years * 2, 15)
        dependents_score = min(num_dependents * 10, 35)
        subscription_score = min(subscription_years, 17)

        total_score = homeless_score + dependents_score + subscription_score
        validated_data['total_score'] = total_score

        return super().create(validated_data)


class RecruitNoticeSerializer(serializers.ModelSerializer):
    favorites_count = serializers.SerializerMethodField()

    class Meta:
        model = RecruitNotice
        fields = [
            'id', 'title', 'category', 'region', 'apply_start', 'apply_end',
            'detail_url', 'image_url', 'location', 'scale', 'notice_url',
            'favorites_count',  # ✅ 찜 수
            'status',
            'winner_announcement_date'           # ✅ 상태 추가!
        ]

    def get_favorites_count(self, obj):
        return obj.favorited_by.count()

class FavoriteNoticeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteNotice
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        user = self.context['request'].user
        notice = data['notice']
        if FavoriteNotice.objects.filter(user=user, notice=notice).exists():
            raise serializers.ValidationError("이미 찜한 공고입니다.")
        return data


class FavoriteNoticeReadSerializer(serializers.ModelSerializer):
    notice = RecruitNoticeSerializer(read_only=True)

    class Meta:
        model = FavoriteNotice
        fields = ['id', 'notice']

# 마감임박 알림용
class FavoriteNoticeFlatSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='notice.title', read_only=True)
    deadline = serializers.DateField(source='notice.apply_end', read_only=True)

    class Meta:
        model = FavoriteNotice
        fields = ['id', 'title', 'deadline']