from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        post_migrate.connect(load_initial_data, sender=self)

def load_initial_data(sender, **kwargs):
    from django.db import connection
    if 'products_financialproduct' in connection.introspection.table_names():
        from products.models import FinancialProduct
        if not FinancialProduct.objects.exists():
            print("📥 예적금  로드 중...")
            call_command('loaddata', 'fixtures/financial_products.json')
