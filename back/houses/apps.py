from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class HousesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'houses'

    def ready(self):
        post_migrate.connect(load_initial_data, sender=self)

def load_initial_data(sender, **kwargs):
    from django.db import connection
    from django.core.management import call_command

    if 'accounts_user' in connection.introspection.table_names():
        from accounts.models import User
        if not User.objects.exists():
            print("👤 사용자 데이터 로드 중...")
            call_command('loaddata', 'fixtures/users.json')

    if 'community_communitypost' in connection.introspection.table_names():
        from community.models import CommunityPost
        if not CommunityPost.objects.exists():
            print("📝 커뮤니티 게시글 데이터 로드 중...")
            call_command('loaddata', 'fixtures/community_posts.json')

    if 'community_comment' in connection.introspection.table_names():
        from community.models import Comment
        if not Comment.objects.exists():
            print("💬 댓글 데이터 로드 중...")
            call_command('loaddata', 'fixtures/comments.json')

    if 'houses_competitionrate' in connection.introspection.table_names():
        from houses.models import CompetitionRate
        if not CompetitionRate.objects.exists():
            print("📈 경쟁률 데이터 로드 중...")
            call_command('loaddata', 'fixtures/competition_rates.json')

    if 'houses_recruitnotice' in connection.introspection.table_names():
        from houses.models import RecruitNotice
        if not RecruitNotice.objects.exists():
            print("📄 청약 공고문 데이터 로드 중...")
            call_command('loaddata', 'fixtures/recruit_notices.json')

