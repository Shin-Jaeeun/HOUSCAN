from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        post_migrate.connect(load_initial_data, sender=self)

def load_initial_data(sender, **kwargs):
    from django.db import connection
    if 'accounts_user' in connection.introspection.table_names():
        from accounts.models import User
        if not User.objects.exists():
            print("👤 사용자 데이터 로드 중...")
            call_command('loaddata', 'fixtures/users.json')
