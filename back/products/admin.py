from django.contrib import admin
from .models import FinancialProduct, FavoriteProduct

admin.site.register(FinancialProduct)
admin.site.register(FavoriteProduct)
