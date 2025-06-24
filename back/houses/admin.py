from django.contrib import admin
from .models import UserScore, CompetitionRate, FavoriteNotice, RecruitNotice

admin.site.register(UserScore)
admin.site.register(CompetitionRate)
admin.site.register(FavoriteNotice)
admin.site.register(RecruitNotice)
